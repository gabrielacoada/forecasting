#!/usr/bin/env Rscript
# ===========================================================================
# MIDAS & ADL-MIDAS Analysis in R — Climate Risk Loan Portfolio Project
# ===========================================================================
# Uses the midasr package for proper NLS estimation of mixed-frequency models.
# Following Professor Pesavento's lab (ECON522_Lab_MIDAS) approach exactly.
#
# Low-frequency target:  QUARTERLY loan growth (~140 obs, 1990-2025)
# High-frequency predictors: MONTHLY FRED macro data (m=3 months/quarter)
#
# Models:
#   1. MIDAS (Exponential Almon)
#   2. MIDAS (Beta weights)
#   3. ADL-MIDAS (Almon + lagged dependent variable)
#   4. AR benchmark (BIC-selected)
#
# Outputs: weight plots, OOS evaluation, NGFS scenario forecasts, summary table
# ===========================================================================

suppressPackageStartupMessages({
  library(midasr)
  library(readxl)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(zoo)
  library(lubridate)
  library(forecast)
})

cat(strrep("=", 75), "\n")
cat(" MIDAS & ADL-MIDAS Analysis in R\n")
cat(" Quarterly LHS / Monthly RHS  (m = 3)\n")
cat(strrep("=", 75), "\n\n")

# ---- Paths ----------------------------------------------------------------
BASE_DIR   <- "."
DATA_DIR   <- file.path(BASE_DIR, "data", "raw")
FIG_DIR    <- file.path(BASE_DIR, "outputs", "figures")
TAB_DIR    <- file.path(BASE_DIR, "outputs", "tables")
dir.create(FIG_DIR, recursive = TRUE, showWarnings = FALSE)
dir.create(TAB_DIR, recursive = TRUE, showWarnings = FALSE)

# ===========================================================================
# STEP 1: DATA LOADING & TRANSFORMATION
# ===========================================================================
cat("\n--- Step 1: Data Loading & Transformation ---\n\n")

read_fred <- function(file) {
  df <- read.csv(file, stringsAsFactors = FALSE)
  colnames(df) <- c("date", "value")
  df$date  <- as.Date(df$date)
  df$value <- suppressWarnings(as.numeric(df$value))
  df <- df[!is.na(df$value), ]
  df
}

# Load FRED series
busloans <- read_fred(file.path(DATA_DIR, "BUSLOANS.csv"))
consumer <- read_fred(file.path(DATA_DIR, "CONSUMER.csv"))
unrate   <- read_fred(file.path(DATA_DIR, "UNRATE.csv"))
cpi      <- read_fred(file.path(DATA_DIR, "CPIAUCSL.csv"))
fedfunds <- read_fred(file.path(DATA_DIR, "FEDFUNDS.csv"))
dgs10    <- read_fred(file.path(DATA_DIR, "DGS10.csv"))

cat(sprintf("  BUSLOANS:  %d monthly obs (%s to %s)\n", nrow(busloans),
            min(busloans$date), max(busloans$date)))
cat(sprintf("  CONSUMER:  %d monthly obs (%s to %s)\n", nrow(consumer),
            min(consumer$date), max(consumer$date)))
cat(sprintf("  UNRATE:    %d monthly obs\n", nrow(unrate)))
cat(sprintf("  CPI:       %d monthly obs\n", nrow(cpi)))
cat(sprintf("  FEDFUNDS:  %d monthly obs\n", nrow(fedfunds)))
cat(sprintf("  DGS10:     %d daily obs\n", nrow(dgs10)))

# --- Aggregate DGS10 daily -> monthly (average) ---
dgs10$ym <- floor_date(dgs10$date, "month")
dgs10_monthly <- dgs10 %>%
  group_by(ym) %>%
  summarise(value = mean(value, na.rm = TRUE), .groups = "drop") %>%
  rename(date = ym)
cat(sprintf("  DGS10 monthly (aggregated): %d obs\n", nrow(dgs10_monthly)))

# --- Compute QUARTERLY loan growth (QoQ log growth, annualised %) ---
# Use end-of-quarter (last month) value for each quarter
compute_quarterly_growth <- function(df, label) {
  df$year  <- year(df$date)
  df$month <- month(df$date)
  df$qtr   <- quarter(df$date)
  # End-of-quarter months: 3,6,9,12
  eoq <- df[df$month %in% c(3, 6, 9, 12), ]
  eoq <- eoq[order(eoq$date), ]
  eoq$log_val <- log(eoq$value)
  eoq$growth  <- c(NA, diff(eoq$log_val) * 400)   # QoQ annualised %
  eoq <- eoq[!is.na(eoq$growth), ]
  eoq$yq <- paste0(eoq$year, "Q", eoq$qtr)
  cat(sprintf("  %s quarterly growth: %d obs (%s to %s)\n",
              label, nrow(eoq), eoq$yq[1], eoq$yq[nrow(eoq)]))
  eoq[, c("year", "qtr", "yq", "date", "growth")]
}

ci_qtr  <- compute_quarterly_growth(busloans, "C&I")
con_qtr <- compute_quarterly_growth(consumer, "Consumer")

# --- Monthly predictor transformations ---
# UNRATE -> monthly first difference
unrate_m <- unrate %>%
  arrange(date) %>%
  mutate(d_unrate = c(NA, diff(value)),
         year = year(date), month = month(date), qtr = quarter(date)) %>%
  filter(!is.na(d_unrate))

# CPI -> monthly log growth rate (annualised %)
cpi_m <- cpi %>%
  arrange(date) %>%
  mutate(cpi_growth = c(NA, diff(log(value)) * 1200),
         year = year(date), month = month(date), qtr = quarter(date)) %>%
  filter(!is.na(cpi_growth))

# FEDFUNDS -> monthly first difference
fedfunds_m <- fedfunds %>%
  arrange(date) %>%
  mutate(d_ff = c(NA, diff(value)),
         year = year(date), month = month(date), qtr = quarter(date)) %>%
  filter(!is.na(d_ff))

# DGS10 (monthly avg) -> first difference
dgs10_m <- dgs10_monthly %>%
  arrange(date) %>%
  mutate(d_dgs10 = c(NA, diff(value)),
         year = year(date), month = month(date), qtr = quarter(date)) %>%
  filter(!is.na(d_dgs10))

cat("\nMonthly predictor transformations complete.\n")

# ===========================================================================
# STEP 2: MIDAS DATA ALIGNMENT  (quarterly ~ monthly, m = 3)
# ===========================================================================
cat("\n--- Step 2: MIDAS Data Alignment (m = 3) ---\n\n")

m <- 3   # frequency ratio: 3 months per quarter

# For each quarterly obs, stack the 3 monthly predictor values in that quarter
# Chronological order (month-1 first, month-3 last) — mls() expects this
build_hf_vector_q <- function(monthly_df, value_col, qtr_df) {
  X_hf <- c()
  valid_idx <- c()
  for (i in seq_len(nrow(qtr_df))) {
    yr <- qtr_df$year[i]
    qt <- qtr_df$qtr[i]
    m_data <- monthly_df[monthly_df$year == yr & monthly_df$qtr == qt, ]
    m_data <- m_data[order(m_data$month), ]
    if (nrow(m_data) == 3) {
      X_hf <- c(X_hf, m_data[[value_col]])
      valid_idx <- c(valid_idx, i)
    }
  }
  list(X_hf = X_hf, valid_idx = valid_idx)
}

# Filter to 1990 onward
common_start <- 1990
ci_qtr  <- ci_qtr[ci_qtr$year >= common_start, ]
con_qtr <- con_qtr[con_qtr$year >= common_start, ]

cat(sprintf("Target: quarterly obs from %d onward\n", common_start))

# Build HF vectors for C&I predictors (UNRATE, CPI)
hf_unrate_ci <- build_hf_vector_q(unrate_m, "d_unrate", ci_qtr)
hf_cpi_ci    <- build_hf_vector_q(cpi_m, "cpi_growth", ci_qtr)

# Build HF vectors for Consumer predictors (FEDFUNDS, DGS10)
hf_ff_con    <- build_hf_vector_q(fedfunds_m, "d_ff", con_qtr)
hf_dgs10_con <- build_hf_vector_q(dgs10_m, "d_dgs10", con_qtr)

# Intersect valid indices to get quarters where ALL predictors are available
valid_ci  <- intersect(hf_unrate_ci$valid_idx, hf_cpi_ci$valid_idx)
valid_con <- intersect(hf_ff_con$valid_idx, hf_dgs10_con$valid_idx)

# Rebuild aligned data using common valid quarters
rebuild_aligned_q <- function(monthly_df, value_col, qtr_df, valid_idx) {
  X <- c()
  for (i in valid_idx) {
    yr <- qtr_df$year[i]
    qt <- qtr_df$qtr[i]
    m_data <- monthly_df[monthly_df$year == yr & monthly_df$qtr == qt, ]
    m_data <- m_data[order(m_data$month), ]
    X <- c(X, m_data[[value_col]])
  }
  X
}

# C&I model data
y_ci        <- ci_qtr$growth[valid_ci]
years_ci    <- ci_qtr$year[valid_ci]
qtrs_ci     <- ci_qtr$qtr[valid_ci]
yq_ci       <- ci_qtr$yq[valid_ci]
dates_ci    <- ci_qtr$date[valid_ci]
X_unrate_ci <- rebuild_aligned_q(unrate_m, "d_unrate", ci_qtr, valid_ci)
X_cpi_ci    <- rebuild_aligned_q(cpi_m, "cpi_growth", ci_qtr, valid_ci)

# Consumer model data
y_con        <- con_qtr$growth[valid_con]
years_con    <- con_qtr$year[valid_con]
qtrs_con     <- con_qtr$qtr[valid_con]
yq_con       <- con_qtr$yq[valid_con]
dates_con    <- con_qtr$date[valid_con]
X_ff_con     <- rebuild_aligned_q(fedfunds_m, "d_ff", con_qtr, valid_con)
X_dgs10_con  <- rebuild_aligned_q(dgs10_m, "d_dgs10", con_qtr, valid_con)

n_ci  <- length(y_ci)
n_con <- length(y_con)

cat(sprintf("C&I:      %d quarterly obs (%s to %s), %d monthly HF values each\n",
            n_ci, yq_ci[1], yq_ci[n_ci], length(X_unrate_ci)))
cat(sprintf("Consumer: %d quarterly obs (%s to %s), %d monthly HF values each\n",
            n_con, yq_con[1], yq_con[n_con], length(X_ff_con)))

# Sanity checks
stopifnot(length(X_unrate_ci) == n_ci * m)
stopifnot(length(X_cpi_ci)    == n_ci * m)
stopifnot(length(X_ff_con)    == n_con * m)
stopifnot(length(X_dgs10_con) == n_con * m)
cat("  Alignment checks passed.\n")

# ===========================================================================
# STEP 3: MODEL ESTIMATION
# ===========================================================================
cat("\n--- Step 3: Model Estimation ---\n\n")

safe_midas <- function(formula, start, label) {
  tryCatch({
    fit <- midas_r(formula, start = start)
    cat(sprintf("  %s: converged (RSS = %.2f)\n", label, deviance(fit)))
    fit
  }, error = function(e) {
    cat(sprintf("  %s: FAILED — %s\n", label, e$message))
    NULL
  })
}

# =========================================
# C&I MODELS
# =========================================
cat("=== C&I Loan Models ===\n\n")

# 1. MIDAS Exponential Almon — C&I
cat("Estimating MIDAS Almon (C&I)...\n")
ci_almon <- safe_midas(
  y_ci ~ mls(X_unrate_ci, 1:m, m, nealmon) + mls(X_cpi_ci, 1:m, m, nealmon),
  start = list(X_unrate_ci = c(0, 0, 0), X_cpi_ci = c(0, 0, 0)),
  "MIDAS Almon C&I"
)
if (!is.null(ci_almon)) summary(ci_almon)

# 2. MIDAS Beta — C&I
cat("\nEstimating MIDAS Beta (C&I)...\n")
ci_beta <- safe_midas(
  y_ci ~ mls(X_unrate_ci, 1:m, m, nbeta) + mls(X_cpi_ci, 1:m, m, nbeta),
  start = list(X_unrate_ci = c(1, 5, 0), X_cpi_ci = c(1, 5, 0)),
  "MIDAS Beta C&I"
)
if (!is.null(ci_beta)) summary(ci_beta)

# 3. ADL-MIDAS — C&I
cat("\nEstimating ADL-MIDAS (C&I)...\n")
y_lag1_ci     <- c(NA, y_ci[-n_ci])
idx_adl_ci    <- !is.na(y_lag1_ci)

y_ci_adl      <- y_ci[idx_adl_ci]
y_lag1_ci_adl <- y_lag1_ci[idx_adl_ci]
adl_start_ci  <- which(idx_adl_ci)[1]
X_unrate_ci_adl <- X_unrate_ci[((adl_start_ci - 1) * m + 1):length(X_unrate_ci)]
X_cpi_ci_adl    <- X_cpi_ci[((adl_start_ci - 1) * m + 1):length(X_cpi_ci)]

ci_adl <- safe_midas(
  y_ci_adl ~ y_lag1_ci_adl +
    mls(X_unrate_ci_adl, 1:m, m, nealmon) +
    mls(X_cpi_ci_adl, 1:m, m, nealmon),
  start = list(X_unrate_ci_adl = c(0, 0, 0), X_cpi_ci_adl = c(0, 0, 0)),
  "ADL-MIDAS C&I"
)
if (!is.null(ci_adl)) summary(ci_adl)

# 4. AR benchmark — C&I (BIC-selected)
cat("\nEstimating AR benchmark (C&I)...\n")
best_bic_ci <- Inf; best_p_ci <- 1
for (p in 1:6) {
  fit <- tryCatch(Arima(y_ci, order = c(p, 0, 0)), error = function(e) NULL)
  if (!is.null(fit) && BIC(fit) < best_bic_ci) {
    best_bic_ci <- BIC(fit); best_p_ci <- p
  }
}
ar_ci <- Arima(y_ci, order = c(best_p_ci, 0, 0))
cat(sprintf("  AR(%d) selected by BIC for C&I\n", best_p_ci))

# =========================================
# CONSUMER MODELS
# =========================================
cat("\n=== Consumer Loan Models ===\n\n")

# 1. MIDAS Exponential Almon — Consumer
cat("Estimating MIDAS Almon (Consumer)...\n")
con_almon <- safe_midas(
  y_con ~ mls(X_ff_con, 1:m, m, nealmon) + mls(X_dgs10_con, 1:m, m, nealmon),
  start = list(X_ff_con = c(0, 0, 0), X_dgs10_con = c(0, 0, 0)),
  "MIDAS Almon Consumer"
)
if (!is.null(con_almon)) summary(con_almon)

# 2. MIDAS Beta — Consumer
cat("\nEstimating MIDAS Beta (Consumer)...\n")
con_beta <- safe_midas(
  y_con ~ mls(X_ff_con, 1:m, m, nbeta) + mls(X_dgs10_con, 1:m, m, nbeta),
  start = list(X_ff_con = c(1, 5, 0), X_dgs10_con = c(1, 5, 0)),
  "MIDAS Beta Consumer"
)
if (!is.null(con_beta)) summary(con_beta)

# 3. ADL-MIDAS — Consumer
cat("\nEstimating ADL-MIDAS (Consumer)...\n")
y_lag1_con     <- c(NA, y_con[-n_con])
idx_adl_con    <- !is.na(y_lag1_con)

y_con_adl      <- y_con[idx_adl_con]
y_lag1_con_adl <- y_lag1_con[idx_adl_con]
adl_start_con  <- which(idx_adl_con)[1]
X_ff_con_adl    <- X_ff_con[((adl_start_con - 1) * m + 1):length(X_ff_con)]
X_dgs10_con_adl <- X_dgs10_con[((adl_start_con - 1) * m + 1):length(X_dgs10_con)]

con_adl <- safe_midas(
  y_con_adl ~ y_lag1_con_adl +
    mls(X_ff_con_adl, 1:m, m, nealmon) +
    mls(X_dgs10_con_adl, 1:m, m, nealmon),
  start = list(X_ff_con_adl = c(0, 0, 0), X_dgs10_con_adl = c(0, 0, 0)),
  "ADL-MIDAS Consumer"
)
if (!is.null(con_adl)) summary(con_adl)

# 4. AR benchmark — Consumer
cat("\nEstimating AR benchmark (Consumer)...\n")
best_bic_con <- Inf; best_p_con <- 1
for (p in 1:6) {
  fit <- tryCatch(Arima(y_con, order = c(p, 0, 0)), error = function(e) NULL)
  if (!is.null(fit) && BIC(fit) < best_bic_con) {
    best_bic_con <- BIC(fit); best_p_con <- p
  }
}
ar_con <- Arima(y_con, order = c(best_p_con, 0, 0))
cat(sprintf("  AR(%d) selected by BIC for Consumer\n", best_p_con))

# ===========================================================================
# STEP 4: WEIGHT VISUALIZATION
# ===========================================================================
cat("\n--- Step 4: Weight Visualization ---\n\n")

month_in_qtr_labels <- c("Month 1", "Month 2", "Month 3")

plot_weights <- function(almon_fit, beta_fit, predictor_names, pred_labels,
                         loan_type, filename) {
  df_all <- data.frame()

  for (i in seq_along(predictor_names)) {
    pname <- predictor_names[i]
    plabel <- pred_labels[i]

    # Almon weights
    if (!is.null(almon_fit)) {
      params <- coef(almon_fit)
      theta_names <- paste0(pname, c("2", "3"))
      theta_vals  <- params[theta_names]
      if (all(!is.na(theta_vals))) {
        w_almon <- nealmon(theta_vals, m)
        df_all <- rbind(df_all, data.frame(
          lag = 1:m, weight = w_almon,
          scheme = "Exponential Almon",
          predictor = plabel, stringsAsFactors = FALSE))
      }
    }

    # Beta weights
    if (!is.null(beta_fit)) {
      params_b <- coef(beta_fit)
      theta_b_names <- paste0(pname, c("1", "2", "3"))
      theta_b_vals  <- params_b[theta_b_names]
      if (all(!is.na(theta_b_vals))) {
        w_beta <- nbeta(theta_b_vals, m)
        df_all <- rbind(df_all, data.frame(
          lag = 1:m, weight = w_beta,
          scheme = "Beta",
          predictor = plabel, stringsAsFactors = FALSE))
      }
    }
  }

  if (nrow(df_all) == 0) {
    cat(sprintf("  WARNING: No weights to plot for %s\n", loan_type))
    return(invisible(NULL))
  }

  df_all$month_label <- factor(month_in_qtr_labels[df_all$lag],
                               levels = month_in_qtr_labels)

  p <- ggplot(df_all, aes(x = month_label, y = weight, color = scheme, group = scheme)) +
    geom_line(linewidth = 1.2) +
    geom_point(size = 3) +
    facet_wrap(~ predictor, scales = "free_y") +
    labs(title = sprintf("MIDAS Weight Functions — %s Loans (m=3)", loan_type),
         subtitle = "Monthly weights within each quarter",
         x = "Month within Quarter", y = "Weight", color = "Weighting Scheme") +
    theme_minimal(base_size = 13) +
    theme(legend.position = "bottom")

  ggsave(file.path(FIG_DIR, filename), p, width = 10, height = 5, dpi = 150)
  cat(sprintf("  Saved: %s\n", filename))

  # Degeneracy check
  for (pred in unique(df_all$predictor)) {
    for (sch in unique(df_all$scheme)) {
      w <- df_all$weight[df_all$predictor == pred & df_all$scheme == sch]
      max_w <- max(abs(w))
      if (length(w) > 0 && max_w > 0.9) {
        cat(sprintf("  WARNING: %s %s — max |weight| = %.3f (degenerate)\n",
                    pred, sch, max_w))
      } else if (length(w) > 0) {
        cat(sprintf("  OK: %s %s — weights = [%.3f, %.3f, %.3f]\n",
                    pred, sch, w[1], w[2], w[3]))
      }
    }
  }
}

# C&I weight plots
plot_weights(ci_almon, ci_beta,
             c("X_unrate_ci", "X_cpi_ci"),
             c("UNRATE (delta)", "CPI (growth)"),
             "C&I", "midas_r_weights_ci.png")

# Consumer weight plots
plot_weights(con_almon, con_beta,
             c("X_ff_con", "X_dgs10_con"),
             c("FEDFUNDS (delta)", "DGS10 (delta)"),
             "Consumer", "midas_r_weights_consumer.png")

# ===========================================================================
# STEP 5: OUT-OF-SAMPLE EVALUATION
# ===========================================================================
cat("\n--- Step 5: Out-of-Sample Evaluation ---\n\n")

oos_evaluate <- function(y, X_hf_list, years, qtrs, yq_labels,
                         loan_type, test_start = 2005,
                         covid_years = c(2020, 2021)) {
  n <- length(y)

  # Train = before test_start, Test = test_start onward excl. COVID
  train_mask <- years < test_start
  test_mask  <- years >= test_start & !(years %in% covid_years)
  train_end  <- max(which(train_mask))
  test_idx   <- which(test_mask)

  cat(sprintf("  %s: Train %s-%s (%d obs), Test %d-%d excl COVID (%d obs)\n",
              loan_type, yq_labels[1], yq_labels[train_end], train_end,
              test_start, max(years), length(test_idx)))

  # --- Fixed-window MIDAS estimation (train once, forecast all test) ---
  y_train  <- y[1:train_end]
  X1_train <- X_hf_list[[1]][1:(train_end * m)]
  X2_train <- X_hf_list[[2]][1:(train_end * m)]

  # MIDAS Almon
  midas_params <- NULL
  tryCatch({
    X1_t <- X1_train; X2_t <- X2_train
    fit_oos <- midas_r(
      y_train ~ mls(X1_t, 1:m, m, nealmon) + mls(X2_t, 1:m, m, nealmon),
      start = list(X1_t = c(0, 0, 0), X2_t = c(0, 0, 0))
    )
    midas_params <- coef(fit_oos)
    cat(sprintf("  MIDAS fixed-window estimated (%d train obs)\n", train_end))
  }, error = function(e) {
    cat(sprintf("  MIDAS estimation failed: %s\n", e$message))
  })

  # ADL-MIDAS
  adl_params <- NULL
  tryCatch({
    y_adl_t  <- y_train[-1]
    y_lag_t  <- y_train[-length(y_train)]
    X1_adl_t <- X1_train[(m + 1):length(X1_train)]
    X2_adl_t <- X2_train[(m + 1):length(X2_train)]
    fit_adl_oos <- midas_r(
      y_adl_t ~ y_lag_t +
        mls(X1_adl_t, 1:m, m, nealmon) +
        mls(X2_adl_t, 1:m, m, nealmon),
      start = list(X1_adl_t = c(0, 0, 0), X2_adl_t = c(0, 0, 0))
    )
    adl_params <- coef(fit_adl_oos)
    cat(sprintf("  ADL-MIDAS fixed-window estimated\n"))
  }, error = function(e) {
    cat(sprintf("  ADL-MIDAS estimation failed: %s\n", e$message))
  })

  # --- Generate forecasts ---
  midas_fc <- numeric(length(test_idx))
  adl_fc   <- numeric(length(test_idx))
  ar_fc    <- numeric(length(test_idx))
  actuals  <- numeric(length(test_idx))

  for (j in seq_along(test_idx)) {
    ti <- test_idx[j]
    actuals[j] <- y[ti]

    X1_test <- X_hf_list[[1]][((ti - 1) * m + 1):(ti * m)]
    X2_test <- X_hf_list[[2]][((ti - 1) * m + 1):(ti * m)]

    # MIDAS forecast
    if (!is.null(midas_params)) {
      b0 <- midas_params["(Intercept)"]
      b1 <- midas_params["X1_t1"]
      b2 <- midas_params["X2_t1"]
      w1 <- nealmon(midas_params[c("X1_t2", "X1_t3")], m)
      w2 <- nealmon(midas_params[c("X2_t2", "X2_t3")], m)
      midas_fc[j] <- b0 + b1 * sum(X1_test * w1) + b2 * sum(X2_test * w2)
    } else {
      midas_fc[j] <- NA
    }

    # ADL-MIDAS forecast
    if (!is.null(adl_params)) {
      b0_a <- adl_params["(Intercept)"]
      rho  <- adl_params["y_lag_t"]
      b1_a <- adl_params["X1_adl_t1"]
      b2_a <- adl_params["X2_adl_t1"]
      w1_a <- nealmon(adl_params[c("X1_adl_t2", "X1_adl_t3")], m)
      w2_a <- nealmon(adl_params[c("X2_adl_t2", "X2_adl_t3")], m)
      adl_fc[j] <- b0_a + rho * y[ti - 1] +
                   b1_a * sum(X1_test * w1_a) +
                   b2_a * sum(X2_test * w2_a)
    } else {
      adl_fc[j] <- NA
    }

    # AR forecast (expanding window)
    y_hist <- y[1:(ti - 1)]
    tryCatch({
      best_bic <- Inf; best_p <- 1
      for (p in 1:6) {
        fit_ar <- tryCatch(Arima(y_hist, order = c(p, 0, 0)), error = function(e) NULL)
        if (!is.null(fit_ar) && BIC(fit_ar) < best_bic) {
          best_bic <- BIC(fit_ar); best_p <- p
        }
      }
      ar_fit <- Arima(y_hist, order = c(best_p, 0, 0))
      ar_fc[j] <- as.numeric(forecast(ar_fit, h = 1)$mean)
    }, error = function(e) {
      ar_fc[j] <<- mean(y_hist)
    })
  }

  # Metrics
  valid_m <- !is.na(midas_fc)
  valid_a <- !is.na(adl_fc)
  msfe_ar <- mean((actuals - ar_fc)^2)

  results <- data.frame(
    Model = c("AR (BIC)", "MIDAS (Almon)", "ADL-MIDAS"),
    RMSE = c(
      sqrt(mean((actuals - ar_fc)^2)),
      if (any(valid_m)) sqrt(mean((actuals[valid_m] - midas_fc[valid_m])^2)) else NA,
      if (any(valid_a)) sqrt(mean((actuals[valid_a] - adl_fc[valid_a])^2)) else NA
    ),
    MAE = c(
      mean(abs(actuals - ar_fc)),
      if (any(valid_m)) mean(abs(actuals[valid_m] - midas_fc[valid_m])) else NA,
      if (any(valid_a)) mean(abs(actuals[valid_a] - adl_fc[valid_a])) else NA
    ),
    stringsAsFactors = FALSE
  )
  results$Rel_MSFE  <- results$RMSE^2 / msfe_ar
  results$vs_AR_pct <- (1 - results$Rel_MSFE) * 100

  cat(sprintf("\n  === %s OOS Results ===\n", loan_type))
  cat(sprintf("  %-20s %8s %8s %10s %10s\n", "Model", "RMSE", "MAE", "Rel MSFE", "vs AR %"))
  cat(sprintf("  %s\n", strrep("-", 60)))
  for (i in 1:nrow(results)) {
    if (is.na(results$RMSE[i])) {
      cat(sprintf("  %-20s %8s %8s %10s %10s\n", results$Model[i], "NA", "NA", "NA", "NA"))
    } else {
      cat(sprintf("  %-20s %8.3f %8.3f %10.3f %+9.1f%%\n",
                  results$Model[i], results$RMSE[i], results$MAE[i],
                  results$Rel_MSFE[i], results$vs_AR_pct[i]))
    }
  }

  list(results = results, years = years[test_idx], qtrs = qtrs[test_idx],
       yq = yq_labels[test_idx], actuals = actuals,
       ar_fc = ar_fc, midas_fc = midas_fc, adl_fc = adl_fc)
}

# Run OOS
oos_ci <- oos_evaluate(y_ci, list(X_unrate_ci, X_cpi_ci),
                       years_ci, qtrs_ci, yq_ci, "C&I")
oos_con <- oos_evaluate(y_con, list(X_ff_con, X_dgs10_con),
                        years_con, qtrs_con, yq_con, "Consumer")

# --- OOS Evaluation Plots ---
cat("\n  Generating OOS evaluation plots...\n")

plot_oos <- function(oos, loan_type, filename) {
  # Use numeric x-axis: year + (qtr-1)/4
  x_vals <- oos$years + (oos$qtrs - 1) / 4

  df <- data.frame(
    X = rep(x_vals, 4),
    Value = c(oos$actuals, oos$ar_fc, oos$midas_fc, oos$adl_fc),
    Series = rep(c("Actual", "AR", "MIDAS (Almon)", "ADL-MIDAS"),
                 each = length(x_vals))
  )
  df <- df[!is.na(df$Value), ]

  p <- ggplot(df, aes(x = X, y = Value, color = Series, linetype = Series)) +
    geom_line(linewidth = 0.9) +
    geom_point(data = df[df$Series == "Actual", ], size = 1.2) +
    scale_color_manual(values = c("Actual" = "black", "AR" = "grey50",
                                  "MIDAS (Almon)" = "#1b9e77",
                                  "ADL-MIDAS" = "#d95f02")) +
    scale_linetype_manual(values = c("Actual" = "solid", "AR" = "dashed",
                                     "MIDAS (Almon)" = "solid",
                                     "ADL-MIDAS" = "dotdash")) +
    labs(title = sprintf("Out-of-Sample Forecasts — %s Loans (MIDAS-R, m=3)", loan_type),
         subtitle = "Fixed-window estimation, 2005Q1-2025Q4 excl. COVID 2020-2021",
         x = "Year", y = "QoQ Annualised Growth (%)",
         color = "Model", linetype = "Model") +
    theme_minimal(base_size = 13) +
    theme(legend.position = "bottom")

  ggsave(file.path(FIG_DIR, filename), p, width = 11, height = 6, dpi = 150)
  cat(sprintf("  Saved: %s\n", filename))
}

plot_oos(oos_ci, "C&I", "midas_r_oos_ci.png")
plot_oos(oos_con, "Consumer", "midas_r_oos_consumer.png")

# ===========================================================================
# STEP 6: NGFS SCENARIO FORECASTING
# ===========================================================================
cat("\n--- Step 6: NGFS Scenario Forecasting ---\n\n")

# Load NGFS NiGEM data
nigem_raw <- read_excel(file.path(DATA_DIR, "ngfs-phase5-nigem.xlsx"), sheet = "data")
nigem_us  <- nigem_raw[grepl("United States", nigem_raw$Region), ]
nigem_us  <- nigem_us[!duplicated(paste(nigem_us$Model, nigem_us$Scenario,
                                        nigem_us$Variable)), ]

year_cols <- colnames(nigem_us)[grepl("^\\d{4}$", colnames(nigem_us))]
models    <- sort(unique(nigem_us$Model))

cat(sprintf("  NGFS: %d rows, %d models, years %s-%s\n",
            nrow(nigem_us), length(models), min(year_cols), max(year_cols)))

# Variable mapping
VAR_MAP <- list(
  list(level = "Unemployment rate ; %",
       diff = "Unemployment rate ; %(combined)", type = "abs", label = "UNRATE"),
  list(level = "Inflation rate ; %",
       diff = "Inflation rate ; %(combined)", type = "abs", label = "CPI_INFLATION"),
  list(level = "Central bank Intervention rate (policy interest rate) ; %",
       diff = "Central bank Intervention rate (policy interest rate) ; %(combined)",
       type = "abs", label = "FEDFUNDS"),
  list(level = "Long term interest rate ; %",
       diff = "Long term interest rate ; %(combined)", type = "abs", label = "DGS10")
)

KEY_SCENARIOS <- c("Net Zero 2050", "Delayed transition",
                   "Nationally Determined Contributions (NDCs)")
SCENARIO_SHORT <- c("Net Zero 2050" = "Net Zero",
                    "Delayed transition" = "Delayed Trans.",
                    "Nationally Determined Contributions (NDCs)" = "NDCs")
SCENARIO_COLORS <- c("Net Zero 2050" = "#1b9e77",
                     "Delayed transition" = "#d95f02",
                     "Nationally Determined Contributions (NDCs)" = "#e7298a")

# Reconstruct NGFS levels from baseline + diffs
reconstruct_ngfs <- function(nigem_us, var_info, year_cols, models) {
  all_paths <- list()
  for (mod in models) {
    ms <- sub(".*\\[(.*)\\]", "\\1", mod)
    baseline <- nigem_us[nigem_us$Variable == var_info$level &
                         nigem_us$Model == mod &
                         nigem_us$Scenario == "Baseline", ]
    if (nrow(baseline) == 0) next
    base_vals <- as.numeric(baseline[1, year_cols])

    diffs <- nigem_us[nigem_us$Variable == var_info$diff & nigem_us$Model == mod, ]
    for (i in seq_len(nrow(diffs))) {
      scen <- diffs$Scenario[i]
      diff_vals <- as.numeric(diffs[i, year_cols])
      if (var_info$type == "pct") {
        level_vals <- base_vals * (1 + diff_vals / 100)
      } else {
        level_vals <- base_vals + diff_vals
      }
      all_paths[[paste(ms, scen, sep = "|")]] <- data.frame(
        year = as.integer(year_cols), value = level_vals,
        model = ms, scenario = scen, stringsAsFactors = FALSE)
    }
    all_paths[[paste(ms, "Baseline", sep = "|")]] <- data.frame(
      year = as.integer(year_cols), value = base_vals,
      model = ms, scenario = "Baseline", stringsAsFactors = FALSE)
  }
  do.call(rbind, all_paths)
}

ngfs_paths <- list()
for (vi in VAR_MAP) {
  ngfs_paths[[vi$label]] <- reconstruct_ngfs(nigem_us, vi, year_cols, models)
}
for (label in names(ngfs_paths)) {
  cat(sprintf("  %s: %d scenario-model combinations\n",
              label, length(unique(paste(ngfs_paths[[label]]$model,
                                        ngfs_paths[[label]]$scenario)))))
}

# --- Interpolate annual NGFS -> monthly, then transform ---
interpolate_to_monthly <- function(annual_df) {
  annual_df <- annual_df[order(annual_df$year), ]
  # Place annual values at June (mid-year) for smoother interpolation
  mid_dates <- as.Date(paste0(annual_df$year, "-06-15"))
  start_date <- as.Date(paste0(min(annual_df$year), "-01-01"))
  end_date   <- as.Date(paste0(max(annual_df$year), "-12-01"))
  monthly_dates <- seq(start_date, end_date, by = "month")
  monthly_vals <- approx(as.numeric(mid_dates), annual_df$value,
                         xout = as.numeric(monthly_dates), rule = 2)$y
  data.frame(date = monthly_dates, value = monthly_vals,
             year = year(monthly_dates), month = month(monthly_dates),
             qtr = quarter(monthly_dates))
}

# Transform functions
tf_first_diff <- function(x) c(0, diff(x))  # first month gets 0 (no prior)
tf_passthrough <- function(x) x  # NGFS inflation rate is already annualised %

# --- Generate scenario forecasts ---
generate_scenario_fc <- function(loan_type, midas_fit, adl_fit,
                                 pred_labels, transform_fns,
                                 y_full, years_full, qtrs_full,
                                 forecast_start = 2026, forecast_end = 2050) {
  cat(sprintf("\n  === %s scenario forecasts ===\n", loan_type))

  if (is.null(midas_fit) && is.null(adl_fit)) {
    cat("  WARNING: No MIDAS model available.\n")
    return(NULL)
  }

  # Prefer MIDAS for projection stability
  use_adl <- is.null(midas_fit)
  fit <- if (!use_adl) midas_fit else adl_fit
  params <- coef(fit)
  pnames <- names(params)

  # Identify HF variable base names
  hf_bases <- c()
  for (pn in pnames) {
    if (grepl("[0-9]$", pn) && !grepl("Intercept|y_lag", pn)) {
      hf_bases <- unique(c(hf_bases, sub("[0-9]+$", "", pn)))
    }
  }
  cat(sprintf("  Model: %s | HF vars: %s\n",
              if (use_adl) "ADL-MIDAS" else "MIDAS",
              paste(hf_bases, collapse = ", ")))

  model_names <- unique(ngfs_paths[[pred_labels[1]]]$model)
  results_all <- list()

  # Build quarterly forecast dates: Q1-Q4 for each year
  fc_quarters <- expand.grid(qtr = 1:4, year = forecast_start:forecast_end)
  fc_quarters <- fc_quarters[order(fc_quarters$year, fc_quarters$qtr), ]

  for (scen in KEY_SCENARIOS) {
    for (mod in model_names) {
      # Interpolate NGFS to monthly for all predictors
      all_available <- TRUE
      monthly_preds <- list()
      for (k in seq_along(pred_labels)) {
        path_data <- ngfs_paths[[pred_labels[k]]]
        sub_df <- path_data[path_data$scenario == scen & path_data$model == mod, ]
        if (nrow(sub_df) == 0) { all_available <- FALSE; break }
        mp <- interpolate_to_monthly(sub_df[, c("year", "value")])
        mp$transformed <- transform_fns[[k]](mp$value)
        monthly_preds[[k]] <- mp
      }
      if (!all_available) next

      y_prev <- y_full[length(y_full)]
      fc_yrs <- c(); fc_qtrs <- c(); fc_vals <- c()

      for (row in seq_len(nrow(fc_quarters))) {
        fc_yr <- fc_quarters$year[row]
        fc_qt <- fc_quarters$qtr[row]

        X_fc <- list()
        skip <- FALSE
        for (k in seq_along(pred_labels)) {
          mp <- monthly_preds[[k]]
          qdata <- mp[mp$year == fc_yr & mp$qtr == fc_qt, ]
          qdata <- qdata[order(qdata$month), ]
          if (nrow(qdata) < 3) { skip <- TRUE; break }
          X_fc[[k]] <- qdata$transformed[1:3]
        }
        if (skip) next

        # Compute forecast
        fc <- params["(Intercept)"]
        if (use_adl) {
          rho_name <- grep("y_lag", pnames, value = TRUE)[1]
          if (!is.na(rho_name)) fc <- fc + params[rho_name] * y_prev
        }
        for (k in seq_along(hf_bases)) {
          sn  <- hf_bases[k]
          bk  <- params[paste0(sn, "1")]
          thk <- params[c(paste0(sn, "2"), paste0(sn, "3"))]
          if (any(is.na(c(bk, thk)))) next
          wk  <- nealmon(thk, m)
          fc  <- fc + bk * sum(X_fc[[k]] * wk)
        }

        fc <- as.numeric(fc)
        fc_yrs  <- c(fc_yrs, fc_yr)
        fc_qtrs <- c(fc_qtrs, fc_qt)
        fc_vals <- c(fc_vals, fc)
        y_prev  <- fc
      }

      if (length(fc_yrs) > 0) {
        results_all[[paste(mod, scen)]] <- data.frame(
          year = fc_yrs, qtr = fc_qtrs, growth = fc_vals,
          model = mod, scenario = scen, stringsAsFactors = FALSE)
      }
    }
  }

  if (length(results_all) == 0) {
    cat("  WARNING: No forecasts generated.\n")
    return(NULL)
  }
  result <- do.call(rbind, results_all)
  cat(sprintf("  Generated %d forecast points across %d scenario-model combos\n",
              nrow(result), length(results_all)))
  result
}

ci_scenario_fc <- generate_scenario_fc(
  "C&I", ci_almon, ci_adl,
  c("UNRATE", "CPI_INFLATION"), list(tf_first_diff, tf_passthrough),
  y_ci, years_ci, qtrs_ci
)

con_scenario_fc <- generate_scenario_fc(
  "Consumer", con_almon, con_adl,
  c("FEDFUNDS", "DGS10"), list(tf_first_diff, tf_first_diff),
  y_con, years_con, qtrs_con
)

# --- Fan Chart Plots ---
cat("\n  Generating scenario fan chart plots...\n")

plot_fan_chart <- function(scenario_fc, y_hist, years_hist, qtrs_hist,
                           loan_type, filename) {
  if (is.null(scenario_fc) || nrow(scenario_fc) == 0) {
    cat(sprintf("  WARNING: No data for %s fan chart\n", loan_type))
    return(invisible(NULL))
  }

  # Annualise: average quarterly growth per year for each scenario-model
  annual_fc <- scenario_fc %>%
    filter(scenario %in% KEY_SCENARIOS) %>%
    group_by(year, scenario, model) %>%
    summarise(growth = mean(growth, na.rm = TRUE), .groups = "drop")

  summary_fc <- annual_fc %>%
    group_by(year, scenario) %>%
    summarise(median = median(growth), lo = quantile(growth, 0.1),
              hi = quantile(growth, 0.9), .groups = "drop")

  # Historical annual averages
  hist_annual <- data.frame(year = years_hist, growth = y_hist) %>%
    group_by(year) %>%
    summarise(growth = mean(growth), .groups = "drop")

  p <- ggplot() +
    geom_line(data = hist_annual, aes(x = year, y = growth),
              color = "black", linewidth = 0.8) +
    geom_point(data = hist_annual, aes(x = year, y = growth),
               color = "black", size = 1.2)

  for (scen in KEY_SCENARIOS) {
    sub <- summary_fc[summary_fc$scenario == scen, ]
    if (nrow(sub) == 0) next
    col <- SCENARIO_COLORS[scen]
    p <- p +
      geom_ribbon(data = sub, aes(x = year, ymin = lo, ymax = hi),
                  fill = col, alpha = 0.2) +
      geom_line(data = sub, aes(x = year, y = median),
                color = col, linewidth = 1)
  }

  p <- p +
    geom_vline(xintercept = max(years_hist) + 0.5, linetype = "dashed",
               color = "grey40") +
    annotate("text", x = max(years_hist) + 1, y = max(y_hist) * 0.9,
             label = "Forecast", hjust = 0, size = 3.5, color = "grey40") +
    labs(title = sprintf("MIDAS-R Scenario Forecasts — %s Loans (m=3)", loan_type),
         subtitle = "Median across IAM models, 10-90% bands | Annual avg of quarterly growth",
         x = "Year", y = "Annualised Growth (%)") +
    theme_minimal(base_size = 13)

  ggsave(file.path(FIG_DIR, filename), p, width = 12, height = 7, dpi = 150)
  cat(sprintf("  Saved: %s\n", filename))
}

plot_fan_chart(ci_scenario_fc, y_ci, years_ci, qtrs_ci,
               "C&I", "midas_r_scenario_fan_ci.png")
plot_fan_chart(con_scenario_fc, y_con, years_con, qtrs_con,
               "Consumer", "midas_r_scenario_fan_consumer.png")

# --- Cumulative Impact Plots ---
cat("\n  Generating cumulative impact plots...\n")

plot_cumulative <- function(scenario_fc, loan_type, filename) {
  if (is.null(scenario_fc) || nrow(scenario_fc) == 0) {
    cat(sprintf("  WARNING: No data for %s cumulative\n", loan_type))
    return(invisible(NULL))
  }

  # Compute cumulative balance: compound quarterly growth
  cumul <- scenario_fc %>%
    filter(scenario %in% KEY_SCENARIOS) %>%
    group_by(model, scenario) %>%
    arrange(year, qtr) %>%
    mutate(balance = 100 * cumprod(1 + growth / 400)) %>%   # QoQ annualised -> quarterly
    ungroup()

  # Annual snapshots (Q4 each year)
  annual_snap <- cumul %>%
    filter(qtr == 4) %>%
    group_by(year, scenario) %>%
    summarise(median = median(balance), lo = quantile(balance, 0.1),
              hi = quantile(balance, 0.9), .groups = "drop")

  p <- ggplot(annual_snap, aes(x = year)) +
    geom_hline(yintercept = 100, linetype = "dotted", color = "grey50")

  for (scen in KEY_SCENARIOS) {
    sub <- annual_snap[annual_snap$scenario == scen, ]
    if (nrow(sub) == 0) next
    col <- SCENARIO_COLORS[scen]
    p <- p +
      geom_ribbon(data = sub, aes(ymin = lo, ymax = hi), fill = col, alpha = 0.15) +
      geom_line(data = sub, aes(y = median), color = col, linewidth = 1.1)
  }

  p <- p +
    labs(title = sprintf("MIDAS-R Cumulative Impact — %s Loans (m=3)", loan_type),
         subtitle = "Balance index (100 = start of forecast), Q4 snapshots",
         x = "Year", y = "Balance Index") +
    theme_minimal(base_size = 13)

  ggsave(file.path(FIG_DIR, filename), p, width = 12, height = 7, dpi = 150)
  cat(sprintf("  Saved: %s\n", filename))
}

plot_cumulative(ci_scenario_fc, "C&I", "midas_r_cumulative_ci.png")
plot_cumulative(con_scenario_fc, "Consumer", "midas_r_cumulative_consumer.png")

# ===========================================================================
# STEP 7: SUMMARY TABLE & OUTPUT
# ===========================================================================
cat("\n--- Step 7: Summary Output ---\n\n")

# OOS summary
oos_summary <- rbind(
  cbind(Loan = "C&I", oos_ci$results),
  cbind(Loan = "Consumer", oos_con$results)
)

# Scenario summary at key horizons
scenario_table <- data.frame()
for (lt in c("C&I", "Consumer")) {
  fc <- if (lt == "C&I") ci_scenario_fc else con_scenario_fc
  if (is.null(fc)) next

  for (scen in KEY_SCENARIOS) {
    for (hz in c(2030, 2040, 2050)) {
      # Annual average growth for that year
      sub <- fc[fc$scenario == scen & fc$year == hz, ]
      if (nrow(sub) == 0) next
      med_growth <- median(tapply(sub$growth, sub$model, mean), na.rm = TRUE)

      # Cumulative balance through Q4 of that year
      cum_by_model <- fc %>%
        filter(scenario == scen) %>%
        group_by(model) %>%
        arrange(year, qtr) %>%
        mutate(bal = 100 * cumprod(1 + growth / 400)) %>%
        filter(year == hz, qtr == 4) %>%
        ungroup()
      med_bal <- median(cum_by_model$bal, na.rm = TRUE)

      scenario_table <- rbind(scenario_table, data.frame(
        Loan_Type = lt, Scenario = SCENARIO_SHORT[scen],
        Horizon = hz, Growth_Pct = round(med_growth, 2),
        Balance_Index = round(med_bal, 1), stringsAsFactors = FALSE))
    }
  }
}

# Print
cat(strrep("=", 75), "\n")
cat("  MIDAS-R RESULTS SUMMARY  (Quarterly LHS, Monthly RHS, m=3)\n")
cat(strrep("=", 75), "\n\n")

cat("--- Out-of-Sample Evaluation (2005-2025, excl. COVID) ---\n\n")
cat(sprintf("  %-10s %-20s %8s %8s %10s %10s\n",
            "Loan", "Model", "RMSE", "MAE", "Rel MSFE", "vs AR"))
cat(sprintf("  %s\n", strrep("-", 70)))
for (i in 1:nrow(oos_summary)) {
  if (is.na(oos_summary$RMSE[i])) {
    cat(sprintf("  %-10s %-20s %8s %8s %10s %10s\n",
                oos_summary$Loan[i], oos_summary$Model[i], "NA","NA","NA","NA"))
  } else {
    cat(sprintf("  %-10s %-20s %8.3f %8.3f %10.3f %+9.1f%%\n",
                oos_summary$Loan[i], oos_summary$Model[i],
                oos_summary$RMSE[i], oos_summary$MAE[i],
                oos_summary$Rel_MSFE[i], oos_summary$vs_AR_pct[i]))
  }
}

if (nrow(scenario_table) > 0) {
  cat("\n--- Scenario Forecasts (Median across IAM models) ---\n\n")
  cat(sprintf("  %-10s %-15s %7s %10s %12s\n",
              "Loan", "Scenario", "Year", "Growth(%)", "Bal. Index"))
  cat(sprintf("  %s\n", strrep("-", 60)))
  for (i in 1:nrow(scenario_table)) {
    cat(sprintf("  %-10s %-15s %7d %10.2f %12.1f\n",
                scenario_table$Loan_Type[i], scenario_table$Scenario[i],
                scenario_table$Horizon[i], scenario_table$Growth_Pct[i],
                scenario_table$Balance_Index[i]))
  }
}

# Save
write.csv(oos_summary, file.path(TAB_DIR, "midas_r_oos_summary.csv"), row.names = FALSE)
cat(sprintf("\n  Saved: midas_r_oos_summary.csv\n"))
if (nrow(scenario_table) > 0) {
  write.csv(scenario_table, file.path(TAB_DIR, "midas_r_scenario_summary.csv"),
            row.names = FALSE)
  cat(sprintf("  Saved: midas_r_scenario_summary.csv\n"))
}

cat("\n--- Output Files ---\n")
cat(sprintf("  Figures: %s\n",
            paste(list.files(FIG_DIR, pattern = "midas_r_"), collapse = ", ")))
cat(sprintf("  Tables:  %s\n",
            paste(list.files(TAB_DIR, pattern = "midas_r_"), collapse = ", ")))

cat("\n")
cat(strrep("=", 75), "\n")
cat("  MIDAS-R analysis complete.\n")
cat(strrep("=", 75), "\n")
