"""mine_kit - shared toolkit for the Ore Factory mines (Blender 5.x / bpy).

Every mine script does:  from mine_kit import *   then   begin("Name", [...collections])
builds its parts with the helpers below, and ends with   finish_mine()
which writes  <Name>.blend, <Name>_Roblox.fbx (one mesh per material, 1 unit = 1 stud),
<Name>_RobloxSetup.lua (colours, Roblox materials, glow lights, working ore dropper) and,
with --render, Cycles previews in renders/.   Mines face -Y, +Z is up.

Run:  python3 <mine>.py -- --out <folder> [--render] [--views hero,front,left,back] [--samples 64]
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix, Euler

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            return argv[i + 1]
        return True
    return default


OUT = os.path.abspath(arg("--out", os.getcwd()))
RENDER = bool(arg("--render", False))
VIEWS = arg("--views", "hero,front,left,back")
SAMPLES = int(arg("--samples", 64))
V = lambda *a: Vector(a)
X_AXIS = V(1, 0, 0)
MINE_OBJECTS = []
RBX = {}          # export name -> (Roblox material, (r,g,b) 0-255, transparency, light (r,g,b,range,brightness) or None)
STATE = {}


def begin(name, collections, seed=1):
    """Reset the scene and create the mine's collections. Returns the collections in order."""
    random.seed(seed)
    STATE["name"] = name
    sc = bpy.context.scene
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    root = bpy.data.collections.new(name)
    sc.collection.children.link(root)
    stage = bpy.data.collections.new("Stage (not exported)")
    sc.collection.children.link(stage)
    STATE["root"], STATE["stage"] = root, stage
    out = []
    for n in collections:
        c = bpy.data.collections.new(n)
        root.children.link(c)
        out.append(c)
    return out

def lin(c):
    """sRGB 0-255 -> linear 0-1."""
    def f(x):
        x /= 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return tuple(f(x) for x in c)


def new_mat(name, color, rough=0.7, metal=0.0, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = emit_strength
    m.diffuse_color = (*color, 1)
    return m


def tex_vec(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    return tc.outputs["Object"]


def add_noise(m, c1, c2, scale=1.5, detail=8.0, bump=0.2, lo=0.3, hi=0.75, distortion=0.0):
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = detail
    nz.inputs["Distortion"].default_value = distortion
    nt.links.new(tex_vec(nt), nz.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position, cr.color_ramp.elements[0].color = lo, (*c1, 1)
    cr.color_ramp.elements[1].position, cr.color_ramp.elements[1].color = hi, (*c2, 1)
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    if bump:
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def add_plate_bump(m, scale=9.0, strength=0.35):
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    vo = nt.nodes.new("ShaderNodeTexVoronoi")
    vo.inputs["Scale"].default_value = scale
    nt.links.new(tex_vec(nt), vo.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = strength
    nt.links.new(vo.outputs["Distance"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def add_marble(m, dark, vein):
    """Dark stone with thin bright veins (veins sit where the noise crosses 0.5)."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Distortion"].default_value = 1.5
    nt.links.new(tex_vec(nt), nz.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    els = cr.color_ramp.elements
    els[0].position, els[0].color = 0.46, (*dark, 1)
    els[1].position, els[1].color = 0.54, (*dark, 1)
    mid = els.new(0.5)
    mid.color = (*vein, 1)
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])


def export_name(mat_name):
    return mat_name.split(" (")[0].replace(" ", "")


def M(name, rgb, rough=0.6, metal=0.0, glow=None, glow_strength=0.0, rbx=None, alpha=0.0, light=None,
      noise=None, marble=None, plate=None):
    """Material + its Roblox look in one call. rgb/glow are 0-255.
    rbx: Roblox material name (default: Neon if it glows hard, Metal if metallic, else SmoothPlastic).
    light: (range, brightness) adds a PointLight in Roblox.  noise=(rgb_dark, rgb_light, scale, bump),
    marble=(rgb_dark, rgb_vein), plate=scale (diamond-plate bump)."""
    m = new_mat(name, lin(rgb), rough=rough, metal=metal,
                emit=lin(glow) if glow else None, emit_strength=glow_strength)
    if noise:
        add_noise(m, lin(noise[0]), lin(noise[1]), scale=noise[2], bump=noise[3])
    if marble:
        add_marble(m, lin(marble[0]), lin(marble[1]))
    if plate:
        add_plate_bump(m, scale=plate)
    if rbx is None:
        rbx = "Neon" if glow_strength >= 2 else "Metal" if metal >= 0.6 else "SmoothPlastic"
    lc = None
    if light:
        g = glow or rgb
        lc = (g[0], g[1], g[2], light[0], light[1])
    RBX[export_name(name)] = (rbx, tuple(rgb), alpha, lc)
    return m


def finish(name, bm, mat, coll, smooth=False, merge=0.0005):
    if merge:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if smooth:
        for f in bm.faces:
            f.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    me.materials.append(mat)
    MINE_OBJECTS.append(ob)
    return ob


def ring_pts(C, u, v, r, n, phase=0.0):
    """Circle around C in the plane spanned by v (angle 0) and u (angle 90)."""
    return [C + r * (math.cos(phase + 2 * math.pi * i / n) * v + math.sin(phase + 2 * math.pi * i / n) * u)
            for i in range(n)]


def loft(rings, cap0=True, cap1=True, smooth_sides=True, bm=None):
    bm = bm or bmesh.new()
    vs = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(rings[0])
    for i in range(len(vs) - 1):
        for j in range(n):
            k = (j + 1) % n
            f = bm.faces.new((vs[i][j], vs[i][k], vs[i + 1][k], vs[i + 1][j]))
            f.smooth = smooth_sides
    if cap0:
        bm.faces.new(list(reversed(vs[0])))
    if cap1:
        bm.faces.new(vs[-1])
    return bm


def perp_basis(a, hint=V(0, 0, 1)):
    a = a.normalized()
    if abs(a.dot(hint)) > 0.95:
        hint = V(1, 0, 0) if abs(a.x) < 0.9 else V(0, 1, 0)
    u = (hint - a * hint.dot(a)).normalized()
    v = u.cross(a).normalized()
    return u, v


def cyl(name, p0, p1, r0, r1, mat, coll, n=24, hint=V(0, 0, 1)):
    a = (p1 - p0)
    u, v = perp_basis(a, hint)
    bm = loft([ring_pts(p0, u, v, r0, n), ring_pts(p1, u, v, max(r1, 1e-4), n)])
    return finish(name, bm, mat, coll, merge=0.0005 if r1 < 1e-3 else 0)


def tube(name, C, a, u, r_out, r_in, depth, mat, coll, n=40):
    a = a.normalized()
    v = a.cross(u).normalized() * -1
    f0, f1 = C - a * depth / 2, C + a * depth / 2
    bm = bmesh.new()
    o0 = [bm.verts.new(p) for p in ring_pts(f0, u, v, r_out, n)]
    o1 = [bm.verts.new(p) for p in ring_pts(f1, u, v, r_out, n)]
    i0 = [bm.verts.new(p) for p in ring_pts(f0, u, v, r_in, n)]
    i1 = [bm.verts.new(p) for p in ring_pts(f1, u, v, r_in, n)]
    for j in range(n):
        k = (j + 1) % n
        bm.faces.new((o0[j], o0[k], o1[k], o1[j])).smooth = True
        bm.faces.new((i0[k], i0[j], i1[j], i1[k])).smooth = True
        bm.faces.new((o0[k], o0[j], i0[j], i0[k]))
        bm.faces.new((o1[j], o1[k], i1[k], i1[j]))
    return finish(name, bm, mat, coll, merge=0)


def torus(name, C, a, u, R, r, mat, coll, n_major=40, n_minor=10):
    a = a.normalized()
    v = a.cross(u).normalized() * -1
    bm = bmesh.new()
    grid = []
    for i in range(n_major):
        t = 2 * math.pi * i / n_major
        radial = math.cos(t) * v + math.sin(t) * u
        cen = C + R * radial
        grid.append([bm.verts.new(cen + r * (math.cos(2 * math.pi * j / n_minor) * radial +
                                             math.sin(2 * math.pi * j / n_minor) * a)) for j in range(n_minor)])
    for i in range(n_major):
        for j in range(n_minor):
            i2, j2 = (i + 1) % n_major, (j + 1) % n_minor
            bm.faces.new((grid[i][j], grid[i2][j], grid[i2][j2], grid[i][j2])).smooth = True
    return finish(name, bm, mat, coll, merge=0)


def hexa(name, pts, mat, coll):
    """Closed 6-faced solid from 8 corners: 4 'bottom' then 4 'top' (same winding)."""
    bm = bmesh.new()
    v = [bm.verts.new(p) for p in pts]
    for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        bm.faces.new([v[i] for i in f])
    return finish(name, bm, mat, coll, merge=0)


def abox(name, x0, x1, y0, y1, z0, z1, mat, coll):
    return hexa(name, [V(x0, y0, z0), V(x1, y0, z0), V(x1, y1, z0), V(x0, y1, z0),
                       V(x0, y0, z1), V(x1, y0, z1), V(x1, y1, z1), V(x0, y1, z1)], mat, coll)


def obox(name, C, size, ax, ay, az, mat, coll):
    """Box centred at C with edge directions ax, ay, az and sizes size=(sx, sy, sz)."""
    hx, hy, hz = (ax.normalized() * size[0] / 2, ay.normalized() * size[1] / 2, az.normalized() * size[2] / 2)
    pts = [C - hx - hy - hz, C + hx - hy - hz, C + hx + hy - hz, C - hx + hy - hz,
           C - hx - hy + hz, C + hx - hy + hz, C + hx + hy + hz, C - hx + hy + hz]
    return hexa(name, pts, mat, coll)


def beam(name, p0, p1, w, h, side, mat, coll):
    d = p1 - p0
    a = d.normalized()
    s = (side - a * side.dot(a)).normalized()
    t = a.cross(s).normalized()
    return obox(name, (p0 + p1) / 2, (d.length, w, h), a, s, t, mat, coll)


def profile_x(name, pts_yz, x0, x1, mat, coll):
    r0 = [V(x0, y, z) for y, z in pts_yz]
    r1 = [V(x1, y, z) for y, z in pts_yz]
    bm = loft([r0, r1], smooth_sides=False)
    return finish(name, bm, mat, coll, merge=0)


def chamfer_rect(w, l, c):
    hw, hl = w / 2, l / 2
    return [(hw - c, -hl), (hw, -hl + c), (hw, hl - c), (hw - c, hl),
            (-hw + c, hl), (-hw, hl - c), (-hw, -hl + c), (-hw + c, -hl)]


def slab(name, outline0, z0, outline1, z1, mat, coll):
    bm = loft([[V(x, y, z0) for x, y in outline0], [V(x, y, z1) for x, y in outline1]], smooth_sides=False)
    return finish(name, bm, mat, coll, merge=0)


def blade(name, pts, thickness, mat, coll):
    """Flat polygon (list of 3D points, roughly planar) given thickness."""
    nrm = (pts[1] - pts[0]).cross(pts[-1] - pts[0]).normalized()
    off = nrm * thickness / 2
    bm = bmesh.new()
    f = [bm.verts.new(p + off) for p in pts]
    b = [bm.verts.new(p - off) for p in pts]
    bm.faces.new(f)
    bm.faces.new(list(reversed(b)))
    n = len(pts)
    for j in range(n):
        k = (j + 1) % n
        bm.faces.new((f[k], f[j], b[j], b[k]))
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
    return finish(name, bm, mat, coll, merge=0)


def crystal(name, base, direction, length, radius, mat, coll, sides=6):
    a = direction.normalized()
    u, v = perp_basis(a)
    ph = random.random()
    rings = [ring_pts(base, u, v, radius * 0.85, sides, ph),
             ring_pts(base + a * length * 0.7, u, v, radius, sides, ph),
             [base + a * length] * sides]
    bm = loft(rings, cap0=True, cap1=False, smooth_sides=False)
    return finish(name, bm, mat, coll, merge=0.001)


def rock(name, C, scale, mat, coll, rough=0.18):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    for v in bm.verts:
        v.co *= 1.0 + random.uniform(-rough, rough)
        v.co = V(v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]) + C
    return finish(name, bm, mat, coll, smooth=True, merge=0)


def sphere(name, C, r, mat, coll):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=r)
    bmesh.ops.translate(bm, verts=bm.verts, vec=C)
    return finish(name, bm, mat, coll, smooth=True, merge=0)


def cone(name, base, tip, r, mat, coll, n=12):
    return cyl(name, base, tip, r, 0.0, mat, coll, n=n)


def path_tube(name, pts, radii, mat, coll, n=12, cap=True):
    """Tube along a list of points with a radius per point (tentacles, tails, pipes, horns)."""
    rings = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        u, v = perp_basis(d)
        rings.append(ring_pts(p, u, v, max(radii[i], 1e-3), n))
    return finish(name, loft(rings, cap0=cap, cap1=cap), mat, coll, merge=0.0005)


def lathe(name, C, profile, mat, coll, n=24, smooth=True):
    """Solid of revolution around +Z: profile = [(radius, z), ...] bottom to top (pots, caps, domes, towers)."""
    rings = [ring_pts(C + V(0, 0, z), V(0, 1, 0), X_AXIS, max(r, 1e-3), n) for r, z in profile]
    bm = loft(rings, cap0=profile[0][0] > 1e-3, cap1=profile[-1][0] > 1e-3, smooth_sides=smooth)
    return finish(name, bm, mat, coll, merge=0.0005)


def dot(name, C, r, mat, coll):
    """Tiny low-poly sphere (rivets, suckers, spots, studs) - 80 triangles."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
    bmesh.ops.translate(bm, verts=bm.verts, vec=C)
    return finish(name, bm, mat, coll, smooth=True, merge=0)


def rock_f(name, C, scale, mat, coll, rough=0.22, subd=1, seed=None):
    """Faceted low-poly boulder (flat shaded) - chunkier than rock()."""
    rnd = random.Random(seed if seed is not None else hash(name) & 0xffff)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subd, radius=1.0)
    for v in bm.verts:
        v.co *= 1.0 + rnd.uniform(-rough, rough)
        v.co = V(v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]) + C
    return finish(name, bm, mat, coll, smooth=False, merge=0)


def base_plinth(w, l, mat_base, mat_trim, mat_top, coll, c=1.0, h=1.8):
    """The common mine base: chamfered slab, glowing trim, inset top. Returns the top height."""
    slab("Base Slab", chamfer_rect(w, l, c), 0.0, chamfer_rect(w, l, c), h, mat_base, coll)
    slab("Base Trim", chamfer_rect(w + 0.08, l + 0.08, c + 0.03), h, chamfer_rect(w + 0.08, l + 0.08, c + 0.03), h + 0.2, mat_trim, coll)
    slab("Base Top", chamfer_rect(w - 0.4, l - 0.4, c * 0.92), h + 0.2, chamfer_rect(w - 1.1, l - 1.1, c * 0.75), h + 0.7, mat_top, coll)
    return h + 0.7


def crystal_cluster(name, C, n, size, mat_crystal, mat_rock, coll, up=V(0, 0, 1), seed=0):
    rnd = random.Random(seed)
    rock(f"{name} Rock", C, (size * 1.1, size * 0.9, size * 0.6), mat_rock, coll)
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = (up + V(math.cos(a), math.sin(a), 0) * rnd.uniform(0.2, 0.7)).normalized()
        crystal(f"{name} Crystal {k + 1}", C + V(math.cos(a), math.sin(a), 0) * size * 0.4, d,
                size * rnd.uniform(1.6, 2.8), size * rnd.uniform(0.35, 0.55), mat_crystal, coll)


def ore_cube(pos, mat, coll, size=0.95, rot=(0.4, 0.3, 0.6)):
    """The ore drop marker: becomes the drop point of the Roblox dropper (keep its material name ending in 'Ore')."""
    r = Euler(rot).to_matrix()
    STATE["ore_mat"] = export_name(mat.name)
    return obox("Ore (drop point)", pos, (size, size, size), r @ X_AXIS, r @ V(0, 1, 0), r @ V(0, 0, 1), mat, coll)


def post_lantern(name, P, h, mat_post, mat_glow, mat_cap, coll, r=0.5):
    cyl(f"{name} Post", P, P + V(0, 0, h), 0.16, 0.16, mat_post, coll, n=8)
    cyl(f"{name} Glass", P + V(0, 0, h), P + V(0, 0, h + 1.1), r, r, mat_glow, coll, n=8)
    cyl(f"{name} Cap", P + V(0, 0, h + 1.1), P + V(0, 0, h + 1.8), r + 0.2, 0.0, mat_cap, coll, n=8)



def _lua_color(c):
    return "%d, %d, %d" % tuple(int(x) for x in c)


def write_roblox_setup(path, name, ore_key):
    look = ",\n".join('\t%s = {"%s", %s, %g}' % (k, v[0], _lua_color(v[1]), v[2]) for k, v in sorted(RBX.items()))
    lights = ",\n".join('\t%s = {%s, %g, %g}' % (k, _lua_color(v[3][:3]), v[3][3], v[3][4])
                        for k, v in sorted(RBX.items()) if v[3])
    lua = f"""-- {name}: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import {name}_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {{
{look}
}}
local LIGHTS = {{
{lights}
}}
local ORE_PART = "{ore_key}"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("{name}_Roblox", true) or workspace:FindFirstChild("{name}", true) end
assert(model, "Select the imported {name} model first.")
local styled, lit, drop = 0, 0, nil
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") then
		local key = p.Name:gsub("%.%d+$", "")
		local l = LOOK[key]
		pcall(function()
			p.Anchored = true
			for _, sa in ipairs(p:GetChildren()) do if sa:IsA("SurfaceAppearance") then sa:Destroy() end end
			if l then
				p.Material = Enum.Material[l[1]]
				p.Color = Color3.fromRGB(l[2], l[3], l[4])
				p.Transparency = l[5]
				if p:IsA("MeshPart") then p.TextureID = "" end
				styled += 1
			end
			local L = LIGHTS[key]
			if L then
				local light = p:FindFirstChild("MineLight") or Instance.new("PointLight")
				light.Name = "MineLight"; light.Color = Color3.fromRGB(L[1], L[2], L[3]); light.Range = L[4]; light.Brightness = L[5]
				light.Parent = p
				lit += 1
			end
		end)
		if key == ORE_PART then drop = p end
	end
end
if drop then
	drop.Transparency = 1; drop.CanCollide = false; drop.CanQuery = false; drop.Name = "Drop"
	local oreLook = LOOK[ORE_PART]
	model:SetAttribute("OreValue", model:GetAttribute("OreValue") or 25)
	model:SetAttribute("DropInterval", model:GetAttribute("DropInterval") or 2)
	model:SetAttribute("OreSize", model:GetAttribute("OreSize") or 1)
	model:SetAttribute("OreColor", Color3.fromRGB(oreLook[2], oreLook[3], oreLook[4]))
	model:SetAttribute("OreMaterial", oreLook[1])
	local old = model:FindFirstChild("Dropper"); if old then old:Destroy() end
	local s = Instance.new("Script")
	s.Name = "Dropper"
	s.Source = [[
local Debris = game:GetService("Debris")
local mine = script.Parent
local drop = mine:FindFirstChild("Drop", true)
while true do
	task.wait(mine:GetAttribute("DropInterval") or 2)
	if drop and mine:GetAttribute("Enabled") ~= false then
		local size = mine:GetAttribute("OreSize") or 1
		local ore = Instance.new("Part")
		ore.Name = "Ore"
		ore.Size = Vector3.new(size, size, size)
		ore.Material = Enum.Material[mine:GetAttribute("OreMaterial") or "Neon"]
		ore.Color = mine:GetAttribute("OreColor") or Color3.new(1, 1, 1)
		ore.CFrame = drop.CFrame * CFrame.Angles(math.random() * 6.28, math.random() * 6.28, 0)
		ore:SetAttribute("Value", mine:GetAttribute("OreValue") or 25)
		ore.Parent = workspace
		Debris:AddItem(ore, 30)
	end
end
]]
	s.Parent = model
end
print(("[{name}] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
"""
    with open(path, "w") as f:
        f.write(lua)


def finish_mine(bg=(0.01, 0.012, 0.03), tint=(0.75, 0.75, 1.0), cams=None, mood_light=(0, -4, 20)):
    name = STATE["name"]
    scene = bpy.context.scene
    root = STATE["root"]
    stage = STATE["stage"]
    root_empty = bpy.data.objects.new(name, None)
    root_empty.empty_display_type = 'PLAIN_AXES'
    root.objects.link(root_empty)
    lo, hi = V(1e9, 1e9, 1e9), V(-1e9, -1e9, -1e9)
    for ob in MINE_OBJECTS:
        me = ob.data
        c = sum((v.co for v in me.vertices), Vector()) / max(len(me.vertices), 1)
        for v in me.vertices:
            lo = V(min(lo.x, v.co.x), min(lo.y, v.co.y), min(lo.z, v.co.z))
            hi = V(max(hi.x, v.co.x), max(hi.y, v.co.y), max(hi.z, v.co.z))
        me.transform(Matrix.Translation(-c))
        ob.location = c
        ob.parent = root_empty
    tris = sum(len(p.vertices) - 2 for ob in MINE_OBJECTS for p in ob.data.polygons)
    print(f"[mine] {name}: parts={len(MINE_OBJECTS)} triangles={tris} size={tuple(round(x, 1) for x in (hi - lo))}")
    # stage
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.new("Night")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (*bg, 1)
    gme = bpy.data.meshes.new("Ground")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=120)
    bm.to_mesh(gme)
    bm.free()
    ground = bpy.data.objects.new("Ground", gme)
    ground.location.z = -0.01
    stage.objects.link(ground)
    gm = new_mat("Ground", lin((90, 92, 104)), rough=0.95)
    gme.materials.append(gm)

    def add_light(n, kind, loc, energy, color, size=0.5, rot=None):
        ld = bpy.data.lights.new(n, kind)
        ld.energy = energy
        ld.color = color
        if kind == 'SUN':
            ld.angle = math.radians(10)
        else:
            ld.shadow_soft_size = size
        ob = bpy.data.objects.new(n, ld)
        ob.location = loc
        if rot:
            ob.rotation_euler = rot
        stage.objects.link(ob)
    ctr = (lo + hi) / 2
    H = hi.z
    add_light("Moon", 'SUN', V(0, 0, 30), 1.5, tint, rot=Euler((math.radians(50), 0, math.radians(30))))
    add_light("Mine Glow", 'POINT', V(*mood_light), 6000, tint, size=3)
    add_light("Front Fill", 'POINT', V(0, -16, H * 0.6 + 3), 3500, tint, size=4)
    add_light("Back Fill", 'POINT', V(0, 15, H * 0.6 + 4), 2500, tint, size=4)
    add_light("Side Fill L", 'POINT', V(14, -2, H * 0.5 + 2), 2000, tint, size=4)
    add_light("Side Fill R", 'POINT', V(-14, -2, H * 0.5 + 2), 2000, tint, size=4)
    span = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z)
    tgt = V(ctr.x, ctr.y, ctr.z)
    default = {
        "hero": (tgt + V(1.0, -1.1, 0.42).normalized() * span * 1.75, tgt, 35, (1200, 1100)),
        "front": (tgt + V(0, -1, 0.12).normalized() * span * 2.15, tgt, 50, (1000, 1000)),
        "left": (tgt + V(-1, -0.05, 0.2).normalized() * span * 2.15, tgt, 50, (1000, 1000)),
        "back": (tgt + V(-0.15, 1, 0.35).normalized() * span * 2.15, tgt, 50, (1000, 1000)),
    }
    default.update(cams or {})
    cam_objs = {}
    for n, (loc, t, lens, res) in default.items():
        cd = bpy.data.cameras.new(f"Cam {n}")
        cd.lens = lens
        co = bpy.data.objects.new(f"Cam {n}", cd)
        co.location = loc
        co.rotation_euler = (t - loc).to_track_quat('-Z', 'Y').to_euler()
        stage.objects.link(co)
        cam_objs[n] = (co, res)
    scene.camera = cam_objs["hero"][0]
    os.makedirs(OUT, exist_ok=True)
    # Roblox export: one mesh per material
    exp = bpy.data.collections.new("_export")
    scene.collection.children.link(exp)
    groups = {}
    for ob in MINE_OBJECTS:
        groups.setdefault(ob.data.materials[0].name, []).append(ob)
    joined = []
    for mname, obs in groups.items():
        dups = []
        for ob in obs:
            dd = ob.copy()
            dd.data = ob.data.copy()
            dd.parent = None
            dd.matrix_world = ob.matrix_world.copy()
            exp.objects.link(dd)
            dups.append(dd)
        with bpy.context.temp_override(active_object=dups[0], selected_editable_objects=dups, selected_objects=dups):
            bpy.ops.object.join()
        j = dups[0]
        j.name = export_name(mname)
        joined.append(j)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for j in joined:
        j.select_set(True)
    fbx = os.path.join(OUT, f"{name}_Roblox.fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={'MESH'}, use_triangles=True,
                             mesh_smooth_type='FACE', apply_unit_scale=True)
    for j in joined:
        bpy.data.objects.remove(j, do_unlink=True)
    bpy.data.collections.remove(exp)
    write_roblox_setup(os.path.join(OUT, f"{name}_RobloxSetup.lua"), name, STATE.get("ore_mat", "Ore"))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"{name}.blend"))
    print(f"[mine] saved {name}.blend, {name}_Roblox.fbx, {name}_RobloxSetup.lua")
    if RENDER:
        rdir = os.path.join(OUT, "renders")
        os.makedirs(rdir, exist_ok=True)
        for n in VIEWS.split(","):
            co, res = cam_objs[n]
            scene.camera = co
            scene.render.resolution_x, scene.render.resolution_y = res
            scene.render.resolution_percentage = 100
            scene.render.filepath = os.path.join(rdir, f"{n}.png")
            bpy.ops.render.render(write_still=True)
            print("[mine] rendered", n)
