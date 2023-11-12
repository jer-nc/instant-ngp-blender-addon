import bpy

class NGP_PT_Panel(bpy.types.Panel):
    bl_idname = "ngp.panel"
    bl_label = "BNGP Configuration"
    bl_category = "BNGP Dataset"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Camera Settings")
        layout.prop(context.scene.ngp_props, "camera_radius")
        # Label frame number
        layout.label(text="Number of Frames")
        layout.prop(context.scene.ngp_props, "num_frames")
        # Label AABB scale
        layout.label(text="AABB Scale")
        layout.prop(context.scene.ngp_props, "aabb_scale")
        layout.separator()
        # Update animation button
        layout.operator("ngp.animate_operator")
