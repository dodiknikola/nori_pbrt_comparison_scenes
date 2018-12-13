import bpy
import os

# get the path where the blend file is located
basedir = bpy.path.abspath('//')
export_to = 'pbrt'

# deselect all objects
bpy.ops.object.select_all(action='DESELECT')    

# loop through all the objects in the scene
scene = bpy.context.scene
for ob in scene.objects:
    # make the current object active and select it
    scene.objects.active = ob
    ob.select = True

    # make sure that we only export meshes
    if ob.type == 'MESH':
        # export the currently selected object to its own file based on its name
        if export_to == 'nori':
            bpy.ops.export_scene.obj(
                    filepath=os.path.join(basedir, export_to, 'models', ob.name + '.obj'),
                    use_selection=True,
                    use_normals=True,
                    use_uvs=True,
                    use_mesh_modifiers=True,
                    use_materials=False,
                    use_triangles=True
                    )
        elif export_to == 'pbrt':
            bpy.ops.export_mesh.ply(
                    filepath=os.path.join(basedir, export_to, 'models', ob.name + '.ply'),
                    use_normals=True,
                    use_mesh_modifiers=True,
                    use_uv_coords=True
                    )
    # deselect the object and move on to another if any more are left
    ob.select = False   