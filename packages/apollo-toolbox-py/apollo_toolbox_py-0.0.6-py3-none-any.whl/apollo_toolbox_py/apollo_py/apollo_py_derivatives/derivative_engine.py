from enum import Enum
import numpy as np
import jax.numpy as jnp

class FunctionMode(Enum):
    Numpy = 1,
    Jax = 2


class JitCompileMode(Enum):
    DoNotJitCompile = 1,
    Jax = 2
    Numba = 3


class ADMode(Enum):
    Forward = 1,
    Reverse = 2


class DerivativeEngine:
    def __init__(self, f, n: int, m: int):
        self.f = f
        self.n = n
        self.m = m

    def call_numpy(self, x) -> np.ndarray:
        return np.array(self.f(np.array(x)))

    def call_jax(self, x):
        return jnp.array(self.f(jnp.array(x)))

    def derivative(self, x) -> np.ndarray:
        raise NotImplemented("This must be implemented in subclass")
