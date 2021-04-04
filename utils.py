from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


def count_options(column):
    '''
    INPUT
    column - Column to be analized

    OUTPUT
    count - a dictionary with the options in the column an the number of occurencies

    This function will count all the different options in multi-options columns (splited by a ;)
    and then it will count the occurrences for each option
    '''
    count = defaultdict(lambda: 0)
    for options in (row.split('; ') for row in column):
        for option in options:
            count[option] += 1
    return count

def imputing_data(df, y_column):
    '''
    INPUT
    df - Data Frame with all information that is going to be used to train and test our model
    y_column - The column that will be used as expected output for our linear model

    OUTPUT
    X - A Data Frame with the input information for our linear model
    Y - A Serie with the output information for our linuear model

    This funtion will try to prepare the information to be used in linear models.
    In this case it will handle NAN quantitative data with the mean and it will normalize
    the values
    For NAN Categorical data, it will apply a "dummy" strategy. 
    '''

    print(f"initial shape: {df.shape}")
    df = df.dropna(subset=[y_column], axis=0)
    print(f"Shape without NAN {y_column}: {df.shape}")
    
    y = df[y_column]
    
    X = df.drop([y_column,], axis=1)
    print(f"Shape without unnecessary columns: {X.shape}")

    num_vars = X.select_dtypes(include=['float', 'int']).columns
    print(f"Quantitative columns: {num_vars}")
    for c in num_vars:
        X[c].fillna((X[c].mean()), inplace=True)
        X[c] = (X[c] - X[c].min()) / (X[c].max() - X[c].min())
    
    print(f"Shape after imputing quantitative data: {X.shape}")
        
    cat_vars = df.select_dtypes(include=['object']).columns
    print(f"Categorical columns: {cat_vars}")
    for c in  cat_vars:
        dummies = pd.get_dummies(X[c], prefix=c, prefix_sep='_', drop_first=True)
        X = X.drop(c, axis=1)
        X = pd.concat([X, dummies], axis=1)
    
    print(f"Shape after imputing categorical data: {X.shape}")
    
    return X, y

# I have copied this function from Udacity Datascience nanodegree program
def find_optimal_lm_mod(X, y, cutoffs, test_size = .30, random_state=42, plot=True):
    '''
    INPUT
    X - pandas dataframe, X matrix
    y - pandas dataframe, response variable
    cutoffs - list of ints, cutoff for number of non-zero values in dummy categorical vars
    test_size - float between 0 and 1, default 0.3, determines the proportion of data as test data
    random_state - int, default 42, controls random state for train_test_split
    plot - boolean, default 0.3, True to plot result

    OUTPUT
    r2_scores_test - list of floats of r2 scores on the test data
    r2_scores_train - list of floats of r2 scores on the train data
    lm_model - model object from sklearn
    X_train, X_test, y_train, y_test - output from sklearn train test split used for optimal model
    '''
    r2_scores_test, r2_scores_train, num_feats, results = [], [], [], dict()
    for cutoff in cutoffs:

        #reduce X matrix
        reduce_X = X.iloc[:, np.where((X.sum() > cutoff) == True)[0]]
        num_feats.append(reduce_X.shape[1])

        #split the data into train and test
        X_train, X_test, y_train, y_test = train_test_split(reduce_X, y, test_size = test_size, random_state=random_state)

        #fit the model and obtain pred response
        lm_model = LinearRegression(normalize=True)
        lm_model.fit(X_train, y_train)
        y_test_preds = lm_model.predict(X_test)
        y_train_preds = lm_model.predict(X_train)

        #append the r2 value from the test set
        r2_scores_test.append(r2_score(y_test, y_test_preds))
        r2_scores_train.append(r2_score(y_train, y_train_preds))
        results[str(cutoff)] = r2_score(y_test, y_test_preds)

    if plot:
        plt.plot(num_feats, r2_scores_test, label="Test", alpha=.5)
        plt.plot(num_feats, r2_scores_train, label="Train", alpha=.5)
        plt.xlabel('Number of Features')
        plt.ylabel('Rsquared')
        plt.title('Rsquared by Number of Features')
        plt.legend(loc=1)
        plt.show()

    best_cutoff = max(results, key=results.get)

    #reduce X matrix
    reduce_X = X.iloc[:, np.where((X.sum() > int(best_cutoff)) == True)[0]]
    num_feats.append(reduce_X.shape[1])

    #split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(reduce_X, y, test_size = test_size, random_state=random_state)

    #fit the model
    lm_model = LinearRegression(normalize=True)
    lm_model.fit(X_train, y_train)

    return r2_scores_test, r2_scores_train, lm_model, X_train, X_test, y_train, y_test