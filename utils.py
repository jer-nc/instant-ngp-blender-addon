import bpy
import math

def create_empty(self, name, location):
    if name not in bpy.context.scene.objects:
        bpy.ops.object.empty_add(location=location)
        bpy.context.active_object.name = name
        return bpy.context.active_object
    else:
        return bpy.context.scene.objects[name]

def create_camera(self):
    if 'BNGP_CAMERA' not in bpy.context.scene.objects:
        bpy.ops.object.camera_add(location=(10, 0, 0))
        bpy.context.active_object.name = 'BNGP_CAMERA'
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.context.scene.objects['BNGP_EMPTY']
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'

def create_aabb(self, context, center_empty):
    if 'BNGP_AABB' not in bpy.context.scene.objects:
        aabb_location = center_empty.location
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=aabb_location)
        aabb_cube = bpy.context.active_object
        aabb_cube.name = 'BNGP_AABB'
        aabb_cube.display_type = 'WIRE'
        aabb_cube.hide_render = True
        aabb_cube.scale = (context.scene.ngp_props.aabb_scale, context.scene.ngp_props.aabb_scale, context.scene.ngp_props.aabb_scale)
        return aabb_cube

def animate_camera(self, radius, num_frames, aabb_scale):
    num_frames = int(num_frames)  # Añade esta línea para convertir num_frames a un entero
    scene = bpy.context.scene
    camera = bpy.context.scene.objects['BNGP_CAMERA']
    empty = bpy.context.scene.objects['BNGP_EMPTY']
    aabb_empty = bpy.context.scene.objects.get('BNGP_AABB')


    camera.animation_data_clear()

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
        camera.location.x = empty.location.x + radius * x / norm
        camera.location.y = empty.location.y + radius * y / norm
        camera.location.z = empty.location.z + radius * z / norm

        aabb_empty.location.x = empty.location.x 
        aabb_empty.location.y = empty.location.y 
        aabb_empty.location.z = empty.location.z 

        # Actualizar la escala del AABB utilizando la nueva propiedad
        aabb_empty.scale = (aabb_scale, aabb_scale, aabb_scale)

        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

        scene.frame_end = frame


