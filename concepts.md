# Concepts & Tools Reference

## 1. Time Series Fundamentals

### Stationarity
A series is stationary if its mean, variance, and autocorrelation structure do not change over time. Most financial series are non-stationary — they trend. Models like VAR require stationarity, so we transform the data first.

### ADF Test (Augmented Dickey-Fuller)
Tests whether a series has a unit root — i.e. is non-stationary. 
- Null hypothesis: series has a unit root (non-stationary)
- If p-value < 0.05 we reject the null and conclude stationarity
- Applied to: INR/USD returns, log Brent, reserve changes

### Differencing
If a series is non-stationary, taking first differences (today minus yesterday) usually makes it stationary. Log returns of INR/USD are the first difference of log prices.

### ACF / PACF
- Autocorrelation Function: how correlated is a series with its own past values at various lags
- Partial Autocorrelation Function: same but removes intermediate lag effects
- Used to: diagnose serial correlation, select lag length for models

### Rolling Mean and Variance
Compute mean and variance over a sliding window. Used in EDA to visually identify regime changes — if rolling variance jumps at a point, something structural changed.

---

## 2. Structural Break Analysis

### Chow Test
Tests whether coefficients in a regression are the same across two subperiods split at a known breakpoint.
- Null hypothesis: no structural break at the specified date
- Requires you to specify the breakpoint in advance
- Use case: test if depreciation rate changed after a known event (e.g. rupee-rouble collapse)

### Bai-Perron Test
Extends Chow test to find breakpoints endogenously — you don't need to specify them in advance.
- Identifies multiple structural breaks simultaneously
- More powerful than Chow when break date is uncertain
- Use case: let the data tell us when the INR regime changed, then check if it matches real events
- Library: `ruptures`

---

## 3. Volatility Modelling

### ARCH (Autoregressive Conditional Heteroskedasticity)
Volatility is not constant — it clusters. High volatility today predicts high volatility tomorrow. ARCH models this by making variance a function of past squared residuals.

### GARCH(1,1) (Generalized ARCH)
Extension of ARCH. Variance today depends on:
- Yesterday's squared residual (ARCH term) — recent shock
- Yesterday's variance (GARCH term) — persistence of volatility

Formula:
σ²_t = ω + α·ε²_(t-1) + β·σ²_(t-1)

Where:
- ω = long-run variance
- α = reaction to shocks
- β = persistence of volatility
- α + β < 1 for stationarity

### Intervention Footprint
The gap between GARCH-predicted volatility and realized volatility.
- When realized vol < predicted vol: something is compressing it — likely RBI intervention
- We use this gap as a proxy for intervention intensity over time
- Intuition: if the market *should* be volatile given recent shocks but *isn't*, someone is smoothing it

### Realized Volatility
Rolling standard deviation of daily returns over a fixed window (e.g. 21 days). Simple empirical measure of how much the series actually moved.

---

## 4. VAR Model

### Vector Autoregression (VAR)
Models multiple time series simultaneously. Each variable is regressed on its own lags and the lags of all other variables.
- Captures interdependencies between oil, reserves, and INR
- No need to specify which variable causes which — the model estimates all directions
- Requires all series to be stationary

### Lag Selection
We use information criteria to pick the right number of lags:
- AIC (Akaike Information Criterion) — penalizes complexity less
- BIC (Bayesian Information Criterion) — penalizes complexity more
- Lower is better for both

### Granger Causality
Tests whether past values of variable X help predict variable Y beyond Y's own past.
- Not true causality — predictive causality
- Use case: does oil Granger-cause reserve depletion? Do reserves Granger-cause INR weakness?

### Impulse Response Functions (IRF)
Traces the effect of a one-unit shock in one variable on all other variables over time.
- Use case: if oil spikes by $10 today, what happens to reserves over 6 months and INR over 12 months?
- This is the transmission mechanism quantified

### Forecast Error Variance Decomposition (FEVD)
Breaks down how much of the variance in one variable is explained by shocks from each other variable.
- Use case: what fraction of INR variance is explained by oil shocks vs reserve shocks vs Fed shocks?

---

## 5. Data Series

### INR/USD — `DEXINUS` (FRED)
- Indian Rupees per US Dollar, daily spot rate
- Role: dependent variable, what we are explaining
- Source: Federal Reserve via FRED

### Brent Crude — `DCOILBRENTEU` (FRED)
- Price of Brent crude oil in USD per barrel, daily
- Role: proxy for India's dollar import bill and current account pressure
- Why: India imports ~85% of crude priced in dollars, oil spike = wider CAD = reserve drain

### India Forex Reserves — `TRESEGINM052N` (FRED)
- Total reserves excluding gold, monthly, in USD
- Role: proxy for RBI's intervention capacity
- Why: when reserves deplete, RBI loses ability to defend INR

### Fed Funds Rate — `FEDFUNDS` (FRED)
- US federal funds effective rate, monthly
- Role: proxy for global dollar strength and EM capital flow pressure
- Why: Fed hikes → dollar strengthens → EM capital flees → India's borrowed forex exits

---

## 6. Research Hypotheses

### H1 — Structural Break
The INR/USD depreciation regime underwent a statistically significant structural break
coinciding with RBI reserve depletion and the collapse of the rupee-rouble corridor.
Post-break drift rate is significantly higher than the historical 3% annualized baseline.

### H2 — Intervention Footprint
RBI intervention is detectable as systematic compression of realized volatility below
GARCH-predicted volatility. Intervention intensity correlates negatively with reserve levels —
as reserves deplete, intervention capacity and frequency decline measurably.

### H3 — Oil-Reserve-INR Transmission
An oil price shock transmits to INR weakness via reserve depletion with a measurable lag.
Granger causality runs: Brent → Reserves → INR/USD.
Impulse response functions quantify the magnitude and timing of this transmission.

### H4 — Psychological Threshold Effects
INR/USD volatility and forward market pricing exhibit measurable anomalies as the rate
approaches round number levels (80, 85, 90, 95, 100), consistent with threshold effects
in investor sentiment and RBI defence behaviour.

---

## 7. Libraries

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation, time series handling |
| `numpy` | Numerical operations |
| `matplotlib` | Plotting and visualization |
| `fredapi` | Pull data from FRED API |
| `statsmodels` | ADF test, VAR model, Granger causality |
| `arch` | GARCH modelling |
| `ruptures` | Bai-Perron structural break detection |
| `python-dotenv` | Load API keys from .env file |

EOF
