from __future__ import division  # floating point division
import numpy as np


# Main load functions
def load_games(train_size=100, test_size=40):
    filename = 'practice-nba-games.csv'
    data_set = np.genfromtxt(filename, delimiter=',')
    train_set, test_set = split_dataset(data_set, train_size, test_size)
    return train_set, test_set


# Helper functions
def split_dataset(data_set, train_size, test_size):
    """
    Splits the data_set into a train and test split
    """
    # Generate random indices without replacement, to make train and test sets disjoint
    rand_indices = np.random.choice(data_set.shape[0], train_size+test_size, replace=False)
    feature_end = data_set.shape[1]
    output_location = feature_end
    feature_offset = 0

    # Define the training and testing matrices
    x_train = data_set[rand_indices[0:train_size], feature_offset:feature_end]
    y_train = data_set[rand_indices[0:train_size], output_location]
    x_test = data_set[rand_indices[train_size:train_size+test_size], feature_offset:feature_end]
    y_test = data_set[rand_indices[train_size:train_size+test_size], output_location]

    # Normalize features, with maximum value in training set
    # as realistically, this would be the only possibility
    """
    for ii in range(x_train.shape[1]):
        maxval = np.max(np.abs(x_train[:, ii]))
        if maxval > 0:
            x_train[:, ii] = np.divide(x_train[:, ii], maxval)
            x_test[:, ii] = np.divide(x_test[:, ii], maxval)
    """

    # Add a column of ones; done after to avoid modifying entire data_set
    x_train = np.hstack((x_train, np.ones((x_train.shape[0], 1))))
    x_test = np.hstack((x_test, np.ones((x_test.shape[0], 1))))

    return (x_train, y_train), (x_test, y_test)

