"""Combine every Ore Haven model into ONE Blender file and ONE FBX for Roblox Import 3D.
Run: python3 build_all.py   (uses the bpy module).  Each item becomes its own Model (empty) laid out on a grid."""
import bpy, os, glob, math, re
from mathutils import Vector
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.dirname(os.path.abspath(__file__))
def g(p): return sorted(glob.glob(os.path.join(ROOT, p)))
GROUPS = [
    ("Droppers", g("mines20/droppers10/d*/*_Roblox.fbx")),
    ("Mines", [f for f in g("mines20/*/*_Roblox.fbx") if "Mine_" in f or "Forge_" in f]),
    ("Drake Mines", g("mine/*/*_Roblox.fbx")),
    ("Furnaces", [f for f in g("mines20/*/*Furnace_Roblox.fbx")] + g("mines20/furnaces9/f*/*_Roblox.fbx")),
    ("Upgraders", g("mines20/upgrader/*_Roblox.fbx")),
    ("Boost Pads", g("mines20/boostpads/pad*/*_Roblox.fbx")),
]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
top = bpy.data.collections.new("OreHaven_AllModels"); sc.collection.children.link(top)
items = []          # (item empty, lua path)

def import_item(name, fbxs, coll):
    before = set(bpy.data.objects)
    for f in fbxs:
        bpy.ops.import_scene.fbx(filepath=f)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:                                      # bake any import scale/rotation into the mesh
        for c in o.users_collection: c.objects.unlink(o)
        coll.objects.link(o)
    meshes = [o for o in new if o.type == 'MESH']
    for o in meshes:
        mw = o.matrix_world.copy(); o.parent = None; o.data.transform(mw); o.matrix_world.identity()
    for o in new:
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in meshes:
        for v in o.data.vertices:
            lo = Vector(map(min, lo, v.co)); hi = Vector(map(max, hi, v.co))
    e = bpy.data.objects.new(name, None); coll.objects.link(e)
    for o in meshes:
        o.parent = e
    return e, lo, hi, meshes

z_row_y = 0.0
for gname, files in GROUPS + [("Workshop", None)]:
    coll = bpy.data.collections.new(gname); top.children.link(coll)
    if gname == "Workshop":
        d = os.path.join(ROOT, "ore_haven/machine_workshop")
        packs = [("MachineWorkshop", [os.path.join(d, "MachineWorkshop_Building_Roblox.fbx"), os.path.join(d, "MachineWorkshop_Foundation_Roblox.fbx")], os.path.join(d, "MachineWorkshop_RobloxSetup.lua"))]
    else:
        packs = [(os.path.basename(f).replace("_Roblox.fbx", ""), [f], f.replace("_Roblox.fbx", "_RobloxSetup.lua")) for f in files]
    x = 0.0; row_depth = 0.0; made = []
    for name, fbxs, lua in packs:
        e, lo, hi, meshes = import_item(name, fbxs, coll)
        size = hi - lo
        if x > 0 and x + size.x > 260.0:               # wrap long rows so the layout stays compact
            z_row_y += row_depth + 14.0; x = 0.0; row_depth = 0.0
        off = Vector((x - lo.x, z_row_y - lo.y, -lo.z))   # sit on the ground, laid out left to right
        for o in meshes: o.data.transform(__import__("mathutils").Matrix.Translation(off))
        x += size.x + 12.0; row_depth = max(row_depth, size.y)
        items.append((name, lua if os.path.exists(lua) else None, gname))
        print(f"[all] {gname:12s} {name:28s} {size.x:6.1f} x {size.y:6.1f} x {size.z:6.1f}  parts={len(meshes)}")
    z_row_y += row_depth + 24.0

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "OreHaven_AllModels.blend"), compress=True)
for o in bpy.data.objects: o.select_set(True)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "OreHaven_AllModels_Roblox.fbx"), use_selection=True, object_types={'MESH', 'EMPTY'},
                         use_triangles=True, mesh_smooth_type='FACE', apply_unit_scale=True, bake_space_transform=False)

# one Command Bar script that styles + wires up every item inside the imported model
out = ['-- OreHaven_AllModels: styles every imported item and adds its working scripts (droppers, furnaces, upgrader).',
       '-- 1. Import OreHaven_AllModels_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh").',
       '-- 2. Select the imported OreHaven_AllModels model in the Explorer.  3. Paste this whole file into View > Command Bar, press Enter.',
       'local ROOT = game:GetService("Selection"):Get()[1]',
       'assert(ROOT, "Select the imported OreHaven_AllModels model first.")',
       'local done, missing = 0, {}']
for name, lua, gname in items:
    if not lua:
        continue
    src = open(lua).read()
    src = src.replace('game:GetService("Selection"):Get()[1]', '__M').replace('game:GetService("Selection"):Get()', '{__M}')
    out.append(f'do local __M = ROOT:FindFirstChild("{name}", true)\nif __M then local ok, err = pcall(function()\n{src}\nend) if ok then done += 1 else warn("{name}: " .. tostring(err)) end else table.insert(missing, "{name}") end end')
out.append('print("[OreHaven] set up " .. done .. " items" .. (#missing > 0 and (", not found: " .. table.concat(missing, ", ")) or ""))')
open(os.path.join(OUT, "OreHaven_AllModels_Setup.lua"), "w").write("\n".join(out))
print("[all] items", len(items), "with scripts", sum(1 for i in items if i[1]))
