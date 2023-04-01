# Copy Bone Transforms
A blender plugin to copy bone transforms of one armature to another armature having same bone names.
Designed to simplify the process of aligning bones of armatures before merging them.


### Installation
- Download the latest plugin from the [released](https://github.com/Nuzair46/Copy-Bone-Transforms/releases/latest).
- In Blender, go to `Edit > Preferences > Add-ons`.
- Click `Install` and select the downloaded zip file.
- Check the box next to "Copy Bone Transforms Plugin" to enable the plugin.

### Usage:

- Open a Blender project containing two armatures with bones having the same name.
- Go to the "3D View" workspace.
- Press N to open the "Properties" panel.
- Scroll down to the "CBT" tab and expand it.
- Click on "Init Scene Properties" to initialize the scene properties.
- In the "Base Armature" dropdown, select the armature containing the desired bone transforms to copy.
- In the "Target Armature" dropdown, select the armature to copy the bone transforms to.
- Click on "Apply Transforms" to copy the bone transforms from the base armature to the target armature.
- The copied transforms will now be applied to the target armature bones with matching names.

Note: If you encounter any issues, ensure that both armatures have the same bone names and that the plugin is correctly installed and enabled in Blender.
