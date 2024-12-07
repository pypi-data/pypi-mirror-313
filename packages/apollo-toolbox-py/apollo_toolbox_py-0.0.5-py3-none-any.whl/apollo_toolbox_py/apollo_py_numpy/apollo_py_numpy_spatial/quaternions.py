from typing import Union, List

import numpy as np

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3

__all__ = ['Quaternion', 'UnitQuaternion']


class Quaternion:
    def __init__(self, wxyz_array: Union[List[float], np.ndarray]):
        self.array = np.asarray(wxyz_array, dtype=np.float64)
        if self.array.shape != (4,):
            raise ValueError("Quaternion must be a 4-vector.")

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value

    @property
    def w(self):
        return self.array[0]

    @property
    def x(self):
        return self.array[1]

    @property
    def y(self):
        return self.array[2]

    @property
    def z(self):
        return self.array[3]

    def conjugate(self) -> 'Quaternion':
        w, x, y, z = self.array
        return self.__class__([w, -x, -y, -z])

    def inverse(self) -> 'Quaternion':
        conjugate = self.conjugate()
        norm_sq = np.linalg.norm(self.array) ** 2
        return Quaternion(conjugate.array / norm_sq)

    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        w1, x1, y1, z1 = self.array
        w2, x2, y2, z2 = other.array

        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2

        return Quaternion([w, x, y, z])

    def __matmul__(self, other: 'Quaternion') -> 'Quaternion':
        return self * other

    def __repr__(self) -> str:
        return f"Quaternion(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"Quaternion(\n{np.array2string(self.array)}\n)"


class UnitQuaternion(Quaternion):
    def __init__(self, wxyz_array: Union[List[float], np.ndarray]):
        super().__init__(wxyz_array)
        if not np.isclose(np.linalg.norm(self.array), 1.0, rtol=1e-7, atol=1e-7):
            raise ValueError("Unit quaternion must be unit length.")

    @classmethod
    def new_unchecked(cls, wxyz_array: Union[List[float], np.ndarray]) -> 'UnitQuaternion':
        out = cls.__new__(cls)
        out.array = np.asarray(wxyz_array)
        return out

    @classmethod
    def new_normalize(cls, wxyz_array: Union[List[float], np.ndarray]) -> 'UnitQuaternion':
        out = cls.new_unchecked(wxyz_array)
        out.array /= np.linalg.norm(out.array)
        return out

    @classmethod
    def from_euler_angles(cls, xyz: V3) -> 'UnitQuaternion':
        cy = np.cos(xyz[2] * 0.5)
        sy = np.sin(xyz[2] * 0.5)
        cp = np.cos(xyz[1] * 0.5)
        sp = np.sin(xyz[1] * 0.5)
        cr = np.cos(xyz[0] * 0.5)
        sr = np.sin(xyz[0] * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return cls([w, x, y, z])

    @classmethod
    def from_axis_angle(cls, axis: V3, angle: float) -> 'UnitQuaternion':
        scaled_axis = axis / axis.norm()
        scaled_axis = scaled_axis * angle
        return UnitQuaternion.from_scaled_axis(scaled_axis)

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3) -> 'UnitQuaternion':
        norm = scaled_axis.norm()
        if norm < 1e-8:
            return cls.new_unchecked([1.0, 0.0, 0.0, 0.0])

        half_angle = norm / 2.0
        sin_half_angle = np.sin(half_angle)
        cos_half_angle = np.cos(half_angle)

        return cls([cos_half_angle, *(sin_half_angle * scaled_axis / norm)])

    def inverse(self) -> 'UnitQuaternion':
        return self.conjugate()

    def to_rotation_matrix(self) -> 'Rotation3':
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3
        w, x, y, z = self.array
        matrix = [
            [1 - 2 * (y ** 2 + z ** 2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x ** 2 + z ** 2), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x ** 2 + y ** 2)]
        ]
        return Rotation3.new_unchecked(matrix)

    def map_point(self, v: V3) -> 'V3':
        qv = Quaternion([0.0, v.array[0], v.array[1], v.array[2]])
        res = self @ qv @ self.conjugate()
        return V3([res[1], res[2], res[3]])

    def to_lie_group_h1(self) -> 'LieGroupH1':
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.h1 import LieGroupH1
        return LieGroupH1(self.array)

    def __mul__(self, other: Union['UnitQuaternion', 'Quaternion']) -> Union['UnitQuaternion', 'Quaternion']:
        tmp = super().__mul__(other)
        if isinstance(other, UnitQuaternion):
            return UnitQuaternion.new_unchecked(tmp.array)
        else:
            return tmp

    def __matmul__(self, other: Union['UnitQuaternion', 'Quaternion']) -> Union['UnitQuaternion', 'Quaternion']:
        return self * other

    def __repr__(self) -> str:
        return f"UnitQuaternion(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"UnitQuaternion(\n{np.array2string(self.array)}\n)"
