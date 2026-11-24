# Jalankan dengan: blender -b --factory-startup --python tools/make_bus.py
# Membuat model bus sederhana dan mengekspornya ke assets/models/bus.glb
import bpy
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models")
OUT_FILE = os.path.join(OUT_DIR, "bus.glb")

# Bersihkan scene
bpy.ops.wm.read_factory_settings(use_empty=True)

BODY_COLOR = (1.0, 0.75, 0.0, 1.0)
GLASS_COLOR = (0.1, 0.15, 0.2, 1.0)
DARK_COLOR = (0.05, 0.05, 0.05, 1.0)


def make_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    return mat


def add_box(name, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    return obj


def add_wheel(name, location, material):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.4, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = (0, 0, 1.5708)
    obj.data.materials.append(material)
    return obj


body_mat = make_material("Body", BODY_COLOR)
glass_mat = make_material("Glass", GLASS_COLOR)
dark_mat = make_material("Dark", DARK_COLOR)

# Bodi utama: panjang 10 m, lebar 2.5 m, tinggi 3 m
bus_parts = []
bus_parts.append(add_box("BusBody", (0, 0, 2.0), (5.0, 1.25, 1.5), body_mat))
# Jendela
bus_parts.append(add_box("Windows", (0, 0, 3.0), (4.95, 1.27, 0.6), glass_mat))
# Kap depan yang sedikit turun
bus_parts.append(add_box("Hood", (4.6, 0, 1.2), (0.8, 1.2, 0.8), body_mat))
# Roda
for i, (x, y) in enumerate([(3.0, 1.2), (3.0, -1.2), (-3.0, 1.2), (-3.0, -1.2)]):
    bus_parts.append(add_wheel(f"Wheel{i}", (x, y, 0.5), dark_mat))
# Lampu depan
for i, y in enumerate([0.8, -0.8]):
    bus_parts.append(add_box(f"Headlight{i}", (5.0, y, 1.6), (0.05, 0.25, 0.15), glass_mat))

# Gabungkan semua bagian menjadi satu objek
bpy.ops.object.select_all(action="DESELECT")
for obj in bus_parts:
    obj.select_set(True)
bpy.context.view_layer.objects.active = bus_parts[0]
bpy.ops.object.join()

# Pusatkan dan letakkan roda di permukaan jalan
bus = bpy.context.active_object
bus.name = "Bus"

os.makedirs(OUT_DIR, exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT_FILE, export_format="GLB", use_selection=True)
print("Model bus diekspor ke", OUT_FILE)
