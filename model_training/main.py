import joblib
import os
import numpy as np
import pandas as pd
import glob
import sklearn
print("scikit-learn version:", sklearn.__version__)

import helper_functions

# Define variables
k_fold_splits = 6
num_estimators = 64
max_leaf_nodes = 1500
max_depth = 25
verbose = 1

# Get the file containing the processed data, and convert the CSV file into a dataframe
file_name = "train.csv"
train_df = pd.read_csv(file_name)

# Split the dataset into labels and input features.
# The labels in this case would be the estimated time for the ship to make its trip, in the first column
# All remaining columns would be the input features for the model
y = train_df.iloc[:, 0].values
X = train_df.iloc[:, 1:].values

# Train the model
helper_functions.train(X, y, k_fold_splits, num_estimators, max_leaf_nodes, max_depth, verbose)