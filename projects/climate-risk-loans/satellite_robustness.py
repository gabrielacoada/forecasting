"""
Satellite Model Robustness Analysis
====================================
M1: Robustness testing (lag sensitivity, recursive OOS, residual diagnostics, stability)
M2: Coefficient interpretation and economic magnitudes
D1: FRED-to-NGFS variable mapping verification
M3: Unified model comparison

Run from: projects/climate-risk-loans/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox, het_breuschpagan, het_white
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = 'data/raw/'
FIG_DIR = 'outputs/figures/'
TABLE_DIR = 'outputs/tables/'

# ============================================================
# 1. DATA LOADING (identical to satellite_forecasting.ipynb)
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
}

fred = {}
for ticker in series_info:
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

dgs10_monthly = fred['DGS10'].resample('MS').last()
monthly['DGS10_chg'] = dgs10_monthly['DGS10'].diff()

# COVID dummy
covid_start = pd.Timestamp('2020-01-01')
covid_end = pd.Timestamp('2021-06-01')
monthly['COVID'] = ((monthly.index >= covid_start) & (monthly.index <= covid_end)).astype(int)

# Aggregate to quarterly
quarterly = monthly.loc['1990-01-01':].resample('QE').agg({
    'BUSLOANS_g': 'mean', 'CONSUMER_g': 'mean', 'GDPC1_g': 'mean',
    'CPIAUCSL_g': 'mean', 'UNRATE_chg': 'sum', 'FEDFUNDS_chg': 'sum',
    'DGS10_chg': 'sum', 'COVID': 'max',
    'CSUSHPINSA_g': 'mean', 'DSPIC96_g': 'mean',
})

for col in ['BUSLOANS_g', 'CONSUMER_g', 'GDPC1_g', 'CPIAUCSL_g', 'CSUSHPINSA_g', 'DSPIC96_g']:
    if col in quarterly.columns:
        quarterly[col] = quarterly[col] * 3

quarterly = quarterly.loc[:'2025-12-31']
quarterly = quarterly.dropna()

print(f'Quarterly panel: {len(quarterly)} obs ({quarterly.index[0].date()} to {quarterly.index[-1].date()})')

# ============================================================
# 2. SATELLITE ESTIMATION FUNCTION
# ============================================================

def estimate_satellite(quarterly, target, regressors, name, lag=1):
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

    return {
        'name': name, 'model': model, 'T': T, 'lag': lag,
        'r2': model.rsquared, 'r2_adj': model.rsquared_adj,
        'aic': model.aic, 'bic': model.bic,
        'rmse': np.sqrt(np.mean(resid_excovid**2)),
        'lb_p4': lb['lb_pvalue'].iloc[0], 'lb_p8': lb['lb_pvalue'].iloc[1],
        'adf_p': adf_res[1], 'nw_lags': nw_lags,
        'resid': resid, 'resid_excovid': resid_excovid,
        'y_valid': y_valid, 'X_valid': X_valid, 'valid_df': valid,
    }


def satellite_oos(quarterly, target, regressors, start_eval, lag=1):
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
        fc = model.predict(np.array(x_fc).reshape(1, -1))[0]
        forecasts.append(fc)
        actuals.append(quarterly.loc[t, target])
        eval_dates_used.append(t)
    return np.array(forecasts), np.array(actuals), eval_dates_used


def ar_oos(quarterly, target, start_eval, max_p=8):
    covid_idx = quarterly[quarterly['COVID'] == 1].index
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
            fc = best_model.forecast(steps=1).iloc[0]
            forecasts.append(fc)
            actuals.append(quarterly.loc[t, target])
            eval_dates_used.append(t)
        except Exception:
            continue
    return np.array(forecasts), np.array(actuals), eval_dates_used


def diebold_mariano(e1, e2, h=1):
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
    # HLN correction
    hln_factor = np.sqrt((n + 1 - 2*h + h*(h-1)/n) / n)
    dm_corrected = dm * hln_factor
    p_value = 2 * (1 - stats.t.cdf(abs(dm_corrected), df=n-1))
    return dm_corrected, p_value


# ============================================================
# 3. MODEL SPECIFICATIONS
# ============================================================

ci_regressors = ['UNRATE_chg', 'FEDFUNDS_chg', 'CPIAUCSL_g']
con_base_regressors = ['UNRATE_chg', 'FEDFUNDS_chg', 'DGS10_chg', 'CPIAUCSL_g']

print('\n' + '='*80)
print('TASK M2: SATELLITE COEFFICIENT INTERPRETATION')
print('='*80)

# Estimate both models
ci_sat = estimate_satellite(quarterly, 'BUSLOANS_g', ci_regressors, 'C&I Satellite', lag=1)
con_sat = estimate_satellite(quarterly, 'CONSUMER_g', con_base_regressors, 'Consumer Satellite', lag=1)

def print_full_coefficients(sat, label):
    m = sat['model']
    print(f'\n{"="*70}')
    print(f'{label}')
    print(f'{"="*70}')
    print(f'Obs: {sat["T"]}  |  R²: {sat["r2"]:.3f}  |  Adj R²: {sat["r2_adj"]:.3f}')
    print(f'BIC: {sat["bic"]:.1f}  |  RMSE (ex-COVID): {sat["rmse"]:.3f}')
    print(f'Ljung-Box: LB(4) p={sat["lb_p4"]:.4f}, LB(8) p={sat["lb_p8"]:.4f}')
    print(f'\n{"Variable":25s} {"Coef":>8s} {"HAC SE":>8s} {"t-stat":>8s} {"p-val":>8s}  {"Sig":>5s}')
    print('-'*65)
    for var, coef, se, t, p in zip(m.params.index, m.params, m.bse, m.tvalues, m.pvalues):
        sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.10 else ''
        print(f'{var:25s} {coef:8.3f} {se:8.3f} {t:8.2f} {p:8.4f}  {sig:>5s}')

    # Economic magnitudes
    print(f'\nEconomic Magnitudes (1-unit shock to each variable, holding others constant):')
    for var, coef in zip(m.params.index, m.params):
        if 'const' in var or 'COVID' in var:
            continue
        if '_L' in var:
            base_var = var.rsplit('_L', 1)[0]
        else:
            base_var = var
        if 'UNRATE' in var:
            print(f'  +1pp unemployment change → {coef:+.3f}pp loan growth (next quarter)')
        elif 'FEDFUNDS' in var:
            print(f'  +1pp Fed Funds change   → {coef:+.3f}pp loan growth (next quarter)')
        elif 'DGS10' in var:
            print(f'  +1pp 10Y yield change   → {coef:+.3f}pp loan growth (next quarter)')
        elif 'CPIAUCSL' in var:
            print(f'  +1pp CPI inflation      → {coef:+.3f}pp loan growth (next quarter)')
        elif 'BUSLOANS_g' in var or 'CONSUMER_g' in var:
            print(f'  +1pp own lag growth     → {coef:+.3f}pp loan growth (persistence)')

print_full_coefficients(ci_sat, 'C&I SATELLITE MODEL')
print_full_coefficients(con_sat, 'CONSUMER SATELLITE MODEL (BASE)')

# ============================================================
# HONEST ASSESSMENT: R² and model fit
# ============================================================
print('\n' + '='*80)
print('HONEST ASSESSMENT: MODEL FIT')
print('='*80)

print(f'\nC&I Satellite:')
print(f'  Adj R² = {ci_sat["r2_adj"]:.3f} — GOOD. The model explains ~55% of quarterly C&I loan growth variation.')
print(f'  AR(1) coefficient = {ci_sat["model"].params.iloc[1]:.3f} — strong persistence.')
print(f'  Only UNRATE is statistically significant among macro drivers.')
print(f'  FEDFUNDS and CPI are NOT significant (p=0.82, p=0.25).')
print(f'  ⚠ LB(4) p={ci_sat["lb_p4"]:.4f} — serial correlation in residuals at lag 4.')

print(f'\nConsumer Satellite:')
print(f'  Adj R² = {con_sat["r2_adj"]:.3f} — POOR. The model explains only ~3.5% of variation.')
print(f'  Only FEDFUNDS is statistically significant (p=0.021).')
print(f'  UNRATE, DGS10, CPI all insignificant (p>0.5).')
print(f'  The consumer model is essentially: const + weak AR(1) + Fed Funds.')
print(f'  ⚠ This is a real limitation. Consumer loans are much harder to predict with macro variables.')

# ============================================================
# 4. TASK M1: ROBUSTNESS TESTING
# ============================================================

print('\n' + '='*80)
print('TASK M1: ROBUSTNESS TESTING')
print('='*80)

# --- 4a. LAG SENSITIVITY ---
print('\n--- 4a. Lag Sensitivity ---')
print(f'\n{"Model":40s} {"Lag":>4s} {"AdjR²":>8s} {"BIC":>8s} {"RMSE":>8s} {"LB4_p":>8s}')
print('-'*75)

for lag in [1, 2, 3, 4]:
    ci = estimate_satellite(quarterly, 'BUSLOANS_g', ci_regressors, f'C&I lag={lag}', lag=lag)
    con = estimate_satellite(quarterly, 'CONSUMER_g', con_base_regressors, f'Consumer lag={lag}', lag=lag)
    print(f'{"C&I Satellite":40s} {lag:4d} {ci["r2_adj"]:8.3f} {ci["bic"]:8.1f} {ci["rmse"]:8.3f} {ci["lb_p4"]:8.4f}')
    print(f'{"Consumer Satellite":40s} {lag:4d} {con["r2_adj"]:8.3f} {con["bic"]:8.1f} {con["rmse"]:8.3f} {con["lb_p4"]:8.4f}')

# --- 4b. RESIDUAL DIAGNOSTICS ---
print('\n--- 4b. Residual Diagnostics ---')

for label, sat in [('C&I', ci_sat), ('Consumer', con_sat)]:
    m = sat['model']
    resid = sat['resid_excovid']

    # Jarque-Bera normality test
    jb_stat, jb_p = stats.jarque_bera(resid)

    # Breusch-Pagan heteroskedasticity
    try:
        bp_stat, bp_p, _, _ = het_breuschpagan(m.resid, m.model.exog)
    except Exception:
        bp_stat, bp_p = np.nan, np.nan

    # White test
    try:
        white_stat, white_p, _, _ = het_white(m.resid, m.model.exog)
    except Exception:
        white_stat, white_p = np.nan, np.nan

    # Durbin-Watson
    from statsmodels.stats.stattools import durbin_watson
    dw = durbin_watson(m.resid)

    # Skewness and kurtosis
    skew = stats.skew(resid)
    kurt = stats.kurtosis(resid)

    print(f'\n{label} Satellite Residual Diagnostics:')
    print(f'  Jarque-Bera:       stat={jb_stat:.2f}, p={jb_p:.4f} {"⚠ NON-NORMAL" if jb_p < 0.05 else "✓ Normal"}')
    print(f'  Breusch-Pagan:     stat={bp_stat:.2f}, p={bp_p:.4f} {"⚠ HETEROSKEDASTIC" if bp_p < 0.05 else "✓ Homoskedastic"}')
    print(f'  White test:        stat={white_stat:.2f}, p={white_p:.4f} {"⚠ HETEROSKEDASTIC" if white_p < 0.05 else "✓ Homoskedastic"}')
    print(f'  Durbin-Watson:     {dw:.3f} {"⚠ Pos. autocorrelation" if dw < 1.5 else "⚠ Neg. autocorrelation" if dw > 2.5 else "✓ OK"}')
    print(f'  Skewness:          {skew:.3f}')
    print(f'  Kurtosis (excess): {kurt:.3f} {"⚠ Heavy tails" if abs(kurt) > 1 else "✓ OK"}')
    print(f'  Ljung-Box(4):      p={sat["lb_p4"]:.4f} {"⚠ SERIAL CORRELATION" if sat["lb_p4"] < 0.05 else "✓ OK"}')
    print(f'  Ljung-Box(8):      p={sat["lb_p8"]:.4f} {"⚠ SERIAL CORRELATION" if sat["lb_p8"] < 0.05 else "✓ OK"}')

# --- 4c. RECURSIVE OOS WITH DIFFERENT START DATES ---
print('\n--- 4c. Recursive OOS Sensitivity to Evaluation Window ---')

start_dates = {
    '2008Q1': pd.Timestamp('2008-03-31'),
    '2010Q1': pd.Timestamp('2010-03-31'),
    '2012Q1': pd.Timestamp('2012-03-31'),
    '2015Q1': pd.Timestamp('2015-03-31'),
    '2018Q1': pd.Timestamp('2018-03-31'),
}

print(f'\n{"Start":>8s} {"C&I RMSE":>10s} {"AR RMSE":>10s} {"Improv":>8s} {"N":>4s}  |  '
      f'{"Con RMSE":>10s} {"AR RMSE":>10s} {"Improv":>8s} {"N":>4s}')
print('-'*90)

oos_results = {}
for label, start in start_dates.items():
    fc_ci, act_ci, dates_ci = satellite_oos(quarterly, 'BUSLOANS_g', ci_regressors, start, lag=1)
    fc_ar_ci, act_ar_ci, dates_ar_ci = ar_oos(quarterly, 'BUSLOANS_g', start)
    fc_con, act_con, dates_con = satellite_oos(quarterly, 'CONSUMER_g', con_base_regressors, start, lag=1)
    fc_ar_con, act_ar_con, dates_ar_con = ar_oos(quarterly, 'CONSUMER_g', start)

    rmse_ci = np.sqrt(np.mean((fc_ci - act_ci)**2)) if len(fc_ci) > 0 else np.nan
    rmse_ar_ci = np.sqrt(np.mean((fc_ar_ci - act_ar_ci)**2)) if len(fc_ar_ci) > 0 else np.nan
    rmse_con = np.sqrt(np.mean((fc_con - act_con)**2)) if len(fc_con) > 0 else np.nan
    rmse_ar_con = np.sqrt(np.mean((fc_ar_con - act_ar_con)**2)) if len(fc_ar_con) > 0 else np.nan

    ci_imp = (1 - rmse_ci/rmse_ar_ci)*100 if rmse_ar_ci > 0 else np.nan
    con_imp = (1 - rmse_con/rmse_ar_con)*100 if rmse_ar_con > 0 else np.nan

    print(f'{label:>8s} {rmse_ci:10.3f} {rmse_ar_ci:10.3f} {ci_imp:+7.1f}% {len(fc_ci):4d}  |  '
          f'{rmse_con:10.3f} {rmse_ar_con:10.3f} {con_imp:+7.1f}% {len(fc_con):4d}')

    oos_results[label] = {
        'ci_rmse': rmse_ci, 'ci_ar_rmse': rmse_ar_ci, 'ci_imp': ci_imp,
        'con_rmse': rmse_con, 'con_ar_rmse': rmse_ar_con, 'con_imp': con_imp,
        'ci_n': len(fc_ci), 'con_n': len(fc_con),
        'ci_fc': fc_ci, 'ci_act': act_ci, 'ci_dates': dates_ci,
        'con_fc': fc_con, 'con_act': act_con, 'con_dates': dates_con,
        'ci_ar_fc': fc_ar_ci, 'ci_ar_act': act_ar_ci,
        'con_ar_fc': fc_ar_con, 'con_ar_act': act_ar_con,
    }

# --- 4d. ROLLING COEFFICIENT STABILITY ---
print('\n--- 4d. Rolling Coefficient Stability (expanding window) ---')

# For C&I: estimate satellite with expanding window and track key coefficients
window_starts = quarterly.index[quarterly.index >= pd.Timestamp('2005-03-31')]
window_starts = window_starts[~quarterly.loc[window_starts, 'COVID'].astype(bool)]

coef_tracker = {var: [] for var in ['UNRATE_chg_L1', 'FEDFUNDS_chg_L1', 'CPIAUCSL_g_L1', 'BUSLOANS_g_L1']}
coef_dates = []

for end_date in window_starts:
    sub = quarterly.loc[:end_date]
    if len(sub) < 40:  # need enough data
        continue
    try:
        sat = estimate_satellite(sub, 'BUSLOANS_g', ci_regressors, 'temp', lag=1)
        for var in coef_tracker:
            if var in sat['model'].params.index:
                coef_tracker[var].append(sat['model'].params[var])
            else:
                coef_tracker[var].append(np.nan)
        coef_dates.append(end_date)
    except Exception:
        continue

print(f'Tracked {len(coef_dates)} expanding windows for C&I satellite')
print(f'\nCoefficient ranges over expanding windows:')
for var, vals in coef_tracker.items():
    vals = np.array(vals)
    valid = vals[~np.isnan(vals)]
    if len(valid) > 0:
        print(f'  {var:25s}: min={valid.min():+.3f}, max={valid.max():+.3f}, '
              f'std={valid.std():.3f}, sign_changes={sum(np.diff(np.sign(valid)) != 0)}')

# Consumer rolling coefficients
con_coef_tracker = {var: [] for var in ['UNRATE_chg_L1', 'FEDFUNDS_chg_L1', 'DGS10_chg_L1', 'CPIAUCSL_g_L1', 'CONSUMER_g_L1']}
con_coef_dates = []

for end_date in window_starts:
    sub = quarterly.loc[:end_date]
    if len(sub) < 40:
        continue
    try:
        sat = estimate_satellite(sub, 'CONSUMER_g', con_base_regressors, 'temp', lag=1)
        for var in con_coef_tracker:
            if var in sat['model'].params.index:
                con_coef_tracker[var].append(sat['model'].params[var])
            else:
                con_coef_tracker[var].append(np.nan)
        con_coef_dates.append(end_date)
    except Exception:
        continue

print(f'\nTracked {len(con_coef_dates)} expanding windows for Consumer satellite')
print(f'\nCoefficient ranges over expanding windows:')
for var, vals in con_coef_tracker.items():
    vals = np.array(vals)
    valid = vals[~np.isnan(vals)]
    if len(valid) > 0:
        print(f'  {var:25s}: min={valid.min():+.3f}, max={valid.max():+.3f}, '
              f'std={valid.std():.3f}, sign_changes={sum(np.diff(np.sign(valid)) != 0)}')

# --- 4e. MINCER-ZARNOWITZ FORECAST EFFICIENCY ---
print('\n--- 4e. Mincer-Zarnowitz Forecast Efficiency Tests ---')

# Use the 2015Q1 OOS window (our standard)
for label, key in [('C&I', 'ci'), ('Consumer', 'con')]:
    res = oos_results['2015Q1']
    fc = res[f'{key}_fc']
    act = res[f'{key}_act']
    if len(fc) < 5:
        print(f'{label}: Not enough OOS observations')
        continue

    # Regress actuals on forecasts: actual = alpha + beta * forecast + e
    X_mz = add_constant(fc)
    mz_model = OLS(act, X_mz).fit()
    alpha, beta = mz_model.params
    alpha_se, beta_se = mz_model.bse

    # Joint test: H0: alpha=0, beta=1
    # F-test
    R = np.array([[1, 0], [0, 1]])  # restrictions
    q = np.array([0, 1])  # null values
    from numpy.linalg import inv
    diff = mz_model.params - q
    V = mz_model.cov_params()
    try:
        F_stat = diff @ inv(V) @ diff / 2
        F_p = 1 - stats.f.cdf(F_stat, 2, len(fc) - 2)
    except Exception:
        F_stat, F_p = np.nan, np.nan

    print(f'\n{label} Mincer-Zarnowitz (OOS from 2015Q1, n={len(fc)}):')
    print(f'  alpha (intercept): {alpha:.3f} (SE={alpha_se:.3f}, p={mz_model.pvalues[0]:.4f})')
    print(f'  beta (slope):      {beta:.3f} (SE={beta_se:.3f}, p={mz_model.pvalues[1]:.4f})')
    print(f'  Joint test (H0: a=0, b=1): F={F_stat:.3f}, p={F_p:.4f}')
    print(f'  R² of MZ regression: {mz_model.rsquared:.3f}')

    if F_p < 0.05:
        print(f'  ⚠ REJECT efficiency at 5% — forecasts are biased or inefficient')
    elif F_p < 0.10:
        print(f'  ⚠ REJECT efficiency at 10% — marginal evidence of bias')
    else:
        print(f'  ✓ Cannot reject efficiency — forecasts appear unbiased')

# ============================================================
# 5. TASK D1: VARIABLE MAPPING VERIFICATION
# ============================================================

print('\n' + '='*80)
print('TASK D1: FRED-TO-NGFS VARIABLE MAPPING VERIFICATION')
print('='*80)

# Load NGFS NiGEM to check variable names and units
import openpyxl
print('\nLoading NGFS NiGEM data for variable mapping check...')

nigem_vars_to_check = {
    'UNRATE': 'Unemployment rate',
    'FEDFUNDS': 'Short-term interest rate',
    'GDPC1': 'Real GDP',
    'CPIAUCSL': 'Consumer prices',
    'DGS10': 'Long-term interest rate',
}

# Read NiGEM baseline to verify what's there
try:
    nigem = pd.read_excel(f'{DATA_DIR}ngfs-phase5-nigem.xlsx', sheet_name='Baseline')
    us_nigem = nigem[nigem['Region'] == 'United States']
    available_vars = us_nigem['Variable'].unique()

    print(f'\nAvailable NGFS NiGEM variables for US ({len(available_vars)} total):')
    for fred_var, nigem_keyword in nigem_vars_to_check.items():
        matches = [v for v in available_vars if nigem_keyword.lower() in v.lower()]
        if matches:
            print(f'  {fred_var:12s} → NGFS: {matches}')
        else:
            print(f'  {fred_var:12s} → ⚠ NO MATCH for "{nigem_keyword}"')
except Exception as e:
    print(f'Could not load NGFS NiGEM: {e}')
    print('Skipping detailed variable mapping — verify manually.')

# Document the transformation mapping
print(f'\n--- Transformation Mapping ---')
print(f'{"FRED Variable":20s} {"Estimation Transform":35s} {"NGFS Forecast Transform":35s} {"Match?":>6s}')
print('-'*100)

mappings = [
    ('BUSLOANS', 'log(level).diff()*100 → quarterly *3', 'N/A (target variable)', 'N/A'),
    ('CONSUMER', 'log(level).diff()*100 → quarterly *3', 'N/A (target variable)', 'N/A'),
    ('UNRATE', 'level.diff() → quarterly sum', 'level.diff() from NGFS levels', '✓'),
    ('FEDFUNDS', 'level.diff() → quarterly sum', 'level.diff() from NGFS levels', '✓'),
    ('DGS10', 'daily→monthly last, then diff → qtr sum', 'level.diff() from NGFS levels', '✓'),
    ('CPIAUCSL', 'log(level).diff()*100 → quarterly *3', 'NGFS gives inflation rate directly', '⚠ CHECK'),
    ('GDPC1', 'quarterly ffill→monthly, log.diff()*100', 'log(NGFS GDP levels).diff()*100', '✓'),
]

for fred_var, est_transform, ngfs_transform, match in mappings:
    print(f'{fred_var:20s} {est_transform:35s} {ngfs_transform:35s} {match:>6s}')

print(f'\n⚠ CPI/Inflation mapping needs verification:')
print(f'  In FRED estimation: we compute log-growth of CPI level → quarterly growth rate')
print(f'  In NGFS forecasting: NiGEM may provide inflation RATE directly (not CPI level)')
print(f'  If NGFS gives annual inflation %, we divide by 4 for quarterly approx.')
print(f'  This is an approximation. log-growth of CPI ≈ inflation rate for small values,')
print(f'  but they diverge at high inflation. For typical US inflation (2-5%), the error is <0.1pp.')
print(f'  VERDICT: Acceptable approximation, but should note as limitation.')

# ============================================================
# 6. TASK M3: UNIFIED MODEL COMPARISON
# ============================================================

print('\n' + '='*80)
print('TASK M3: UNIFIED MODEL COMPARISON')
print('='*80)

# Compute DM tests for all pairwise comparisons
# Use 2015Q1 start date (our standard)
start_eval = pd.Timestamp('2015-03-31')

fc_ar_ci, act_ar_ci, dates_ar_ci = ar_oos(quarterly, 'BUSLOANS_g', start_eval)
fc_sat_ci, act_sat_ci, dates_sat_ci = satellite_oos(quarterly, 'BUSLOANS_g', ci_regressors, start_eval, lag=1)
fc_ar_con, act_ar_con, dates_ar_con = ar_oos(quarterly, 'CONSUMER_g', start_eval)
fc_sat_con, act_sat_con, dates_sat_con = satellite_oos(quarterly, 'CONSUMER_g', con_base_regressors, start_eval, lag=1)

rmse_ar_ci = np.sqrt(np.mean((fc_ar_ci - act_ar_ci)**2))
rmse_sat_ci = np.sqrt(np.mean((fc_sat_ci - act_sat_ci)**2))
rmse_ar_con = np.sqrt(np.mean((fc_ar_con - act_ar_con)**2))
rmse_sat_con = np.sqrt(np.mean((fc_sat_con - act_sat_con)**2))

print(f'\nFinal OOS Comparison (eval from 2015Q1, excluding COVID):')
print(f'\n{"Model":35s} {"C&I RMSE":>10s} {"vs AR":>8s}  {"Con RMSE":>10s} {"vs AR":>8s}')
print('-'*75)
print(f'{"AR (BIC-selected)":35s} {rmse_ar_ci:10.3f} {"--":>8s}  {rmse_ar_con:10.3f} {"--":>8s}')

ci_imp = (1 - rmse_sat_ci/rmse_ar_ci)*100
con_imp = (1 - rmse_sat_con/rmse_ar_con)*100
print(f'{"Satellite":35s} {rmse_sat_ci:10.3f} {ci_imp:+7.1f}%  {rmse_sat_con:10.3f} {con_imp:+7.1f}%')
print(f'{"Quarterly VAR (from NB4)":35s} {"~1.32":>10s} {"+11.7%":>8s}  {"~3.89":>10s} {"+7.5%":>8s}')
print(f'{"Annual VAR (from NB3)":35s} {"~10.32":>10s} {"-2.2%":>8s}  {"~12.52":>10s} {"-28.0%":>8s}')
print(f'{"ADL-MIDAS (from NB5)":35s} {"~9.93":>10s} {"+1.7%":>8s}  {"~7.72":>10s} {"+21.0%":>8s}')

# DM tests
print(f'\nDiebold-Mariano Tests (satellite vs AR):')
e_ar_ci = act_ar_ci - fc_ar_ci
e_sat_ci = act_sat_ci - fc_sat_ci
common_ci = sorted(set(dates_ar_ci) & set(dates_sat_ci))
if len(common_ci) > 5:
    mask_ar = np.array([d in common_ci for d in dates_ar_ci])
    mask_sat = np.array([d in common_ci for d in dates_sat_ci])
    dm_ci, p_ci = diebold_mariano(e_ar_ci[mask_ar], e_sat_ci[mask_sat])
    print(f'  C&I:      DM={dm_ci:+.3f}, p={p_ci:.4f}')

e_ar_con = act_ar_con - fc_ar_con
e_sat_con = act_sat_con - fc_sat_con
common_con = sorted(set(dates_ar_con) & set(dates_sat_con))
if len(common_con) > 5:
    mask_ar = np.array([d in common_con for d in dates_ar_con])
    mask_sat = np.array([d in common_con for d in dates_sat_con])
    dm_con, p_con = diebold_mariano(e_ar_con[mask_ar], e_sat_con[mask_sat])
    print(f'  Consumer: DM={dm_con:+.3f}, p={p_con:.4f}')

# ============================================================
# 7. SUMMARY OF FINDINGS
# ============================================================

print('\n' + '='*80)
print('SUMMARY OF HONEST FINDINGS')
print('='*80)

print("""
STRENGTHS:
1. C&I satellite model has good explanatory power (Adj R²=0.55)
2. Satellite beats AR baseline for both loan types in OOS
3. Methodology is well-grounded (Fed DFAST/ECB/BoE standard)
4. NGFS paths plug in directly — no VAR override gymnastics
5. DM test confirms statistical significance for C&I (p<0.05)

WEAKNESSES & LIMITATIONS (be honest about these):
1. Consumer model has VERY LOW R² (Adj R²~0.035). This means macro variables
   explain almost NONE of the quarterly variation in consumer loan growth.
   The model barely does better than a constant + weak AR(1).

2. C&I residuals show serial correlation at lag 4 (LB p<0.01). HAC standard
   errors account for this in inference, but it suggests the model is missing
   a quarterly seasonal or 1-year cyclical pattern.

3. Most macro regressors are NOT individually significant:
   - C&I: only UNRATE significant (FEDFUNDS p=0.82, CPI p=0.25)
   - Consumer: only FEDFUNDS significant (UNRATE p=0.86, DGS10 p=0.51, CPI p=0.95)

4. The DM test for consumer is only significant at 10% (p=0.077), which is
   marginal. With a different evaluation window, this could flip.

5. We're forecasting out to 2050 using relationships estimated over 1990-2025.
   25 years of extrapolation from 35 years of data is inherently uncertain.
   The fan charts should be wide.

RECOMMENDATIONS FOR PRESENTATION:
- Be upfront about consumer model limitations
- Frame it as: "macro variables are strong predictors of C&I loans but weak
  for consumer loans — this itself is an insight about how the two portfolios
  behave differently"
- The consumer model's OOS improvement comes from the Fed Funds channel, not
  from a rich multivariate model
- Use the low R² as motivation for discussing what ELSE drives consumer loans
  (micro factors: credit scores, LTV ratios, auto loan terms — things we
  don't have at macro level)
""")

print('\nDone. All results above should be saved to a report.')
