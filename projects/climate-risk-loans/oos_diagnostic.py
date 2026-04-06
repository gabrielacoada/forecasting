"""
OOS Shift Diagnostic & Historical Trendline Visualizations
===========================================================
1. Diagnose whether the satellite OOS graph has a one-period shift bug
2. Create historical trendlines for all macro variables + C&I loan growth
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa.ar_model import AutoReg
from scipy import stats
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.dpi'] = 150
SAVE_DPI = 300
FIG_DIR = 'outputs/figures/'
DATA_DIR = 'data/raw/'

# ─────────────────────────────────────────────────────────────
# DATA LOADING (identical to satellite_forecasting.ipynb)
# ─────────────────────────────────────────────────────────────
series_info = {
    'BUSLOANS':   ('C&I Loans ($B)', 'M'),
    'CONSUMER':   ('Consumer Loans ($B)', 'M'),
    'GDPC1':      ('Real GDP ($B 2017)', 'Q'),
    'UNRATE':     ('Unemployment Rate (%)', 'M'),
    'FEDFUNDS':   ('Fed Funds Rate (%)', 'M'),
    'DGS10':      ('10-Year Treasury (%)', 'D'),
    'CPIAUCSL':   ('CPI (Index)', 'M'),
    'CSUSHPINSA': ('Case-Shiller HPI (Index)', 'M'),
    'DSPIC96':    ('Real Disposable Income ($B 2017)', 'M'),
}

fred = {}
for ticker, (label, freq) in series_info.items():
    df = pd.read_csv(f'{DATA_DIR}{ticker}.csv', parse_dates=['date'], index_col='date')
    df.columns = [ticker]
    df = df.replace('.', np.nan).dropna()
    df[ticker] = df[ticker].astype(float)
    fred[ticker] = df

# Monthly transformations
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

# Quarterly aggregation
quarterly = monthly.loc['1990-01-01':].resample('QE').agg({
    'BUSLOANS_g': 'mean', 'CONSUMER_g': 'mean', 'CPIAUCSL_g': 'mean',
    'GDPC1_g': 'mean', 'CSUSHPINSA_g': 'mean', 'DSPIC96_g': 'mean',
    'UNRATE_chg': 'sum', 'FEDFUNDS_chg': 'sum', 'FEDFUNDS_lvl': 'mean',
    'DGS10_chg': 'sum', 'COVID': 'max',
})
for col in ['BUSLOANS_g', 'CONSUMER_g', 'CPIAUCSL_g', 'GDPC1_g', 'CSUSHPINSA_g', 'DSPIC96_g']:
    quarterly[col] = quarterly[col] * 3
quarterly = quarterly.loc[:'2025-12-31'].dropna()

print(f'Quarterly panel: {len(quarterly)} obs ({quarterly.index[0].date()} to {quarterly.index[-1].date()})')

# ─────────────────────────────────────────────────────────────
# PART 1: OOS SHIFT DIAGNOSTIC
# ─────────────────────────────────────────────────────────────
print('\n' + '='*70)
print('PART 1: OOS SHIFT DIAGNOSTIC')
print('='*70)

CI_REGS  = ['UNRATE_chg', 'FEDFUNDS_chg', 'CPIAUCSL_g']
CON_REGS = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_chg', 'CPIAUCSL_g']

def satellite_oos(quarterly, target, regressors, start_eval, lag=1):
    """Expanding-window OOS — identical to notebook."""
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
        X_cols = []
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
    """AR baseline OOS — identical to notebook."""
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

# Run OOS for C&I
rmse_ar_ci,  fc_ar_ci,  act_ar_ci,  dates_ar_ci  = ar_oos_q(quarterly, 'BUSLOANS_g', start_eval)
rmse_sat_ci, fc_sat_ci, act_sat_ci, dates_sat_ci = satellite_oos(quarterly, 'BUSLOANS_g', CI_REGS, start_eval)

# Run OOS for Consumer
rmse_ar_con,  fc_ar_con,  act_ar_con,  dates_ar_con  = ar_oos_q(quarterly, 'CONSUMER_g', start_eval)
rmse_sat_con, fc_sat_con, act_sat_con, dates_sat_con = satellite_oos(quarterly, 'CONSUMER_g', CON_REGS, start_eval)

print(f'\nC&I:      AR RMSE={rmse_ar_ci:.3f}  Satellite={rmse_sat_ci:.3f}  ({(1-rmse_sat_ci/rmse_ar_ci)*100:+.1f}%)')
print(f'Consumer: AR RMSE={rmse_ar_con:.3f}  Satellite={rmse_sat_con:.3f}  ({(1-rmse_sat_con/rmse_ar_con)*100:+.1f}%)')

# ── Diagnostic 1: Check that forecast dates and actual dates are aligned ──
print('\n--- Diagnostic 1: Date alignment ---')
for name, dates, fc, act in [
    ('C&I Satellite', dates_sat_ci, fc_sat_ci, act_sat_ci),
    ('C&I AR', dates_ar_ci, fc_ar_ci, act_ar_ci),
    ('Consumer Satellite', dates_sat_con, fc_sat_con, act_sat_con),
    ('Consumer AR', dates_ar_con, fc_ar_con, act_ar_con),
]:
    print(f'\n  {name}: {len(dates)} eval dates')
    print(f'    First 5 dates: {[str(d.date()) for d in dates[:5]]}')
    print(f'    First 5 actuals: {[f"{a:.2f}" for a in act[:5]]}')
    print(f'    First 5 forecasts: {[f"{f:.2f}" for f in fc[:5]]}')
    # Verify actuals match the quarterly data at those dates
    for i, d in enumerate(dates[:5]):
        true_val = quarterly.loc[d, 'BUSLOANS_g' if 'C&I' in name else 'CONSUMER_g']
        match = '✓' if abs(act[i] - true_val) < 1e-10 else '✗ MISMATCH'
        print(f'    Date {d.date()}: actual={act[i]:.4f}, quarterly[{d.date()}]={true_val:.4f} {match}')

# ── Diagnostic 2: Cross-correlation of forecast with actual at different leads/lags ──
print('\n--- Diagnostic 2: Cross-correlation test (is forecast shifted?) ---')
for name, dates, fc, act in [
    ('C&I Satellite', dates_sat_ci, fc_sat_ci, act_sat_ci),
    ('Consumer Satellite', dates_sat_con, fc_sat_con, act_sat_con),
]:
    print(f'\n  {name}:')
    # Correlation of forecast with actual (same period)
    corr_0 = np.corrcoef(fc, act)[0,1]
    print(f'    corr(forecast_t, actual_t)   = {corr_0:.4f}  ← should be highest')

    # Correlation of forecast with actual shifted by 1 (forecast leads actual)
    corr_lead = np.corrcoef(fc[:-1], act[1:])[0,1]
    print(f'    corr(forecast_t, actual_t+1) = {corr_lead:.4f}  ← if this is higher, forecast is late')

    # Correlation of forecast with actual shifted by -1 (forecast lags actual)
    corr_lag = np.corrcoef(fc[1:], act[:-1])[0,1]
    print(f'    corr(forecast_t, actual_t-1) = {corr_lag:.4f}  ← if this is higher, forecast is early')

    # Also: correlation of forecast with LAGGED actual (i.e., is forecast just repeating last known value?)
    # This checks if forecast ≈ y_{t-1}
    actual_lagged = []
    for d in dates:
        prev_d = quarterly.index[quarterly.index < d][-1]
        target = 'BUSLOANS_g' if 'C&I' in name else 'CONSUMER_g'
        actual_lagged.append(quarterly.loc[prev_d, target])
    actual_lagged = np.array(actual_lagged)
    corr_naive = np.corrcoef(fc, actual_lagged)[0,1]
    print(f'    corr(forecast_t, actual_t-1_from_data) = {corr_naive:.4f}')

    # MSE at different alignments
    mse_0 = np.mean((fc - act)**2)
    mse_lead = np.mean((fc[:-1] - act[1:])**2)
    mse_lag = np.mean((fc[1:] - act[:-1])**2)
    print(f'    MSE(fc_t, actual_t)   = {mse_0:.4f}')
    print(f'    MSE(fc_t, actual_t+1) = {mse_lead:.4f}')
    print(f'    MSE(fc_t, actual_t-1) = {mse_lag:.4f}')

# ── Diagnostic 3: Check if AR model and Satellite have same eval dates ──
print('\n--- Diagnostic 3: Do AR and Satellite share the same evaluation dates? ---')
common_ci = set(dates_ar_ci) & set(dates_sat_ci)
print(f'  C&I: AR has {len(dates_ar_ci)} dates, Satellite has {len(dates_sat_ci)} dates, {len(common_ci)} in common')
ar_only = set(dates_ar_ci) - set(dates_sat_ci)
sat_only = set(dates_sat_ci) - set(dates_ar_ci)
if ar_only:
    print(f'    AR only: {sorted([d.date() for d in ar_only])}')
if sat_only:
    print(f'    Sat only: {sorted([d.date() for d in sat_only])}')

common_con = set(dates_ar_con) & set(dates_sat_con)
print(f'  Consumer: AR has {len(dates_ar_con)} dates, Satellite has {len(dates_sat_con)} dates, {len(common_con)} in common')

# ── Diagnostic 4: Spot-check a few forecasts manually ──
print('\n--- Diagnostic 4: Manual spot-check of forecast computation ---')
target = 'BUSLOANS_g'
regressors = CI_REGS
lag = 1
t = dates_sat_ci[10]  # Pick a middle date
print(f'\n  Spot-checking C&I forecast at t = {t.date()}')

train = quarterly.loc[:t].iloc[:-1]
df_train = train.copy()
X_cols = []
df_train[f'{target}_L{lag}'] = df_train[target].shift(lag)
X_cols.append(f'{target}_L{lag}')
for reg in regressors:
    col = f'{reg}_L{lag}'
    df_train[col] = df_train[reg].shift(lag)
    X_cols.append(col)
X_cols.append('COVID')
valid_train = df_train[[target] + X_cols].dropna()
m = OLS(valid_train[target], add_constant(valid_train[X_cols])).fit()

prev_t = quarterly.index[quarterly.index < t][-1]
print(f'  prev_t = {prev_t.date()}')
print(f'  Training ends at: {train.index[-1].date()} (= prev_t? {train.index[-1] == prev_t})')
print(f'  Actual target at t ({t.date()}): {quarterly.loc[t, target]:.4f}')
print(f'  Actual target at prev_t ({prev_t.date()}): {quarterly.loc[prev_t, target]:.4f}')
print(f'  Regressors at prev_t:')
for reg in regressors:
    print(f'    {reg} = {quarterly.loc[prev_t, reg]:.4f}')

x_fc = [1.0, quarterly.loc[prev_t, target]]
x_fc += [quarterly.loc[prev_t, reg] for reg in regressors]
x_fc.append(quarterly.loc[t, 'COVID'])
fc_manual = m.predict(np.array(x_fc).reshape(1, -1))[0]
print(f'  Manual forecast: {fc_manual:.4f}')
print(f'  Stored forecast: {fc_sat_ci[10]:.4f}')
print(f'  Match: {"✓" if abs(fc_manual - fc_sat_ci[10]) < 1e-10 else "✗ MISMATCH"}')

# ── Diagnostic 5: Visual check — zoomed in OOS plot with point labels ──
print('\n--- Generating diagnostic OOS plot ---')
fig, axes = plt.subplots(2, 2, figsize=(20, 14))

for row, (target_name, dates_ar, act_ar, fc_ar, dates_sat, fc_sat, act_sat) in enumerate([
    ('C&I', dates_ar_ci, act_ar_ci, fc_ar_ci, dates_sat_ci, fc_sat_ci, act_sat_ci),
    ('Consumer', dates_ar_con, act_ar_con, fc_ar_con, dates_sat_con, fc_sat_con, act_sat_con),
]):
    # Left panel: full OOS
    ax = axes[row, 0]
    ax.plot(dates_sat, act_sat, 'k-o', ms=4, lw=1.2, label='Actual', zorder=4)
    ax.plot(dates_sat, fc_sat, 'r-^', ms=3, lw=1, alpha=0.8,
            label='Satellite Forecast', zorder=5)
    ax.plot(dates_ar, fc_ar, 'b--s', ms=2, lw=0.8, alpha=0.6,
            label='AR Forecast', zorder=3)
    ax.axhline(0, color='black', lw=0.5, ls='--')
    ax.set_title(f'{target_name} — Full OOS (2005–2025)', fontweight='bold')
    ax.set_ylabel('Quarterly Growth (%)')
    ax.legend(fontsize=8)

    # Right panel: zoomed to last 20 points for visual inspection
    ax = axes[row, 1]
    n_zoom = 20
    d_zoom = dates_sat[-n_zoom:]
    a_zoom = act_sat[-n_zoom:]
    f_zoom = fc_sat[-n_zoom:]

    ax.plot(d_zoom, a_zoom, 'k-o', ms=6, lw=1.5, label='Actual', zorder=4)
    ax.plot(d_zoom, f_zoom, 'r-^', ms=5, lw=1.2, label='Satellite Forecast', zorder=5)

    # Add value annotations
    for i in range(len(d_zoom)):
        ax.annotate(f'{a_zoom[i]:.1f}', (d_zoom[i], a_zoom[i]),
                    textcoords='offset points', xytext=(0, 8), fontsize=6, ha='center', color='black')
        ax.annotate(f'{f_zoom[i]:.1f}', (d_zoom[i], f_zoom[i]),
                    textcoords='offset points', xytext=(0, -12), fontsize=6, ha='center', color='red')

    ax.axhline(0, color='black', lw=0.5, ls='--')
    ax.set_title(f'{target_name} — Last {n_zoom} Quarters (zoomed)', fontweight='bold')
    ax.set_ylabel('Quarterly Growth (%)')
    ax.legend(fontsize=8)

plt.suptitle('OOS Shift Diagnostic — Are forecasts aligned with the correct time period?',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
fname = f'{FIG_DIR}oos_shift_diagnostic.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# ─────────────────────────────────────────────────────────────
# PART 2: HISTORICAL TRENDLINE VISUALIZATIONS
# ─────────────────────────────────────────────────────────────
print('\n' + '='*70)
print('PART 2: HISTORICAL TRENDLINE VISUALIZATIONS')
print('='*70)

# --- Figure A: C&I and Consumer Loan Levels + Growth Rates ---
fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Panel 1: C&I Loan Levels
ax = axes[0, 0]
busloans = fred['BUSLOANS']
ax.plot(busloans.index, busloans['BUSLOANS'], color='#1a6faf', lw=1.5)
ax.axvspan(pd.Timestamp('2007-12-01'), pd.Timestamp('2009-06-01'), alpha=0.15, color='gray', label='GFC')
ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'), alpha=0.15, color='red', label='COVID')
ax.set_title('C&I Loans — Level ($B)', fontsize=13, fontweight='bold')
ax.set_ylabel('Billions ($)')
ax.legend(fontsize=9)

# Panel 2: Consumer Loan Levels
ax = axes[0, 1]
consumer = fred['CONSUMER']
ax.plot(consumer.index, consumer['CONSUMER'], color='#d95f02', lw=1.5)
ax.axvspan(pd.Timestamp('2007-12-01'), pd.Timestamp('2009-06-01'), alpha=0.15, color='gray', label='GFC')
ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'), alpha=0.15, color='red', label='COVID')
ax.set_title('Consumer Loans — Level ($B)', fontsize=13, fontweight='bold')
ax.set_ylabel('Billions ($)')
ax.legend(fontsize=9)

# Panel 3: C&I Loan Growth Rate (quarterly)
ax = axes[1, 0]
ax.plot(quarterly.index, quarterly['BUSLOANS_g'], color='#1a6faf', lw=1.2)
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.fill_between(quarterly.index, 0, quarterly['BUSLOANS_g'],
                where=quarterly['BUSLOANS_g'] > 0, alpha=0.15, color='#1a6faf')
ax.fill_between(quarterly.index, 0, quarterly['BUSLOANS_g'],
                where=quarterly['BUSLOANS_g'] < 0, alpha=0.15, color='red')
ax.axvspan(pd.Timestamp('2007-12-01'), pd.Timestamp('2009-06-01'), alpha=0.1, color='gray')
ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'), alpha=0.1, color='red')
ax.set_title('C&I Loan Growth Rate (Quarterly, %)', fontsize=13, fontweight='bold')
ax.set_ylabel('Growth (%)')

# Panel 4: Consumer Loan Growth Rate (quarterly)
ax = axes[1, 1]
ax.plot(quarterly.index, quarterly['CONSUMER_g'], color='#d95f02', lw=1.2)
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.fill_between(quarterly.index, 0, quarterly['CONSUMER_g'],
                where=quarterly['CONSUMER_g'] > 0, alpha=0.15, color='#d95f02')
ax.fill_between(quarterly.index, 0, quarterly['CONSUMER_g'],
                where=quarterly['CONSUMER_g'] < 0, alpha=0.15, color='red')
ax.axvspan(pd.Timestamp('2007-12-01'), pd.Timestamp('2009-06-01'), alpha=0.1, color='gray')
ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-06-01'), alpha=0.1, color='red')
ax.set_title('Consumer Loan Growth Rate (Quarterly, %)', fontsize=13, fontweight='bold')
ax.set_ylabel('Growth (%)')

plt.suptitle('Historical Loan Portfolio Trends (1990–2025)',
             fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
fname = f'{FIG_DIR}historical_loan_trends.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# --- Figure B: Macro Variable Trendlines (all key regressors) ---
fig, axes = plt.subplots(3, 2, figsize=(18, 16))

RECESSION_SHADES = [
    ('2001-03-01', '2001-11-01'),
    ('2007-12-01', '2009-06-01'),
    ('2020-02-01', '2020-04-01'),
]

def add_recessions(ax):
    for start, end in RECESSION_SHADES:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   alpha=0.12, color='gray', zorder=0)

# Panel 1: Unemployment Rate (level)
ax = axes[0, 0]
unrate = fred['UNRATE']
ax.plot(unrate.loc['1990':].index, unrate.loc['1990':, 'UNRATE'], color='#e74c3c', lw=1.5)
add_recessions(ax)
ax.set_title('Unemployment Rate (%)', fontsize=13, fontweight='bold')
ax.set_ylabel('Percent')

# Panel 2: Unemployment Rate Change (quarterly)
ax = axes[0, 1]
ax.plot(quarterly.index, quarterly['UNRATE_chg'], color='#e74c3c', lw=1.2)
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.fill_between(quarterly.index, 0, quarterly['UNRATE_chg'],
                where=quarterly['UNRATE_chg'] > 0, alpha=0.2, color='#e74c3c')
ax.fill_between(quarterly.index, 0, quarterly['UNRATE_chg'],
                where=quarterly['UNRATE_chg'] < 0, alpha=0.2, color='#27ae60')
add_recessions(ax)
ax.set_title('Unemployment Rate — Quarterly Change (pp)', fontsize=13, fontweight='bold')
ax.set_ylabel('Change (pp)')

# Panel 3: Fed Funds Rate (level)
ax = axes[1, 0]
fedfunds = fred['FEDFUNDS']
ax.plot(fedfunds.loc['1990':].index, fedfunds.loc['1990':, 'FEDFUNDS'], color='#2980b9', lw=1.5)
add_recessions(ax)
ax.set_title('Federal Funds Rate (%)', fontsize=13, fontweight='bold')
ax.set_ylabel('Percent')

# Panel 4: 10-Year Treasury Rate (level)
ax = axes[1, 1]
dgs10 = fred['DGS10']
ax.plot(dgs10.loc['1990':].index, dgs10.loc['1990':, 'DGS10'], color='#8e44ad', lw=1)
add_recessions(ax)
ax.set_title('10-Year Treasury Yield (%)', fontsize=13, fontweight='bold')
ax.set_ylabel('Percent')

# Panel 5: CPI Growth (quarterly)
ax = axes[2, 0]
ax.plot(quarterly.index, quarterly['CPIAUCSL_g'], color='#f39c12', lw=1.2)
ax.axhline(0, color='black', lw=0.5, ls='--')
add_recessions(ax)
ax.set_title('CPI Inflation — Quarterly Growth (%)', fontsize=13, fontweight='bold')
ax.set_ylabel('Growth (%)')

# Panel 6: C&I Loan Growth + Unemployment overlay
ax = axes[2, 1]
ax.plot(quarterly.index, quarterly['BUSLOANS_g'], color='#1a6faf', lw=1.2, label='C&I Loan Growth (%)')
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.set_ylabel('C&I Loan Growth (%)', color='#1a6faf')
ax.tick_params(axis='y', labelcolor='#1a6faf')
add_recessions(ax)

ax2 = ax.twinx()
ax2.plot(quarterly.index, quarterly['UNRATE_chg'], color='#e74c3c', lw=1, alpha=0.7, label='Unemployment Change (pp)')
ax2.set_ylabel('Unemployment Change (pp)', color='#e74c3c')
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2.invert_yaxis()  # Invert so rising unemployment (bad) aligns with falling loans

ax.set_title('C&I Loan Growth vs Unemployment Change', fontsize=13, fontweight='bold')
# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='lower left')

plt.suptitle('Macro Variable Historical Trends (1990–2025)\nGray shading = NBER recessions',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
fname = f'{FIG_DIR}historical_macro_trends.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

# --- Figure C: Consumer Drivers ---
fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Panel 1: Consumer Loan Growth vs Fed Funds Level
ax = axes[0, 0]
ax.plot(quarterly.index, quarterly['CONSUMER_g'], color='#d95f02', lw=1.2, label='Consumer Loan Growth (%)')
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.set_ylabel('Consumer Loan Growth (%)', color='#d95f02')
ax.tick_params(axis='y', labelcolor='#d95f02')
add_recessions(ax)
ax2 = ax.twinx()
ax2.plot(quarterly.index, quarterly['FEDFUNDS_lvl'], color='#2980b9', lw=1, alpha=0.7, label='Fed Funds Rate (%)')
ax2.set_ylabel('Fed Funds Rate (%)', color='#2980b9')
ax2.tick_params(axis='y', labelcolor='#2980b9')
ax.set_title('Consumer Loan Growth vs Fed Funds Rate Level', fontsize=13, fontweight='bold')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='lower left')

# Panel 2: House Prices
ax = axes[0, 1]
hpi = fred['CSUSHPINSA']
ax.plot(hpi.loc['1990':].index, hpi.loc['1990':, 'CSUSHPINSA'], color='#27ae60', lw=1.5)
add_recessions(ax)
ax.set_title('Case-Shiller Home Price Index', fontsize=13, fontweight='bold')
ax.set_ylabel('Index')

# Panel 3: Real Disposable Income
ax = axes[1, 0]
dpi = fred['DSPIC96']
ax.plot(dpi.loc['1990':].index, dpi.loc['1990':, 'DSPIC96'], color='#16a085', lw=1.5)
add_recessions(ax)
ax.set_title('Real Disposable Personal Income ($B 2017)', fontsize=13, fontweight='bold')
ax.set_ylabel('Billions ($)')

# Panel 4: All growth rates together
ax = axes[1, 1]
ax.plot(quarterly.index, quarterly['BUSLOANS_g'], lw=1.2, alpha=0.8, label='C&I Loans')
ax.plot(quarterly.index, quarterly['CONSUMER_g'], lw=1.2, alpha=0.8, label='Consumer Loans')
ax.axhline(0, color='black', lw=0.5, ls='--')
add_recessions(ax)
ax.set_title('Loan Growth Rates — C&I vs Consumer', fontsize=13, fontweight='bold')
ax.set_ylabel('Quarterly Growth (%)')
ax.legend(fontsize=10)

plt.suptitle('Consumer Loan Drivers — Historical Trends (1990–2025)',
             fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
fname = f'{FIG_DIR}historical_consumer_drivers.png'
plt.savefig(fname, dpi=SAVE_DPI, bbox_inches='tight')
plt.close()
print(f'  Saved → {fname}')

print('\n' + '='*70)
print('DONE — All diagnostics and visualizations complete.')
print('='*70)
