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
from .operators import NGP_OT_AnimateOperator, NGP_OT_RenderOperator
from .panels import NGP_PT_Panel
from .properties import NGP_Properties


def register():
    bpy.utils.register_class(NGP_OT_AnimateOperator)
    bpy.utils.register_class(NGP_OT_RenderOperator) 
    bpy.utils.register_class(NGP_PT_Panel)
    bpy.utils.register_class(NGP_Properties)
    bpy.types.Scene.ngp_props = bpy.props.PointerProperty(type=NGP_Properties)

def unregister():
    bpy.utils.unregister_class(NGP_OT_AnimateOperator)
    bpy.utils.unregister_class(NGP_OT_RenderOperator)
    bpy.utils.unregister_class(NGP_PT_Panel)
    bpy.utils.unregister_class(NGP_Properties)
    del bpy.types.Scene.ngp_props

if __name__ == "__main__":
    register()
