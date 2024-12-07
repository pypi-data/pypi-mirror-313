from typing import List, TypeVar, Type, Union

from apollo_toolbox_py.apollo_py.apollo_py_robotics.chain import Chain
from apollo_toolbox_py.apollo_py.apollo_py_robotics.resources_directories import ResourcesSubDirectory

__all__ = ['ChainNumpy']

from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_functions.robot_kinematics_functions import \
    RobotKinematicFunctions

from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V, V3, V6
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.se3_implicit import LieGroupISE3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.se3_implicit_quaternion import LieGroupISE3q


class ChainNumpy(Chain):
    def __init__(self, s: ResourcesSubDirectory):
        super().__init__(s)
        self.urdf_module = s.to_urdf_numpy_module()

    def fk(self, state: V, lie_group_type: Union[Type[LieGroupISE3q], Type[LieGroupISE3]] = LieGroupISE3q) -> List[
        Union[LieGroupISE3q, LieGroupISE3]]:
        return RobotKinematicFunctions.fk(state, self.urdf_module, self.chain_module, self.dof_module, lie_group_type,
                                          V3, V6)

    def reverse_of_fk(self, link_frames: List[Union[LieGroupISE3q, LieGroupISE3]],
                      lie_group_type: Union[Type[LieGroupISE3q], Type[LieGroupISE3]] = LieGroupISE3q):
        return RobotKinematicFunctions.reverse_of_fk(link_frames, self.urdf_module, self.chain_module, self.dof_module,
                                                     lie_group_type, V, V3)
