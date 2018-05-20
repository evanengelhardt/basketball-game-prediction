import numpy as np

class LogisticRegression:

    def __init__(self):
        self.weights = None

    def learn(self, x_train, y_train, epochs, init_wgt, learn_step, sample_size):
        self.weights = self.weight_learner(x_train, y_train, epochs, init_wgt, learn_step, sample_size)

    def predict(self, x_test):
        y_test = np.dot(x_test, self.weights)
        for i in range(len(y_test)):
            if self.sigmoid(y_test[i]) > .5:
                y_test[i] = 1
            else:
                y_test[i] = 0

        return y_test

    # Uses stochastic along with logistic regression
    def weight_learner(self, x_train, y_train, epochs, init_wgt, learn_step, sample_size):
        est_w = [init_wgt for i in range(len(x_train[0]))]

        for epoch in range(epochs):
            # create random order for testing
            random_order = list(range(len(x_train)))
            np.random.shuffle(random_order)
            sample_count = 0
            for i in random_order:
                if sample_count < sample_size:
                    y_est = self.estimation_helper(x_train[i], est_w)
                    err = y_est - y_train[i]

                    for n in range(len(x_train[i])):
                        est_w[n] -= learn_step * err * x_train[i][n]

                    sample_count += 1
                else:
                    break
        return est_w

    def estimation_helper(self, data_point, curr_wgt):
        y_est = 0
        for i in range(len(data_point)):
            y_est += data_point[i]*curr_wgt[i]
        return self.sigmoid(y_est)

    def sigmoid(self, var):
        if type(var) is list:
            var[var < -100] = -100
            var[var > 100] = 100

        return 1.0 / (1.0 + np.exp(np.negative(var)))
