import bpy

class NGP_Properties(bpy.types.PropertyGroup):
    camera_radius: bpy.props.FloatProperty(name="Camera Radius", default=3.3)
    num_frames: bpy.props.EnumProperty(
        name="",
        description="Select the number of frames for the animation",
        items=[
            ("50", "50", "50 frames"),
            ("75", "75", "75 frames"),
            ("100", "100", "100 frames"),
            ("125", "125", "125 frames"),
            ("150", "150", "150 frames")
        ],
        default="100"
    )
    aabb_scale: bpy.props.IntProperty(
        name="AABB",
        description="Set the scale of the AABB",
        default=4,
        )
     # New: Export name property
    export_name: bpy.props.StringProperty(name="", default="dataset")

    # New: Output folder property
    output_folder: bpy.props.StringProperty(
        name="",
        default="",
        subtype='DIR_PATH'
    )

