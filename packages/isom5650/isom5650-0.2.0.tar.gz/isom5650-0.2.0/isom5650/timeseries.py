
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import adfuller

import numpy as np

# Define function of KPSS
def kpss_test(timeseries,null="c"):
    kpsstest = kpss(timeseries, regression=null)
    kpss_output = pd.Series(kpsstest[0:2], index=['Test Statistic','p-value'])
    return kpss_output.iloc[:2]



from statsmodels.tsa.stattools import adfuller
# Define function of ADF
def adf_test(timeseries, reg="c"):
    dftest = adfuller(timeseries, regression=reg)
    # Test Statistic, p-value, Lags Used, Number of Observations Used
    dfoutput = pd.Series(dftest[0:2], index=['Test Statistic','p-value'])
    return dfoutput.iloc[:2]


# Define correlogram function
def plot_correlogram(x, lags=None, title=None):
    # Lag
    lags = min(10, int(len(x)/5)) if lags is None else lags
    # Four subplots on the graph
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 8))

    # Plot of x
    x.plot(ax=axes[0][0], title='Residuals')
    # Rolling mean of last 21 days
    x.rolling(21).mean().plot(ax=axes[0][0], c='k', lw=1)
    # Q-Stat
    q_p = np.max(q_stat(acf(x, nlags=lags), len(x))[1])
    # Text on the label
    stats = f'Q-Stat: {np.max(q_p):>8.2f}\nADF: {adfuller(x)[1]:>11.2f}'
    # Label on top left-hand corner
    axes[0][0].text(x=.02, y=.85, s=stats, transform=axes[0][0].transAxes)

    # Probability Plot
    probplot(x, plot=axes[0][1])
    # Mean, var, skewness, kurtosis
    mean, var, skew, kurtosis = moment(x, moment=[1, 2, 3, 4])
    # Text on the label
    s = f'Mean: {mean:>12.2f}\nSD: {np.sqrt(var):>16.2f}\nSkew: {skew:12.2f}\nKurtosis:{kurtosis:9.2f}'
    # Label on top left-hand corner
    axes[0][1].text(x=.02, y=.75, s=s, transform=axes[0][1].transAxes)

    # ACF
    plot_acf(x=x, lags=lags, zero=False, ax=axes[1][0])
    # PACF
    plot_pacf(x, lags=lags, zero=False, ax=axes[1][1])
    # xlabel of ACF
    axes[1][0].set_xlabel('Lag')
    # xlabel of PACF
    axes[1][1].set_xlabel('Lag')

    # Title of the big graph
    fig.suptitle(title, fontsize=14)
    # Style
    fig.tight_layout()
    fig.subplots_adjust(top=.9)


def hurst_exponent(ts, max_lag=20):
    """
    Calculate the Hurst Exponent of a time series.
    """
    # Ensure input is a NumPy array
    ts = np.array(ts)

    # Check for valid input
    if len(ts) < max_lag:
        raise ValueError("Time series is too short for the specified max_lag.")

    # Ensure no NaNs or infs
    ts = ts[np.isfinite(ts)]
    if len(ts) == 0:
        raise ValueError("Time series contains only NaN or inf values.")

    # Calculate tau
    lags = range(2, max_lag)
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]

    # Log-log regression
    tau = np.array(tau)
    tau = tau[tau > 0]  # Exclude zero or negative values
    lags = np.array(lags)[:len(tau)]  # Adjust lags accordingly

    if len(tau) == 0:
        raise ValueError("No valid tau values for Hurst exponent calculation.")

    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0
