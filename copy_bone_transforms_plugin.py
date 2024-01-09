'''
MIT License

Copyright (c) 2024 Nuzair

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
    'version': (0, 1, 3),
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
        row.operator("scene.select_base_armature")

        row = layout.row()
        row.label(text="Target Armature:")
        row = layout.row()
        row.prop(context.scene, "target_armature", text="")
        row.operator("scene.select_target_armature")

        row = layout.row()
        row.operator("armature.apply_scale", text="Copy Scale")

        row = layout.row()
        row.operator("armature.apply_transforms", text="Copy Transforms")
        
class ArmatureOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    def get_armature_objects(self, context):
        base_armature = context.scene.base_armature
        target_armature = context.scene.target_armature

        if not base_armature or not target_armature:
            self.report({'ERROR'}, "Both base and target armatures must be selected.")
            return None, None

        base_armature_obj = bpy.data.objects[base_armature]
        target_armature_obj = bpy.data.objects[target_armature]

        return base_armature_obj, target_armature_obj

    def apply_transforms(self, armature_obj):
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


class ApplyScale(ArmatureOperator):
    bl_idname = "armature.apply_scale"
    bl_label = "Apply Scale"

    def execute(self, context):
        base_armature_obj, target_armature_obj = self.get_armature_objects(context)

        if not base_armature_obj or not target_armature_obj:
            return {'CANCELLED'}

        self.apply_transforms(base_armature_obj)

        # Scale the entire target armature to match the base armature
        target_armature_obj.scale = base_armature_obj.scale

        self.report({'INFO'}, "Scale applied successfully.")
        return {'FINISHED'}


class ApplyTransformsOperator(ArmatureOperator):
    bl_idname = "armature.apply_transforms"
    bl_label = "Apply Transforms"

    def execute(self, context):
        base_armature_obj, target_armature_obj = self.get_armature_objects(context)

        if not base_armature_obj or not target_armature_obj:
            return {'CANCELLED'}

        self.apply_transforms(base_armature_obj)

        # Scale the entire target armature to match the base armature
        target_armature_obj.scale = base_armature_obj.scale

        # Highlight the target armature
        target_armature_obj.select_set(True)
        
        self.apply_transforms(target_armature_obj)

        base_bones = base_armature_obj.data.bones

        with bpy.context.temp_override(
            active_object=target_armature_obj
        ):
            bpy.ops.object.mode_set(mode='EDIT')
            for base_bone in base_bones:
                try:
                    bone_edit = target_armature_obj.data.edit_bones[base_bone.name]
                    if bone_edit:
                        bone_edit.matrix = base_bone.matrix_local  # Copy the transformation matrix

                except KeyError:
                    pass
        
            bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Transforms and scales applied successfully.")
        return {'FINISHED'}


class SelectBaseArmature(bpy.types.Operator):
    bl_idname = "scene.select_base_armature"
    bl_label = "Select Base Armature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
        bpy.types.Scene.base_armature = bpy.props.EnumProperty(
            name="Base Armature",
            items=[(arm.name, arm.name, "") for arm in armatures],
        )
        
        return {'FINISHED'}
    

class SelectTargetArmature(bpy.types.Operator):
    bl_idname = "scene.select_target_armature"
    bl_label = "Select Target Armature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
        bpy.types.Scene.target_armature = bpy.props.EnumProperty(
            name="Target Armature",
            items=[(arm.name, arm.name, "") for arm in armatures],
        )
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SelectBaseArmature)
    bpy.utils.register_class(SelectTargetArmature)
    bpy.utils.register_class(ArmatureSelectorPanel)
    bpy.utils.register_class(ApplyScale)
    bpy.utils.register_class(ApplyTransformsOperator)

def unregister():
    bpy.utils.unregister_class(SelectBaseArmature)
    bpy.utils.unregister_class(SelectTargetArmature)
    bpy.utils.unregister_class(ArmatureSelectorPanel)
    bpy.utils.unregister_class(ApplyScale)
    bpy.utils.unregister_class(ApplyTransformsOperator)
    del bpy.types.Scene.base_armature
    del bpy.types.Scene.target_armature

if __name__ == "__main__":
    register()