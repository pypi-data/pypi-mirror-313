from typing import List, Optional, Dict, Union


class ApolloURDFPose:
    def __init__(self, xyz: List[float], rpy: List[float]):
        self.xyz = xyz
        self.rpy = rpy

    def __repr__(self):
        return f"ApolloURDFPose(xyz={self.xyz}, rpy={self.rpy})"


class ApolloURDFMass:
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"ApolloURDFMass(value={self.value})"


class ApolloURDFInertia:
    def __init__(self, ixx: float, ixy: float, ixz: float, iyy: float, iyz: float, izz: float):
        self.ixx = ixx
        self.ixy = ixy
        self.ixz = ixz
        self.iyy = iyy
        self.iyz = iyz
        self.izz = izz

    def __repr__(self):
        return f"ApolloURDFInertia(ixx={self.ixx}, ixy={self.ixy}, ixz={self.ixz}, iyy={self.iyy}, iyz={self.iyz}, izz={self.izz})"


class ApolloURDFInertial:
    def __init__(self, origin: ApolloURDFPose, mass: ApolloURDFMass, inertia: ApolloURDFInertia):
        self.origin = origin
        self.mass = mass
        self.inertia = inertia

    def __repr__(self):
        return f"ApolloURDFInertial(origin={self.origin}, mass={self.mass}, inertia={self.inertia})"


class ApolloURDFGeometry:
    def __init__(self, box: Optional[Dict[str, List[float]]] = None, cylinder: Optional[Dict[str, float]] = None,
                 capsule: Optional[Dict[str, float]] = None, sphere: Optional[Dict[str, float]] = None,
                 mesh: Optional[Dict[str, Union[str, List[float]]]] = None):
        self.box = box
        self.cylinder = cylinder
        self.capsule = capsule
        self.sphere = sphere
        self.mesh = mesh

    def __repr__(self):
        return f"ApolloURDFGeometry(box={self.box}, cylinder={self.cylinder}, capsule={self.capsule}, sphere={self.sphere}, mesh={self.mesh})"


class ApolloURDFColor:
    def __init__(self, rgba: List[float]):
        self.rgba = rgba

    def __repr__(self):
        return f"ApolloURDFColor(rgba={self.rgba})"


class ApolloURDFTexture:
    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self):
        return f"ApolloURDFTexture(filename={self.filename})"


class ApolloURDFMaterial:
    def __init__(self, name: str, color: Optional[ApolloURDFColor] = None, texture: Optional[ApolloURDFTexture] = None):
        self.name = name
        self.color = color
        self.texture = texture

    def __repr__(self):
        return f"ApolloURDFMaterial(name={self.name}, color={self.color}, texture={self.texture})"


class ApolloURDFVisual:
    def __init__(self, name: Optional[str], origin: ApolloURDFPose, geometry: ApolloURDFGeometry,
                 material: Optional[ApolloURDFMaterial]):
        self.name = name
        self.origin = origin
        self.geometry = geometry
        self.material = material

    def __repr__(self):
        return f"ApolloURDFVisual(name={self.name}, origin={self.origin}, geometry={self.geometry}, material={self.material})"


class ApolloURDFCollision:
    def __init__(self, name: Optional[str], origin: ApolloURDFPose, geometry: ApolloURDFGeometry):
        self.name = name
        self.origin = origin
        self.geometry = geometry

    def __repr__(self):
        return f"ApolloURDFCollision(name={self.name}, origin={self.origin}, geometry={self.geometry})"


class ApolloURDFLink:
    def __init__(self, name: str, inertial: ApolloURDFInertial, visual: List[ApolloURDFVisual],
                 collision: List[ApolloURDFCollision]):
        self.name = name
        self.inertial = inertial
        self.visual = visual
        self.collision = collision

    def __repr__(self):
        return f"ApolloURDFLink(name={self.name}, inertial={self.inertial}, visual={self.visual}, collision={self.collision})"


class ApolloURDFAxis:
    def __init__(self, xyz: List[float]):
        self.xyz = xyz

    def __repr__(self):
        return f"ApolloURDFAxis(xyz={self.xyz})"


class ApolloURDFLimit:
    def __init__(self, lower: float, upper: float, effort: float, velocity: float):
        self.lower = lower
        self.upper = upper
        self.effort = effort
        self.velocity = velocity

    def __repr__(self):
        return f"ApolloURDFLimit(lower={self.lower}, upper={self.upper}, effort={self.effort}, velocity={self.velocity})"


class ApolloURDFDynamics:
    def __init__(self, damping: float, friction: float):
        self.damping = damping
        self.friction = friction

    def __repr__(self):
        return f"ApolloURDFDynamics(damping={self.damping}, friction={self.friction})"


class ApolloURDFMimic:
    def __init__(self, joint: str, multiplier: Optional[float] = None, offset: Optional[float] = None):
        self.joint = joint
        self.multiplier = multiplier
        self.offset = offset

    def __repr__(self):
        return f"ApolloURDFMimic(joint={self.joint}, multiplier={self.multiplier}, offset={self.offset})"


class ApolloURDFSafetyController:
    def __init__(self, soft_lower_limit: float, soft_upper_limit: float, k_position: float, k_velocity: float):
        self.soft_lower_limit = soft_lower_limit
        self.soft_upper_limit = soft_upper_limit
        self.k_position = k_position
        self.k_velocity = k_velocity

    def __repr__(self):
        return f"ApolloURDFSafetyController(soft_lower_limit={self.soft_lower_limit}, soft_upper_limit={self.soft_upper_limit}, k_position={self.k_position}, k_velocity={self.k_velocity})"


class ApolloURDFJoint:
    def __init__(self, name: str, joint_type: str, origin: ApolloURDFPose, parent: Dict[str, str],
                 child: Dict[str, str],
                 axis: ApolloURDFAxis, limit: ApolloURDFLimit, dynamics: Optional[ApolloURDFDynamics] = None,
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

    def __repr__(self):
        return f"ApolloURDFJoint(name={self.name}, joint_type={self.joint_type}, origin={self.origin}, parent={self.parent}, child={self.child}, axis={self.axis}, limit={self.limit}, dynamics={self.dynamics}, mimic={self.mimic}, safety_controller={self.safety_controller})"


class ApolloURDFModule:
    def __init__(self, name: str, links: List[ApolloURDFLink], joints: List[ApolloURDFJoint],
                 materials: List[ApolloURDFMaterial]):
        self.name = name
        self.links = links
        self.joints = joints
        self.materials = materials

    def __repr__(self):
        return f"ApolloURDFModule(name={self.name}, links={self.links}, joints={self.joints}, materials={self.materials})"

    @classmethod
    def from_dict(cls, data: Dict):
        links = [ApolloURDFLink(
            name=link['name'],
            inertial=ApolloURDFInertial(
                origin=ApolloURDFPose(**link['inertial']['origin']),
                mass=ApolloURDFMass(**link['inertial']['mass']),
                inertia=ApolloURDFInertia(**link['inertial']['inertia'])
            ),
            visual=[ApolloURDFVisual(
                name=visual.get('name'),
                origin=ApolloURDFPose(**visual['origin']),
                geometry=ApolloURDFGeometry(
                    box=visual['geometry'].get('Box'),
                    cylinder=visual['geometry'].get('Cylinder'),
                    capsule=visual['geometry'].get('Capsule'),
                    sphere=visual['geometry'].get('Sphere'),
                    mesh=visual['geometry'].get('Mesh')
                ),
                material=ApolloURDFMaterial(
                    name=visual['material']['name'],
                    color=ApolloURDFColor(**visual['material']['color']) if visual['material']['color'] else None,
                    texture=ApolloURDFTexture(**visual['material']['texture']) if visual['material'][
                        'texture'] else None
                ) if visual.get('material') else None
            ) for visual in link['visual']],
            collision=[ApolloURDFCollision(
                name=collision.get('name'),
                origin=ApolloURDFPose(**collision['origin']),
                geometry=ApolloURDFGeometry(
                    box=collision['geometry'].get('Box'),
                    cylinder=collision['geometry'].get('Cylinder'),
                    capsule=collision['geometry'].get('Capsule'),
                    sphere=collision['geometry'].get('Sphere'),
                    mesh=collision['geometry'].get('Mesh')
                )
            ) for collision in link['collision']]
        ) for link in data['links']]

        joints = [ApolloURDFJoint(
            name=joint['name'],
            joint_type=joint['joint_type'],
            origin=ApolloURDFPose(**joint['origin']),
            parent=joint['parent'],
            child=joint['child'],
            axis=ApolloURDFAxis(**joint['axis']),
            limit=ApolloURDFLimit(**joint['limit']),
            dynamics=ApolloURDFDynamics(**joint['dynamics']) if joint['dynamics'] else None,
            mimic=ApolloURDFMimic(**joint['mimic']) if joint.get('mimic') else None,
            safety_controller=ApolloURDFSafetyController(**joint['safety_controller']) if joint.get(
                'safety_controller') else None
        ) for joint in data['joints']]

        materials = [ApolloURDFMaterial(
            name=material['name'],
            color=ApolloURDFColor(**material['color']) if material.get('color') else None,
            texture=ApolloURDFTexture(**material['texture']) if material.get('texture') else None
        ) for material in data.get('materials', [])]

        return cls(
            name=data['name'],
            links=links,
            joints=joints,
            materials=materials
        )

'''
__all__ = ['ApolloURDFVisual',
           'ApolloURDFPose',
           'ApolloURDFDynamics',
           'ApolloURDFInertia',
           'ApolloURDFCollision',
           'ApolloURDFAxis',
           'ApolloURDFInertial',
           'ApolloURDFLink',
           'ApolloURDFMass',
           'ApolloURDFGeometry',
           'ApolloURDFJoint',
           'ApolloURDFLimit',
           'ApolloURDFMimic',
           'ApolloURDFLimit',
           'ApolloURDFTexture',
           'ApolloURDFMaterial',
           'ApolloURDFColor',
           'ApolloURDFModule',
           'ApolloURDFSafetyController']
'''
