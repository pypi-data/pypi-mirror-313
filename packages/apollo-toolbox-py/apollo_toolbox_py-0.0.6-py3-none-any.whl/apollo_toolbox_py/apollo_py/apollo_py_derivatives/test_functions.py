import jax.numpy as jnp
from jax import random, nn
import jax
import numpy as np


def random_vector(n: int, low: float, high: float):
    return np.random.uniform(low, high, n)


class MatrixMultiply:
    def __init__(self, matrix):
        self.matrix = jnp.array(matrix)
        self.f = jax.jit(self._call_internal)

    @staticmethod
    def new_random(m: int, n: int, seed: int):
        key = random.PRNGKey(seed)
        random_matrix = random.uniform(key, (m, n))
        return MatrixMultiply(random_matrix)

    def _call_internal(self, x):
        return self.matrix @ jnp.array(x)

    def call(self, x):
        return self.f(x)


class SimpleNeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim, params):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.params = params
        self.f = jax.jit(self._call_internal)

    @staticmethod
    def initialize_params(input_dim, hidden_dim, output_dim, seed):
        key = random.PRNGKey(seed)
        keys = random.split(key, 11)  # 10 hidden layers + 1 output layer

        params = []
        # Initialize hidden layers
        for i in range(10):
            weight = random.uniform(keys[i], (input_dim, hidden_dim))
            bias = random.uniform(keys[i], (hidden_dim,))
            params.append((weight, bias))
            input_dim = hidden_dim  # Update input_dim for the next layer

        # Initialize output layer
        output_weight = random.uniform(keys[-1], (hidden_dim, output_dim))
        output_bias = random.uniform(keys[-1], (output_dim,))
        params.append((output_weight, output_bias))

        return params

    @staticmethod
    def new_random(input_dim, hidden_dim, output_dim, seed):
        params = SimpleNeuralNetwork.initialize_params(input_dim, hidden_dim, output_dim, seed)
        return SimpleNeuralNetwork(input_dim, hidden_dim, output_dim, params)

    def _call_internal(self, x):
        output = jnp.array(x)
        if output.ndim == 1:
            output = output[jnp.newaxis, :]  # Convert to 2D array

        for weight, bias in self.params[:-1]:  # Apply hidden layers
            output = nn.sigmoid(jnp.dot(output, weight) + bias)

        # Apply output layer (no activation function)
        output_weight, output_bias = self.params[-1]
        output = jnp.dot(output, output_weight) + output_bias
        return jnp.array(output)

    def call(self, x):
        return self.f(x)
