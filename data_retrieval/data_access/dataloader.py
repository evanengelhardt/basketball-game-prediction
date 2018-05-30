from __future__ import division  # floating point division
import numpy as np
from main import variables as var



# Main load functions
def load_games(train_size=100, test_size=40, raw_data=None):
    parsed_data = convert_data_set(raw_data)
    train_set, test_set, favorite_set = split_dataset(parsed_data, train_size, test_size)
    return train_set, test_set, favorite_set


# Helper functions
def split_dataset(data_set, train_size, test_size):
    """
    Splits the data_set into a train and test split
    """
    # Generate random indices without replacement, to make train and test sets disjoint
    rand_indices = np.random.choice(data_set.shape[0], train_size+test_size, replace=False)
    feature_end = data_set.shape[1] - 1
    output_location = feature_end
    feature_offset = var.ALGORITHM_INFO['feature_offset']

    # Define the training and testing matrices
    x_train = data_set[rand_indices[0:train_size], feature_offset:feature_end]
    y_train = data_set[rand_indices[0:train_size], output_location]
    x_test = data_set[rand_indices[train_size:train_size+test_size], feature_offset:feature_end]
    y_test = data_set[rand_indices[train_size:train_size+test_size], output_location]
    favorite_test = data_set[rand_indices[train_size:train_size+test_size], 0]

    # Normalize features, with maximum value in training set
    # as realistically, this would be the only possibility

    for ii in range(x_train.shape[1]):
        maxval = np.max(np.abs(x_train[:, ii]))
        if maxval > 0:
            x_train[:, ii] = np.divide(x_train[:, ii], maxval)
            x_test[:, ii] = np.divide(x_test[:, ii], maxval)


    # Add a column of ones; done after to avoid modifying entire data_set
    x_train = np.hstack((x_train, np.ones((x_train.shape[0], 1))))
    x_test = np.hstack((x_test, np.ones((x_test.shape[0], 1))))

    return (x_train, y_train), (x_test, y_test), favorite_test

def convert_data_set(raw_data):
    for i in range(len(raw_data)):
        raw_data[i] = np.asarray(raw_data[i])
    raw_data = np.asarray(raw_data)

    return raw_data
