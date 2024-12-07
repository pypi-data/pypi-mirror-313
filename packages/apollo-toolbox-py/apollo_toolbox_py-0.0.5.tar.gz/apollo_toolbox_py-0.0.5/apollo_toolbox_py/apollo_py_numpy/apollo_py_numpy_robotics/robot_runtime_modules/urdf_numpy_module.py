from typing import List, Dict, Optional, Type

import numpy as np

from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.urdf_module import *
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.se3_implicit import LieGroupISE3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.lie.se3_implicit_quaternion import LieGroupISE3q
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.quaternions import UnitQuaternion
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3

'''
__all__ = ['ApolloURDFNumpyPose',
           'ApolloURDFNumpyInertia',
           'ApolloURDFNumpyInertial',
           'ApolloURDFNumpyAxis',
           'ApolloURDFNumpyVisual',
           'ApolloURDFNumpyLink',
           'ApolloURDFNumpyJoint',
           'ApolloURDFNumpyCollision',
           'ApolloURDFNumpyModule']
'''


class ApolloURDFNumpyPose:
    def __init__(self, xyz: np.ndarray, rpy: np.ndarray):
        self.xyz = xyz
        self.rpy = rpy
        self.pose: LieGroupISE3q = LieGroupISE3q(UnitQuaternion.from_euler_angles(V3(self.rpy)), V3(self.xyz))
        self.pose_m: LieGroupISE3 = LieGroupISE3(Rotation3.from_euler_angles(V3(self.rpy)), V3(self.xyz))

    @classmethod
    def from_apollo_urdf_pose(cls, pose: ApolloURDFPose):
        return cls(np.array(pose.xyz), np.array(pose.rpy))

    def get_pose_from_lie_group_type(self, lie_group_type: Union[Type[LieGroupISE3q], Type[LieGroupISE3]]) -> Union[LieGroupISE3q, LieGroupISE3]:
        if issubclass(lie_group_type, LieGroupISE3):
            return self.pose_m
        elif issubclass(lie_group_type, LieGroupISE3q):
            return self.pose
        else:
            raise ValueError('not legal argument')

    def __repr__(self):
        return f"ApolloURDFNumpyPose(xyz={self.xyz}, rpy={self.rpy})"


class ApolloURDFNumpyInertia:
    def __init__(self, inertia_matrix: np.ndarray):
        self.inertia_matrix = inertia_matrix

    @classmethod
    def from_apollo_urdf_inertia(cls, inertia: ApolloURDFInertia):
        inertia_matrix = np.array([
            [inertia.ixx, inertia.ixy, inertia.ixz],
            [inertia.ixy, inertia.iyy, inertia.iyz],
            [inertia.ixz, inertia.iyz, inertia.izz]
        ])
        return cls(inertia_matrix)

    def __repr__(self):
        return f"ApolloURDFNumpyInertia(inertia_matrix={self.inertia_matrix})"


class ApolloURDFNumpyInertial:
    def __init__(self, origin: ApolloURDFNumpyPose, mass: ApolloURDFMass, inertia: ApolloURDFNumpyInertia):
        self.origin = origin
        self.mass = mass
        self.inertia = inertia

    @classmethod
    def from_apollo_urdf_inertial(cls, inertial: ApolloURDFInertial):
        origin = ApolloURDFNumpyPose.from_apollo_urdf_pose(inertial.origin)
        inertia = ApolloURDFNumpyInertia.from_apollo_urdf_inertia(inertial.inertia)
        return cls(origin, inertial.mass, inertia)

    def __repr__(self):
        return (f"ApolloURDFNumpyInertial(origin={self.origin}, mass={self.mass}, "
                f"inertia={self.inertia})")


class ApolloURDFNumpyAxis:
    def __init__(self, xyz: V3):
        self.xyz: V3 = xyz

    @classmethod
    def from_apollo_urdf_axis(cls, axis: ApolloURDFAxis):
        return cls(V3(axis.xyz))

    def __repr__(self):
        return f"ApolloURDFNumpyAxis(xyz={self.xyz})"


class ApolloURDFNumpyVisual:
    def __init__(self, name: Optional[str], origin: ApolloURDFNumpyPose, geometry: ApolloURDFGeometry,
                 material: Optional[ApolloURDFMaterial]):
        self.name = name
        self.origin = origin
        self.geometry = geometry
        self.material = material

    @classmethod
    def from_apollo_urdf_visual(cls, visual: ApolloURDFVisual):
        origin = ApolloURDFNumpyPose.from_apollo_urdf_pose(visual.origin)
        return cls(visual.name, origin, visual.geometry, visual.material)

    def __repr__(self):
        return (f"ApolloURDFNumpyVisual(name={self.name}, origin={self.origin}, "
                f"geometry={self.geometry}, material={self.material})")


class ApolloURDFNumpyCollision:
    def __init__(self, name: Optional[str], origin: ApolloURDFNumpyPose, geometry: ApolloURDFGeometry):
        self.name = name
        self.origin = origin
        self.geometry = geometry

    @classmethod
    def from_apollo_urdf_collision(cls, collision: ApolloURDFCollision):
        origin = ApolloURDFNumpyPose.from_apollo_urdf_pose(collision.origin)
        return cls(collision.name, origin, collision.geometry)

    def __repr__(self):
        return (f"ApolloURDFNumpyCollision(name={self.name}, origin={self.origin}, "
                f"geometry={self.geometry})")


class ApolloURDFNumpyLink:
    def __init__(self, name: str, inertial: ApolloURDFNumpyInertial, visual: List[ApolloURDFNumpyVisual],
                 collision: List[ApolloURDFNumpyCollision]):
        self.name = name
        self.inertial = inertial
        self.visual = visual
        self.collision = collision

    @classmethod
    def from_apollo_urdf_link(cls, link: ApolloURDFLink):
        inertial = ApolloURDFNumpyInertial.from_apollo_urdf_inertial(link.inertial)
        visual = [ApolloURDFNumpyVisual.from_apollo_urdf_visual(v) for v in link.visual]
        collision = [ApolloURDFNumpyCollision.from_apollo_urdf_collision(c) for c in link.collision]
        return cls(link.name, inertial, visual, collision)

    def __repr__(self):
        return (f"ApolloURDFNumpyLink(name={self.name}, inertial={self.inertial}, "
                f"visual={self.visual}, collision={self.collision})")


class ApolloURDFNumpyJoint:
    def __init__(self, name: str, joint_type: str, origin: ApolloURDFNumpyPose, parent: Dict[str, str],
                 child: Dict[str, str],
                 axis: ApolloURDFNumpyAxis, limit: ApolloURDFLimit, dynamics: Optional[ApolloURDFDynamics] = None,
                 mimic: Optional[ApolloURDFMimic] = None,
                 safety_controller: Optional[ApolloURDFSafetyController] = None):
        self.name = name
        self.joint_type = joint_type
        self.origin = origin
        self.parent = parent
        self.child = child
        self.axis = axis
        self.limit = limit
        self.dynamics = dynamics
        self.mimic = mimic
        self.safety_controller = safety_controller

    @classmethod
    def from_apollo_urdf_joint(cls, joint: ApolloURDFJoint):
        origin = ApolloURDFNumpyPose.from_apollo_urdf_pose(joint.origin)
        axis = ApolloURDFNumpyAxis.from_apollo_urdf_axis(joint.axis)
        return cls(joint.name, joint.joint_type, origin, joint.parent, joint.child, axis, joint.limit, joint.dynamics,
                   joint.mimic, joint.safety_controller)

    def __repr__(self):
        return (f"ApolloURDFNumpyJoint(name={self.name}, joint_type={self.joint_type}, "
                f"origin={self.origin}, parent={self.parent}, child={self.child}, "
                f"axis={self.axis}, limit={self.limit}, dynamics={self.dynamics}, "
                f"mimic={self.mimic}, safety_controller={self.safety_controller})")


class ApolloURDFNumpyModule:
    def __init__(self, name: str, links: List[ApolloURDFNumpyLink], joints: List[ApolloURDFNumpyJoint],
                 materials: List[ApolloURDFMaterial]):
        self.name = name
        self.links = links
        self.joints = joints
        self.materials = materials

    @classmethod
    def from_urdf_module(cls, urdf_module: ApolloURDFModule):
        links = [ApolloURDFNumpyLink.from_apollo_urdf_link(link) for link in urdf_module.links]
        joints = [ApolloURDFNumpyJoint.from_apollo_urdf_joint(joint) for joint in urdf_module.joints]
        return cls(urdf_module.name, links, joints, urdf_module.materials)

    def __repr__(self):
        return (f"ApolloURDFNumpyModule(name={self.name}, links={self.links}, "
                f"joints={self.joints}, materials={self.materials})")
