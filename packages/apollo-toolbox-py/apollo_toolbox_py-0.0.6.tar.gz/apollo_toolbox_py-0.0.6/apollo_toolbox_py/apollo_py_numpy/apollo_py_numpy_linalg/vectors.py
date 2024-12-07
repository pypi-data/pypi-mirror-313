from typing import Union, List
import numpy as np

__all__ = ['V', 'V3', 'V6']


class V:
    def __init__(self, array: Union[List[float], np.ndarray]):
        self.array = np.asarray(array, dtype=np.float64)

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value

    def dot(self, other):
        if isinstance(other, V):
            other = other.array
        return np.dot(self.array, other)

    def norm(self, ord=None):
        return np.linalg.norm(self.array, ord=ord)

    def normalize(self):
        return self.__class__(self.array / self.norm())

    def __add__(self, other):
        if isinstance(other, V):
            other = other.array
        return self.__class__(self.array + other)

    def __sub__(self, other):
        if isinstance(other, V):
            other = other.array
        return self.__class__(self.array - other)

    def __mul__(self, scalar):
        return self.__class__(self.array * scalar)

    def __rmul__(self, scalar):
        return self.__class__(self.array * scalar)

    def __neg__(self):
        return self.__class__(-self.array)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Division by zero is not allowed.")
        return self.__class__(self.array / scalar)

    def __rtruediv__(self, scalar):
        return self.__class__(scalar / self.array)

    def magnitude(self):
        return np.linalg.norm(self.array)

    def unit(self):
        norm = self.norm()
        if norm == 0:
            raise ValueError("Zero vector has no direction.")
        return self.__class__(self.array / norm)

    def __repr__(self) -> str:
        return f"V(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"V(\n{np.array2string(self.array)}\n)"


class V3(V):
    def __init__(self, array: Union[List[float], np.ndarray]):
        super().__init__(array)
        if self.array.shape != (3,):
            raise ValueError("V3 must be a 3-vector.")

    def to_lie_alg_so3(self):
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.so3 import LieAlgSO3
        return LieAlgSO3.from_euclidean_space_element(self.array)

    def to_lie_alg_h1(self):
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.h1 import LieAlgH1
        return LieAlgH1.from_euclidean_space_element(self.array)

    def cross(self, other: 'V3') -> 'V3':
        if not isinstance(other, V3):
            raise TypeError("Cross product requires another V3 vector.")
        return V3(np.linalg.cross(self.array, other.array))

    def __repr__(self) -> str:
        return f"V3(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"V3(\n{np.array2string(self.array)}\n)"


class V6(V):
    def __init__(self, array: Union[List[float], np.ndarray]):
        super().__init__(array)
        if self.array.shape != (6,):
            raise ValueError("V6 must be a 6-vector.")

    def __repr__(self) -> str:
        return f"V6(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"V6(\n{np.array2string(self.array)}\n)"
