# Copy Bone Transforms

A blender plugin to copy bone transforms of one armature to another armature having same bone names.
Designed to simplify the process of aligning bones of armatures before merging them. Mainly intended for use with the [CATS](https://github.com/absolute-quantum/cats-blender-plugin) for VRChat avatars.

### Installation

- Download the latest plugin from the [releases](https://github.com/Nuzair46/Copy-Bone-Transforms/releases/latest).
- In Blender, go to `Edit > Preferences > Add-ons`.
- Click `Install` and select the downloaded zip file.
- Check the box next to "Copy Bone Transforms Plugin" to enable the plugin.

### Video Example:

https://github.com/Nuzair46/Copy-Bone-Transforms/blob/main/videos/final.gif

### Usage:

- Open a Blender project containing two armatures with bones having the same name.
- Make sure the bones of new armature is same as base armature. If not, rename the existing bones of new armature to match the base armature.
- Go to the "3D View" workspace.
- Make sure the base and target armatures are aligned in the 3D space in any 2 axes.
- Press N to open the "Properties" panel.
- Scroll down to the "CBT" tab and expand it.
- In the "Base Armature" dropdown, select the armature containing the desired bone transforms to copy.
- In the "Target Armature" dropdown, select the armature to copy the bone transforms to.
- Click "Copy Scale" if you only want to copy the armature scale.
- Click on "Copy Transforms" to copy the bone transforms from the base armature to the target armature.
- The copied transforms will now be applied to the target armature bones with matching names.
- Further, use CATS plugin to merge the armatures.

#### Note:

- If you encounter any issues, ensure that both armatures have the same bone names and that the plugin is correctly installed and enabled in Blender.
- This addon is not failproof and may not work as it should at this moment. For all its worth, take it as a poc.
