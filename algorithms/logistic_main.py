import data_retrieval.dataloader as data
from algorithms.logistic_regression import LogisticRegression
import numpy as np


def getaccuracy(y_test, predictions):
    correct = 0
    for i in range(len(y_test)):
        if y_test[i] == predictions[i]:
            correct += 1
    return (correct / float(len(y_test))) * 100.0


def geterror(ytest, predictions):
    return 100.0-getaccuracy(ytest, predictions)

trainset, testset = data.load_games(4000, 2000)

print("Running logistic regression on file\n")

log_reg = LogisticRegression()

log_reg.learn(x_train=trainset[0], y_train=trainset[1], epochs=100, init_wgt=1, learn_step=.3, sample_size=2000)

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(log_reg.weights)

predictions = log_reg.predict(testset[0])
error = geterror(testset[1], predictions)

print('Error for Logistic Regression: ' + str(error))
