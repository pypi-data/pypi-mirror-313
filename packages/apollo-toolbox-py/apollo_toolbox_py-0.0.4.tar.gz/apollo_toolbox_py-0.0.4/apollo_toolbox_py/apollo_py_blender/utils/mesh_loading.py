from typing import Optional

import bpy
from easybpy.easybpy import rename_object, ao, get_object, so, delete_object, set_parent, move_object_to_collection, \
    rotate_around_global_x, apply_rotation

__all__ = ['BlenderMeshLoader']


class BlenderMeshLoader:
    @staticmethod
    def import_stl(object_name: str, filepath: str, collection_name: Optional[str] = None) -> bpy.types.Object:
        bpy.ops.wm.stl_import(filepath=filepath)
        rename_object(ao(), object_name)
        if collection_name is not None:
            move_object_to_collection(object_name, collection_name)

        apply_rotation(ao())

        return ao()

    @staticmethod
    def import_obj(object_name: str, filepath: str, collection_name: Optional[str] = None, rotate_for_z_up: bool = True) -> bpy.types.Object:
        bpy.ops.wm.obj_import(filepath=filepath)
        rename_object(ao(), object_name)
        if collection_name is not None:
            move_object_to_collection(object_name, collection_name)

        if rotate_for_z_up:
            rotate_around_global_x(-90.0, ao())
            apply_rotation(ao())

        return ao()

    @staticmethod
    def import_dae(object_name: str, filepath: str, collection_name: Optional[str] = None) -> bpy.types.Object:
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        rename_object(ao(), object_name)
        empty_object = ao()
        empty_object.empty_display_size = 0.002
        bpy.ops.wm.collada_import(filepath=filepath)
        for s in so():
            if s.type != 'MESH':
                delete_object(s)
            else:
                set_parent(s, empty_object)

            if collection_name is not None:
                move_object_to_collection(s, collection_name)

        return empty_object

    @staticmethod
    def import_glb(object_name: str, filepath: str, collection_name: Optional[str] = None, rotate_for_z_up: bool = True) -> bpy.types.Object:
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        rename_object(ao(), object_name)
        empty_object = ao()
        empty_object.empty_display_size = 0.002
        bpy.ops.import_scene.gltf(filepath=filepath)
        for s in so():
            if s.type != 'MESH':
                delete_object(s)
            else:
                set_parent(s, empty_object)

            if collection_name is not None:
                move_object_to_collection(s, collection_name)

        if rotate_for_z_up:
            rotate_around_global_x(-90.0, empty_object)
            apply_rotation(empty_object)

        return empty_object

    @staticmethod
    def import_mesh_file(object_name, filepath, collection_name=None):
        split = filepath.split('.')
        if len(split) == 0:
            return
        ext = split[-1]
        if ext == 'stl' or ext == 'STL':
            return BlenderMeshLoader.import_stl(object_name, filepath, collection_name)
        elif ext == 'obj' or ext == 'OBJ':
            return BlenderMeshLoader.import_obj(object_name, filepath, collection_name)
        elif ext == 'dae' or ext == 'DAE':
            return BlenderMeshLoader.import_dae(object_name, filepath, collection_name)
        elif ext == 'glb' or ext == 'gltf' or ext == 'GLB' or ext == 'GLTF':
            return BlenderMeshLoader.import_glb(object_name, filepath, collection_name)
