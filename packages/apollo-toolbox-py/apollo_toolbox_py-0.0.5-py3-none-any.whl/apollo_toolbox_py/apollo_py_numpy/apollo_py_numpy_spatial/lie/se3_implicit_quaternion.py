from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.isometries import Isometry3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.h1 import LieGroupH1, LieAlgH1
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.so3 import LieAlgSO3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.quaternions import UnitQuaternion, Quaternion
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3, V6
import numpy as np

__all__ = ['LieGroupISE3q', 'LieAlgISE3q']


class LieGroupISE3q(Isometry3):
    @staticmethod
    def get_lie_alg_type() -> type:
        return LieAlgISE3q

    @classmethod
    def from_isometry3(cls, isometry: 'Isometry3') -> 'LieGroupISE3q':
        rotation = isometry.rotation
        translation = isometry.translation
        return cls(rotation, translation)

    @classmethod
    def from_scaled_axis(cls, scaled_axis: V3, translation: V3) -> 'LieGroupISE3q':
        return LieGroupISE3q.from_isometry3(Isometry3(UnitQuaternion.from_scaled_axis(scaled_axis), translation))

    @classmethod
    def from_euler_angles(cls, euler_angles: V3, translation: V3) -> 'LieGroupISE3q':
        return LieGroupISE3q.from_isometry3(Isometry3(UnitQuaternion.from_euler_angles(euler_angles), translation))

    @classmethod
    def identity(cls) -> 'LieGroupISE3q':
        return LieGroupISE3q(UnitQuaternion.new_unchecked([1, 0, 0, 0]), V3([0, 0, 0]))

    def group_operator(self, other: 'LieGroupISE3q') -> 'LieGroupISE3q':
        return LieGroupISE3q.from_isometry3(self @ other)

    def ln(self) -> 'LieAlgISE3q':
        a_quat = LieGroupH1(self.rotation.array).ln()
        u = a_quat.vee()
        a_mat: LieAlgSO3 = u.to_lie_alg_so3()
        beta = np.linalg.norm(u.array)

        if abs(beta) < 0.00001:
            pp = 0.5 - ((beta ** 2.0) / 24.0) + ((beta ** 4.0) / 720.0)
            qq = (1.0 / 6.0) - ((beta ** 2.0) / 120.0) + ((beta ** 4.0) / 5040.0)
        else:
            pp = (1.0 - np.cos(beta)) / (beta ** 2.0)
            qq = (beta - np.sin(beta)) / (beta ** 3.0)

        c_mat = np.identity(3) + (pp * a_mat.array) + qq * (a_mat.array @ a_mat.array)
        c_inv = np.linalg.inv(c_mat)

        b = V3(c_inv @ self.translation.array)

        return LieAlgISE3q(a_quat, b)

    def inverse(self) -> 'LieGroupISE3q':
        new_rotation = self.rotation.conjugate()
        new_translation = new_rotation.map_point(-self.translation)
        return LieGroupISE3q(new_rotation, new_translation)

    def displacement(self, other: 'LieGroupISE3q') -> 'LieGroupISE3q':
        return self.inverse().group_operator(other)

    def __repr__(self) -> str:
        return f"LieGroupISE3q(\n  rotation: {np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"

    def __str__(self) -> str:
        return f"LieGroupISE3q(\n  rotation: {np.array2string(self.rotation.array)},\n  ----- \n  translation: {np.array2string(self.translation.array)}\n)"


class LieAlgISE3q:
    def __init__(self, quaternion: Quaternion, vector: V3):
        self.quaternion = quaternion
        self.vector = vector

    @classmethod
    def from_euclidean_space_element(cls, e: V6) -> 'LieAlgISE3q':
        u = V3([e[0], e[1], e[2]])
        q = u.to_lie_alg_h1()
        v = V3([e[3], e[4], e[5]])
        return LieAlgISE3q(q, v)

    def exp(self) -> 'LieGroupISE3q':
        u = LieAlgH1(self.quaternion.array).vee()
        a_mat: LieAlgSO3 = u.to_lie_alg_so3()

        beta = np.linalg.norm(u.array)

        if abs(beta) < 0.00001:
            pp = 0.5 - ((beta ** 2.0) / 24.0) + ((beta ** 4.0) / 720.0)
            qq = (1.0 / 6.0) - ((beta ** 2.0) / 120.0) + ((beta ** 4.0) / 5040.0)
        else:
            pp = (1.0 - np.cos(beta)) / (beta ** 2.0)
            qq = (beta - np.sin(beta)) / (beta ** 3.0)

        c_mat = np.identity(3) + pp * a_mat.array + qq * (a_mat.array @ a_mat.array)
        t = V3(c_mat @ self.vector.array)
        q = LieAlgH1(self.quaternion.array).exp()

        return LieGroupISE3q(UnitQuaternion(q.array), t)

    def vee(self) -> 'V6':
        u = LieAlgH1(self.quaternion.array).vee()
        v = self.vector

        return V6([u[0], u[1], u[2], v[0], v[1], v[2]])

    def __repr__(self) -> str:
        return f"LieAlgISE3q(\n  quaternion: {np.array2string(self.quaternion.array)},\n  ----- \n  vector: {np.array2string(self.vector.array)}\n)"

    def __str__(self) -> str:
        return f"LieAlgISE3q(\n  quaternion: {np.array2string(self.quaternion.array)},\n  ----- \n  vector: {np.array2string(self.vector.array)}\n)"
