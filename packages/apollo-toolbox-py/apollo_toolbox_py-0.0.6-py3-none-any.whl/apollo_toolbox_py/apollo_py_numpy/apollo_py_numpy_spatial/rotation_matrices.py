import math
from typing import Union, List, Any

import numpy as np

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.matrices import M3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3


__all__ = ['Rotation3']


class Rotation3(M3):
    def __init__(self, array: Union[List[List[float]], np.ndarray]):
        super().__init__(array)
        if not np.allclose(self.array @ self.array.T, np.eye(3), rtol=1e-7, atol=1e-7):
            raise ValueError("Rotation matrix must be orthonormal.")

    @classmethod
    def new_unchecked(cls, array: Union[List[List[float]], np.ndarray]) -> 'Rotation3':
        out = cls.__new__(cls)
        out.array = array
        return out

    @classmethod
    def new_normalize(cls, array: Union[List[List[float]], np.ndarray]) -> 'Rotation3':
        array = np.asarray(array, dtype=np.float64)

        u, _, vh = np.linalg.svd(array)
        array = np.dot(u, vh)

        if np.linalg.det(array) < 0:
            u[:, -1] *= -1
            array = np.dot(u, vh)

        return cls.new_unchecked(array)

    @classmethod
    def from_euler_angles(cls, xyz: V3) -> 'Rotation3':
        roll, pitch, yaw = xyz.array

        R_x = np.array([
            [1, 0, 0],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll), np.cos(roll)]
        ])

        R_y = np.array([
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)]
        ])

        R_z = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])

        rotation_matrix = R_z @ R_y @ R_x

        return cls(rotation_matrix)

    @classmethod
    def from_axis_angle(cls, axis: V3, angle: float) -> 'Rotation3':
        if angle == 0.0:
            return Rotation3.new_unchecked(np.eye(3))

        axis = axis.array / np.linalg.norm(axis.array)
        x, y, z = axis
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        one_minus_cos = 1 - cos_theta

        rotation_matrix = np.array([
            [cos_theta + x * x * one_minus_cos,
             x * y * one_minus_cos - z * sin_theta,
             x * z * one_minus_cos + y * sin_theta],
            [y * x * one_minus_cos + z * sin_theta,
             cos_theta + y * y * one_minus_cos,
             y * z * one_minus_cos - x * sin_theta],
            [z * x * one_minus_cos - y * sin_theta,
             z * y * one_minus_cos + x * sin_theta,
             cos_theta + z * z * one_minus_cos]
        ])

        return cls(rotation_matrix)

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3) -> 'Rotation3':
        n = scaled_axis.norm()
        return Rotation3.from_axis_angle(scaled_axis, n)

    @classmethod
    def from_look_at(cls, look_at_vector: V3, axis: V3) -> 'Rotation3':
        look_at_vector = look_at_vector.normalize()
        axis = axis.normalize()

        rotation_axis = axis.cross(look_at_vector)
        angle = np.acos(min(axis.dot(look_at_vector), 1.0))

        return Rotation3.from_axis_angle(rotation_axis, angle)

    def transpose(self) -> 'Rotation3':
        return Rotation3(self.array.T)

    def to_euler_angles(self) -> V3:
        m = self.array
        if m[2][0] < 1:
            if m[2][0] > -1:
                pitch = np.arcsin(-m[2][0])
                roll = np.arctan2(m[2][1], m[2][2])
                yaw = np.arctan2(m[1][0], m[0][0])
            else:
                pitch = np.pi / 2
                roll = np.arctan2(-m[1][2], m[1][1])
                yaw = 0
        else:
            pitch = -np.pi / 2
            roll = np.arctan2(-m[1][2], m[1][1])
            yaw = 0
        return V3([roll, pitch, yaw])

    def inverse(self) -> 'Rotation3':
        return self.new_unchecked(self.array.T)

    def to_unit_quaternion(self) -> 'UnitQuaternion':
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.quaternions import UnitQuaternion

        m = self.array
        trace = np.trace(m)
        if trace > 0:
            s = 0.5 / np.sqrt(trace + 1.0)
            w = 0.25 / s
            x = (m[2, 1] - m[1, 2]) * s
            y = (m[0, 2] - m[2, 0]) * s
            z = (m[1, 0] - m[0, 1]) * s
        elif (m[0, 0] > m[1, 1]) and (m[0, 0] > m[2, 2]):
            s = 2.0 * np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2])
            w = (m[2, 1] - m[1, 2]) / s
            x = 0.25 * s
            y = (m[0, 1] + m[1, 0]) / s
            z = (m[0, 2] + m[2, 0]) / s
        elif m[1, 1] > m[2, 2]:
            s = 2.0 * np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2])
            w = (m[0, 2] - m[2, 0]) / s
            x = (m[0, 1] + m[1, 0]) / s
            y = 0.25 * s
            z = (m[1, 2] + m[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1])
            w = (m[1, 0] - m[0, 1]) / s
            x = (m[0, 2] + m[2, 0]) / s
            y = (m[1, 2] + m[2, 1]) / s
            z = 0.25 * s

        return UnitQuaternion.new_unchecked([w, x, y, z])

    def map_point(self, v: V3) -> 'V3':
        return V3(self.array@v.array)

    def to_lie_group_so3(self):
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.so3 import LieGroupSO3
        return LieGroupSO3(self.array)

    def __repr__(self) -> str:
        return f"Rotation3(\n{np.array2string(self.array)}\n)"

    def __str__(self) -> str:
        return f"Rotation3(\n{np.array2string(self.array)}\n)"



