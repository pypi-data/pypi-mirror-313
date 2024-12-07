from typing import Union, List

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.matrices import M3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3
import numpy as np

__all__ = ['LieGroupSO3', 'LieAlgSO3']


class LieGroupSO3(Rotation3):
    @classmethod
    def identity(cls) -> 'LieGroupSO3':
        return cls(np.identity(3, dtype=np.float64))

    def ln(self) -> 'LieAlgSO3':
        m = self.array
        trace = np.trace(m)
        beta = np.arccos(max(min((trace - 1) / 2.0, 1.0), -1.0))

        if np.isclose(beta, 0):
            f = 0.5 + (beta ** 2 / 12.0) + (7.0 * beta ** 4 / 720.0)
            skew_symmetric = (m - m.T) * f
        elif np.isclose(beta, np.pi):
            r11 = np.pi * np.sqrt(0.5 * (m[0, 0] + 1.0))
            r22 = np.pi * np.sqrt(0.5 * (m[1, 1] + 1.0))
            r33 = np.pi * np.sqrt(0.5 * (m[2, 2] + 1.0))
            skew_symmetric = np.array([[0.0, -r33, r22], [r33, 0.0, -r11], [-r22, r11, 0.0]])
        else:
            f = beta / (2.0 * np.sin(beta))
            skew_symmetric = (m - m.T) * f

        return LieAlgSO3(skew_symmetric)

    def __repr__(self) -> str:
        return f"LieGroupSO3(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"LieGroupSO3(\n{np.array2string(self.array)}\n)"


class LieAlgSO3(M3):
    @classmethod
    def from_euclidean_space_element(cls, e: Union[List[float], np.ndarray]) -> 'LieAlgSO3':
        if isinstance(e, list):
            if len(e) != 3:
                raise ValueError("List must contain exactly three numbers.")
            e = np.array(e, dtype=np.float64)
        elif isinstance(e, np.ndarray):
            if e.shape != (3,):
                raise ValueError("Array must have shape (3,).")
        else:
            raise TypeError("Input must be either a list of three numbers or a numpy array with shape (3,).")

        skew_symmetric = np.array([[0, -e[2], e[1]], [e[2], 0, -e[0]], [-e[1], e[0], 0]])
        return cls(skew_symmetric)

    def exp(self) -> 'LieGroupSO3':
        u = np.array([self[2, 1], self[0, 2], self[1, 0]])
        beta = np.linalg.norm(u)

        if np.isclose(beta, 0):
            p = 1.0 - (beta ** 2 / 6.0) + (beta ** 4 / 120.0)
            q = 0.5 - (beta ** 2 / 24.0) + (beta ** 4 / 720.0)
        else:
            p = np.sin(beta) / beta
            q = (1.0 - np.cos(beta)) / (beta ** 2)

        rotation_matrix = np.eye(3) + p * self.array + q * (self.array @ self.array)
        return LieGroupSO3(rotation_matrix)

    def vee(self) -> np.ndarray:
        return np.array([self[2, 1], self[0, 2], self[1, 0]])

    def __repr__(self) -> str:
        return f"LieAlgSO3(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"LieAlgSO3(\n{np.array2string(self.array)}\n)"
