import time

from apollo_toolbox_py.apollo_py.apollo_py_derivatives.derivative_engine import JitCompileMode, ADMode
from apollo_toolbox_py.apollo_py.apollo_py_derivatives.fd_derivatives import FDDerivativeEngine
from apollo_toolbox_py.apollo_py.apollo_py_derivatives.jax_derivatives import JaxDerivativeEngine
from apollo_toolbox_py.apollo_py.apollo_py_derivatives.test_functions import random_vector
from apollo_toolbox_py.apollo_py.apollo_py_derivatives.wasp_derivatives import WASPDerivativeEngine
import numpy as np


class DerivativeEngineEvaluator:
    def __init__(self,
                 function_object,
                 n: int,
                 m: int,
                 include_fd_engine: bool = True,
                 num_calls: int = 100,
                 lagrange_multiplier_inf_norm_cutoff=0.1):
        self.n = n
        self.m = m

        self.function_object = function_object
        self.jax_forward_engine = JaxDerivativeEngine(function_object.call, n, m, JitCompileMode.Jax, True,
                                                      ADMode.Forward)
        self.jax_reverse_engine = JaxDerivativeEngine(function_object.call, n, m, JitCompileMode.Jax, True,
                                                      ADMode.Reverse)
        self.fd_engine = FDDerivativeEngine(function_object.call, n, m, JitCompileMode.Jax)
        self.wasp_engine = WASPDerivativeEngine(function_object.call, n, m, JitCompileMode.Jax,
                                                lagrange_multiplier_inf_norm_cutoff)

        self.include_fd_engine = include_fd_engine
        self.num_calls = num_calls

        r = random_vector(n, -1.0, 1.0)
        start = time.time()
        self.jax_forward_engine.derivative(r)
        self.jax_forward_engine_first_time = time.time() - start

        start = time.time()
        self.jax_reverse_engine.derivative(r)
        self.jax_reverse_engine_first_time = time.time() - start

        self.wasp_engine_errors = []
        self.fd_engine_errors = []

        self.jax_forward_engine_times = []
        self.jax_reverse_engine_times = []
        self.wasp_engine_times = []
        self.fd_engine_times = []

        self.wasp_num_f_calls = []

    def evaluate(self):
        x = random_vector(self.n, -1.0, 1.0)

        for i in range(self.num_calls):
            print('evaluation iteration {} of {}'.format(i+1, self.num_calls))
            x = x + random_vector(self.n, -0.01, 0.01)

            start = time.time()
            res = self.jax_forward_engine.derivative(x)
            self.jax_forward_engine_times.append(time.time() - start)
            gt = res

            start = time.time()
            self.jax_reverse_engine.derivative(x)
            self.jax_reverse_engine_times.append(time.time() - start)

            start = time.time()
            res = self.wasp_engine.derivative(x)
            print(res - gt)
            self.wasp_engine_times.append(time.time() - start)
            self.wasp_num_f_calls.append(self.wasp_engine.num_f_calls)
            error = np.linalg.norm(gt - res, ord=np.inf)
            self.wasp_engine_errors.append(error)

            if self.include_fd_engine:
                start = time.time()
                res = self.fd_engine.derivative(x)
                self.fd_engine_times.append(time.time() - start)
                error = np.linalg.norm(gt - res, ord=np.inf)
                self.fd_engine_errors.append(error)
