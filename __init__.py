'''
MIT License

Copyright (c) 2023 Nuzair

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import bpy

bl_info = {
    'name': 'Copy Bone Transforms Plugin',
    'category': '3D View',
    'author': 'Nuzair46',
    'description': 'A tool designed to shorten steps needed to import and optimize models into VRChat',
    'version': (0, 1, 0),
    'blender': (2, 80, 0),
    'wiki_url': 'https://github.com/Nuzair46/Copy-Bone-Transforms',
    'tracker_url': 'https://github.com/Nuzair46/Copy-Bone-Transforms',
    'warning': '',
}

class ArmatureSelectorPanel(bpy.types.Panel):
    bl_label = "Copy Bone Transforms"
    bl_idname = "OBJECT_PT_armature_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CBT"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Base Armature:")
        row = layout.row()
        row.prop(context.scene, "base_armature", text="")

        row = layout.row()
        row.label(text="Target Armature:")
        row = layout.row()
        row.prop(context.scene, "target_armature", text="")

        row = layout.row()
        row.operator("armature.apply_transforms", text="Apply Transforms")

class ApplyTransformsOperator(bpy.types.Operator):
    bl_idname = "armature.apply_transforms"
    bl_label = "Apply Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        base_armature = context.scene.base_armature
        target_armature = context.scene.target_armature

        if not base_armature or not target_armature:
            self.report({'ERROR'}, "Both base and target armatures must be selected.")
            return {'CANCELLED'}

        base_bones = bpy.data.armatures[base_armature].bones

        target_armature_obj = bpy.data.objects[target_armature]
        bpy.context.view_layer.objects.active = target_armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        for base_bone in base_bones:
            try:
                bone_pose = target_armature_obj.pose.bones[base_bone.name]
                if bone_pose:
                    bone_pose.matrix = base_bone.matrix_local

            except KeyError:
                pass

        self.report({'INFO'}, "Transforms applied successfully.")
        return {'FINISHED'}

armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
 
class InitSceneProperties(bpy.types.Operator):
    bl_idname = "scene.init_scene_properties"
    bl_label = "Init Scene Properties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.types.Scene.base_armature = bpy.props.EnumProperty(
            name="Base Armature",
            items=[(arm.name, arm.name, "") for arm in armatures],
        )
        bpy.types.Scene.target_armature = bpy.props.EnumProperty(
            name="Target Armature",
            items=[(arm.name, arm.name, "") for arm in armatures],
        )
        return {'FINISHED'}

def register():
    bpy.utils.register_class(InitSceneProperties)
    bpy.utils.register_class(ArmatureSelectorPanel)
    bpy.utils.register_class(ApplyTransformsOperator)
    bpy.types.Scene.base_armature = bpy.props.EnumProperty(
        name="Base Armature",
        items=[(arm.name, arm.name, "") for arm in armatures],
    )
    bpy.types.Scene.target_armature = bpy.props.EnumProperty(
        name="Target Armature",
        items=[(arm.name, arm.name, "") for arm in armatures],
    )
    

def unregister():
    bpy.utils.unregister_class(InitSceneProperties)
    bpy.utils.unregister_class(ArmatureSelectorPanel)
    bpy.utils.unregister_class(ApplyTransformsOperator)
    del bpy.types.Scene.base_armature
    del bpy.types.Scene.target_armature

if __name__ == "__main__":
    register()
