"""Astral Orrery Mine - original Ore Factory mine for Blender 5.x (same pipeline as the Dragonglass Mine).

    python3 astral_orrery_mine.py -- --out <folder> [--render] [--views hero,front,left,back] [--samples 64]
    (or: blender -b --factory-startup -P astral_orrery_mine.py -- --out <folder> --render)

A glowing star core floats inside a gold armillary of tilted rings and orbiting planets;
stardust ore drips through a funnel and out of the front spout. Saves
AstralOrreryMine.blend, exports AstralOrreryMine_Roblox.fbx (one mesh per material, 1 unit = 1 stud)
and optionally renders previews (Cycles, so it also works without a GPU).
The mine faces -Y, +Z is up.
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
random.seed(5)
V = lambda *a: Vector(a)
X_AXIS = V(1, 0, 0)

scene = bpy.context.scene
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
root_coll = bpy.data.collections.new("AstralOrreryMine")
scene.collection.children.link(root_coll)
stage_coll = bpy.data.collections.new("Stage (not exported)")
scene.collection.children.link(stage_coll)


def sub_coll(name):
    c = bpy.data.collections.new(name)
    root_coll.children.link(c)
    return c


C_BASE, C_PEDESTAL, C_ARMILLARY, C_FUNNEL, C_DETAIL = (sub_coll(n) for n in ("Base", "Pedestal", "Armillary", "Funnel", "Details"))
MINE_OBJECTS = []

# ---------------------------------------------------------------- materials
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


M_NAVY = new_mat("Night Metal (Metal)", lin((26, 32, 78)), rough=0.3, metal=0.8)
add_plate_bump(M_NAVY, scale=8.0, strength=0.2)
M_GOLD = new_mat("Gold (Metal)", lin((232, 182, 72)), rough=0.25, metal=1.0, emit=lin((120, 80, 20)), emit_strength=0.3)
M_BLACK = new_mat("Black", lin((8, 8, 18)), rough=0.45)
M_SKY = new_mat("Star Marble (Marble)", lin((14, 16, 40)), rough=0.2)
add_marble(M_SKY, lin((12, 14, 36)), lin((210, 220, 255)))
M_CORE = new_mat("Star Core (Neon)", lin((235, 250, 255)), rough=0.2, emit=lin((170, 230, 255)), emit_strength=14.0)
M_NEON = new_mat("Neon (Cyan Glow)", lin((190, 245, 255)), rough=0.3, emit=lin((110, 220, 255)), emit_strength=3.0)
M_CRYSTAL = new_mat("Crystal (Starglass)", lin((175, 135, 255)), rough=0.12, emit=lin((130, 90, 255)), emit_strength=1.0)
M_ROCK = new_mat("Meteor Rock", lin((38, 34, 52)), rough=0.95)
add_noise(M_ROCK, lin((24, 22, 34)), lin((66, 60, 86)), scale=3.0, bump=0.5)
M_PLANET_R = new_mat("Planet Red", lin((220, 90, 60)), rough=0.6)
add_noise(M_PLANET_R, lin((170, 60, 40)), lin((240, 150, 100)), scale=5.0, bump=0.1)
M_PLANET_T = new_mat("Planet Teal", lin((60, 190, 170)), rough=0.6)
add_noise(M_PLANET_T, lin((40, 140, 140)), lin((120, 230, 200)), scale=5.0, bump=0.1)
M_PLANET_P = new_mat("Planet Purple", lin((140, 90, 210)), rough=0.6)
add_noise(M_PLANET_P, lin((100, 60, 170)), lin((190, 150, 240)), scale=5.0, bump=0.1)
M_MOON = new_mat("Moon", lin((210, 210, 220)), rough=0.8)
M_RUNE = new_mat("Rune Glow", lin((200, 240, 255)), rough=0.3, emit=lin((120, 210, 255)), emit_strength=6.0)
M_GLASS = new_mat("Lens Glass", lin((150, 210, 255)), rough=0.05, emit=lin((80, 160, 255)), emit_strength=1.5)
M_ORE = new_mat("Stardust Ore", lin((215, 225, 255)), rough=0.15, emit=lin((160, 190, 255)), emit_strength=1.6)

# ---------------------------------------------------------------- geometry helpers

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


# ---------------------------------------------------------------- BASE (10 x 10 chamfered)
slab("Base Slab", chamfer_rect(10, 10, 1.4), 0.0, chamfer_rect(10, 10, 1.4), 1.6, M_BLACK, C_BASE)
slab("Base Trim", chamfer_rect(10.08, 10.08, 1.42), 1.6, chamfer_rect(10.08, 10.08, 1.42), 1.85, M_GOLD, C_BASE)
slab("Base Top", chamfer_rect(9.6, 9.6, 1.3), 1.85, chamfer_rect(8.8, 8.8, 1.1), 2.3, M_SKY, C_BASE)
for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):   # corner star studs
    sphere(f"Corner Stud {i + 1}", V(sx * 4.2, sy * 4.2, 2.45), 0.32, M_NEON, C_BASE)

# ---------------------------------------------------------------- PEDESTAL: stepped plinths, gear ring, curved arms
PC = V(0, 0.6, 0)
cyl("Plinth 1", PC + V(0, 0, 2.3), PC + V(0, 0, 3.2), 3.6, 3.4, M_NAVY, C_PEDESTAL, n=32)
tube("Plinth 1 Band", PC + V(0, 0, 3.05), V(0, 0, 1), V(0, 1, 0), 3.5, 3.1, 0.25, M_GOLD, C_PEDESTAL, n=32)
cyl("Plinth 2", PC + V(0, 0, 3.2), PC + V(0, 0, 4.4), 2.8, 2.4, M_NAVY, C_PEDESTAL, n=32)
cyl("Column", PC + V(0, 0, 4.4), PC + V(0, 0, 7.6), 1.1, 0.9, M_NAVY, C_PEDESTAL, n=24)
for z in (5.2, 6.6):
    torus(f"Column Ring {z}", PC + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 1.05, 0.13, M_GOLD, C_PEDESTAL, n_major=24, n_minor=6)
# big flat gear round the lower plinth
GZ = 3.9
tube("Gear Disc", PC + V(0, 0, GZ), V(0, 0, 1), V(0, 1, 0), 3.9, 2.9, 0.35, M_GOLD, C_PEDESTAL, n=48)
for k in range(24):
    a = 2 * math.pi * k / 24
    r_ = V(math.cos(a), math.sin(a), 0);t_ = V(-math.sin(a), math.cos(a), 0)
    obox(f"Gear Tooth {k + 1}", PC + r_ * 4.15 + V(0, 0, GZ), (0.55, 0.45, 0.35), r_, t_, V(0, 0, 1), M_GOLD, C_PEDESTAL)
# four curved arms rising to cradle the armillary
CORE = PC + V(0, 0, 12.0)
for k in range(4):
    a = math.radians(45 + 90 * k)
    d = V(math.cos(a), math.sin(a), 0)
    pts = [PC + d * (1.0 + 3.2 * math.sin(math.pi / 2 * t)) + V(0, 0, 6.8 + 5.2 * t) for t in [i / 6 for i in range(7)]]
    for i in range(6):
        cyl(f"Arm {k + 1}-{i + 1}", pts[i], pts[i + 1], 0.28, 0.24, M_GOLD, C_PEDESTAL, n=8)
    sphere(f"Arm Knob {k + 1}", pts[-1], 0.38, M_NEON, C_PEDESTAL)

# ---------------------------------------------------------------- ARMILLARY: star core, tilted rings, planets
sphere("Star Core", CORE, 2.0, M_CORE, C_ARMILLARY)
torus("Core Halo", CORE, V(0, -1, 0.15), V(0, 0, 1), 2.35, 0.08, M_NEON, C_ARMILLARY, n_major=40, n_minor=6)
RINGS = [(V(0.25, 0.15, 1), 3.4, M_PLANET_R, 30, 0.55), (V(1, 0.35, 0.45), 4.1, M_PLANET_T, 200, 0.7), (V(0.3, 1, 0.6), 4.8, M_PLANET_P, 300, 0.85)]
for i, (axis, R, pmat, ang, pr) in enumerate(RINGS):
    axis = axis.normalized();u, _ = perp_basis(axis)
    torus(f"Orbit Ring {i + 1}", CORE, axis, u, R, 0.12, M_GOLD, C_ARMILLARY, n_major=56, n_minor=6)
    v = axis.cross(u).normalized() * -1
    t = math.radians(ang);pos = CORE + R * (math.cos(t) * v + math.sin(t) * u)
    sphere(f"Planet {i + 1}", pos, pr, pmat, C_ARMILLARY)
    if i == 1:
        torus("Planet Ring", pos, V(0.3, 0.2, 1), V(0, 1, 0), pr * 1.6, 0.06, M_GOLD, C_ARMILLARY, n_major=24, n_minor=4)
    if i == 2:
        sphere("Moon", pos + V(0.9, -0.6, 0.7), 0.25, M_MOON, C_ARMILLARY)
# spire, crescent moon and star on top
cyl("Spire", CORE + V(0, 0, 2.0), CORE + V(0, 0, 6.6), 0.16, 0.08, M_GOLD, C_ARMILLARY, n=8)
MC, MR = CORE + V(0, 0, 5.4), 1.3                       # crescent: outer arc minus an offset circle
r2 = math.hypot(0.6, MR)
outer = [MC + MR * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in range(90, 271, 15)]
a0, a1 = math.degrees(math.atan2(-MR, -0.6)) % 360, math.degrees(math.atan2(MR, -0.6))
inner = [MC + V(0.6, 0, 0) + r2 * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in [a0 - (a0 - a1) * k / 8 for k in range(1, 8)]]
blade("Crescent Moon", outer + inner, 0.25, M_GOLD, C_ARMILLARY)
crystal("Star Tip", CORE + V(0, 0, 6.7), V(0, 0, 1), 1.4, 0.35, M_CRYSTAL, C_ARMILLARY, sides=4)

# ---------------------------------------------------------------- FUNNEL + SPOUT (ore drips from the core to the front)
F0 = PC + V(0, -2.2, 9.0)
cyl("Funnel Cup", F0, F0 + V(0, -0.2, -1.6), 1.5, 0.55, M_NAVY, C_FUNNEL, n=20)
torus("Funnel Rim Glow", F0, V(0, 0, 1), V(0, 1, 0), 1.5, 0.1, M_NEON, C_FUNNEL, n_major=24, n_minor=6)
pipe = [F0 + V(0, -0.2, -1.6), F0 + V(0, -1.2, -3.0), F0 + V(0, -2.8, -3.6)]
for i in range(2):
    cyl(f"Spout Pipe {i + 1}", pipe[i], pipe[i + 1], 0.55, 0.55, M_NAVY, C_FUNNEL, n=16)
SP = pipe[-1]
tube("Spout Collar", SP, V(0, -1, 0), V(0, 0, 1), 0.85, 0.5, 0.45, M_GOLD, C_FUNNEL, n=24)
torus("Spout Glow", SP + V(0, -0.25, 0), V(0, -1, 0), V(0, 0, 1), 0.68, 0.09, M_NEON, C_FUNNEL, n_major=24, n_minor=6)
for k in range(5):                                         # stardust stream from the core into the funnel
    sphere(f"Stardust {k + 1}", CORE + V(0, -1.0 - 0.25 * k, -1.9 - 0.55 * k), 0.16 - 0.015 * k, M_RUNE, C_FUNNEL)
ore_rot = Euler((0.4, 0.2, 0.7)).to_matrix()
obox("Ore (optional)", SP + V(0, -1.6, -0.9), (0.9, 0.9, 0.9), ore_rot @ X_AXIS, ore_rot @ V(0, 1, 0), ore_rot @ V(0, 0, 1), M_ORE, C_FUNNEL)

# ---------------------------------------------------------------- DETAILS
# telescope (+X side)
TB = V(3.6, 2.6, 2.3)
for k, (dx, dy) in enumerate(((0.5, 0.4), (-0.5, 0.4), (0, -0.6))):
    beam(f"Tripod Leg {k + 1}", TB + V(dx, dy, 0), TB + V(0, 0, 2.6), 0.12, 0.12, V(0, 0, 1), M_GOLD, C_DETAIL)
tdir = V(-0.2, -0.6, 0.75).normalized()
cyl("Telescope Tube", TB + V(0, 0, 2.6) - tdir * 1.2, TB + V(0, 0, 2.6) + tdir * 1.6, 0.32, 0.42, M_NAVY, C_DETAIL, n=16)
tube("Telescope Band", TB + V(0, 0, 2.6), tdir, perp_basis(tdir)[0], 0.4, 0.3, 0.25, M_GOLD, C_DETAIL, n=16)
cyl("Telescope Lens", TB + V(0, 0, 2.6) + tdir * 1.6, TB + V(0, 0, 2.6) + tdir * 1.68, 0.38, 0.38, M_GLASS, C_DETAIL, n=16)
# star chart panel (-X side)
abox("Chart Frame", -4.35, -4.1, -1.6, 1.8, 3.0, 6.0, M_GOLD, C_DETAIL)
abox("Chart Back", -4.1, -3.9, -1.6, 1.8, 2.3, 6.0, M_NAVY, C_DETAIL)
abox("Chart Face", -4.4, -4.3, -1.35, 1.55, 3.25, 5.75, M_SKY, C_DETAIL)
for k in range(9):
    sphere(f"Chart Star {k + 1}", V(-4.42, random.uniform(-1.1, 1.3), random.uniform(3.5, 5.5)), random.uniform(0.06, 0.12), M_RUNE, C_DETAIL)
# floating rune stones orbiting the column
for k in range(6):
    a = 2 * math.pi * k / 6 + 0.3
    c = PC + V(2.6 * math.cos(a), 2.6 * math.sin(a), 8.6 + 0.5 * math.sin(3 * a))
    rr = Euler((0.6, 0.3, a)).to_matrix()
    obox(f"Rune Stone {k + 1}", c, (0.5, 0.35, 0.7), rr @ X_AXIS, rr @ V(0, 1, 0), rr @ V(0, 0, 1), M_RUNE, C_DETAIL)
# starglass crystal clusters on meteor rocks
for i, (c, n, sz) in enumerate(((V(-3.6, 3.7, 2.3), 4, 1.0), (V(3.9, -3.5, 2.3), 3, 0.8), (V(-3.9, -3.7, 2.3), 3, 0.75))):
    rock(f"Meteor {i + 1}", c, (sz * 1.1, sz * 0.9, sz * 0.6), M_ROCK, C_DETAIL)
    for k in range(n):
        a = random.uniform(0, 2 * math.pi)
        crystal(f"Starglass {i + 1}-{k + 1}", c + V(math.cos(a), math.sin(a), 0) * sz * 0.4,
                V(math.cos(a) * 0.5, math.sin(a) * 0.5, 1), sz * random.uniform(1.6, 2.6), sz * random.uniform(.35, .5), M_CRYSTAL, C_DETAIL)

# ---------------------------------------------------------------- tidy
root_empty = bpy.data.objects.new("AstralOrreryMine", None)
root_empty.empty_display_type = 'PLAIN_AXES'
root_coll.objects.link(root_empty)
for ob in MINE_OBJECTS:
    me = ob.data
    c = sum((v.co for v in me.vertices), Vector()) / max(len(me.vertices), 1)
    me.transform(Matrix.Translation(-c))
    ob.location = c
    ob.parent = root_empty
tris = sum(len(p.vertices) - 2 for ob in MINE_OBJECTS for p in ob.data.polygons)
print(f"[mine] parts={len(MINE_OBJECTS)} triangles={tris}")

# ---------------------------------------------------------------- stage (renders only)
scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'AgX'
world = bpy.data.worlds.new("Night")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.008, 0.03, 1)
gme = bpy.data.meshes.new("Ground")
bm = bmesh.new();bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=120);bm.to_mesh(gme);bm.free()
ground = bpy.data.objects.new("Ground", gme);ground.location.z = -0.01;stage_coll.objects.link(ground)
M_GROUND = new_mat("Ground", lin((90, 96, 108)), rough=0.95);gme.materials.append(M_GROUND)
def add_light(name, kind, loc, energy, color, size=0.5, rot=None):
    ld = bpy.data.lights.new(name, kind);ld.energy = energy;ld.color = color
    if kind == 'SUN':ld.angle = math.radians(10)
    else:ld.shadow_soft_size = size
    ob = bpy.data.objects.new(name, ld);ob.location = loc
    if rot:ob.rotation_euler = rot
    stage_coll.objects.link(ob);return ob
add_light("Moon", 'SUN', V(0, 0, 30), 1.5, (0.7, 0.7, 1.0), rot=Euler((math.radians(50), 0, math.radians(30))))
add_light("Mine Glow", 'POINT', V(0, -4, 20), 6000, (0.6, 0.7, 1.0), size=3)
add_light("Front Fill", 'POINT', V(0, -16, 9), 3500, (0.75, 0.75, 1.0), size=4)
add_light("Back Fill", 'POINT', V(0, 15, 10), 2500, (0.65, 0.6, 1.0), size=4)
add_light("Side Fill L", 'POINT', V(14, -2, 8), 2000, (0.75, 0.75, 1.0), size=4)
add_light("Side Fill R", 'POINT', V(-14, -2, 8), 2000, (0.75, 0.75, 1.0), size=4)
CAMS = {
    "hero": (V(18, -21, 13), V(0, -0.5, 9.0), 35, (1200, 1000)),
    "front": (V(0, -38, 11), V(0, 0, 9.0), 50, (1000, 900)),
    "left": (V(-34, -1, 13), V(0, -1, 7.5), 50, (1000, 900)),
    "back": (V(-2, 34, 15), V(0, 0, 7.5), 50, (1000, 900)),
}
cam_objs = {}
for name, (loc, tgt, lens, res) in CAMS.items():
    cd = bpy.data.cameras.new(f"Cam {name}");cd.lens = lens
    co = bpy.data.objects.new(f"Cam {name}", cd);co.location = loc
    co.rotation_euler = (tgt - loc).to_track_quat('-Z', 'Y').to_euler();stage_coll.objects.link(co);cam_objs[name] = (co, res)
scene.camera = cam_objs["hero"][0]

# ---------------------------------------------------------------- export, save, render
os.makedirs(OUT, exist_ok=True)
exp_coll = bpy.data.collections.new("_export");scene.collection.children.link(exp_coll)
groups = {}
for ob in MINE_OBJECTS:
    groups.setdefault(ob.data.materials[0].name, []).append(ob)
joined = []
for mname, obs in groups.items():
    dups = []
    for ob in obs:
        dd = ob.copy();dd.data = ob.data.copy();dd.parent = None;dd.matrix_world = ob.matrix_world.copy()
        exp_coll.objects.link(dd);dups.append(dd)
    with bpy.context.temp_override(active_object=dups[0], selected_editable_objects=dups, selected_objects=dups):
        bpy.ops.object.join()
    j = dups[0];j.name = mname.split(" (")[0].replace(" ", "");joined.append(j)
for o in bpy.context.view_layer.objects:o.select_set(False)
for j in joined:
    j.select_set(True);print(f"[mine] export part {j.name}: {sum(len(p.vertices) - 2 for p in j.data.polygons)} tris")
fbx_path = os.path.join(OUT, "AstralOrreryMine_Roblox.fbx")
bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=True, object_types={'MESH'}, use_triangles=True, mesh_smooth_type='FACE', apply_unit_scale=True)
print("[mine] exported", fbx_path)
for j in joined:bpy.data.objects.remove(j, do_unlink=True)
bpy.data.collections.remove(exp_coll)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "AstralOrreryMine.blend"))
print("[mine] saved AstralOrreryMine.blend")
if RENDER:
    rdir = os.path.join(OUT, "renders");os.makedirs(rdir, exist_ok=True)
    for name in VIEWS.split(","):
        co, res = cam_objs[name];scene.camera = co
        scene.render.resolution_x, scene.render.resolution_y = res;scene.render.resolution_percentage = 100
        scene.render.filepath = os.path.join(rdir, f"{name}.png");bpy.ops.render.render(write_still=True);print("[mine] rendered", name)
