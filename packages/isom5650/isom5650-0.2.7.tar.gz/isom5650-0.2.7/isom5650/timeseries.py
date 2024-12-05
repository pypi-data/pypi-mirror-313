
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.tsa.api as tsa
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, q_stat, adfuller
from scipy.stats import probplot, moment
from sklearn import (linear_model, metrics, neural_network, pipeline, preprocessing, model_selection)
import statsmodels.formula.api as sm
from statsmodels.tsa.arima.model import ARIMA

# Import MSE
from sklearn.metrics import mean_squared_error
# Import LinAlgError
from numpy.linalg import LinAlgError
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from numpy.linalg import LinAlgError

def find_best_arima(data, train_size=40, compare_size=30, max_p=5, max_d=2, max_q=5):
    """
    Finds the best ARIMA model based on RMSE, AIC, and BIC.

    Parameters:
    - data: pd.Series, the time series data to evaluate.
    - train_size: int, the size of the training dataset.
    - compare_size: int, the size of the evaluation dataset.
    - max_p: int, maximum AR (p) order to consider.
    - max_d: int, maximum differencing (d) order to consider.
    - max_q: int, maximum MA (q) order to consider.

    Returns:
    - pd.DataFrame: Results with (p, d, q) and corresponding RMSE, AIC, and BIC.
    """
    results = {}

    # Check if data is sufficient
    if len(data) < train_size + compare_size:
        raise ValueError("Not enough data for the specified train_size and compare_size.")

    # True y (evaluation set)
    y_true = data.iloc[train_size:train_size + compare_size]

    # Iterate over p, d, q
    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                if (p, d, q) == (0, 0, 0):  # Skip (0, 0, 0)
                    continue
                
                print(f"Trying ARIMA({p}, {d}, {q})...")
                
                # Track errors and model metrics
                convergence_error = stationarity_error = 0
                y_pred = []
                aic, bic = [], []

                # Sliding window for evaluation
                for T in range(train_size, train_size + compare_size):
                    train_set = data.iloc[max(0, T - train_size):T]
                    
                    # Skip if train_set is too small
                    if len(train_set) < train_size:
                        continue
                    
                    try:
                        # Fit ARIMA model
                        model = ARIMA(train_set, order=(p, d, q)).fit()
                        
                        # Forecast one step ahead
                        forecast = model.forecast(steps=1)
                        y_pred.append(forecast.iloc[0])

                        # Collect AIC and BIC
                        aic.append(model.aic)
                        bic.append(model.bic)
                    
                    except (LinAlgError, ValueError):
                        convergence_error += 1
                        break

                # Skip if no valid predictions
                if len(y_pred) == 0:
                    continue

                # Calculate RMSE
                result = pd.DataFrame({'y_true': y_true[:len(y_pred)], 'y_pred': y_pred}).dropna()
                rmse = np.sqrt(mean_squared_error(result['y_true'], result['y_pred']))
                
                # Store results
                results[(p, d, q)] = [rmse, np.mean(aic) if aic else np.inf, np.mean(bic) if bic else np.inf]

    # Compile results into a DataFrame
    results_df = pd.DataFrame(results).T
    results_df.columns = ['RMSE', 'AIC', 'BIC']
    results_df.index.names = ['p', 'd', 'q']
    
    return results_df.sort_values("RMSE")


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
