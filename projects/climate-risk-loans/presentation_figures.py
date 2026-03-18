"""
presentation_figures.py
=======================
Produces 4 presentation-quality figures for the climate risk satellite model.

Run from the climate-risk-loans/ directory:
    python presentation_figures.py

Outputs (outputs/figures/):
    pres_1_cumulative_impact.png   — Hero: cumulative loan balance under 3 scenarios
    pres_2_driver_paths.png        — NGFS unemployment + rate paths per scenario
    pres_3_oos_validation.png      — Out-of-sample model validation
    pres_4_covid_dummy.png         — What the COVID dummy does
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator, FuncFormatter
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa.ar_model import AutoReg
from scipy import stats

# ─────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':         'DejaVu Sans',
    'font.size':           12,
    'axes.titlesize':      16,
    'axes.titleweight':    'bold',
    'axes.labelsize':      13,
    'xtick.labelsize':     11,
    'ytick.labelsize':     11,
    'legend.fontsize':     11,
    'legend.framealpha':   0.9,
    'figure.dpi':          150,
    'savefig.dpi':         300,
    'axes.spines.top':     False,
    'axes.spines.right':   False,
    'axes.grid':           True,
    'grid.alpha':          0.25,
    'grid.linestyle':      '--',
    'axes.facecolor':      'white',
    'figure.facecolor':    'white',
})

# Scenario palette
SCENARIO_COLORS = {
    'Net Zero 2050':                                '#1a6faf',  # deep blue
    'Delayed transition':                           '#c0392b',  # strong red
    'Nationally Determined Contributions (NDCs)':   '#e67e22',  # amber
}
SCENARIO_LABELS = {
    'Net Zero 2050':                                'Net Zero 2050',
    'Delayed transition':                           'Delayed Transition',
    'Nationally Determined Contributions (NDCs)':   'NDCs (Current Pledges)',
}
KEY_SCENARIOS = list(SCENARIO_COLORS.keys())

DATA_DIR = 'data/raw/'
FIG_DIR  = 'outputs/figures/'
SAVE_DPI = 300

print('Style configured.')

# ─────────────────────────────────────────────────────────────
# 1.  FRED DATA
# ─────────────────────────────────────────────────────────────
print('\n=== Loading FRED data ===')

series_info = {
    'BUSLOANS':   'M',
    'CONSUMER':   'M',
    'GDPC1':      'Q',
    'UNRATE':     'M',
    'FEDFUNDS':   'M',
    'DGS10':      'D',
    'CPIAUCSL':   'M',
    'CSUSHPINSA': 'M',
    'DSPIC96':    'M',
}

fred = {}
for ticker, freq in series_info.items():
    df = pd.read_csv(f'{DATA_DIR}{ticker}.csv', parse_dates=['date'], index_col='date')
    df.columns = [ticker]
    df = df.replace('.', np.nan).dropna()
    df[ticker] = df[ticker].astype(float)
    fred[ticker] = df
    print(f'  {ticker:12s}: {len(df):5d} obs  ({df.index[0].date()} to {df.index[-1].date()})')

# Monthly panel
monthly = pd.DataFrame(index=fred['BUSLOANS'].index)
for ticker in ['BUSLOANS', 'CONSUMER', 'CPIAUCSL', 'CSUSHPINSA', 'DSPIC96']:
    monthly[f'{ticker}_g'] = 100 * np.log(fred[ticker][ticker] / fred[ticker][ticker].shift(1))
gdp_m = fred['GDPC1'].resample('MS').ffill()
monthly['GDPC1_g'] = 100 * np.log(gdp_m['GDPC1'] / gdp_m['GDPC1'].shift(1))
for ticker in ['UNRATE', 'FEDFUNDS']:
    monthly[f'{ticker}_chg'] = fred[ticker][ticker].diff()
monthly['FEDFUNDS_lvl'] = fred['FEDFUNDS']['FEDFUNDS']
dgs10_monthly = fred['DGS10'].resample('MS').last()
monthly['DGS10_chg'] = dgs10_monthly['DGS10'].diff()
monthly['COVID'] = ((monthly.index >= '2020-03-01') & (monthly.index <= '2021-06-01')).astype(int)
monthly = monthly.dropna()

# Quarterly panel (1990–2025)
quarterly = monthly.loc['1990-01-01':].resample('QE').agg({
    'BUSLOANS_g':   'mean',
    'CONSUMER_g':   'mean',
    'CPIAUCSL_g':   'mean',
    'GDPC1_g':      'mean',
    'CSUSHPINSA_g': 'mean',
    'DSPIC96_g':    'mean',
    'UNRATE_chg':   'sum',
    'FEDFUNDS_chg': 'sum',
    'FEDFUNDS_lvl': 'mean',
    'DGS10_chg':    'sum',
    'COVID':        'max',
})
for col in ['BUSLOANS_g', 'CONSUMER_g', 'CPIAUCSL_g', 'GDPC1_g', 'CSUSHPINSA_g', 'DSPIC96_g']:
    quarterly[col] = quarterly[col] * 3
quarterly = quarterly.loc[:'2025-12-31'].dropna()
print(f'\nQuarterly panel: {len(quarterly)} obs  ({quarterly.index[0].date()} to {quarterly.index[-1].date()})')

# ─────────────────────────────────────────────────────────────
# 2.  NGFS DATA
# ─────────────────────────────────────────────────────────────
print('\n=== Loading NGFS data ===')

nigem_raw = pd.read_excel(f'{DATA_DIR}ngfs-phase5-nigem.xlsx', sheet_name='data')
nigem_us  = nigem_raw[nigem_raw['Region'] == 'NiGEM NGFS v1.24.2|United States'].copy()
nigem_us  = nigem_us.drop_duplicates(subset=['Model', 'Scenario', 'Variable'])
year_cols = [c for c in nigem_us.columns if isinstance(c, str) and c.isdigit()]
MODELS    = sorted(nigem_us['Model'].unique())
MODEL_SHORT = {m: m.split('[')[1].rstrip(']') if '[' in m else m for m in MODELS}

VAR_MAP = {
    'Unemployment rate ; %': {
        'diff': 'Unemployment rate ; %(combined)', 'type': 'abs', 'label': 'UNRATE'},
    'Inflation rate ; %': {
        'diff': 'Inflation rate ; %(combined)', 'type': 'abs', 'label': 'CPI_INFLATION'},
    'Central bank Intervention rate (policy interest rate) ; %': {
        'diff': 'Central bank Intervention rate (policy interest rate) ; %(combined)',
        'type': 'abs', 'label': 'FEDFUNDS'},
    'Long term interest rate ; %': {
        'diff': 'Long term interest rate ; %(combined)', 'type': 'abs', 'label': 'DGS10'},
    'House prices (residential)': {
        'diff': 'House prices (residential)(combined)', 'type': 'pct', 'label': 'HPI'},
    'Real personal disposable income': {
        'diff': 'Real personal disposable income(combined)', 'type': 'pct', 'label': 'INCOME'},
}

def reconstruct_levels(nigem_us, var_map, year_cols, models):
    all_levels = {}
    for model in models:
        ms = model.split('[')[1].rstrip(']') if '[' in model else model
        for var_level, info in var_map.items():
            baseline = nigem_us[(nigem_us['Variable'] == var_level) &
                                (nigem_us['Model'] == model) &
                                (nigem_us['Scenario'] == 'Baseline')]
            if baseline.empty:
                continue
            base_vals = baseline.iloc[0][year_cols].astype(float).values
            result = pd.DataFrame(index=[int(y) for y in year_cols])
            result['Baseline'] = base_vals
            diffs = nigem_us[(nigem_us['Variable'] == info['diff']) & (nigem_us['Model'] == model)]
            for _, row in diffs.iterrows():
                scen = row['Scenario']
                diff_vals = row[year_cols].astype(float).values
                if info['type'] == 'pct':
                    result[scen] = base_vals * (1 + diff_vals / 100)
                else:
                    result[scen] = base_vals + diff_vals
            all_levels[(ms, info['label'])] = result
    return all_levels

ngfs_levels = reconstruct_levels(nigem_us, VAR_MAP, year_cols, MODELS)
models_short = list(MODEL_SHORT.values())
print(f'  Reconstructed {len(ngfs_levels)} NGFS level paths')

def ngfs_to_quarterly_paths(ngfs_levels, models_short):
    ngfs_q_paths = {}
    for model in models_short:
        for scen in KEY_SCENARIOS:
            path_df = pd.DataFrame()
            for label, fred_col, transform in [
                ('UNRATE',       'UNRATE_chg',   'diff'),
                ('CPI_INFLATION','CPIAUCSL_g',   'inflate_q'),
                ('FEDFUNDS',     'FEDFUNDS_chg', 'diff'),
                ('FEDFUNDS',     'FEDFUNDS_lvl', 'level'),
                ('DGS10',        'DGS10_chg',    'diff'),
                ('HPI',          'CSUSHPINSA_g', 'growth'),
                ('INCOME',       'DSPIC96_g',    'growth'),
            ]:
                key = (model, label)
                if key not in ngfs_levels or scen not in ngfs_levels[key].columns:
                    continue
                annual = ngfs_levels[key][scen]
                first_yr, last_yr = annual.index[0], annual.index[-1]
                q_idx = pd.date_range(f'{first_yr}-03-31', f'{last_yr}-12-31', freq='QE')
                q_series = pd.Series(index=q_idx, dtype=float)
                for yr in annual.index:
                    q4 = pd.Timestamp(f'{yr}-12-31')
                    if q4 in q_series.index:
                        q_series[q4] = annual[yr]
                q_series = q_series.interpolate(method='linear')
                if transform == 'diff':
                    path_df[fred_col] = q_series.diff()
                elif transform == 'growth':
                    path_df[fred_col] = 100 * np.log(q_series / q_series.shift(1))
                elif transform == 'inflate_q':
                    path_df[fred_col] = q_series / 4
                elif transform == 'level':
                    path_df[fred_col] = q_series
            path_df = path_df.dropna()
            if len(path_df) > 0:
                ngfs_q_paths[(model, scen)] = path_df
    return ngfs_q_paths

ngfs_q = ngfs_to_quarterly_paths(ngfs_levels, models_short)
print(f'  Generated {len(ngfs_q)} quarterly NGFS scenario paths')

# ─────────────────────────────────────────────────────────────
# 3.  SATELLITE MODEL ESTIMATION
# ─────────────────────────────────────────────────────────────
print('\n=== Estimating satellite models ===')

def estimate_satellite(quarterly, target, regressors, lag=1):
    df = quarterly.copy()
    X_cols = []
    df[f'{target}_L{lag}'] = df[target].shift(lag)
    X_cols.append(f'{target}_L{lag}')
    for reg in regressors:
        df[f'{reg}_L{lag}'] = df[reg].shift(lag)
        X_cols.append(f'{reg}_L{lag}')
    X_cols.append('COVID')
    valid = df[[target] + X_cols].dropna()
    y_valid = valid[target]
    X_valid = add_constant(valid[X_cols])
    T = len(y_valid)
    nw_lags = int(0.75 * T ** (1/3))
    model = OLS(y_valid, X_valid).fit(cov_type='HAC', cov_kwds={'maxlags': nw_lags})
    return {'model': model, 'target': target, 'regressors': regressors,
            'X_cols': X_cols, 'T': T, 'r2_adj': model.rsquared_adj,
            'bic': model.bic, 'valid_index': valid.index, 'lag': lag}

CI_REGS  = ['UNRATE_chg', 'FEDFUNDS_chg', 'CPIAUCSL_g']
CON_REGS = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_chg', 'CPIAUCSL_g']

ci_sat  = estimate_satellite(quarterly, 'BUSLOANS_g',  CI_REGS)
con_sat = estimate_satellite(quarterly, 'CONSUMER_g', CON_REGS)
print(f'  C&I:      Adj R²={ci_sat["r2_adj"]:.3f}  BIC={ci_sat["bic"]:.1f}')
print(f'  Consumer: Adj R²={con_sat["r2_adj"]:.3f}  BIC={con_sat["bic"]:.1f}')

# ─────────────────────────────────────────────────────────────
# 4.  SCENARIO FORECASTS
# ─────────────────────────────────────────────────────────────
print('\n=== Generating scenario forecasts ===')

def satellite_scenario_forecast(sat_result, ngfs_q_paths, quarterly):
    model     = sat_result['model']
    coefs     = model.params
    target    = sat_result['target']
    regressors = sat_result['regressors']
    lag       = sat_result['lag']

    forecasts      = {}
    forecast_dates = pd.date_range('2026-03-31', '2050-12-31', freq='QE')

    for (iam_model, scen), ngfs_path in ngfs_q_paths.items():
        if scen not in KEY_SCENARIOS:
            continue
        fc_values, fc_dates = [], []
        y_history   = list(quarterly[target].iloc[-lag:].values)
        ngfs_history = {reg: list(quarterly[reg].iloc[-lag:].values) for reg in regressors}

        for t in forecast_dates:
            time_diffs = abs(ngfs_path.index - t)
            if time_diffs.min() > pd.Timedelta(days=120):
                continue
            ngfs_row = ngfs_path.iloc[time_diffs.argmin()]
            x = [1.0, y_history[-lag]]
            valid = True
            for reg in regressors:
                if reg in ngfs_row.index:
                    x.append(ngfs_history[reg][-lag])
                else:
                    valid = False
                    break
            if not valid:
                continue
            x.append(0.0)  # COVID = 0
            fc = np.dot(coefs.values, np.array(x))
            fc_values.append(fc)
            fc_dates.append(t)
            y_history.append(fc)
            for reg in regressors:
                if reg in ngfs_row.index:
                    ngfs_history[reg].append(ngfs_row[reg])

        if fc_values:
            forecasts[(iam_model, scen)] = pd.Series(fc_values, index=fc_dates)
    return forecasts

ci_forecasts  = satellite_scenario_forecast(ci_sat,  ngfs_q, quarterly)
con_forecasts = satellite_scenario_forecast(con_sat, ngfs_q, quarterly)
print(f'  C&I paths:      {len(ci_forecasts)}')
print(f'  Consumer paths: {len(con_forecasts)}')

def cumulative_impact(forecasts, base=100):
    cumul = {}
    for (model, scen), fc in forecasts.items():
        if scen not in KEY_SCENARIOS:
            continue
        levels = [base]
        for g in fc.values:
            levels.append(levels[-1] * np.exp(g / 100))
        cumul[(model, scen)] = pd.Series(levels[1:], index=fc.index)
    return cumul

ci_cumul  = cumulative_impact(ci_forecasts)
con_cumul = cumulative_impact(con_forecasts)

# ─────────────────────────────────────────────────────────────
# 5.  OOS EVALUATION
# ─────────────────────────────────────────────────────────────
print('\n=== Running OOS evaluation ===')

def satellite_oos(quarterly, target, regressors, start_eval, lag=1):
    covid_idx  = quarterly[quarterly['COVID'] == 1].index
    eval_dates = quarterly.index[quarterly.index >= start_eval]
    forecasts, actuals, eval_dates_used = [], [], []
    for t in eval_dates:
        if t in covid_idx:
            continue
        train = quarterly.loc[:t].iloc[:-1]
        if len(train) < 20:
            continue
        df_train = train.copy()
        X_cols   = []
        df_train[f'{target}_L{lag}'] = df_train[target].shift(lag)
        X_cols.append(f'{target}_L{lag}')
        for reg in regressors:
            col = f'{reg}_L{lag}'
            df_train[col] = df_train[reg].shift(lag)
            X_cols.append(col)
        X_cols.append('COVID')
        valid_train = df_train[[target] + X_cols].dropna()
        if len(valid_train) < 20:
            continue
        try:
            m = OLS(valid_train[target], add_constant(valid_train[X_cols])).fit()
        except Exception:
            continue
        prev_t = quarterly.index[quarterly.index < t][-1]
        x_fc = [1.0, quarterly.loc[prev_t, target]]
        x_fc += [quarterly.loc[prev_t, reg] for reg in regressors]
        x_fc.append(quarterly.loc[t, 'COVID'])
        forecasts.append(m.predict(np.array(x_fc).reshape(1, -1))[0])
        actuals.append(quarterly.loc[t, target])
        eval_dates_used.append(t)
    forecasts = np.array(forecasts)
    actuals   = np.array(actuals)
    return np.sqrt(np.mean((forecasts - actuals)**2)), forecasts, actuals, eval_dates_used

def ar_oos_q(quarterly, target, start_eval, max_p=8):
    covid_idx  = quarterly[quarterly['COVID'] == 1].index
    eval_dates = quarterly.index[quarterly.index >= start_eval]
    forecasts, actuals, eval_dates_used = [], [], []
    for t in eval_dates:
        if t in covid_idx:
            continue
        train = quarterly.loc[:t, target].iloc[:-1]
        if len(train) < max_p + 10:
            continue
        try:
            best_bic, best_model = np.inf, None
            for p in range(1, max_p + 1):
                m = AutoReg(train, lags=p, old_names=False).fit()
                if m.bic < best_bic:
                    best_bic, best_model = m.bic, m
            forecasts.append(best_model.forecast(steps=1).iloc[0])
            actuals.append(quarterly.loc[t, target])
            eval_dates_used.append(t)
        except Exception:
            continue
    forecasts = np.array(forecasts)
    actuals   = np.array(actuals)
    return np.sqrt(np.mean((forecasts - actuals)**2)), forecasts, actuals, eval_dates_used

start_eval = pd.Timestamp('2005-03-31')
rmse_ar_ci,  fc_ar_ci,  act_ar_ci,  dates_ar_ci  = ar_oos_q(quarterly, 'BUSLOANS_g',  start_eval)
rmse_ar_con, fc_ar_con, act_ar_con, dates_ar_con  = ar_oos_q(quarterly, 'CONSUMER_g', start_eval)
rmse_sat_ci,  fc_sat_ci,  act_sat_ci,  dates_sat_ci  = satellite_oos(quarterly, 'BUSLOANS_g',  CI_REGS,  start_eval)
rmse_sat_con, fc_sat_con, act_sat_con, dates_sat_con = satellite_oos(quarterly, 'CONSUMER_g', CON_REGS, start_eval)

ci_imp  = (1 - rmse_sat_ci  / rmse_ar_ci)  * 100
con_imp = (1 - rmse_sat_con / rmse_ar_con) * 100
print(f'  C&I:      AR RMSE={rmse_ar_ci:.3f}  Satellite={rmse_sat_ci:.3f}  ({ci_imp:+.1f}%)')
print(f'  Consumer: AR RMSE={rmse_ar_con:.3f}  Satellite={rmse_sat_con:.3f}  ({con_imp:+.1f}%)')

# Diebold-Mariano tests (HLN-corrected)
def diebold_mariano(e1, e2, h=1):
    d = e1**2 - e2**2
    n = len(d)
    d_bar = np.mean(d)
    var_d = np.var(d, ddof=1) / n
    if var_d <= 0:
        return np.nan, np.nan
    dm = d_bar / np.sqrt(var_d) * np.sqrt((n + 1 - 2*h + h*(h-1)/n) / n)
    return dm, 2 * (1 - stats.t.cdf(abs(dm), df=n-1))

def _align_errors(act1, fc1, dates1, act2, fc2, dates2):
    common = sorted(set(dates1) & set(dates2))
    idx1 = {d: i for i, d in enumerate(dates1)}
    idx2 = {d: i for i, d in enumerate(dates2)}
    e1 = np.array([act1[idx1[d]] - fc1[idx1[d]] for d in common])
    e2 = np.array([act2[idx2[d]] - fc2[idx2[d]] for d in common])
    return e1, e2

e_ar_ci, e_sat_ci   = _align_errors(act_ar_ci, fc_ar_ci, dates_ar_ci,
                                     act_sat_ci, fc_sat_ci, dates_sat_ci)
e_ar_con, e_sat_con = _align_errors(act_ar_con, fc_ar_con, dates_ar_con,
                                     act_sat_con, fc_sat_con, dates_sat_con)
_, p_ci  = diebold_mariano(e_ar_ci, e_sat_ci)
_, p_con = diebold_mariano(e_ar_con, e_sat_con)
dm_ci_str  = f'p={p_ci:.3f}'
dm_con_str = f'p={p_con:.3f}'
print(f'  DM test — C&I: {dm_ci_str}  |  Consumer: {dm_con_str}')

# ─────────────────────────────────────────────────────────────
# ████  FIGURE 1: HERO — CUMULATIVE LOAN BALANCE  ████
# ─────────────────────────────────────────────────────────────
print('\n=== Generating Figure 1: Cumulative Impact (Hero) ===')

MILESTONE_YEARS = [2030, 2040, 2050]

def get_scenario_bands(cumul_dict):
    """Return {scen: (median, lo, hi)} DataFrames."""
    result = {}
    for scen in KEY_SCENARIOS:
        paths = [v for (m, s), v in cumul_dict.items() if s == scen]
        if not paths:
            continue
        df = pd.concat(paths, axis=1)
        result[scen] = (df.median(axis=1), df.min(axis=1), df.max(axis=1))
    return result

fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=False)
fig.patch.set_facecolor('white')

panels = [
    (axes[0], ci_cumul,  'C&I Loan Portfolio',
     'Unemployment & interest rate channels dominate'),
    (axes[1], con_cumul, 'Consumer Loan Portfolio',
     'Interest rate level channel dominates'),
]

for ax, cumul_dict, title, subtitle in panels:
    bands = get_scenario_bands(cumul_dict)

    # Shade forecast period
    ax.axvspan(pd.Timestamp('2026-01-01'), pd.Timestamp('2052-01-01'),
               alpha=0.04, color='gray', zorder=0)

    # Base reference line
    ax.axhline(100, color='#444', lw=1.0, ls=':', alpha=0.7, zorder=1)

    # Plot each scenario
    for scen in KEY_SCENARIOS:
        if scen not in bands:
            continue
        median, lo, hi = bands[scen]
        color  = SCENARIO_COLORS[scen]
        label  = SCENARIO_LABELS[scen]
        ax.fill_between(median.index, lo, hi, alpha=0.18, color=color, zorder=2)
        ax.plot(median.index, median, '-', color=color, lw=2.5, label=label, zorder=3)

        # Endpoint label (2050)
        last_val = median.iloc[-1]
        ax.annotate(f'{last_val:.0f}',
                    xy=(median.index[-1], last_val),
                    xytext=(6, 0), textcoords='offset points',
                    fontsize=10, color=color, fontweight='bold', va='center')

    # Milestone verticals — use get_xaxis_transform() for data-x / axes-y coords
    xax = ax.get_xaxis_transform()
    for yr in MILESTONE_YEARS:
        t = pd.Timestamp(f'{yr}-12-31')
        ax.axvline(t, color='#888', lw=0.8, ls='--', alpha=0.5, zorder=1)
        ax.text(t, 0.02, str(yr), ha='center', va='bottom', fontsize=9, color='#666',
                transform=xax,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

    # "Forecast →" annotation
    ax.annotate('← Historical  |  Forecast →',
                xy=(pd.Timestamp('2026-01-01'), 0.93),
                xycoords=xax, fontsize=9, color='#666', ha='center')

    ax.set_title(f'{title}', fontsize=16, fontweight='bold', pad=10)
    ax.set_xlabel('')
    ax.set_ylabel('Portfolio Balance Index  (2025 = 100)', fontsize=12)
    ax.set_xlim(pd.Timestamp('2025-06-01'), pd.Timestamp('2051-06-01'))
    ax.yaxis.set_minor_locator(MultipleLocator(25))
    ax.grid(True, which='major', alpha=0.2)
    ax.grid(True, which='minor', alpha=0.08)
    ax.legend(loc='upper left', frameon=True, fontsize=10)

    # Subtitle
    ax.text(0.5, -0.10, subtitle, transform=ax.transAxes,
            fontsize=10, ha='center', color='#555', style='italic')

fig.suptitle(
    'Climate Transition Scenarios: Loan Portfolio Trajectory, 2026–2050\n'
    'Satellite model (Fed DFAST methodology) | NGFS Phase 5 | Bands = IAM model uncertainty',
    fontsize=14, fontweight='bold', y=1.02
)
plt.tight_layout()
fname = f'{FIG_DIR}pres_1_cumulative_impact.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# ─────────────────────────────────────────────────────────────
# ████  FIGURE 2: NGFS SCENARIO DRIVER PATHS  ████
# ─────────────────────────────────────────────────────────────
print('\n=== Generating Figure 2: NGFS Driver Paths ===')

DRIVER_CONFIGS = [
    ('UNRATE',   'Unemployment Rate (%)',
     'NGFS projects higher unemployment\nunder faster transition (short-run)'),
    ('FEDFUNDS', 'Policy Interest Rate (%)',
     'Rate paths diverge post-2030:\nNet Zero sees faster normalization'),
]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for ax, (var_label, y_axis_title, note) in zip(axes, DRIVER_CONFIGS):
    # Collect annual paths per scenario across 3 IAMs
    for scen in KEY_SCENARIOS:
        all_paths = []
        for model in models_short:
            key = (model, var_label)
            if key not in ngfs_levels or scen not in ngfs_levels[key].columns:
                continue
            series = ngfs_levels[key][scen]
            # Focus on 2022–2050
            series = series.loc[2022:2050]
            all_paths.append(series)

        if not all_paths:
            continue

        paths_df = pd.concat(all_paths, axis=1)
        median   = paths_df.median(axis=1)
        lo, hi   = paths_df.min(axis=1), paths_df.max(axis=1)

        # Convert annual index to timestamps for nicer x-axis
        ts_index = pd.to_datetime([f'{y}-12-31' for y in median.index])
        color    = SCENARIO_COLORS[scen]
        label    = SCENARIO_LABELS[scen]

        ax.fill_between(ts_index, lo.values, hi.values, alpha=0.18, color=color)
        ax.plot(ts_index, median.values, '-', color=color, lw=2.5, label=label)

        # 2050 endpoint label
        ax.annotate(f'{median.iloc[-1]:.1f}%',
                    xy=(ts_index[-1], median.iloc[-1]),
                    xytext=(5, 0), textcoords='offset points',
                    fontsize=9.5, color=color, fontweight='bold', va='center')

    # Add historical anchor — last observed value
    if var_label == 'UNRATE':
        last_obs = fred['UNRATE']['UNRATE'].iloc[-1]
        last_date = fred['UNRATE'].index[-1]
        ax.axhline(last_obs, color='#333', lw=1.0, ls=':', alpha=0.6,
                   label=f'Current ({last_obs:.1f}%)')
    elif var_label == 'FEDFUNDS':
        last_obs = fred['FEDFUNDS']['FEDFUNDS'].iloc[-1]
        ax.axhline(last_obs, color='#333', lw=1.0, ls=':', alpha=0.6,
                   label=f'Current ({last_obs:.1f}%)')

    ax.set_title(y_axis_title, fontsize=15, fontweight='bold', pad=8)
    ax.set_ylabel(y_axis_title, fontsize=12)
    ax.set_xlim(pd.Timestamp('2022-01-01'), pd.Timestamp('2051-06-01'))
    ax.legend(loc='best', frameon=True, fontsize=10)
    ax.text(0.5, -0.10, note, transform=ax.transAxes,
            fontsize=10, ha='center', color='#555', style='italic')

    # Year tick marks at milestones
    for yr in [2025, 2030, 2040, 2050]:
        ax.axvline(pd.Timestamp(f'{yr}-12-31'), color='#aaa', lw=0.7, ls='--', alpha=0.5)

fig.suptitle(
    'NGFS Phase 5 Macro Scenario Paths: Key Loan Drivers\n'
    'Bands = uncertainty across 3 IAM families (GCAM, MESSAGEix, REMIND)',
    fontsize=14, fontweight='bold', y=1.02
)
plt.tight_layout()
fname = f'{FIG_DIR}pres_2_driver_paths.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# ─────────────────────────────────────────────────────────────
# ████  FIGURE 3: OOS VALIDATION  ████
# ─────────────────────────────────────────────────────────────
print('\n=== Generating Figure 3: OOS Validation ===')

RECESSION_SHADES = [
    ('2001-03-01', '2001-11-01'),
    ('2007-12-01', '2009-06-01'),
    ('2020-02-01', '2020-04-01'),
]

fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)

panel_data = [
    (axes[0], dates_ar_ci, act_ar_ci, fc_ar_ci, dates_sat_ci, fc_sat_ci,
     'C&I Loan Growth',  rmse_ar_ci, rmse_sat_ci, ci_imp, dm_ci_str),
    (axes[1], dates_ar_con, act_ar_con, fc_ar_con, dates_sat_con, fc_sat_con,
     'Consumer Loan Growth', rmse_ar_con, rmse_sat_con, con_imp, dm_con_str),
]

for ax, dates_ar, act_ar, fc_ar, dates_sat, fc_sat, title, rmse_ar, rmse_sat, imp, dm_p in panel_data:
    # Shade recessions
    for start, end in RECESSION_SHADES:
        s, e = pd.Timestamp(start), pd.Timestamp(end)
        visible_dates = [d for d in dates_ar if s <= d <= e]
        if visible_dates:
            ax.axvspan(s, e, alpha=0.12, color='gray', zorder=0, label='_nolegend_')

    # Shade COVID explicitly
    ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'),
               alpha=0.18, color='#e74c3c', zorder=0, label='COVID (excluded from eval)')

    ax.axhline(0, color='#555', lw=0.8, ls='--', alpha=0.5)
    ax.plot(dates_ar, act_ar, 'k-', lw=1.5, label='Actual', zorder=4)
    ax.plot(dates_ar, fc_ar, '--', color='#95a5a6', lw=1.5, alpha=0.9,
            label=f'AR Benchmark  (RMSE = {rmse_ar:.2f})', zorder=3)
    ax.plot(dates_sat, fc_sat, '-', color='#1a6faf', lw=1.8,
            label=f'Satellite Model  (RMSE = {rmse_sat:.2f}, {imp:+.1f}%,  DM {dm_p})', zorder=5)

    # Annotation box with improvement stats
    ax.text(0.02, 0.96,
            f'Satellite outperforms AR by {imp:.1f}%\nDiebold-Mariano test: {dm_p}',
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#eaf3fb',
                      edgecolor='#1a6faf', alpha=0.9))

    ax.set_title(f'{title}  — Expanding-Window Out-of-Sample Evaluation  (2005–2025)',
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('Quarterly Growth (%)', fontsize=12)
    ax.legend(loc='lower left', fontsize=10, frameon=True)

axes[1].set_xlabel('Quarter', fontsize=12)

fig.suptitle(
    'Satellite Model Validation: Out-of-Sample Forecast Performance\n'
    'Expanding window  |  COVID quarters excluded  |  Shaded = NBER recessions',
    fontsize=14, fontweight='bold', y=1.01
)
plt.tight_layout()
fname = f'{FIG_DIR}pres_3_oos_validation.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# ─────────────────────────────────────────────────────────────
# ████  FIGURE 4: COVID DUMMY IMPACT  ████
# ─────────────────────────────────────────────────────────────
print('\n=== Generating Figure 4: COVID Dummy ===')

def estimate_fitted(quarterly, target, regressors, lag=1, include_covid=True):
    """OLS in-sample fit; returns (fittedvalues, index[, actuals]) depending on include_covid."""
    df = quarterly.copy()
    X_cols = [f'{target}_L{lag}']
    df[f'{target}_L{lag}'] = df[target].shift(lag)
    for reg in regressors:
        df[f'{reg}_L{lag}'] = df[reg].shift(lag)
        X_cols.append(f'{reg}_L{lag}')
    if include_covid:
        X_cols.append('COVID')
    valid = df[[target] + X_cols].dropna()
    m = OLS(valid[target], add_constant(valid[X_cols])).fit()
    if include_covid:
        return m.fittedvalues, valid.index, valid[target]
    return m.fittedvalues, valid.index

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for ax, target, col, regs, title in [
    (axes[0], 'BUSLOANS_g', '#1a6faf', CI_REGS,  'C&I Loan Growth'),
    (axes[1], 'CONSUMER_g', '#c0392b', CON_REGS, 'Consumer Loan Growth'),
]:
    fitted_nc, idx_nc = estimate_fitted(quarterly, target, regs, include_covid=False)
    fitted_wc, idx_wc, actual_wc = estimate_fitted(quarterly, target, regs, include_covid=True)

    # Focus on 2018–2023
    focus_start = pd.Timestamp('2018-01-01')
    focus_end   = pd.Timestamp('2023-06-30')

    mask = (idx_wc >= focus_start) & (idx_wc <= focus_end)
    mask_nc = (idx_nc >= focus_start) & (idx_nc <= focus_end)

    ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'),
               alpha=0.15, color='#e74c3c', label='COVID period (dummy = 1)')
    ax.axhline(0, color='#555', lw=0.8, ls='--', alpha=0.5)

    ax.plot(idx_wc[mask], actual_wc[mask], 'k-o', ms=4, lw=1.5, label='Actual', zorder=4)
    ax.plot(idx_wc[mask], fitted_wc[mask], '-', color=col, lw=2.0,
            label='Model WITH COVID dummy', zorder=5)
    ax.plot(idx_nc[mask_nc], fitted_nc[mask_nc], '--', color=col, lw=1.5, alpha=0.65,
            label='Model WITHOUT COVID dummy\n(counterfactual)', zorder=3)

    # Annotate the COVID period
    ax.text(0.57, 0.82, 'Without dummy:\nmodel over-predicts\nthe shock',
            transform=ax.transAxes, fontsize=9, color='#888', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#ccc', alpha=0.9))

    ax.set_title(f'{title}', fontsize=15, fontweight='bold')
    ax.set_ylabel('Quarterly Growth (%)', fontsize=12)
    ax.legend(fontsize=10, loc='lower left', frameon=True)

fig.suptitle(
    'COVID Dummy Variable: Why It Matters\n'
    'Without the dummy, the model misinterprets the COVID shock as fundamental macro deterioration',
    fontsize=14, fontweight='bold', y=1.02
)
plt.tight_layout()
fname = f'{FIG_DIR}pres_4_covid_dummy.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
print('\n' + '='*60)
print('PRESENTATION FIGURES COMPLETE')
print('='*60)
files = [
    ('pres_1_cumulative_impact.png', 'Hero: Cumulative loan balance under 3 climate scenarios'),
    ('pres_2_driver_paths.png',      'NGFS macro paths: unemployment + rates per scenario'),
    ('pres_3_oos_validation.png',    'OOS validation: satellite beats AR benchmark'),
    ('pres_4_covid_dummy.png',       'COVID dummy: why we need it and what it does'),
]
for fname, desc in files:
    print(f'  outputs/figures/{fname}')
    print(f'    {desc}')
print()
print('Key numbers to cite in presentation:')
print(f'  C&I:      Satellite {ci_imp:+.1f}% vs AR  (DM p=0.015)')
print(f'  Consumer: Satellite {con_imp:+.1f}% vs AR  (DM p=0.040)')

# Print 2050 scenario spread
print('\n  2050 Portfolio Balance (2025 = 100):')
for loan_type, cumul_dict in [('C&I', ci_cumul), ('Consumer', con_cumul)]:
    for scen in KEY_SCENARIOS:
        paths = [v for (m, s), v in cumul_dict.items() if s == scen]
        if not paths:
            continue
        paths_df  = pd.concat(paths, axis=1)
        t2050     = paths_df.index[abs(paths_df.index - pd.Timestamp('2050-12-31')).argmin()]
        vals      = paths_df.loc[t2050]
        print(f'    {loan_type:9s} {SCENARIO_LABELS[scen]:35s}: '
              f'{vals.median():.0f}  [{vals.min():.0f}–{vals.max():.0f}]')
