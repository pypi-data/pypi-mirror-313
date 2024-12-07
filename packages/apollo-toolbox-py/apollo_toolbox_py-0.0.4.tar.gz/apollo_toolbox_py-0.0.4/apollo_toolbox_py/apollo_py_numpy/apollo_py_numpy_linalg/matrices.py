import numpy as np
from typing import Union, List, Tuple, Any

__all__ = ['M', 'M3']


class M:
    def __init__(self, array: Union[List[List[float]], np.ndarray]):
        self.array = np.asarray(array, dtype=np.float64)

    def __getitem__(self, item: Union[int, Tuple[int, int]]) -> np.ndarray[Any, np.dtype[Any]]:
        return self.array[item]

    def __setitem__(self, key: Union[int, Tuple[int, int]], value: float):
        self.array[key] = value

    def transpose(self) -> 'M':
        return M(self.array.T)

    def determinant(self) -> float:
        return np.linalg.det(self.array)

    def inverse(self) -> 'M':
        return M(np.linalg.inv(self.array))

    def dot(self, other: Union['M', np.ndarray]) -> 'M':
        if isinstance(other, M):
            other = other.array
        return M(np.dot(self.array, other))

    def trace(self) -> float:
        return np.trace(self.array)

    def rank(self) -> int:
        return np.linalg.matrix_rank(self.array)

    def eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvals(self.array)

    def eigenvectors(self) -> 'M':
        _, vectors = np.linalg.eig(self.array)
        return M(vectors.T)

    def svd(self, full_matrices: bool = False) -> Tuple['M', np.ndarray, 'M']:
        U, S, V = np.linalg.svd(self.array, full_matrices=full_matrices)
        return M(U), S, M(V)

    def eigenanalysis(self) -> Tuple[np.ndarray, 'M']:
        values, vectors = np.linalg.eig(self.array)
        return values, M(vectors.T)

    def __add__(self, other: Union['M', np.ndarray]) -> 'M':
        if isinstance(other, M):
            other = other.array
        return M(self.array + other)

    def __sub__(self, other: Union['M', np.ndarray]) -> 'M':
        if isinstance(other, M):
            other = other.array
        return M(self.array - other)

    def __mul__(self, scalar: float) -> 'M':
        return M(self.array * scalar)

    def __truediv__(self, scalar: float) -> 'M':
        if scalar == 0:
            raise ValueError("Division by zero is not allowed.")
        return M(self.array / scalar)

    def __rtruediv__(self, scalar: float) -> 'M':
        return M(scalar / self.array)

    def __matmul__(self, other: Union['M', np.ndarray]) -> 'M':
        if isinstance(other, M):
            other = other.array
        return M(np.matmul(self.array, other))

    def __repr__(self) -> str:
        return f"Matrix(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"Matrix(\n{np.array2string(self.array)}\n)"


class M3(M):
    def __init__(self, array: Union[List[List[float]], np.ndarray]):
        super().__init__(array)
        if self.array.shape != (3, 3):
            raise ValueError("Matrix3 must be a 3x3 matrix.")

    def __repr__(self) -> str:
        return f"Matrix3(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"Matrix3(\n{np.array2string(self.array)}\n)"
