from typing import Optional, Union, Tuple, List

import bpy
import numpy as np
from easybpy.easybpy import (
    collection_exists, create_collection, ao, rename_object,
    move_object_to_collection, copy_object, scale_along_local_z,
    location, rotation, scale_along_local_x, scale_along_local_y, delete_object
)
from apollo_toolbox_py.apollo_py_blender.utils.keyframes import KeyframeUtils
from apollo_toolbox_py.apollo_py_blender.utils.material import BlenderSimpleMaterial
from apollo_toolbox_py.apollo_py_blender.utils.visibility import set_visibility
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V3
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_spatial.rotation_matrices import Rotation3

__all__ = ['BlenderLine', 'BlenderLineSet']


class BlenderLine:
    """
    Class to create and manage a line object in Blender.
    """

    def __init__(self) -> None:
        """
        Initialize the ApolloBlenderLine object with default values.
        """
        self.radius: Optional[float] = None
        self.blender_object: Optional[bpy.types.Object] = None
        self.name: Optional[str] = None
        self.length: float = 2.0

    @staticmethod
    def spawn_new(
            start_point: Union[Tuple[float, float, float], List[float]],
            end_point: Union[Tuple[float, float, float], List[float]],
            radius: float = 0.01, vertices: int = 6,
            name: Optional[str] = None, collection_name: str = 'Lines',
            material: Optional[BlenderSimpleMaterial] = None
    ) -> 'BlenderLine':
        """
        Static method to create a new line object in Blender.

        Parameters:
        - start_point: Starting point of the line.
        - end_point: Ending point of the line.
        - radius: Radius of the line.
        - vertices: Number of vertices of the line.
        - name: Optional name of the line object.
        - collection_name: Name of the collection to which the line belongs.
        - material: Optional material to apply to the line.

        Returns:
        - ApolloBlenderLine: A new instance of ApolloBlenderLine.
        """
        line = BlenderLine()
        line.radius = radius
        line.name = name

        if collection_name is not None:
            exists = collection_exists(collection_name)
            if not exists:
                create_collection(collection_name)
        bpy.ops.mesh.primitive_cylinder_add(depth=2, vertices=vertices, scale=(radius, radius, 1))
        object = ao()
        if name is not None:
            rename_object(object, name)

        if collection_name is not None:
            move_object_to_collection(object, collection_name)

        line.blender_object = object
        line.name = line.blender_object.name

        line.change_pose(start_point, end_point)

        if material is not None:
            material.apply_material_to_object(line.blender_object)

        return line

    @staticmethod
    def spawn_new_copy(
            line: 'BlenderLine',
            start_point: Union[Tuple[float, float, float], List[float]],
            end_point: Union[Tuple[float, float, float], List[float]],
            radius: float = 0.01, name: Optional[str] = None,
            collection_name: str = 'Lines',
            material: Optional[BlenderSimpleMaterial] = None
    ) -> 'BlenderLine':
        """
        Static method to create a copy of an existing line object in Blender.

        Parameters:
        - line: The original line object to copy.
        - start_point: Starting point of the new line.
        - end_point: Ending point of the new line.
        - radius: Radius of the new line.
        - name: Optional name of the new line object.
        - collection_name: Name of the collection to which the new line belongs.
        - material: Optional material to apply to the new line.

        Returns:
        - ApolloBlenderLine: A new instance of ApolloBlenderLine.
        """
        new_mesh = copy_object(line.blender_object, collection_name)
        if name is not None:
            rename_object(new_mesh, name)
        out_line = BlenderLine()
        out_line.radius = radius
        out_line.blender_object = new_mesh
        out_line.name = name
        out_line.length = line.length

        out_line.change_pose(start_point, end_point)

        if material is not None:
            material.apply_material_to_object(out_line.blender_object)

        return out_line

    def change_pose(
            self, start_point: Union[Tuple[float, float, float], List[float]],
            end_point: Union[Tuple[float, float, float], List[float]]
    ) -> None:
        """
        Change the position and orientation of the line object.

        Parameters:
        - start_point: New starting point of the line.
        - end_point: New ending point of the line.
        """
        s = np.array(start_point)
        e = np.array(end_point)
        d = e - s
        center = (s + e) / 2.0
        length = np.linalg.norm(d)

        r = Rotation3.from_look_at(V3([d[0], d[1], d[2]]), V3([0, 0, 1]))
        euler_angles = r.to_euler_angles()

        scale_along_local_z((1.0 / self.length) * length, self.blender_object)
        location(self.blender_object, [center[0], center[1], center[2]])
        rotation(self.blender_object, [euler_angles[0], euler_angles[1], euler_angles[2]])

        self.length = length

    def change_radius(self, radius: float) -> None:
        """
        Change the radius of the line object.

        Parameters:
        - radius: New radius of the line.
        """
        scale_along_local_x((1.0 / self.radius) * radius, self.blender_object)
        scale_along_local_y((1.0 / self.radius) * radius, self.blender_object)

        self.radius = radius


class BlenderLineSet:
    """
    Class to manage a set of line objects in Blender.
    """

    def __init__(
            self, num_lines: int, collection_name: str = 'LineSet',
            material_type: str = 'Emission',
            default_color: Optional[Tuple[float, float, float, float]] = None,
            linked_material_for_each_line: bool = True
    ) -> None:
        """
        Initialize the ApolloBlenderLineSet object with a specified number of lines.

        Parameters:
        - num_lines: Number of lines to create in the set.
        - collection_name: Name of the collection to which the lines belong.
        - material_type: Type of material to apply to the lines.
        - default_color: Default color of the lines.
        - linked_material_for_each_line: Whether each line has a linked material or not.
        """
        self.lines: List[BlenderLine] = []
        self.materials: List[BlenderSimpleMaterial] = []

        line_to_copy: BlenderLine = BlenderLine.spawn_new([0, 0, 0], [0, 0, 1], collection_name=None)

        if default_color is None:
            default_color = (0.2, 0.2, 0.2, 1)

        base_material: BlenderSimpleMaterial = BlenderSimpleMaterial(
            material_type=material_type, default_color=default_color
        )
        base_material.keyframe_material(0)

        for i in range(num_lines):
            line_copy: BlenderLine = BlenderLine.spawn_new_copy(
                line_to_copy, [0, 0, 0], [0, 0, 1], collection_name=collection_name
            )
            if linked_material_for_each_line:
                base_material.apply_material_to_object(line_copy.blender_object)
                self.materials.append(base_material)
            else:
                new_material: BlenderSimpleMaterial = BlenderSimpleMaterial(
                    material_type=material_type, default_color=default_color
                )
                new_material.apply_material_to_object(line_copy.blender_object)
                new_material.keyframe_material(0)
                self.materials.append(new_material)

            set_visibility(line_copy.blender_object, False)
            KeyframeUtils.keyframe_visibility(line_copy.blender_object, 0)
            self.lines.append(line_copy)

        delete_object(line_to_copy.blender_object)

        self.per_frame_next_available_line: List[int] = []

    def set_line_at_frame(
            self, start_point: Union[Tuple[float, float, float], List[float]],
            end_point: Union[Tuple[float, float, float], List[float]], frame: int,
            radius: float = 0.01, color: Optional[Tuple[float, float, float, float]] = None
    ) -> None:
        """
        Set the position, orientation, and visibility of a line at a specific frame.

        Parameters:
        - start_point: Starting point of the line.
        - end_point: Ending point of the line.
        - frame: Frame number at which the line is set.
        - radius: Radius of the line.
        - color: Color of the line.
        """
        while len(self.per_frame_next_available_line) <= frame:
            self.per_frame_next_available_line.append(0)

        if len(self.lines) <= self.per_frame_next_available_line[frame]:
            print(f'WARNING: Not enough lines at frame {frame} to draw the given line.')
            return

        curr_line: BlenderLine = self.lines[self.per_frame_next_available_line[frame]]
        curr_line.change_pose(start_point, end_point)
        curr_line.change_radius(radius)
        set_visibility(curr_line.blender_object, True)

        KeyframeUtils.keyframe_transform(curr_line.blender_object, frame)
        KeyframeUtils.keyframe_visibility(curr_line.blender_object, frame)

        set_visibility(curr_line.blender_object, False)
        KeyframeUtils.keyframe_visibility(curr_line.blender_object, frame + 1)

        if color is not None:
            material: BlenderSimpleMaterial = self.materials[self.per_frame_next_available_line[frame]]
            material.set_color(color)
            material.keyframe_material(frame)

        self.per_frame_next_available_line[frame] += 1
