__all__ = ['WASPDerivativeEngine']

import copy
import random
import jax
import numba
import numpy as np

from apollo_toolbox_py.apollo_py.apollo_py_derivatives.derivative_engine import DerivativeEngine, JitCompileMode


class WASPDerivativeEngine(DerivativeEngine):
    def __init__(self, f, n: int, m: int, jit_compile_f: JitCompileMode = JitCompileMode.DoNotJitCompile,
                 lagrange_multiplier_inf_norm_cutoff=0.1):
        super().__init__(f, n, m)

        if jit_compile_f == JitCompileMode.Jax:
            self.f = jax.jit(f)

        if jit_compile_f == JitCompileMode.Numba:
            self.f = numba.jit(f)

        self.lagrange_multiplier_inf_norm_cutoff = lagrange_multiplier_inf_norm_cutoff
        self.r = self.n + 4
        self.delta_x_mat = np.random.uniform(-1.0, 1.0, (self.n, self.r))
        self.delta_x_mat_T = self.delta_x_mat.T
        self.delta_f_hat_mat_T = np.zeros((self.r, self.m))
        self.i = 0

        tmp = 2.0 * (self.delta_x_mat @ self.delta_x_mat_T)
        self.p_matrices = []
        for i in range(self.r):
            p = np.zeros((self.n + 1, self.n + 1))
            p[0:self.n, 0:self.n] = tmp
            delta_x_i = self.delta_x_mat[:, i]
            p[0: self.n, self.n] = delta_x_i
            p[self.n, 0: self.n] = -delta_x_i.T
            self.p_matrices.append(np.linalg.inv(p))

        self.num_f_calls = 0

    def _derivative_internal(self, x, recursive_call=False, f0=None) -> np.ndarray:
        i = self.i

        p_mat_i = self.p_matrices[i]
        delta_x_i = self.delta_x_mat[:, i]

        if f0 is None:
            f0 = self.call_numpy(x)
            self.num_f_calls += 1

        xh = np.array(x) + (0.00001 * delta_x_i)
        fh = self.call_numpy(xh)
        self.num_f_calls += 1
        delta_f_i = (fh - f0) / 0.00001
        print(delta_f_i)
        print()
        print(self.delta_f_hat_mat_T)
        print()
        self.delta_f_hat_mat_T[i, :] = delta_f_i.flatten()
        print(self.delta_f_hat_mat_T)
        print('---')

        a_mat = 2.0 * self.delta_x_mat @ self.delta_f_hat_mat_T

        b_mat = np.zeros((self.n + 1, self.m))
        b_mat[0:self.n, 0:self.m] = a_mat
        b_mat[self.n, 0:self.m] = delta_f_i.T.flatten()

        c_mat = p_mat_i @ b_mat
        d_mat_t = c_mat[0:self.n, 0:self.m]
        lagrange_multipliers = c_mat[self.n, 0:self.m]
        inf_norm = np.linalg.norm(lagrange_multipliers, ord=np.inf)

        # obj_value = np.linalg.norm(self.delta_x_mat_T @ d_mat_t - self.delta_f_hat_mat_T)
        # print(lagrange_multipliers)

        if not recursive_call:
            self.delta_f_hat_mat_T = self.delta_x_mat_T @ d_mat_t

        self.i += 1
        if self.i >= self.r:
            self.i = 0

        if inf_norm > self.lagrange_multiplier_inf_norm_cutoff:
            return self._derivative_internal(x, True, f0)
        else:
            return d_mat_t.T

    def derivative(self, x) -> np.ndarray:
        self.num_f_calls = 0
        return self._derivative_internal(x, False)
