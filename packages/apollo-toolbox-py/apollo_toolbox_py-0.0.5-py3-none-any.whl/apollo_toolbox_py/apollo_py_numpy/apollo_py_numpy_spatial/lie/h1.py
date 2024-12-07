from typing import Union, List

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.quaternions import UnitQuaternion, Quaternion
import numpy as np

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3


__all__ = ['LieGroupH1', 'LieAlgH1']

class LieGroupH1(UnitQuaternion):
    @classmethod
    def identity(cls) -> 'LieGroupH1':
        return cls([1, 0, 0, 0])

    def ln(self) -> 'LieAlgH1':
        w, x, y, z = self.array
        acos = np.acos(min(w, 1.0))
        if acos == 0.0:
            return LieAlgH1([0, 0, 0, 0])
        else:
            ss = acos / np.sin(acos)
            return LieAlgH1([0, ss * x, ss * y, ss * z])

    def __repr__(self) -> str:
        return f"LieGroupH1(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"LieGroupH1(\n{np.array2string(self.array)}\n)"


class LieAlgH1(Quaternion):
    @classmethod
    def from_euclidean_space_element(cls, e: Union[List[float], np.ndarray]) -> 'LieAlgH1':
        if isinstance(e, list):
            if len(e) != 3:
                raise ValueError("List must contain exactly three numbers.")
            e = np.array(e, dtype=np.float64)
        elif isinstance(e, np.ndarray):
            if e.shape != (3,):
                raise ValueError("Array must have shape (3,).")
        else:
            raise TypeError("Input must be either a list of three numbers or a numpy array with shape (3,).")
        return cls([0, e[0], e[1], e[2]])

    def exp(self) -> 'LieGroupH1':
        v = self.array[1:]
        vn = np.linalg.norm(v)
        if vn == 0.0:
            return LieGroupH1.identity()
        else:
            cc = np.cos(vn)
            ss = np.sin(vn) / vn
            return LieGroupH1.new_unchecked([cc, ss * v[0], ss * v[1], ss * v[2]])

    def vee(self) -> V3:
        w, x, y, z = self
        return V3([x, y, z])

    def __repr__(self) -> str:
        return f"LieAlgH1(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"LieAlgH1(\n{np.array2string(self.array)}\n)"
