"""
Consumer Satellite Model Improvement
=====================================
Track 1: Specification improvements on balance-growth model
Track 2: Delinquency rate as alternative dependent variable
Track 3: Comparison and best model selection

Run from: projects/climate-risk-loans/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = 'data/raw/'
FIG_DIR = 'outputs/figures/'
TABLE_DIR = 'outputs/tables/'

# ============================================================
# 1. DATA LOADING
# ============================================================

series_info = {
    'BUSLOANS': ('C&I Loans', 'M'),
    'CONSUMER': ('Consumer Loans', 'M'),
    'GDPC1': ('Real GDP', 'Q'),
    'UNRATE': ('Unemployment Rate', 'M'),
    'FEDFUNDS': ('Fed Funds Rate', 'M'),
    'DGS10': ('10Y Treasury', 'D'),
    'CPIAUCSL': ('CPI', 'M'),
    'CSUSHPINSA': ('Case-Shiller HPI', 'M'),
    'DSPIC96': ('Real Disposable Income', 'M'),
    'UMCSENT': ('Michigan Consumer Sentiment', 'M'),
}

fred = {}
for ticker in series_info:
    df = pd.read_csv(f'{DATA_DIR}{ticker}.csv', parse_dates=['date'], index_col='date')
    fred[ticker] = df

# Load delinquency data
for ticker in ['DRCCLACBS', 'DRCLACBS']:
    df = pd.read_csv(f'{DATA_DIR}{ticker}.csv', parse_dates=['date'], index_col='date')
    fred[ticker] = df

# Build monthly panel
monthly = pd.DataFrame(index=pd.date_range('1947-01-01', '2025-12-31', freq='MS'))

for ticker in ['BUSLOANS', 'CONSUMER', 'CPIAUCSL', 'CSUSHPINSA', 'DSPIC96']:
    if ticker in fred:
        monthly[f'{ticker}_g'] = np.log(fred[ticker][ticker]).diff() * 100

gdp_m = fred['GDPC1'].resample('MS').ffill()
monthly['GDPC1_g'] = np.log(gdp_m['GDPC1']).diff() * 100

for ticker in ['UNRATE', 'FEDFUNDS']:
    monthly[f'{ticker}_chg'] = fred[ticker][ticker].diff()

# Rate LEVELS (Track 1b)
for ticker in ['UNRATE', 'FEDFUNDS']:
    monthly[f'{ticker}_lvl'] = fred[ticker][ticker]

dgs10_monthly = fred['DGS10'].resample('MS').last()
monthly['DGS10_chg'] = dgs10_monthly['DGS10'].diff()
monthly['DGS10_lvl'] = dgs10_monthly['DGS10']

# Consumer sentiment (Track 1a)
monthly['UMCSENT_lvl'] = fred['UMCSENT']['UMCSENT']
monthly['UMCSENT_chg'] = fred['UMCSENT']['UMCSENT'].diff()

# COVID dummy
covid_start = pd.Timestamp('2020-01-01')
covid_end = pd.Timestamp('2021-06-01')
monthly['COVID'] = ((monthly.index >= covid_start) & (monthly.index <= covid_end)).astype(int)

# Post-GFC deleveraging dummy (Track 1d)
gfc_start = pd.Timestamp('2009-01-01')
gfc_end = pd.Timestamp('2011-12-01')
monthly['DELEVER'] = ((monthly.index >= gfc_start) & (monthly.index <= gfc_end)).astype(int)

# Aggregate to quarterly
agg_dict = {
    'BUSLOANS_g': 'mean', 'CONSUMER_g': 'mean', 'GDPC1_g': 'mean',
    'CPIAUCSL_g': 'mean', 'UNRATE_chg': 'sum', 'FEDFUNDS_chg': 'sum',
    'DGS10_chg': 'sum', 'COVID': 'max',
    'CSUSHPINSA_g': 'mean', 'DSPIC96_g': 'mean',
    'FEDFUNDS_lvl': 'mean', 'DGS10_lvl': 'mean', 'UNRATE_lvl': 'mean',
    'UMCSENT_lvl': 'mean', 'UMCSENT_chg': 'sum',
    'DELEVER': 'max',
}

quarterly = monthly.loc['1990-01-01':].resample('QE').agg(agg_dict)

for col in ['BUSLOANS_g', 'CONSUMER_g', 'GDPC1_g', 'CPIAUCSL_g', 'CSUSHPINSA_g', 'DSPIC96_g']:
    if col in quarterly.columns:
        quarterly[col] = quarterly[col] * 3

quarterly = quarterly.loc[:'2025-12-31']
quarterly = quarterly.dropna(subset=['BUSLOANS_g', 'CONSUMER_g', 'UNRATE_chg',
                                      'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g'])

# Add delinquency data (already quarterly, no aggregation needed)
for ticker in ['DRCCLACBS', 'DRCLACBS']:
    dq = fred[ticker].resample('QE').last()
    quarterly[ticker] = dq[ticker]
    quarterly[f'{ticker}_chg'] = dq[ticker].diff()

print(f'Quarterly panel: {len(quarterly)} obs ({quarterly.index[0].date()} to {quarterly.index[-1].date()})')
print(f'UMCSENT coverage: {quarterly["UMCSENT_lvl"].notna().sum()} obs')
print(f'DRCCLACBS (credit card delinquency) coverage: {quarterly["DRCCLACBS"].notna().sum()} obs')
print(f'DRCLACBS (consumer loan delinquency) coverage: {quarterly["DRCLACBS"].notna().sum()} obs')

# ============================================================
# 2. ESTIMATION & OOS FUNCTIONS
# ============================================================

def estimate_satellite(quarterly, target, regressors, name, lag=1, extra_dummies=None):
    """Estimate ADL satellite with optional extra dummy variables."""
    df = quarterly.copy()
    y = df[target]
    X_cols = []
    df[f'{target}_L{lag}'] = df[target].shift(lag)
    X_cols.append(f'{target}_L{lag}')
    for reg in regressors:
        col_name = f'{reg}_L{lag}'
        df[col_name] = df[reg].shift(lag)
        X_cols.append(col_name)
    X_cols.append('COVID')
    if extra_dummies:
        for d in extra_dummies:
            X_cols.append(d)
    valid = df[[target] + X_cols].dropna()
    y_valid = valid[target]
    X_valid = add_constant(valid[X_cols])
    T = len(y_valid)
    nw_lags = int(0.75 * T ** (1/3))
    model = OLS(y_valid, X_valid).fit(cov_type='HAC', cov_kwds={'maxlags': nw_lags})
    resid = model.resid
    resid_excovid = resid[valid['COVID'] == 0]
    lb = acorr_ljungbox(resid_excovid, lags=[4, 8], return_df=True)
    adf_res = adfuller(resid_excovid)
    skew = stats.skew(resid_excovid)
    kurt = stats.kurtosis(resid_excovid)
    jb_stat, jb_p = stats.jarque_bera(resid_excovid)

    return {
        'name': name, 'model': model, 'T': T, 'lag': lag,
        'r2': model.rsquared, 'r2_adj': model.rsquared_adj,
        'aic': model.aic, 'bic': model.bic,
        'rmse': np.sqrt(np.mean(resid_excovid**2)),
        'lb_p4': lb['lb_pvalue'].iloc[0], 'lb_p8': lb['lb_pvalue'].iloc[1],
        'adf_p': adf_res[1], 'nw_lags': nw_lags,
        'resid': resid, 'resid_excovid': resid_excovid,
        'y_valid': y_valid, 'X_valid': X_valid, 'valid_df': valid,
        'skew': skew, 'kurt': kurt, 'jb_p': jb_p,
        'regressors': regressors, 'target': target,
        'extra_dummies': extra_dummies,
    }


def estimate_distributed_lag(quarterly, target, regressors, name, max_lag=2, extra_dummies=None):
    """ADL with distributed lags on regressors (lags 1..max_lag)."""
    df = quarterly.copy()
    X_cols = []
    # AR(1) term only
    df[f'{target}_L1'] = df[target].shift(1)
    X_cols.append(f'{target}_L1')
    # Distributed lags on regressors
    for reg in regressors:
        for lag in range(1, max_lag + 1):
            col_name = f'{reg}_L{lag}'
            df[col_name] = df[reg].shift(lag)
            X_cols.append(col_name)
    X_cols.append('COVID')
    if extra_dummies:
        for d in extra_dummies:
            X_cols.append(d)
    valid = df[[target] + X_cols].dropna()
    y_valid = valid[target]
    X_valid = add_constant(valid[X_cols])
    T = len(y_valid)
    nw_lags = int(0.75 * T ** (1/3))
    model = OLS(y_valid, X_valid).fit(cov_type='HAC', cov_kwds={'maxlags': nw_lags})
    resid = model.resid
    resid_excovid = resid[valid['COVID'] == 0]
    lb = acorr_ljungbox(resid_excovid, lags=[4, 8], return_df=True)
    skew = stats.skew(resid_excovid)
    kurt = stats.kurtosis(resid_excovid)
    jb_stat, jb_p = stats.jarque_bera(resid_excovid)

    return {
        'name': name, 'model': model, 'T': T,
        'r2': model.rsquared, 'r2_adj': model.rsquared_adj,
        'aic': model.aic, 'bic': model.bic,
        'rmse': np.sqrt(np.mean(resid_excovid**2)),
        'lb_p4': lb['lb_pvalue'].iloc[0], 'lb_p8': lb['lb_pvalue'].iloc[1],
        'skew': skew, 'kurt': kurt, 'jb_p': jb_p,
        'regressors': regressors, 'target': target,
    }


def satellite_oos(quarterly, target, regressors, start_eval, lag=1, extra_dummies=None):
    """Expanding-window OOS for satellite model."""
    covid_idx = quarterly[quarterly['COVID'] == 1].index
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
        if extra_dummies:
            for d in extra_dummies:
                X_cols.append(d)
        valid_train = df_train[[target] + X_cols].dropna()
        if len(valid_train) < 20:
            continue
        y_train = valid_train[target]
        X_train = add_constant(valid_train[X_cols])
        try:
            model = OLS(y_train, X_train).fit()
        except Exception:
            continue
        prev_t = quarterly.index[quarterly.index < t][-1]
        x_fc = [1.0]
        x_fc.append(quarterly.loc[prev_t, target])
        for reg in regressors:
            x_fc.append(quarterly.loc[prev_t, reg])
        x_fc.append(quarterly.loc[t, 'COVID'])
        if extra_dummies:
            for d in extra_dummies:
                x_fc.append(quarterly.loc[t, d])
        fc = model.predict(np.array(x_fc).reshape(1, -1))[0]
        forecasts.append(fc)
        actuals.append(quarterly.loc[t, target])
        eval_dates_used.append(t)
    return np.array(forecasts), np.array(actuals), eval_dates_used


def ar_oos(quarterly, target, start_eval, max_p=8):
    """AR baseline OOS."""
    covid_idx = quarterly[quarterly['COVID'] == 1].index
    eval_dates = quarterly.index[quarterly.index >= start_eval]
    forecasts, actuals, eval_dates_used = [], [], []
    for t in eval_dates:
        if t in covid_idx:
            continue
        train = quarterly.loc[:t, target].dropna().iloc[:-1]
        if len(train) < max_p + 10:
            continue
        try:
            best_bic, best_model = np.inf, None
            for p in range(1, max_p + 1):
                m = AutoReg(train, lags=p, old_names=False).fit()
                if m.bic < best_bic:
                    best_bic, best_model = m.bic, m
            fc = best_model.forecast(steps=1).iloc[0]
            forecasts.append(fc)
            actuals.append(quarterly.loc[t, target])
            eval_dates_used.append(t)
        except Exception:
            continue
    return np.array(forecasts), np.array(actuals), eval_dates_used


def diebold_mariano(e1, e2, h=1):
    """DM test with HLN correction."""
    d = e1**2 - e2**2
    n = len(d)
    d_bar = np.mean(d)
    gamma_0 = np.var(d, ddof=1)
    gamma_sum = 0
    for k in range(1, h):
        if k < n:
            gamma_sum += np.cov(d[k:], d[:-k])[0, 1]
    V = (gamma_0 + 2 * gamma_sum) / n
    if V <= 0:
        return 0, 1.0
    dm = d_bar / np.sqrt(V)
    hln_factor = np.sqrt((n + 1 - 2*h + h*(h-1)/n) / n)
    dm_corrected = dm * hln_factor
    p_value = 2 * (1 - stats.t.cdf(abs(dm_corrected), df=n-1))
    return dm_corrected, p_value


def run_oos_comparison(quarterly, target, regressors, label, lag=1, extra_dummies=None):
    """Run OOS for multiple start dates and compare to AR."""
    start_dates = {
        '2008Q1': pd.Timestamp('2008-03-31'),
        '2012Q1': pd.Timestamp('2012-03-31'),
        '2015Q1': pd.Timestamp('2015-03-31'),
    }
    results = {}
    for sd_label, start in start_dates.items():
        fc_sat, act_sat, dates_sat = satellite_oos(quarterly, target, regressors, start, lag=lag,
                                                    extra_dummies=extra_dummies)
        fc_ar, act_ar, dates_ar = ar_oos(quarterly, target, start)
        if len(fc_sat) == 0 or len(fc_ar) == 0:
            results[sd_label] = {'rmse_sat': np.nan, 'rmse_ar': np.nan, 'imp': np.nan, 'dm_p': np.nan, 'n': 0}
            continue
        rmse_sat = np.sqrt(np.mean((fc_sat - act_sat)**2))
        rmse_ar = np.sqrt(np.mean((fc_ar - act_ar)**2))
        imp = (1 - rmse_sat/rmse_ar) * 100

        # DM test on common dates
        common = sorted(set(dates_sat) & set(dates_ar))
        dm_p = np.nan
        if len(common) > 5:
            mask_ar = np.array([d in common for d in dates_ar])
            mask_sat = np.array([d in common for d in dates_sat])
            e_ar = act_ar[mask_ar] - fc_ar[mask_ar]
            e_sat = act_sat[mask_sat] - fc_sat[mask_sat]
            _, dm_p = diebold_mariano(e_ar, e_sat)

        results[sd_label] = {'rmse_sat': rmse_sat, 'rmse_ar': rmse_ar, 'imp': imp,
                             'dm_p': dm_p, 'n': len(fc_sat)}
    return results


# ============================================================
# TRACK 1: CONSUMER BALANCE-GROWTH SPECIFICATION IMPROVEMENTS
# ============================================================

print('\n' + '='*80)
print('TRACK 1: CONSUMER BALANCE-GROWTH MODEL IMPROVEMENTS')
print('='*80)

# --- Baseline ---
con_base_regressors = ['UNRATE_chg', 'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g']
baseline = estimate_satellite(quarterly, 'CONSUMER_g', con_base_regressors, 'Baseline (original)')

specs = [('Baseline (original)', baseline)]

# --- 1a: Add Consumer Sentiment ---
print('\n--- 1a: Consumer Sentiment (UMCSENT) ---')
# Need to restrict to quarters where UMCSENT is available
q_sent = quarterly.dropna(subset=['UMCSENT_lvl'])
if len(q_sent) > 40:
    con_sent_regressors = ['UNRATE_chg', 'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g', 'UMCSENT_chg']
    spec_1a = estimate_satellite(q_sent, 'CONSUMER_g', con_sent_regressors, '+ Sentiment (UMCSENT_chg)')
    specs.append(('+ UMCSENT change', spec_1a))
    print(f'  UMCSENT_chg coef: {spec_1a["model"].params.get("UMCSENT_chg_L1", np.nan):.4f}, '
          f'p={spec_1a["model"].pvalues.get("UMCSENT_chg_L1", np.nan):.4f}')

    # Also try sentiment level
    con_sent_lvl_regressors = ['UNRATE_chg', 'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g', 'UMCSENT_lvl']
    spec_1a_lvl = estimate_satellite(q_sent, 'CONSUMER_g', con_sent_lvl_regressors, '+ Sentiment Level')
    specs.append(('+ UMCSENT level', spec_1a_lvl))
    print(f'  UMCSENT_lvl coef: {spec_1a_lvl["model"].params.get("UMCSENT_lvl_L1", np.nan):.4f}, '
          f'p={spec_1a_lvl["model"].pvalues.get("UMCSENT_lvl_L1", np.nan):.4f}')
else:
    print(f'  Not enough UMCSENT data (only {len(q_sent)} obs)')

# --- 1b: Rate LEVELS instead of changes ---
print('\n--- 1b: Rate Levels ---')
con_levels_regressors = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_lvl', 'CPIAUCSL_g']
spec_1b = estimate_satellite(quarterly, 'CONSUMER_g', con_levels_regressors, 'Rate Levels')
specs.append(('Rate levels', spec_1b))
print(f'  FEDFUNDS_lvl coef: {spec_1b["model"].params.get("FEDFUNDS_lvl_L1", np.nan):.4f}, '
      f'p={spec_1b["model"].pvalues.get("FEDFUNDS_lvl_L1", np.nan):.4f}')
print(f'  DGS10_lvl coef: {spec_1b["model"].params.get("DGS10_lvl_L1", np.nan):.4f}, '
      f'p={spec_1b["model"].pvalues.get("DGS10_lvl_L1", np.nan):.4f}')

# Try mixed: level for one, change for other
con_mixed_regressors = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_chg', 'CPIAUCSL_g']
spec_1b_mixed = estimate_satellite(quarterly, 'CONSUMER_g', con_mixed_regressors, 'FEDFUNDS level + DGS10 change')
specs.append(('FF level + DGS10 change', spec_1b_mixed))

# --- 1c: Distributed Lags ---
print('\n--- 1c: Distributed Lags ---')
for max_lag in [2, 3, 4]:
    dl_spec = estimate_distributed_lag(quarterly, 'CONSUMER_g', con_base_regressors,
                                        f'ADL(1,{max_lag})', max_lag=max_lag)
    specs.append((f'ADL(1,{max_lag})', dl_spec))
    print(f'  ADL(1,{max_lag}): Adj R²={dl_spec["r2_adj"]:.3f}, BIC={dl_spec["bic"]:.1f}')

# --- 1d: Post-GFC Deleveraging Dummy ---
print('\n--- 1d: Post-GFC Deleveraging Dummy ---')
spec_1d = estimate_satellite(quarterly, 'CONSUMER_g', con_base_regressors,
                              'Baseline + DELEVER dummy', extra_dummies=['DELEVER'])
specs.append(('+ DELEVER dummy', spec_1d))
delever_coef = spec_1d['model'].params.get('DELEVER', np.nan)
delever_p = spec_1d['model'].pvalues.get('DELEVER', np.nan)
print(f'  DELEVER coef: {delever_coef:.3f}, p={delever_p:.4f}')
print(f'  Kurtosis change: {baseline["kurt"]:.1f} → {spec_1d["kurt"]:.1f}')

# Also try baseline + both dummies
spec_1d_both = estimate_satellite(quarterly, 'CONSUMER_g', con_base_regressors,
                                   'Baseline + DELEVER + COVID', extra_dummies=['DELEVER'])
specs.append(('+ DELEVER (both dummies)', spec_1d_both))

# --- 1e: Combined best elements ---
print('\n--- 1e: Combined Specification (best elements from 1a-1d) ---')
# Combine: rate levels + DELEVER dummy
con_combined = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_chg', 'CPIAUCSL_g']
spec_combined = estimate_satellite(quarterly, 'CONSUMER_g', con_combined,
                                    'Combined: FF level + DELEVER', extra_dummies=['DELEVER'])
specs.append(('FF level + DELEVER', spec_combined))

# ============================================================
# TRACK 1 RESULTS SUMMARY
# ============================================================

print('\n' + '='*80)
print('TRACK 1 RESULTS SUMMARY')
print('='*80)
print(f'\n{"Specification":35s} {"AdjR²":>8s} {"BIC":>8s} {"RMSE":>8s} {"Kurt":>6s} {"JB_p":>6s} {"T":>4s}')
print('-'*80)
for name, s in specs:
    print(f'{name:35s} {s["r2_adj"]:8.3f} {s["bic"]:8.1f} {s["rmse"]:8.3f} '
          f'{s["kurt"]:6.1f} {s["jb_p"]:6.4f} {s["T"]:4d}')

# Find best by BIC (comparable sample sizes only)
bic_specs = [(name, s) for name, s in specs if abs(s['T'] - baseline['T']) <= 5]
best_name, best_spec = min(bic_specs, key=lambda x: x[1]['bic'])
print(f'\nBest by BIC (comparable samples): {best_name} (BIC={best_spec["bic"]:.1f})')

# ============================================================
# TRACK 1: OOS EVALUATION OF BEST SPECS
# ============================================================

print('\n' + '='*80)
print('TRACK 1: OOS EVALUATION')
print('='*80)

# OOS for baseline
print('\n--- Baseline ---')
oos_baseline = run_oos_comparison(quarterly, 'CONSUMER_g', con_base_regressors, 'Baseline')
for sd, r in oos_baseline.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

# OOS for rate levels
print('\n--- Rate Levels ---')
oos_levels = run_oos_comparison(quarterly, 'CONSUMER_g', con_levels_regressors, 'Rate Levels')
for sd, r in oos_levels.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

# OOS for baseline + DELEVER
print('\n--- Baseline + DELEVER ---')
oos_delever = run_oos_comparison(quarterly, 'CONSUMER_g', con_base_regressors, 'Baseline+DELEVER',
                                  extra_dummies=['DELEVER'])
for sd, r in oos_delever.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

# OOS for combined spec
print('\n--- Combined: FF Level + DELEVER ---')
oos_combined = run_oos_comparison(quarterly, 'CONSUMER_g', con_combined, 'Combined',
                                   extra_dummies=['DELEVER'])
for sd, r in oos_combined.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

# ============================================================
# TRACK 2: DELINQUENCY RATE AS ALTERNATIVE DV
# ============================================================

print('\n' + '='*80)
print('TRACK 2: DELINQUENCY RATE MODELS')
print('='*80)

# Restrict to quarters with delinquency data
q_dq = quarterly.dropna(subset=['DRCLACBS']).copy()
print(f'Consumer delinquency (DRCLACBS): {len(q_dq)} obs, {q_dq.index[0].date()} to {q_dq.index[-1].date()}')
print(f'  Range: {q_dq["DRCLACBS"].min():.2f}% to {q_dq["DRCLACBS"].max():.2f}%')

q_cc = quarterly.dropna(subset=['DRCCLACBS']).copy()
print(f'Credit card delinquency (DRCCLACBS): {len(q_cc)} obs, {q_cc.index[0].date()} to {q_cc.index[-1].date()}')
print(f'  Range: {q_cc["DRCCLACBS"].min():.2f}% to {q_cc["DRCCLACBS"].max():.2f}%')

# --- 2a: Model delinquency LEVEL ---
print('\n--- 2a: Delinquency Level Models ---')

dq_regressors_base = ['UNRATE_chg', 'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g']
dq_regressors_lvl = ['UNRATE_chg', 'FEDFUNDS_lvl', 'DGS10_chg', 'CPIAUCSL_g']

dq_specs = []

# Consumer loan delinquency - base
dq_con = estimate_satellite(q_dq, 'DRCLACBS', dq_regressors_base,
                             'Consumer DQ (changes)', lag=1)
dq_specs.append(('Consumer DQ (changes)', dq_con))

# Consumer loan delinquency - rate levels
dq_con_lvl = estimate_satellite(q_dq, 'DRCLACBS', dq_regressors_lvl,
                                 'Consumer DQ (FF level)', lag=1)
dq_specs.append(('Consumer DQ (FF level)', dq_con_lvl))

# Consumer loan delinquency - with DELEVER
dq_con_del = estimate_satellite(q_dq, 'DRCLACBS', dq_regressors_base,
                                 'Consumer DQ + DELEVER', lag=1, extra_dummies=['DELEVER'])
dq_specs.append(('Consumer DQ + DELEVER', dq_con_del))

# Credit card delinquency - base
dq_cc = estimate_satellite(q_cc, 'DRCCLACBS', dq_regressors_base,
                            'Credit Card DQ (changes)', lag=1)
dq_specs.append(('Credit Card DQ (changes)', dq_cc))

# Credit card delinquency - rate levels
dq_cc_lvl = estimate_satellite(q_cc, 'DRCCLACBS', dq_regressors_lvl,
                                'Credit Card DQ (FF level)', lag=1)
dq_specs.append(('Credit Card DQ (FF level)', dq_cc_lvl))

print(f'\n{"Specification":35s} {"AdjR²":>8s} {"BIC":>8s} {"RMSE":>8s} {"Kurt":>6s} {"JB_p":>6s} {"T":>4s}')
print('-'*80)
for name, s in dq_specs:
    print(f'{name:35s} {s["r2_adj"]:8.3f} {s["bic"]:8.1f} {s["rmse"]:8.3f} '
          f'{s["kurt"]:6.1f} {s["jb_p"]:6.4f} {s["T"]:4d}')

# Print coefficient tables for best delinquency models
for name, s in dq_specs:
    m = s['model']
    print(f'\n--- {name} ---')
    print(f'{"Variable":25s} {"Coef":>8s} {"HAC SE":>8s} {"t-stat":>8s} {"p-val":>8s}  {"Sig":>5s}')
    print('-'*65)
    for var, coef, se, t, p in zip(m.params.index, m.params, m.bse, m.tvalues, m.pvalues):
        sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.10 else ''
        print(f'{var:25s} {coef:8.4f} {se:8.4f} {t:8.2f} {p:8.4f}  {sig:>5s}')

# --- 2b: OOS Evaluation ---
print('\n--- 2b: OOS Evaluation ---')

# Consumer loan delinquency OOS
print('\nConsumer Loan Delinquency (DRCLACBS):')
oos_dq_con = run_oos_comparison(q_dq, 'DRCLACBS', dq_regressors_base, 'Con DQ changes')
for sd, r in oos_dq_con.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

print('\nConsumer Loan Delinquency (FF level):')
oos_dq_con_lvl = run_oos_comparison(q_dq, 'DRCLACBS', dq_regressors_lvl, 'Con DQ FF level')
for sd, r in oos_dq_con_lvl.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

print('\nCredit Card Delinquency (DRCCLACBS):')
oos_dq_cc = run_oos_comparison(q_cc, 'DRCCLACBS', dq_regressors_base, 'CC DQ changes')
for sd, r in oos_dq_cc.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

print('\nCredit Card Delinquency (FF level):')
oos_dq_cc_lvl = run_oos_comparison(q_cc, 'DRCCLACBS', dq_regressors_lvl, 'CC DQ FF level')
for sd, r in oos_dq_cc_lvl.items():
    print(f'  {sd}: RMSE_sat={r["rmse_sat"]:.3f}, RMSE_ar={r["rmse_ar"]:.3f}, '
          f'Improv={r["imp"]:+.1f}%, DM_p={r["dm_p"]:.3f}, n={r["n"]}')

# ============================================================
# TRACK 3: COMPREHENSIVE COMPARISON
# ============================================================

print('\n' + '='*80)
print('TRACK 3: COMPREHENSIVE COMPARISON — ALL CONSUMER MODELS')
print('='*80)

# Compile all in-sample results
print(f'\n{"Model":40s} {"Target":12s} {"AdjR²":>8s} {"BIC":>8s} {"RMSE":>8s}')
print('-'*72)

all_models = []

# Track 1 models
for name, s in specs:
    print(f'{name:40s} {"CONSUMER_g":12s} {s["r2_adj"]:8.3f} {s["bic"]:8.1f} {s["rmse"]:8.3f}')
    all_models.append((name, 'CONSUMER_g', s))

print()

# Track 2 models
for name, s in dq_specs:
    target = 'DRCLACBS' if 'Consumer DQ' in name else 'DRCCLACBS'
    print(f'{name:40s} {target:12s} {s["r2_adj"]:8.3f} {s["bic"]:8.1f} {s["rmse"]:8.3f}')
    all_models.append((name, target, s))

# ============================================================
# FINAL VERDICTS
# ============================================================

print('\n' + '='*80)
print('FINAL VERDICTS')
print('='*80)

# Track 1 verdict
best_t1_bic = min([(n, s) for n, s in specs if abs(s['T'] - baseline['T']) <= 5],
                   key=lambda x: x[1]['bic'])
print(f'\nTrack 1 Best Spec (by BIC): {best_t1_bic[0]}')
print(f'  BIC: {baseline["bic"]:.1f} (baseline) → {best_t1_bic[1]["bic"]:.1f} (best)')
print(f'  Adj R²: {baseline["r2_adj"]:.3f} (baseline) → {best_t1_bic[1]["r2_adj"]:.3f} (best)')
bic_improved = best_t1_bic[1]['bic'] < baseline['bic']
r2_improved = best_t1_bic[1]['r2_adj'] > baseline['r2_adj']
print(f'  BIC improved: {bic_improved}, R² improved: {r2_improved}')

# Track 2 verdict
print(f'\nTrack 2 Results:')
for name, s in dq_specs:
    print(f'  {name:35s}: Adj R²={s["r2_adj"]:.3f} vs consumer balance baseline={baseline["r2_adj"]:.3f}')

# Overall
print(f'\n--- OVERALL ASSESSMENT ---')
print(f'Consumer balance-growth model Adj R²: {baseline["r2_adj"]:.3f}')
best_dq_spec = max(dq_specs, key=lambda x: x[1]['r2_adj'])
print(f'Best delinquency model Adj R²: {best_dq_spec[1]["r2_adj"]:.3f} ({best_dq_spec[0]})')

if best_dq_spec[1]['r2_adj'] > 0.15:
    print(f'\n*** DELINQUENCY MODEL IS SUBSTANTIALLY STRONGER ***')
    print(f'Recommend: Present dual consumer model:')
    print(f'  (1) Balance growth (weak but honest)')
    print(f'  (2) Delinquency rate ({best_dq_spec[0]}) — stronger, more actionable')
elif best_t1_bic[1]['r2_adj'] > baseline['r2_adj'] + 0.05:
    print(f'\n*** TRACK 1 IMPROVEMENT IS MEANINGFUL ***')
    print(f'Recommend: Use improved balance-growth specification ({best_t1_bic[0]})')
else:
    print(f'\n*** NO MAJOR IMPROVEMENT FOUND ***')
    print(f'Recommend: Keep original consumer model, frame weakness as finding')

print('\nDone. All results above.')
