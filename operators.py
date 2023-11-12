import bpy
import os
import json
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
    
class NGP_OT_RenderOperator(bpy.types.Operator):
    bl_idname = "ngp.render_operator"
    bl_label = "Render Animation"

    def execute(self, context):
        # Accessing NGP_Properties instance here
        ngp_properties = context.scene.ngp_props
        output_folder = f"{ngp_properties.output_folder}{ngp_properties.export_name}/train"
        output_json_train = f"{ngp_properties.output_folder}{ngp_properties.export_name}/transforms_train.json"

        try:
            # Ensure the output folder exists, create it if not
            os.makedirs(output_folder, exist_ok=True)

            # Check if 'BNGP_CAMERA' exists
            camera_object = bpy.context.scene.objects.get('BNGP_CAMERA')
            if not camera_object:
                self.report({'ERROR'}, "Camera 'BNGP_CAMERA' not found. Please create the camera.")
                return {'CANCELLED'}

            bpy.context.scene.frame_end = int(ngp_properties.num_frames)

            # Set film transparency
            bpy.context.scene.render.film_transparent = True

            # Loop through all frames and render
            for frame in range(0, bpy.context.scene.frame_end + 1):
                # Set the render output path for each frame
                bpy.context.scene.render.filepath = f"{output_folder}/{frame:04d}"

                # Set the current frame
                bpy.context.scene.frame_set(frame)

                # Set 'BNGP_CAMERA' as the active camera
                bpy.context.scene.camera = camera_object

                # Render the frame
                bpy.ops.render.render(write_still=True)

            print(f"Rendered Animation to {output_folder}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}
        


