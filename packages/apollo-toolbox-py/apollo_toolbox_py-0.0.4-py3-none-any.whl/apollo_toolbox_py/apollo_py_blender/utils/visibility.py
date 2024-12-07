from easybpy.easybpy import unhide_in_viewport, unhide_in_render, hide_in_viewport, hide_in_render
import bpy

__all__ = ['set_visibility']


def set_visibility(blender_object: bpy.types.Object, visible):
    if visible:
        unhide_in_viewport(blender_object)
        unhide_in_render(blender_object)
    else:
        hide_in_viewport(blender_object)
        hide_in_render(blender_object)

    if blender_object is not None:
        for child in blender_object.children:
            set_visibility(child, visible)
