# Jalankan dengan: blender -b --factory-startup --python tools/render_scene.py
# Membuat render PNG bus mewah sedang melaju di jalan kota.
import bpy
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MODEL = os.path.join(ROOT, "assets", "models", "bus.glb")
OUT_DIR = os.path.join(ROOT, "assets", "design")
OUT_FILE = os.path.join(OUT_DIR, "bus-render.png")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = "PNG"

# Impor model bus yang sudah dibuat make_bus.py
bpy.ops.import_scene.gltf(filepath=MODEL)
bus_objs = [o for o in bpy.context.selected_objects if o.type == "MESH"]
for o in bus_objs:
    if o.parent is None:
        o.location = (0, 0, 0.5)
        o.rotation_euler = (0, 0, math.radians(-15))

# Cat mewah: bodi hitam-emas dan kaca gelap
def mat(name, color, metallic=0.0, rough=0.4, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = color
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit > 0:
        b.inputs["Emission Color"].default_value = color
        b.inputs["Emission Strength"].default_value = emit
    return m

body = mat("BlackGold", (0.02, 0.02, 0.02, 1), metallic=0.6, rough=0.25)
gold = mat("Gold", (1.0, 0.72, 0.2, 1), metallic=1.0, rough=0.2)
glass = mat("Glass", (0.02, 0.05, 0.08, 1), metallic=0.0, rough=0.05)
light = mat("Headlight", (1.0, 0.95, 0.7, 1), emit=12.0)

for o in bus_objs:
    o.data.materials.clear()
    o.data.materials.append(body)

# Jalan aspal
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
road = bpy.context.active_object
road.scale = (60, 12, 1)
road.data.materials.append(mat("Asphalt", (0.05, 0.05, 0.06, 1), rough=0.8))

# Trotoar
for side in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, side * 7.5, 0.1))
    walk = bpy.context.active_object
    walk.scale = (60, 2.5, 0.1)
    walk.data.materials.append(mat("Sidewalk", (0.45, 0.45, 0.48, 1), rough=0.9))

# Garis jalan putus-putus
for i in range(-10, 11):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 3.0, 0, 0.01))
    dash = bpy.context.active_object
    dash.scale = (1.2, 0.12, 0.01)
    dash.data.materials.append(mat("Lane", (1, 0.95, 0.6, 1), emit=1.5))

# Gedung kota di kedua sisi
import random
random.seed(7)
for i in range(-6, 7):
    h = random.uniform(8, 22)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 9.0, random.choice([-16, 16]), h / 2))
    b = bpy.context.active_object
    b.scale = (4.5, 4.5, h / 2)
    b.data.materials.append(mat("Building", (0.12, 0.14, 0.2, 1), rough=0.7))

# Lampu jalan
for x in (-18, -6, 6, 18):
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=7, location=(x, side * 7.8, 3.5))
        pole = bpy.context.active_object
        pole.data.materials.append(mat("Pole", (0.1, 0.1, 0.1, 1), metallic=1.0, rough=0.4))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(x, side * 7.8, 7.2))
        bulb = bpy.context.active_object
        bulb.data.materials.append(mat("Bulb", (1.0, 0.9, 0.6, 1), emit=20.0))

# Langit malam dengan cahaya lembut
world = bpy.data.worlds.new("Night")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.02, 0.03, 0.08, 1)
bg.inputs["Strength"].default_value = 0.6

# Matahari buatan dari arah belakang untuk kilau krom
bpy.ops.object.light_add(type="SUN", location=(10, -10, 15))
sun = bpy.context.active_object
sun.data.energy = 2.0
sun.rotation_euler = (math.radians(50), 0, math.radians(35))

# Kamera sinematik, sedikit di depan dan samping bus
bpy.ops.object.camera_add(location=(-14, -14, 4.5))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(78), 0, math.radians(-45))
cam.data.lens = 50
scene.camera = cam

scene.render.filepath = OUT_FILE
bpy.ops.render.render(write_still=True)
print("Render disimpan ke", OUT_FILE)
