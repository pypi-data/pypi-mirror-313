
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import scipy.stats as stats
import seaborn as sns
from tqdm import notebook
import itertools
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import pandas as pd
import numpy as np
# import warnings
# warnings.filterwarnings('ignore')

from tqdm import notebook
import itertools
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
def fit_linear_reg(X,Y):
    #Fit linear regression model and return SSE and R squared values
    model_k = sm.OLS(Y,sm.add_constant(X)).fit()
    SSE = mean_squared_error(Y,model_k.predict(sm.add_constant(X))) * len(Y)
    RMSE=np.sqrt(SSE/len(X)-1-X.shape[1])
    R_squared = model_k.rsquared
    adj_R2 = model_k.rsquared_adj
    AIC = model_k.aic
    BIC = model_k.bic
    return RMSE, R_squared, adj_R2, AIC, BIC






def visual_best_allinone(df_s1):
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Best subset using Adjusted R2, Cp, AIC, BIC', fontsize=16)

    fig.add_subplot(2, 2, 1)
    visual_stage2_result(df_s1, 'Adj_R2')
    fig.add_subplot(2, 2, 2)
    visual_stage2_result(df_s1, 'C_p')
    fig.add_subplot(2, 2, 3)
    visual_stage2_result(df_s1, 'AIC')
    fig.add_subplot(2, 2, 4)
    visual_stage2_result(df_s1, 'BIC')


def best_subset_init(X, Y):
    k = X.shape[1]
    SSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list, feature_list, Cp_list = [], [], [], [], [], [], []
    numb_features = []

    m = len(Y)
    p = X.shape[1]
    full_model_sse = fit_linear_reg(X, Y)[0]
    hat_sigma_squared = (1 / (m - p - 1)) * full_model_sse

    # Looping over k = 1 to k = 11 features in X
    for k in notebook.trange(1, len(X.columns) + 1, desc='Loop...'):

        # Looping over all possible combinations: from 11 choose k
        for combo in itertools.combinations(X.columns, k):
            tmp_result = fit_linear_reg(X[list(combo)], Y)  # Store temp result
            SSE_list.append(tmp_result[0])  # Adds its argument as a single element to the end of a list.
            R_squared_list.append(tmp_result[1])
            adj_R2_list.append(tmp_result[2])
            AIC_list.append(tmp_result[3])
            BIC_list.append(tmp_result[4])
            feature_list.append(combo)
            numb_features.append(len(combo))
            temp_cp = (1 / m) * (tmp_result[0] + 2 * len(combo) * hat_sigma_squared)
            Cp_list.append(temp_cp)

            # Store in DataFrame
    df = pd.DataFrame(
        {'numb_features': numb_features, 'SSE': SSE_list, 'R_squared': R_squared_list, 'Adj_R2': adj_R2_list,
         'AIC': AIC_list, 'BIC': BIC_list, 'C_p': Cp_list, 'features': feature_list})
    return df


def best_subset_stage1(df):
    df_s1 = df[df.groupby('numb_features')['SSE'].transform(min) == df['SSE']]

    return df_s1


def best_subset_stage2(df_s1, criteria):
    objective_list = {'SSE': 'min', 'R_squared': 'max', 'Adj_R2': 'max',
                      'AIC': 'min', 'BIC': 'min', 'C_p': 'min'}
    if objective_list.get(criteria) == 'min':
        X_feature = list(df_s1.loc[df_s1[criteria].idxmin(), 'features'])
    else:
        X_feature = list(df_s1.loc[df_s1[criteria].idxmax(), 'features'])

    return X_feature


def best_subset_stage2_all(df_s1):
    # criteria_list=['Adj_R2','AIC','BIC','C_p']
    # table=[best_subset_stage2(df_s1,c) for c in criteria_list]
    table_a = pd.DataFrame({'Adj_R2': list(best_subset_stage2(df_s1, 'Adj_R2'))})
    table_b = pd.DataFrame({'AIC': list(best_subset_stage2(df_s1, 'AIC'))})
    table_c = pd.DataFrame({'BIC': list(best_subset_stage2(df_s1, 'BIC'))})
    table_d = pd.DataFrame({'C_p': list(best_subset_stage2(df_s1, 'C_p'))})

    return table_a.join(table_b).join(table_c).join(table_d)


def visual_stage1_result(df, criteria):
    if criteria == 'SSE':
        visual_stage1_result_bySSE(df)
    else:
        visual_stage1_result_byR2(df)


def visual_stage1_result_bySSE(df):
    # using scatter plot to show all the models
    plt.scatter(df.numb_features, df.SSE, alpha=.2, color='darkblue')
    plt.xlabel('# Features')
    plt.ylabel('SSE')
    plt.title('SSE - Best subset selection')
    # outline the candidate models of stage 1
    df_min = df[df.groupby('numb_features')['SSE'].transform(min) == df['SSE']]
    plt.plot(df_min.numb_features, df_min.SSE, color='r', label='Best subset')
    plt.legend()


def visual_stage1_result_byR2(df):
    df_max = df[df.groupby('numb_features')['R_squared'].transform(max) == df['R_squared']]
    plt.scatter(df.numb_features, df.R_squared, alpha=.2, color='darkblue')
    plt.plot(df_max.numb_features, df_max.R_squared, color='r', label='Best subset')
    plt.xlabel('# Features')
    plt.ylabel('R squared')
    plt.title('R_squared - Best subset selection')
    plt.legend()


def visual_stage2_result(df_s1, criteria):
    objective_list = {'SSE': 'min', 'R_squared': 'max', 'Adj_R2': 'max',
                      'AIC': 'min', 'BIC': 'min', 'C_p': 'min', 'MSE_validation': 'min', 'MSE_CV': 'min'}
    if objective_list.get(criteria) == 'min':
        visual_stage2_min(df_s1, criteria)
    else:
        visual_stage2_max(df_s1, criteria)


def visual_stage2_min(df_s1, criteria):
    ylabel_list = {'SSE': 'SSE', 'R_squared': 'R-squared', 'Adj_R2': 'Adj.R-square',
                   'AIC': 'AIC', 'BIC': 'BIC', 'C_p': 'Cp', 'MSE_validation': 'Validation set error (MSE)',
                   'MSE_CV': 'CV error (MSE)'}
    plt.plot(df_s1.numb_features, df_s1[criteria], 'o--', color='darkblue', label='Best subset')
    plt.plot(df_s1.loc[df_s1[criteria].idxmin(), 'numb_features'], df_s1[criteria].min(), marker='x', markersize=20,
             c='r')
    plt.xlabel('# Features')
    plt.ylabel(ylabel_list.get(criteria))
    plt.title(criteria)
    # plt.title(criteria+' - Best subset selection')
    # plt.legend()


def visual_stage2_max(df_s1, criteria):
    ylabel_list = {'SSE': 'SSE', 'R_squared': 'R-squared', 'Adj_R2': 'Adj.R-square',
                   'AIC': 'AIC', 'BIC': 'BIC', 'C_p': 'Cp', 'MSE_validation': 'Validation set error (MSE)',
                   'MSE_CV': 'CV error (MSE)'}
    plt.plot(df_s1.numb_features, df_s1[criteria], 'o--', color='darkblue', label='Best subset')
    plt.plot(df_s1.loc[df_s1[criteria].idxmax(), 'numb_features'], df_s1[criteria].max(), marker='x', markersize=20,
             c='r')
    plt.xlabel('# Features')
    plt.ylabel(ylabel_list.get(criteria))
    plt.title(criteria)
    # plt.title(criteria+' - Best subset selection')
    # plt.legend()


def best_subset_validation(train_set, Y_name, prop, rand_state):
    X = train_set.drop(columns=Y_name)
    Y = train_set[Y_name]

    df = best_subset_init(X, Y)
    df_s1 = best_subset_stage1(df)

    X_feature_validation, df_validation = best_subset_stage2_validation(df_s1, train_set, Y_name, prop, rand_state)
    display(df_validation)

    fig = plt.figure(figsize=(8, 6))
    fig.suptitle('Best subset using validation', fontsize=12)
    visual_stage2_result(df_validation, 'MSE_validation')
    return X_feature_validation


def validation_formation(p, rand_state, data):
    data_copy = data.copy()
    train_subset = data_copy.sample(frac=p, random_state=rand_state)
    validation_set = data_copy.drop(train_subset.index)

    return train_subset, validation_set


def best_subset_stage2_validation(df_s1, train_set, y, prop, rand_state):
    M_list = df_s1['features']

    N_predictor = train_set.shape[1] - 1
    mse_validate_list = []
    train_subset, validation_set = validation_formation(prop, rand_state, train_set)
    # compute mse for each candidate model
    for i in range(0, N_predictor):
        fit = sm.OLS(train_subset[y], sm.add_constant(train_subset[list(M_list.iloc[i])])).fit()
        mse = mean_squared_error(validation_set[y], fit.predict(sm.add_constant(validation_set[list(M_list.iloc[i])])))
        mse_validate_list.append(mse)

    df_validation = pd.DataFrame(
        {'numb_features': range(1, N_predictor + 1), 'MSE_validation': mse_validate_list, 'features': M_list})
    X_feature_validation = list(df_validation.loc[df_validation['MSE_validation'].idxmin(), 'features'])

    return X_feature_validation, df_validation


def best_subset_CV(train_set, Y_name, K):
    X = train_set.drop(columns=Y_name)
    Y = train_set[Y_name]

    df = best_subset_init(X, Y)
    df_s1 = best_subset_stage1(df)

    X_feature_CV, df_CV = best_subset_stage2_CV(df_s1, train_set, Y_name, K)
    display(df_CV)

    fig = plt.figure(figsize=(8, 6))
    fig.suptitle('Best subset using CV', fontsize=12)
    visual_stage2_result(df_CV, 'MSE_CV')

    return X_feature_CV


def best_subset_stage2_CV(df_s1, train_set, y, K):
    # instantiate model
    lm = LinearRegression()

    M_list = df_s1['features']
    N_predictor = train_set.shape[1] - 1
    mse_CV_list = []

    for i in range(0, N_predictor):
        X_CV = sm.add_constant(train_set[list(M_list.iloc[i])])
        y_CV = train_set[y]
        scores = cross_val_score(lm, X_CV, y_CV, cv=K,
                                 scoring='neg_mean_squared_error')  # inpunt 'cv' is used to control K
        # fix the sign of MSE scores
        mse_scores = -scores
        # calculate the average RMSE
        mse = mse_scores.mean()
        mse_CV_list.append(mse)

    df_CV = pd.DataFrame({'numb_features': range(1, N_predictor + 1), 'MSE_CV': mse_CV_list, 'features': M_list})
    X_feature_CV = list(df_CV.loc[df_CV['MSE_CV'].idxmin(), 'features'])

    return X_feature_CV, df_CV


def visual_stage2_valdiation(df_validation):
    plt.plot(df_validation.numb_features, df_validation.MSE_validation, 'o--', color='darkblue')
    plt.xlabel('# Features')
    plt.ylabel('Validation set error (MSE)')
    plt.title('Validation - Best subset selection')
    plt.plot(df_validation.loc[df_validation['MSE_validation'].idxmin(), 'numb_features'],
             df_validation['MSE_validation'].min(),
             marker='x', markersize=20, c='r')


def visual_stage2_CV(df_CV):
    plt.plot(df_CV.numb_features, df_CV.MSE_CV, 'o--', color='darkblue')
    plt.xlabel('# Features')
    plt.ylabel('CV error (MSE)')
    plt.title('CV - Best subset selection')
    plt.plot(df_CV.loc[df_CV['MSE_CV'].idxmin(), 'numb_features'], df_CV['MSE_CV'].min(),
             marker='x', markersize=20, c='r')


def forward_selection(X, Y):
    df_forward_s1 = forward_selection_stage1(X, Y)
    display(df_forward_s1)

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Forward selection using AIC, BIC, Adjusted R2', fontsize=16)

    fig.add_subplot(2, 2, 1)
    visual_stage2_result(df_forward_s1, 'AIC')
    fig.add_subplot(2, 2, 2)
    visual_stage2_result(df_forward_s1, 'BIC')
    fig.add_subplot(2, 2, 3)
    visual_stage2_result(df_forward_s1, 'Adj_R2')

    X_feature_FD_AIC = forward_selection_stage2(df_forward_s1, 'AIC')
    X_feature_FD_BIC = forward_selection_stage2(df_forward_s1, 'BIC')
    X_feature_FD_Adj_R2 = forward_selection_stage2(df_forward_s1, 'Adj_R2')

    table_a = pd.DataFrame({'Adj_R2': list(forward_selection_stage2(df_forward_s1, 'Adj_R2'))})
    table_b = pd.DataFrame({'AIC': list(forward_selection_stage2(df_forward_s1, 'AIC'))})
    table_c = pd.DataFrame({'BIC': list(forward_selection_stage2(df_forward_s1, 'BIC'))})

    return table_a.join(table_b).join(table_c)


def forward_selection_stage1(X, Y):
    k = X.shape[1]

    remaining_features = list(X.columns.values)
    features = []
    sequence = []
    SSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list, Cp_list = [np.inf], [np.inf], [np.inf], [np.inf], [
        np.inf], [np.inf]  # Due to 1 indexing of the loop...
    features_list = dict()

    m = len(Y)
    p = X.shape[1]
    full_model_sse = fit_linear_reg(X, Y)[0]
    hat_sigma_squared = (1 / (m - p - 1)) * full_model_sse

    for i in range(1, k + 1):
        best_SSE = np.inf

        for combo in itertools.combinations(remaining_features, 1):

            tmp_result = fit_linear_reg(X[list(combo) + features], Y)  # Store temp result

            if tmp_result[0] < best_SSE:
                best_SSE = tmp_result[0]
                best_R_squared = tmp_result[1]
                best_adj_R2 = tmp_result[2]
                best_AIC = tmp_result[3]
                best_BIC = tmp_result[4]
                best_feature = combo[0]
                best_cp = (1 / m) * (tmp_result[0] + 2 * (len(features) + 1) * hat_sigma_squared)

        # Updating variables for next loop
        features.append(best_feature)
        remaining_features.remove(best_feature)
        sequence.append(best_feature)

        # Saving values for plotting
        SSE_list.append(best_SSE)
        R_squared_list.append(best_R_squared)
        adj_R2_list.append(best_adj_R2)
        AIC_list.append(best_AIC)
        BIC_list.append(best_BIC)
        Cp_list.append(best_cp)
        features_list[i] = features.copy()

    result = {'SSE': SSE_list,
              'R_squared': R_squared_list,
              'Adj_R2': adj_R2_list,
              'AIC': AIC_list,
              'BIC': BIC_list,
              'C_p': Cp_list,
              'features': features_list,
              'sequence': sequence}

    df1 = pd.DataFrame({'features': [a for a in features_list.values()],
                        'features added': sequence,
                        'SSE': result['SSE'][1:], 'R_squared': result['R_squared'][1:],
                        'Adj_R2': result['Adj_R2'][1:],
                        'AIC': result['AIC'][1:],
                        'BIC': result['BIC'][1:],
                        'C_p': result['C_p'][1:]
                        })

    df1['numb_features'] = df1.index + 1
    t = ['step ' + str(i) for i in range(1, k + 1)]
    df1.index = t
    df1  # data frame of candidate models from stage 1

    return df1


def forward_selection_stage2(df_s1, criteria):
    X_feature = best_subset_stage2(df_s1, criteria)
    return X_feature


def residual_plot_reference(model, cutoff):
    n = int(model.nobs)
    plt.figure(figsize=[8, 8])
    infl = model.get_influence()
    infl_summary = infl.summary_frame()
    standard_resid = infl_summary["standard_resid"]
    plt.scatter(range(0, n), standard_resid)
    sr_large = cutoff
    plt.axhline(y=sr_large, c="red")
    plt.axhline(y=-sr_large, c="red")

    for i in range(0, n):
        if np.abs(standard_resid[i]) > sr_large:
            plt.annotate(i, (i, standard_resid[i]))

    plt.xlabel("Observation Number")
    plt.ylabel("Standardized residuals")


##############################

def backward_selection(X, Y):
    k = X.shape[1]

    remaining_features = list(X.columns.values)
    SSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list = [], [], [], [], []  # Due to 1 indexing of the loop...

    features_list = dict()

    for i in range(1, k + 1):
        best_SSE = np.inf

        for combo in itertools.combinations(remaining_features, k + 1 - i):

            temp_result = fit_linear_reg(X[list(combo)], Y)  # Store temp result

            if temp_result[0] < best_SSE:
                best_SSE = temp_result[0]
                best_R_squared = temp_result[1]
                best_adj_R2 = temp_result[2]
                best_AIC = temp_result[3]
                best_BIC = temp_result[4]
                best_feature = combo

        # Updating variables for next loop
        remaining_features = best_feature

        # Saving values for plotting
        SSE_list.append(best_SSE)
        R_squared_list.append(best_R_squared)
        adj_R2_list.append(best_adj_R2)
        AIC_list.append(best_AIC)
        BIC_list.append(best_BIC)
        features_list[i] = best_feature

    result = {'SSE': SSE_list,
              'R_squared': R_squared_list,
              'adj_R2': adj_R2_list,
              'AIC': AIC_list,
              'BIC': BIC_list,
              'features': features_list}

    return result


def stepwise_selection(X, y,
                       initial_list=[],
                       threshold_in=0.01,
                       threshold_out=0.05,
                       verbose=True):
    """ Perform a forward-backward feature selection
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features
    Always set threshold_in < threshold_out to avoid infinite looping.
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    included = list(initial_list)
    while True:
        changed = False
        # forward step
        excluded = list(set(X.columns) - set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included + [new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed = True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max()  # null if pvalues is empty
        if worst_pval > threshold_out:
            changed = True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included


def best_subset_selection(X, Y):
    k = X.shape[1]
    RMSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list, feature_list = [], [], [], [], [], []
    numb_features = []

    # Looping over k = 1 to k = 11 features in X
    for k in notebook.trange(1, len(X.columns) + 1, desc='Loop...'):

        # Looping over all possible combinations: from 11 choose k
        for combo in itertools.combinations(X.columns, k):
            tmp_result = fit_linear_reg(X[list(combo)], Y)  # Store temp result
            RMSE_list.append(tmp_result[0])  # Adds its argument as a single element to the end of a list.
            R_squared_list.append(tmp_result[1])
            adj_R2_list.append(tmp_result[2])
            AIC_list.append(tmp_result[3])
            BIC_list.append(tmp_result[4])
            feature_list.append(combo)
            numb_features.append(len(combo))

            # Store in DataFrame
    df = pd.DataFrame(
        {'numb_features': numb_features, 'RMSE': RMSE_list, 'R_squared': R_squared_list, 'adj_R2': adj_R2_list,
         'AIC': AIC_list, 'BIC': BIC_list, 'features': feature_list})
    return df

def forward_selection(X, Y):
    k = X.shape[1]

    remaining_features = list(X.columns.values)
    features = []
    SSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list = [np.inf], [np.inf], [np.inf], [np.inf], [np.inf]  # Due to 1 indexing of the loop...
    features_list = dict()

    for i in range(1, k + 1):
        best_SSE = np.inf

        for combo in itertools.combinations(remaining_features, 1):

            tmp_result = fit_linear_reg(X[list(combo) + features], Y)  # Store temp result

            if tmp_result[0] < best_SSE:
                best_SSE = tmp_result[0]
                best_R_squared = tmp_result[1]
                best_adj_R2 = tmp_result[2]
                best_AIC = tmp_result[3]
                best_BIC = tmp_result[4]
                best_feature = combo[0]

        # Updating variables for next loop
        features.append(best_feature)
        remaining_features.remove(best_feature)

        # Saving values for plotting
        SSE_list.append(best_SSE)
        R_squared_list.append(best_R_squared)
        adj_R2_list.append(best_adj_R2)
        AIC_list.append(best_AIC)
        BIC_list.append(best_BIC)
        features_list[i] = features.copy()

    result = {'SSE': SSE_list,
              'R_squared': R_squared_list,
              'adj_R2': adj_R2_list,
              'AIC': AIC_list,
              'BIC': BIC_list,
              'features': features_list}

    return result

def backward_selection(X, Y):
    k = X.shape[1]

    remaining_features = list(X.columns.values)
    SSE_list, R_squared_list, adj_R2_list, AIC_list, BIC_list = [], [], [], [], []  # Due to 1 indexing of the loop...

    features_list = dict()

    for i in range(1, k + 1):
        best_SSE = np.inf

        for combo in itertools.combinations(remaining_features, k + 1 - i):

            temp_result = fit_linear_reg(X[list(combo)], Y)  # Store temp result

            if temp_result[0] < best_SSE:
                best_SSE = temp_result[0]
                best_R_squared = temp_result[1]
                best_adj_R2 = temp_result[2]
                best_AIC = temp_result[3]
                best_BIC = temp_result[4]
                best_feature = combo

        # Updating variables for next loop
        remaining_features = best_feature

        # Saving values for plotting
        SSE_list.append(best_SSE)
        R_squared_list.append(best_R_squared)
        adj_R2_list.append(best_adj_R2)
        AIC_list.append(best_AIC)
        BIC_list.append(best_BIC)
        features_list[i] = best_feature

    result = {'SSE': SSE_list,
              'R_squared': R_squared_list,
              'adj_R2': adj_R2_list,
              'AIC': AIC_list,
              'BIC': BIC_list,
              'features': features_list}

    return result

def stepwise_selection(X, y,
                       initial_list=[],
                       threshold_in=0.01,
                       threshold_out = 0.05,
                       verbose=True):
    """ Perform a forward-backward feature selection
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features
    Always set threshold_in < threshold_out to avoid infinite looping.
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    included = list(initial_list)
    while True:
        changed=False
        # forward step
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed=True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty
        if worst_pval > threshold_out:
            changed=True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included
def outlier(dataframe,model,cutoff="2",Type='all'):
    A = dataframe.copy()
    studentized_residuals = model.get_influence().resid_studentized_internal
    A["Studentized Residuals"] =studentized_residuals
    A["ExpectProfit"] = model.fittedvalues
    if Type == 'neg':
        return(A[["Location","ExpectProfit","Profit","Studentized Residuals"]][studentized_residuals<-cutoff])
    elif Type == 'posi':
        return(A[["Location","ExpectProfit","Profit","Studentized Residuals"]][studentized_residuals>cutoff])
    else:
        return(A[["Location","ExpectProfit","Profit"]][np.abs(studentized_residuals)<cutoff])

def getvif(X):
    X = sm.add_constant(X)
    vif = pd.DataFrame()
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["Predictors"] = X.columns
    return(vif.drop(index = 0).round(2))
def residual_plot(model):
    fitted_y = model.fittedvalues
    studentized_residuals = model.get_influence().resid_studentized_internal
    plt.figure(figsize=(10,10))
    ax1 = plt.subplot(221)
    stats.probplot(studentized_residuals, dist="norm", plot=plt)
    ax1.set_title('Normal Q-Q')
    ax1.set_xlabel('Normal Quantiles')
    ax1.set_ylabel('Studentized Residuals');

    ax2 = plt.subplot(222)
    ax2.hist(studentized_residuals)
    ax2.set_xlabel('Studentized Residuals')
    ax2.set_ylabel('Count')
    ax2.set_title('Histogram')

    ax3 = plt.subplot(223)
    t = range(len(fitted_y))
    ax3.scatter(t, studentized_residuals)
    ax3.set_xlabel('Observation order')
    ax3.set_ylabel('Residuals')
    ax3.set_title('Time series plot of residuals')

    ax4 = plt.subplot(224)
    ax4 = sns.residplot(x=fitted_y, y=studentized_residuals,
                              lowess=True,
                              scatter_kws={'alpha': 0.5},
                              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
    ax4.set_title('Studentized Residuals vs Fitted values')
    ax4.set_xlabel('Fitted values')
    ax4.set_ylabel('Studentized Residuals');