import numpy as np
from lstm_network.util import Logger
import KTimage
import os
from lstm_network import util


class NeuralLayer(object):
    """Simple perceptron layer with weight matrix"""
    def __init__(self, in_size, out_size, activation_fn, activation_fn_deriv):
        util.Logger.debug("create Neural Layer: \n" + \
                          "  in_size: " + str(in_size) + "\n" + \
                          "  out_size: " + str(out_size))
        # initialize weight matrix
        self.weights = np.random.uniform(-0.001, 0.001, (out_size, in_size)).astype(np.float64)
        # set biases if not already set (by child class for example)
        if not hasattr(self, 'biases'):
            self.biases = np.zeros(out_size).astype(np.float64)
        # set activation function and derivate
        self.activation = activation_fn
        self.activation_deriv = activation_fn_deriv
        # set size and input size
        self.size = out_size
        self.in_size = in_size

    def feed(self, input_data):
        # calculate activation of layer for given inputs
        return self.activation(np.dot(self.weights, input_data) + np.atleast_2d(self.biases).T)

    def learn(self, result, delta, learning_rate):
        # apply learning rule
        delta_weights = learning_rate * np.outer(delta, result)
        self.weights += delta_weights

    def get_delta(self, result, last_delta, last_weights):
        """calculate delta for layer before"""
        Logger.debug("delta shape: " + str(np.shape(last_delta)) + " - result shape: " + str(np.shape(result)) + " - weights shape: " + str(np.shape(self.weights)))
        last_weights = np.atleast_2d(last_weights)
        return np.dot(last_delta, last_weights) * self.activation_deriv(result)

    def save(self, path):
        """save weights and biases to path"""
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        np.savez(path, weights=self.weights, biases=self.biases)

    def load(self, path):
        """load weights and biases from path"""
        np_saved = np.load(path)
        self.weights = np_saved['weights']
        self.biases = np_saved['biases']

    def visualize(self, path, idx):
        """create visualization for weights at <path>"""
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        #KTimage.exporttiles(self.biases, self.size, 1, path + "B_" + str(idx) + ".pgm")
        KTimage.exporttiles(self.weights, self.in_size,
                            1, path + "W" + str(idx) + "_0.pgm", 1, self.size)

    @classmethod
    def activation_linear(cls, x):
        return x

    @classmethod
    def activation_linear_deriv(cls, x):
        return 1

    @classmethod
    def activation_sigmoid(cls, x):
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))

    @classmethod
    def activation_sigmoid_deriv(cls, x):
        return (1. - x) * x

    @classmethod
    def activation_tanh(cls, x):
        return np.tanh(x)

    @classmethod
    def activation_tanh_deriv(cls, x):
        return 1.0 - x ** 2


class BiasedNeuralLayer(NeuralLayer):
    """Neural Layer with biases"""
    def learn(self, result, delta, learning_rate):
        super(BiasedNeuralLayer, self).learn(result, delta, learning_rate)
        self.biases += learning_rate * delta
