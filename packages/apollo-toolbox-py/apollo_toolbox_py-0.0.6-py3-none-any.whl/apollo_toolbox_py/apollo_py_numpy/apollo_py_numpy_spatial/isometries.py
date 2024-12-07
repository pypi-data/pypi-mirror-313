from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.quaternions import UnitQuaternion
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3
import numpy as np

__all__ = ['Isometry3', 'IsometryMatrix3']


class Isometry3:
    def __init__(self, q: UnitQuaternion, v: V3):
        self.rotation = q
        self.translation = v

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3, translation: V3) -> 'Isometry3':
        return Isometry3(UnitQuaternion.from_scaled_axis(scaled_axis), translation)

    @classmethod
    def from_euler_angles(cls, euler_angles: V3, translation: V3) -> 'Isometry3':
        return Isometry3(UnitQuaternion.from_euler_angles(euler_angles), translation)

    def map_point(self, v: V3) -> 'V3':
        return V3(self.rotation.map_point(v).array + self.translation.array)

    def get_translation(self) -> V3:
        return self.translation

    def get_rotation(self) -> UnitQuaternion:
        return self.rotation

    def __matmul__(self, other: 'Isometry3') -> 'Isometry3':
        new_rotation = self.rotation @ other.rotation
        new_translation = V3(self.rotation.map_point(other.translation).array + self.translation.array)
        return Isometry3(new_rotation, new_translation)

    def __mul__(self, other: 'Isometry3') -> 'Isometry3':
        return self @ other

    def __repr__(self) -> str:
        return f"Isometry3(\n  rotation: {np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"

    def __str__(self) -> str:
        return f"Isometry3(\n  rotation: {np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"


class IsometryMatrix3:
    def __init__(self, r: Rotation3, v: V3):
        self.rotation = r
        self.translation = v

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3, translation: V3) -> 'IsometryMatrix3':
        return IsometryMatrix3(Rotation3.from_scaled_axis(scaled_axis), translation)

    @classmethod
    def from_euler_angles(cls, euler_angles: V3, translation: V3) -> 'IsometryMatrix3':
        return IsometryMatrix3(Rotation3.from_euler_angles(euler_angles), translation)

    def map_point(self, v: V3) -> 'V3':
        return V3(self.rotation.map_point(v).array + self.translation.array)

    def get_translation(self) -> V3:
        return self.translation

    def get_rotation(self) -> Rotation3:
        return self.rotation

    def __matmul__(self, other: 'IsometryMatrix3') -> 'IsometryMatrix3':
        new_rotation = Rotation3.new_unchecked(self.rotation.array @ other.rotation.array)
        new_translation = V3(self.rotation.array @ other.translation.array + self.translation.array)
        return IsometryMatrix3(new_rotation, new_translation)

    def __mul__(self, other: 'IsometryMatrix3') -> 'IsometryMatrix3':
        return self @ other

    def __repr__(self) -> str:
        return f"IsometryMatrix3(\n  rotation: \n{np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"

    def __str__(self) -> str:
        return f"IsometryMatrix3(\n  rotation: \n{np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"
