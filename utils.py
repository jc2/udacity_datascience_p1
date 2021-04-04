from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error


def count_options(column):
    count = defaultdict(lambda: 0)
    for options in (row.split('; ') for row in column):
        for option in options:
            count[option] += 1
    return count

def imputing_data(df, y_column):

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

def find_optimal_lm_mod(X, y, cutoffs, test_size = .30, random_state=42, plot=True):
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