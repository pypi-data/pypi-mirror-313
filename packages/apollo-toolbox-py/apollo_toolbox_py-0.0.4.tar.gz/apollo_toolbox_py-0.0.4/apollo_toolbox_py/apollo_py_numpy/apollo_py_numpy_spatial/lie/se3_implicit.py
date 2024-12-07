import numpy as np

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.isometries import IsometryMatrix3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.so3 import LieGroupSO3, LieAlgSO3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.matrices import M3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3, V6

__all__ = ['LieGroupISE3', 'LieAlgISE3']


class LieGroupISE3(IsometryMatrix3):
    @staticmethod
    def get_lie_alg_type() -> type:
        return LieAlgISE3

    @classmethod
    def from_isometry_matrix3(cls, isometry: 'IsometryMatrix3') -> 'LieGroupISE3':
        rotation = isometry.rotation
        translation = isometry.translation
        return cls(rotation, translation)

    @classmethod
    def identity(cls) -> 'LieGroupISE3':
        return LieGroupISE3(Rotation3.new_unchecked(np.identity(3)), V3([0, 0, 0]))

    def group_operator(self, other: 'LieGroupISE3') -> 'LieGroupISE3':
        return LieGroupISE3.from_isometry_matrix3(self @ other)

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3, translation: V3) -> 'LieGroupISE3':
        return LieGroupISE3.from_isometry_matrix3(IsometryMatrix3(Rotation3.from_scaled_axis(scaled_axis), translation))

    @classmethod
    def from_euler_angles(cls, euler_angles: V3, translation: V3) -> 'LieGroupISE3':
        return LieGroupISE3.from_isometry_matrix3(IsometryMatrix3(Rotation3.from_euler_angles(euler_angles), translation))

    def ln(self) -> 'LieAlgISE3':
        a_mat = LieGroupSO3.new_unchecked(self.rotation.array).ln()
        u = a_mat.vee()
        beta = np.linalg.norm(u)

        if abs(beta) < 0.00001:
            pp = 0.5 - ((beta ** 2.0) / 24.0) + ((beta ** 4.0) / 720.0)
            qq = (1.0 / 6.0) - ((beta ** 2.0) / 120.0) + ((beta ** 4.0) / 5040.0)
        else:
            pp = (1.0 - np.cos(beta)) / (beta ** 2.0)
            qq = (beta - np.sin(beta)) / (beta ** 3.0)

        c_mat = np.identity(3) + pp * a_mat.array + qq * (a_mat.array @ a_mat.array)
        c_inv = np.linalg.inv(c_mat)

        b = V3(c_inv @ self.translation.array)

        return LieAlgISE3(M3(a_mat.array), b)

    def inverse(self) -> 'LieGroupISE3':
        new_rotation = self.rotation.transpose()
        new_translation = new_rotation.map_point(-self.translation)
        return LieGroupISE3(new_rotation, new_translation)

    def displacement(self, other: 'LieGroupISE3') -> 'LieGroupISE3':
        return self.inverse().group_operator(other)

    def __repr__(self) -> str:
        return f"LieGroupISE3(\n  rotation: \n{np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"

    def __str__(self) -> str:
        return f"LieGroupISE3(\n  rotation: \n{np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"


class LieAlgISE3:
    def __init__(self, matrix: M3, vector: V3):
        self.matrix = matrix
        self.vector = vector

    @classmethod
    def from_euclidean_space_element(cls, e: V6) -> 'LieAlgISE3':
        u = V3([e[0], e[1], e[2]])
        m = u.to_lie_alg_so3()
        v = V3([e[3], e[4], e[5]])
        return LieAlgISE3(m, v)

    def exp(self) -> 'LieGroupISE3':
        a_mat = LieAlgSO3(self.matrix.array)
        u = a_mat.vee()
        beta = np.linalg.norm(u)

        if abs(beta) < 0.00001:
            pp = 0.5 - ((beta ** 2.0) / 24.0) + ((beta ** 4.0) / 720.0)
            qq = (1.0 / 6.0) - ((beta ** 2.0) / 120.0) + ((beta ** 4.0) / 5040.0)
        else:
            pp = (1.0 - np.cos(beta)) / (beta ** 2.0)
            qq = (beta - np.sin(beta)) / (beta ** 3.0)

        c_mat = np.identity(3) + pp * a_mat.array + qq * (a_mat.array @ a_mat.array)
        t = c_mat@self.vector.array
        r_mat = a_mat.exp()

        return LieGroupISE3(Rotation3(r_mat.array), V3(t))

    def vee(self) -> 'V6':
        u = LieAlgSO3(self.matrix.array).vee()
        v = self.vector

        return V6([u[0], u[1], u[2], v[0], v[1], v[2]])

    def __repr__(self) -> str:
        return f"LieAlgISE3(\n  matrix: \n{np.array2string(self.matrix.array)},\n  ----- \n  vector: {np.array2string(self.vector.array)}\n)"

    def __str__(self) -> str:
        return f"LieAlgISE3(\n  matrix: \n{np.array2string(self.matrix.array)},\n  ----- \n  vector: {np.array2string(self.vector.array)}\n)"
