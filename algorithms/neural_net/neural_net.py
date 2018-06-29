import random
import numpy as np
from main import global_functions as global_fn

class NeuralNet(object):

    def __init__(self, sizes):
        print("Initializing Neural Net")
        """
        :param sizes: An array of ints. Index represents layer,
                number represents number of nodes
        : Sets num_layers and sizes according to input,
                sets biases and weights randomly according to the dimensions of sizes
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feed_forward(self, x):
        # Output of sigmoid neurons
        for b, w in zip(self.biases, self.weights):
            x = global_fn.sigmoid(np.dot(w, x) + b)
        return x


    def stoch_grad(self, training_data, epochs, batch_size, learn,
                   lmbda=0.0,
                   test_data=None):
        n = len(training_data[0])
        ref_index = np.arange(n)
        evaluation_accuracy = []
        training_accuracy = []
        for i in range(epochs):
            random.shuffle(ref_index)
            batches = [ref_index[k:k+batch_size] for k in range(0,n,batch_size)]
            for batch in batches:
                self.update_batch(batch, learn, lmbda, n, training_data)
            print("Epoch %s training complete" % i)

            accuracy = self.accuracy(training_data)
            training_accuracy.append(accuracy)
            print("Accuracy on training data: {} / {}".format(accuracy, n))

            if test_data:
                n_data = len(test_data)
                accuracy = self.accuracy(test_data)
                evaluation_accuracy.append(accuracy)
                print("Accuracy on evaluation data: {} / {}".format(
                    accuracy, n_data))

        return evaluation_accuracy[-1]



    def update_batch(self, mini_batch, learn, lmbda, n, training_data):
        gradient_w = [np.zeros(w.shape) for w in self.weights]
        gradient_b = [np.zeros(b.shape) for b in self.biases]

        for i in range(len(mini_batch)):
            x, y = training_data[0][i], training_data[1][i]
            delta_grad_b, delta_grad_w = self.back_prop(x,y)
            gradient_b = [gb + dgb for gb, dgb in zip(gradient_b, delta_grad_b)]
            gradient_w = [gw + dgw for gw, dgw in zip(gradient_w, delta_grad_w)]

        self.weights = [(1-learn*(lmbda/n))*w - (learn/len(mini_batch))*gw
                        for w, gw in zip(self.weights, gradient_w)]
        self.biases = [b-(learn/len(mini_batch))*gb
                       for b, gb in zip(self.biases, gradient_b)]

    def back_prop(self, x, y):
        gradient_w = [np.zeros(w.shape) for w in self.weights]
        gradient_b = [np.zeros(b.shape) for b in self.biases]
        current_act = x
        activations = [x]
        zs = []

        # Feed Forward
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, current_act) + b
            zs.append(z)
            current_act = global_fn.sigmoid(z)[0]
            activations.append(current_act)

        # Calculate Gradients
        # Using cross entropy cost
        delta = 0
        for a in activations[-1]:
            delta += a - y
        delta /= len(activations[-1])
        gradient_b[-1] = delta
        gradient_w[-1] = np.dot(delta, activations[-2].transpose())

        # TODO - Figure out matrix dimensions for proper multiplication
        # Back prop through rest of layers
        for l in range(2, self.num_layers):
            z = zs[-l]
            sig_prime = global_fn.sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sig_prime
            gradient_b[-l] = delta
            gradient_w[-l] = np.dot(delta, activations[-l-1].transpose())

        return gradient_b, gradient_w

    def accuracy(self, data):
        results = []
        for x, y in data:
            activation =  self.feed_forward(x)
            if activation > .5:
                activation = 1
            else:
                activation = 0

            results.append([activation, y])

        return sum(int(x==y) for (x,y) in results)