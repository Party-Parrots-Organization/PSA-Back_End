import joblib
import numpy as np
import pandas as pd
import os
import sklearn
print("scikit-learn version:", sklearn.__version__)

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

def train(X, y, k_fold_splits, num_estimators, max_leaf_nodes, max_depth, verbose):
    kf = KFold(n_splits=k_fold_splits, shuffle=True, random_state=42)
    best = 0
    iteration = 0

    print(kf)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        print("Training has begun")

        # Instantiate the model for this training iteration
        model = RandomForestRegressor(
            n_estimators=num_estimators, verbose=verbose, n_jobs=-1, criterion='squared_error',
            max_leaf_nodes=max_leaf_nodes, max_features='sqrt', max_depth=max_depth, random_state=0
        )
        model.fit(X_train, y_train)
        
        print("Computing scores")
        # Print evaluation metrics
        train_score = r2_score(y_train, model.predict(X_train))
        test_score = r2_score(y_test, model.predict(X_test))
        print("Iteration=%d; train_r2=%f; test_r2=%f;" % (iteration, train_score, test_score))

        # Save the model if it performed better on the test data
        if test_score > best:
            best = test_score
            print("Saving checkpoint for best model: best_r2=%f;" % best)
            joblib.dump(model, os.path.join("output", "best_model.joblib"))
        iteration += 1

    print("\nBest model: best_r2=%f;" % best)
    model = joblib.load(os.path.join("output", "best_model.joblib"))
    joblib.dump(model, os.path.join("model_dir", "model.joblib"))