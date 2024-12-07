from easybpy.easybpy import add_keyframe
import bpy

__all__ = ['KeyframeUtils']


class KeyframeUtils:
    @staticmethod
    def _keyframe_abstract(blender_object: bpy.types.Object, channel_str: str, frame: int):
        add_keyframe(blender_object, channel_str, frame)

    @staticmethod
    def keyframe_visibility(blender_object: bpy.types.Object, frame: int):
        KeyframeUtils._keyframe_abstract(blender_object, 'hide_viewport', frame)
        KeyframeUtils._keyframe_abstract(blender_object, 'hide_render', frame)

    @staticmethod
    def keyframe_rotation(blender_object: bpy.types.Object, frame: int):
        KeyframeUtils._keyframe_abstract(blender_object, 'rotation_euler', frame)

    @staticmethod
    def keyframe_location(blender_object: bpy.types.Object, frame: int):
        KeyframeUtils._keyframe_abstract(blender_object, 'location', frame)

    @staticmethod
    def keyframe_scale(blender_object: bpy.types.Object, frame: int):
        KeyframeUtils._keyframe_abstract(blender_object, 'scale', frame)

    @staticmethod
    def keyframe_transform(blender_object: bpy.types.Object, frame: int):
        KeyframeUtils.keyframe_location(blender_object, frame)
        KeyframeUtils.keyframe_rotation(blender_object, frame)
        KeyframeUtils.keyframe_scale(blender_object, frame)
