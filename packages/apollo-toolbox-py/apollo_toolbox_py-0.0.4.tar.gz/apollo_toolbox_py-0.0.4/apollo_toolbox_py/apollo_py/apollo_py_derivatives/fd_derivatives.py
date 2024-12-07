__all__ = ['FDDerivativeEngine']

import copy

import jax
import numba
import numpy as np

from apollo_toolbox_py.apollo_py.apollo_py_derivatives.derivative_engine import DerivativeEngine, JitCompileMode


class FDDerivativeEngine(DerivativeEngine):
    def __init__(self, f, n: int, m: int, jit_compile_f: JitCompileMode = JitCompileMode.DoNotJitCompile):
        super().__init__(f, n, m)

        self.jit_compile_f = jit_compile_f

        if jit_compile_f == JitCompileMode.Jax:
            self.f = jax.jit(f)

        if jit_compile_f == JitCompileMode.Numba:
            self.f = numba.jit(f)

    def derivative(self, x) -> np.ndarray:
        out = np.zeros((self.m, self.n))

        p = 0.000001

        f0 = self.call_numpy(x)
        for i in range(self.n):
            xh = copy.deepcopy(x)
            xh[i] += p
            fh = self.call_numpy(xh)
            col = (fh - f0) / p
            out[:, i] = col

        return out
