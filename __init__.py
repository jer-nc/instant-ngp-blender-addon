bl_info = {
    "name": "Synthetic NGP Dataset COS",
    "author": "REJDEVX",
    "version": (1, 0),
    "blender": (3, 6, 1),
    "description": "Synthetic NGP Dataset COS",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import bpy
import math

class NGP_OT_AnimateOperator(bpy.types.Operator):
    bl_idname = "ngp.animate_operator"
    bl_label = "Animate Camera"

    def execute(self, context):
        create_empty(self)
        create_camera(self)
        animate_camera(self, context.scene.ngp_props.camera_radius, 100)
        return {'FINISHED'}

class NGP_PT_Panel(bpy.types.Panel):
    bl_idname = "ngp.panel"
    bl_label = "NGP Panel"
    bl_category = "NGP2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.ngp_props, "camera_radius")
        layout.operator("ngp.animate_operator")

class NGP_Properties(bpy.types.PropertyGroup):
    camera_radius: bpy.props.FloatProperty(name="Camera Radius", default=10.0)

def create_empty(self):
    if 'BNGP_EMPTY' not in bpy.context.scene.objects:
        bpy.ops.object.empty_add(location=(0, 0, 0))
        bpy.context.active_object.name = 'BNGP_EMPTY'

def create_camera(self):
    if 'BNGP_CAMERA' not in bpy.context.scene.objects:
        bpy.ops.object.camera_add(location=(10, 0, 0))
        bpy.context.active_object.name = 'BNGP_CAMERA'
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.context.scene.objects['BNGP_EMPTY']
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'

def animate_camera(self, radius, num_frames):
    scene = bpy.context.scene
    camera = bpy.context.scene.objects['BNGP_CAMERA']
    empty = bpy.context.scene.objects['BNGP_EMPTY']

    for frame in range(num_frames):
        angle = (frame / (num_frames // 6)) * 2 * math.pi

        # Rotación alrededor de los ejes X, Y y Z
        if frame < num_frames // 6:
            x = math.cos(angle)
            y = 0
            z = math.sin(angle)
        elif frame < 2*num_frames // 6:
            x = 0
            y = math.cos(angle - math.pi/3)
            z = math.sin(angle - math.pi/3)
        elif frame < 3*num_frames // 6:
            x = math.cos(angle - 2*math.pi/3)
            y = math.sin(angle - 2*math.pi/3)
            z = 0
        elif frame < 4*num_frames // 6:
            x = math.cos(angle - math.pi)
            y = math.sin(angle - math.pi)
            z = math.sin(angle - math.pi)
        elif frame < 5*num_frames // 6:
            x = math.sin(angle - 4*math.pi/3)
            y = math.cos(angle - 4*math.pi/3)
            z = math.sin(angle - 4*math.pi/3)
        else:
            x = math.sin(angle - 5*math.pi/3)
            y = math.sin(angle - 5*math.pi/3)
            z = math.cos(angle - 5*math.pi/3)

        # Normalizar la posición de la cámara y multiplicar por el radio
        norm = math.sqrt(x**2 + y**2 + z**2)
        camera.location.x = radius * x / norm
        camera.location.y = radius * y / norm
        camera.location.z = radius * z / norm

        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

        scene.frame_end = frame






def register():
    bpy.utils.register_class(NGP_OT_AnimateOperator)
    bpy.utils.register_class(NGP_PT_Panel)
    bpy.utils.register_class(NGP_Properties)
    bpy.types.Scene.ngp_props = bpy.props.PointerProperty(type=NGP_Properties)

def unregister():
    bpy.utils.unregister_class(NGP_OT_AnimateOperator)
    bpy.utils.unregister_class(NGP_PT_Panel)
    bpy.utils.unregister_class(NGP_Properties)
    del bpy.types.Scene.ngp_props

if __name__ == "__main__":
    register()
