import bpy
import os
import json
from math import tan, degrees
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
        output_json_train = f"{ngp_properties.output_folder}{ngp_properties.export_name}"

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
            for frame in range(1, bpy.context.scene.frame_end + 1):
                # Set the render output path for each frame
                bpy.context.scene.render.filepath = f"{output_folder}/{frame:04d}"

                # Set the current frame
                bpy.context.scene.frame_set(frame)

                # Set 'BNGP_CAMERA' as the active camera
                bpy.context.scene.camera = camera_object

                # Render the frame
                bpy.ops.render.render(write_still=True)

            # fl_x = bpy.context.scene.render.resolution_x * 0.5 / tan(degrees(camera_object.data.angle_x) * 0.5)
            # fl_y = bpy.context.scene.render.resolution_y * 0.5 / tan(degrees(camera_object.data.angle_y) * 0.5)

            camera_angle_x = camera_object.data.angle_x
            camera_angle_y = camera_object.data.angle_y

            # camera properties
            f_in_mm = camera_object.data.lens # focal length in mm
            scale = bpy.context.scene.render.resolution_percentage / 100
            width_res_in_px = bpy.context.scene.render.resolution_x * scale # width
            height_res_in_px = bpy.context.scene.render.resolution_y * scale # height
            optical_center_x = width_res_in_px / 2
            optical_center_y = height_res_in_px / 2

            # pixel aspect ratios
            size_x = bpy.context.scene.render.pixel_aspect_x * width_res_in_px
            size_y = bpy.context.scene.render.pixel_aspect_y * height_res_in_px
            pixel_aspect_ratio = bpy.context.scene.render.pixel_aspect_x / bpy.context.scene.render.pixel_aspect_y

            # sensor fit and sensor size (and camera angle swap in specific cases)
            if camera_object.data.sensor_fit == 'AUTO':
                sensor_size_in_mm = camera_object.data.sensor_height if width_res_in_px < height_res_in_px else camera_object.data.sensor_width
                if width_res_in_px < height_res_in_px:
                    sensor_fit = 'VERTICAL'
                    camera_angle_x, camera_angle_y = camera_angle_y, camera_angle_x
                elif width_res_in_px > height_res_in_px:
                    sensor_fit = 'HORIZONTAL'
                else:
                    sensor_fit = 'VERTICAL' if size_x <= size_y else 'HORIZONTAL'

            else:
                sensor_fit = camera_object.data.sensor_fit
                if sensor_fit == 'VERTICAL':
                    sensor_size_in_mm = camera_object.data.sensor_height if width_res_in_px <= height_res_in_px else camera_object.data.sensor_width
                    if width_res_in_px <= height_res_in_px:
                        camera_angle_x, camera_angle_y = camera_angle_y, camera_angle_x

            # focal length for horizontal sensor fit
            if sensor_fit == 'HORIZONTAL':
                sensor_size_in_mm = camera_object.data.sensor_width
                s_u = f_in_mm / sensor_size_in_mm * width_res_in_px
                s_v = f_in_mm / sensor_size_in_mm * width_res_in_px * pixel_aspect_ratio

            # focal length for vertical sensor fit
            if sensor_fit == 'VERTICAL':
                s_u = f_in_mm / sensor_size_in_mm * width_res_in_px / pixel_aspect_ratio
                s_v = f_in_mm / sensor_size_in_mm * width_res_in_px

            # Create the transforms_train.json file
            camera_data = {
                "camera_angle_x": camera_object.data.angle_x,
                "camera_angle_y": camera_object.data.angle_y,
                "fl_x": s_u,
                "fl_y": s_v,
                'k1': 0.0,
                'k2': 0.0,
                'p1': 0.0,
                'p2': 0.0,
                "cx": optical_center_x,
                "cy": optical_center_y,
                "w": width_res_in_px,
                "h": height_res_in_px,
                "aabb_scale": int(ngp_properties.aabb_scale),
                "frames": []
            }

            for frame in range(1, bpy.context.scene.frame_end + 1):
                bpy.context.scene.frame_set(frame)
                transform_matrix = camera_object.matrix_world.copy()
                
                # Convertir la matriz a una lista de listas
                transform_list = [[item for item in row] for row in transform_matrix]
                
                camera_data["frames"].append({
                    "file_path": f"train\\{frame:04d}.png",
                    "transform_matrix": transform_list
                })
            # Save the transforms_train.json file
            json_path = os.path.join(output_json_train, 'transforms_train.json')
            with open(json_path, 'w') as json_file:
                json.dump(camera_data, json_file, indent=4)

            print(f"Rendered Animation to {output_folder}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}
        


