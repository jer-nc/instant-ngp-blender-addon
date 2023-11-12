import bpy
from .utils import create_empty, create_camera, create_aabb, animate_camera

class NGP_OT_AnimateOperator(bpy.types.Operator):
    bl_idname = "ngp.animate_operator"
    bl_label = "Update Animation"

    def execute(self, context):
        center_empty = create_empty(self, 'BNGP_EMPTY', (0, 0, 0))
        create_camera(self)
        create_aabb(self, context, center_empty)
        animate_camera(self, context.scene.ngp_props.camera_radius, context.scene.ngp_props.num_frames, context.scene.ngp_props.aabb_scale)
        return {'FINISHED'}
