"""Frost Wyrm Mine - original Ore Factory mine for Blender 5.x (same pipeline as the Dragonglass Mine).

    python3 frost_wyrm_mine.py -- --out <folder> [--render] [--views hero,front,left,back] [--samples 64]
    (or: blender -b --factory-startup -P frost_wyrm_mine.py -- --out <folder> --render)

A frozen serpent coils up an ice-stone furnace and drops ice ore from its jaws. Saves
FrostWyrmMine.blend, exports FrostWyrmMine_Roblox.fbx (one mesh per material, 1 unit = 1 stud)
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
random.seed(11)
V = lambda *a: Vector(a)
X_AXIS = V(1, 0, 0)

scene = bpy.context.scene
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
root_coll = bpy.data.collections.new("FrostWyrmMine")
scene.collection.children.link(root_coll)
stage_coll = bpy.data.collections.new("Stage (not exported)")
scene.collection.children.link(stage_coll)


def sub_coll(name):
    c = bpy.data.collections.new(name)
    root_coll.children.link(c)
    return c


C_BASE, C_FURNACE, C_WYRM, C_ICE, C_DETAIL = (sub_coll(n) for n in ("Base", "Furnace", "Wyrm", "Ice", "Details"))
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


M_FROST = new_mat("Frost Stone (Slate)", lin((150, 180, 205)), rough=0.85)
add_noise(M_FROST, lin((118, 150, 182)), lin((190, 214, 232)), scale=1.8, bump=0.25)
M_DEEP = new_mat("Deep Ice (Marble)", lin((20, 34, 70)), rough=0.25)
add_marble(M_DEEP, lin((16, 28, 60)), lin((120, 200, 255)))
M_IRON = new_mat("Cold Iron (Metal)", lin((70, 78, 92)), rough=0.35, metal=0.8)
add_plate_bump(M_IRON, scale=10.0, strength=0.25)
M_TRIM = new_mat("Cyan Trim (Metal)", lin((40, 200, 230)), rough=0.3, metal=0.5, emit=lin((40, 200, 230)), emit_strength=0.5)
M_BLACK = new_mat("Black", lin((10, 14, 22)), rough=0.45)
M_SCALE = new_mat("Wyrm Scales", lin((60, 110, 170)), rough=0.5)
add_noise(M_SCALE, lin((40, 80, 140)), lin((95, 150, 205)), scale=6.0, bump=0.35)
M_BELLY = new_mat("Wyrm Belly", lin((205, 225, 240)), rough=0.6)
M_SNOW = new_mat("Snow", lin((240, 246, 255)), rough=0.9)
add_noise(M_SNOW, lin((222, 232, 245)), lin((252, 254, 255)), scale=4.0, bump=0.15)
M_ICE = new_mat("Ice Crystal", lin((150, 230, 255)), rough=0.08, emit=lin((90, 210, 255)), emit_strength=1.1)
M_NEON = new_mat("Neon (Frost Glow)", lin((200, 250, 255)), rough=0.3, emit=lin((150, 240, 255)), emit_strength=3.0)
M_EYE = new_mat("Eye Glow", lin((255, 255, 255)), rough=0.3, emit=lin((120, 255, 255)), emit_strength=10.0)
M_FLAME = new_mat("Frost Flame", lin((160, 240, 255)), rough=0.5, emit=lin((80, 220, 255)), emit_strength=12.0)
M_HORN = new_mat("Horn", lin((225, 232, 240)), rough=0.4)
M_ORE = new_mat("Ice Ore", lin((190, 245, 255)), rough=0.1, emit=lin((140, 230, 255)), emit_strength=1.4)

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


# ---------------------------------------------------------------- BASE (10 x 10 stud octagon)
def octagon(r, c):
    return chamfer_rect(2 * r, 2 * r, c)
slab("Base Slab", octagon(5.0, 1.6), 0.0, octagon(5.0, 1.6), 1.6, M_BLACK, C_BASE)
slab("Base Trim", octagon(5.06, 1.62), 1.6, octagon(5.06, 1.62), 1.85, M_TRIM, C_BASE)
slab("Base Top", octagon(4.75, 1.5), 1.85, octagon(4.2, 1.3), 2.35, M_DEEP, C_BASE)
for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):
    rock(f"Base Ice Chunk {i + 1}", V(sx * 4.3, sy * 4.3, 2.3), (0.9, 0.9, 0.6), M_SNOW, C_BASE)

# ---------------------------------------------------------------- FURNACE (round, tapering, iron bands)
FC = V(0, 0.6, 0)
bm = loft([ring_pts(FC + V(0, 0, z), V(0, 1, 0), X_AXIS, r, 16, math.pi / 16)
           for z, r in ((2.35, 3.3), (4.0, 3.15), (8.0, 2.75), (10.4, 2.5))])
finish("Furnace Body", bm, M_FROST, C_FURNACE)
for i, z in enumerate((3.2, 6.2, 9.2)):
    r = 3.3 - (z - 2.35) * 0.1
    tube(f"Furnace Band {i + 1}", FC + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), r + 0.18, r - 0.2, 0.42, M_IRON, C_FURNACE, n=32)
    for k in range(8):
        a = 2 * math.pi * k / 8
        sphere(f"Rivet {i + 1}-{k + 1}", FC + V((r + 0.2) * math.cos(a), (r + 0.2) * math.sin(a), z), 0.11, M_TRIM, C_FURNACE)
# glowing furnace window (front)
abox("Furnace Window Frame", -1.2, 1.2, FC.y - 3.35, FC.y - 2.75, 4.2, 6.6, M_IRON, C_FURNACE)
abox("Furnace Window Glow", -0.9, 0.9, FC.y - 3.4, FC.y - 2.9, 4.45, 6.35, M_NEON, C_FURNACE)
for i, x in enumerate((-0.45, 0, 0.45)):
    abox(f"Furnace Grate {i + 1}", x - 0.07, x + 0.07, FC.y - 3.45, FC.y - 3.3, 4.45, 6.35, M_BLACK, C_FURNACE)
# snow cap and chimney
bm = loft([ring_pts(FC + V(0, 0, 10.35), V(0, 1, 0), X_AXIS, 2.65, 16),
           ring_pts(FC + V(0, 0, 10.9), V(0, 1, 0), X_AXIS, 2.4, 16),
           ring_pts(FC + V(0, 0, 11.3), V(0, 1, 0), X_AXIS, 1.6, 16)])
finish("Snow Cap", bm, M_SNOW, C_FURNACE)
cyl("Chimney", FC + V(1.1, 1.0, 10.8), FC + V(1.1, 1.0, 13.6), 0.55, 0.5, M_IRON, C_FURNACE, n=12)
tube("Chimney Lip", FC + V(1.1, 1.0, 13.6), V(0, 0, 1), V(0, 1, 0), 0.72, 0.42, 0.3, M_IRON, C_FURNACE, n=12)

# ---------------------------------------------------------------- WYRM: coils up the furnace, head over the front
def wyrm_path(t):
    """t 0..1 along the body: 1.6 turns round the furnace rising from the base, then out to the head."""
    a = math.radians(-90 - 576) + t * 2 * math.pi * 1.6  # ends at the front (-Y)
    r = 3.75 - 0.9 * t
    z = 2.7 + 9.0 * t
    return FC + V(r * math.cos(a), r * math.sin(a), z)
pts = [wyrm_path(i / 60) for i in range(61)]
# neck: from the last coil point up and forward over the front
end = pts[-1]
neck = [end + V(-end.x * (k / 8), -1.6 * (k / 8), 2.9 * math.sin(math.pi / 2 * k / 8)) for k in range(1, 9)]
pts += neck
rad = [0.25 + 0.95 * min(1, i / 10) * (1 - 0.25 * i / len(pts)) for i in range(len(pts))]
rings = []
for i, p in enumerate(pts):
    d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
    u, v = perp_basis(d)
    rings.append(ring_pts(p, u, v, rad[i], 12))
finish("Wyrm Body", loft(rings, cap0=True, cap1=True), M_SCALE, C_WYRM, merge=0.0005)
# belly plates and back spines along the coil
for i in range(4, len(pts) - 2, 3):
    p, q = pts[i], pts[i + 1]
    d = (q - p).normalized();out = (p - FC);out.z = 0;out.normalize()
    obox(f"Belly Plate {i}", p - out * rad[i] * 0.75, (0.9, 0.18, rad[i] * 1.1), d, out, d.cross(out), M_BELLY, C_WYRM)
    tip = p + V(0, 0, 1) * (rad[i] + 0.9) + out * 0.2
    blade(f"Spine {i}", [p + V(0, 0, rad[i] * 0.7) - d * 0.35, tip, p + V(0, 0, rad[i] * 0.7) + d * 0.35], 0.16, M_ICE, C_WYRM)
# head: tapered snout pointing forward and down, jaws open
H0 = pts[-1];HD = V(0, -1, -0.35).normalized();hu, hv = perp_basis(HD, V(0, 0, 1))
head_rings = [ring_pts(H0 + HD * s, hu, hv, r, 10) for s, r in ((0, 1.2), (0.9, 1.25), (1.9, 1.0), (2.8, 0.7))]
finish("Wyrm Head", loft(head_rings), M_SCALE, C_WYRM, merge=0)
jaw0 = H0 + HD * 0.6 - hu * 0.9
jd = (HD - V(0, 0, 0.55)).normalized()
ju, jv = perp_basis(jd, V(0, 0, 1))
finish("Wyrm Jaw", loft([ring_pts(jaw0 + jd * s, ju, jv, r, 8) for s, r in ((0, 0.75), (1.2, 0.65), (2.3, 0.35))]), M_SCALE, C_WYRM, merge=0)
for k in range(5):
    s = 1.0 + k * 0.35
    for side in (-1, 1):
        base = H0 + HD * s - hu * 0.85 + X_AXIS * side * 0.55
        cyl(f"Fang {k + 1}{'L' if side < 0 else 'R'}", base, base - V(0, 0, 0.45), 0.1, 0.0, M_HORN, C_WYRM, n=6)
for side, label in ((1, "L"), (-1, "R")):
    sphere(f"Eye {label}", H0 + HD * 1.3 + hu * 0.55 + X_AXIS * side * 0.85, 0.24, M_EYE, C_WYRM)
    cyl(f"Horn {label} 1", H0 + hu * 0.8 + X_AXIS * side * 0.6, H0 + hu * 2.6 + X_AXIS * side * 1.3 + V(0, 1.4, 0), 0.32, 0.05, M_HORN, C_WYRM, n=8)
    cyl(f"Horn {label} 2", H0 + hu * 0.4 + X_AXIS * side * 1.0, H0 + hu * 1.5 + X_AXIS * side * 2.1 + V(0, 1.0, 0), 0.22, 0.03, M_HORN, C_WYRM, n=8)
    blade(f"Fin {label}", [H0 + X_AXIS * side * 1.05, H0 + X_AXIS * side * 2.6 + V(0, 1.2, 0.6), H0 + X_AXIS * side * 1.1 + V(0, 1.4, -0.6)], 0.1, M_ICE, C_WYRM)
# frost breath / ore spout ring in the mouth
MOUTH = H0 + HD * 2.6 - hu * 0.55
torus("Mouth Frost Ring", MOUTH, HD, hu, 0.55, 0.09, M_NEON, C_WYRM, n_major=24, n_minor=8)
ore_rot = Euler((0.4, 0.3, 0.6)).to_matrix()
obox("Ore (optional)", MOUTH + HD * 1.4 - V(0, 0, 1.2), (0.95, 0.95, 0.95), ore_rot @ X_AXIS, ore_rot @ V(0, 1, 0), ore_rot @ V(0, 0, 1), M_ORE, C_WYRM)

# ---------------------------------------------------------------- ICE: crystal clusters
random.seed(23)
def cluster(name, C, n, size):
    rock(f"{name} Rock", C, (size * 1.1, size * 0.9, size * 0.6), M_DEEP, C_ICE)
    for k in range(n):
        a = random.uniform(0, 2 * math.pi)
        dirv = V(math.cos(a) * random.uniform(.2, .7), math.sin(a) * random.uniform(.2, .7), 1)
        crystal(f"{name} Crystal {k + 1}", C + V(math.cos(a), math.sin(a), 0) * size * 0.4, dirv,
                size * random.uniform(1.6, 2.8), size * random.uniform(.35, .55), M_ICE, C_ICE)
cluster("Back Cluster", FC + V(0.2, 3.6, 2.6), 6, 1.3)
cluster("Top Cluster", FC + V(-0.8, -0.2, 11.2), 4, 0.9)
cluster("Side Cluster", FC + V(3.9, -2.4, 2.5), 4, 0.8)

# ---------------------------------------------------------------- DETAILS
# frost lantern (left-front corner)
LX, LY = 3.7, -3.4
cyl("Lantern Post", V(LX, LY, 2.35), V(LX, LY, 4.6), 0.18, 0.18, M_IRON, C_DETAIL, n=8)
cyl("Lantern Cage", V(LX, LY, 4.6), V(LX, LY, 5.9), 0.55, 0.55, M_NEON, C_DETAIL, n=8)
cyl("Lantern Roof", V(LX, LY, 5.9), V(LX, LY, 6.7), 0.75, 0.0, M_IRON, C_DETAIL, n=8)
flame = [ring_pts(V(LX, LY, 4.8 + z), V(0, 1, 0), X_AXIS, r, 10) for z, r in ((0, .12), (.25, .3), (.55, .26), (.85, .1))] + [[V(LX, LY, 5.75)] * 10]
finish("Lantern Frost Flame", loft(flame, cap1=False), M_FLAME, C_DETAIL, smooth=True, merge=0.001)
# snowflake emblem on the right side of the furnace
EM = FC + V(-3.05, 0, 6.2)
torus("Emblem Ring", EM, V(-1, 0, 0), V(0, 0, 1), 1.0, 0.09, M_NEON, C_DETAIL, n_major=24, n_minor=6)
for k in range(6):
    a = math.pi * k / 3
    dvec = V(0, math.cos(a), math.sin(a))
    beam(f"Emblem Spoke {k + 1}", EM, EM + dvec * 0.95, 0.12, 0.12, V(-1, 0, 0), M_NEON, C_DETAIL)
    beam(f"Emblem Twig {k + 1}a", EM + dvec * 0.6, EM + dvec * 0.6 + (dvec + V(0, -dvec.z, dvec.y) * 0.8).normalized() * 0.3, 0.08, 0.08, V(-1, 0, 0), M_NEON, C_DETAIL)
# pressure gauge (back-left)
GC = FC + V(2.2, 2.6, 7.4)
cyl("Gauge Body", GC, GC + V(0.35, 0.35, 0), 0.6, 0.6, M_IRON, C_DETAIL, n=16, hint=V(0, 0, 1))
cyl("Gauge Face", GC + V(0.36, 0.36, 0), GC + V(0.4, 0.4, 0), 0.48, 0.48, M_BELLY, C_DETAIL, n=16, hint=V(0, 0, 1))
beam("Gauge Needle", GC + V(0.42, 0.42, 0), GC + V(0.42, 0.42, 0) + V(-0.2, 0.2, 0.3), 0.05, 0.05, V(1, -1, 0), M_BLACK, C_DETAIL)
# icicles hanging from the snow cap
for k in range(10):
    a = 2 * math.pi * k / 10 + 0.2
    if abs(math.sin(a) + 1) < 0.25:
        continue
    p = FC + V(2.55 * math.cos(a), 2.55 * math.sin(a), 10.4)
    cyl(f"Icicle {k + 1}", p, p - V(0, 0, random.uniform(0.6, 1.4)), 0.16, 0.0, M_ICE, C_DETAIL, n=6)

# ---------------------------------------------------------------- tidy
root_empty = bpy.data.objects.new("FrostWyrmMine", None)
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
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.01, 0.018, 0.04, 1)
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
add_light("Moon", 'SUN', V(0, 0, 30), 1.5, (0.6, 0.75, 1.0), rot=Euler((math.radians(50), 0, math.radians(30))))
add_light("Mine Glow", 'POINT', V(0, -4, 20), 6000, (0.45, 0.8, 1.0), size=3)
add_light("Front Fill", 'POINT', V(0, -16, 9), 3500, (0.6, 0.8, 1.0), size=4)
add_light("Back Fill", 'POINT', V(0, 15, 10), 2500, (0.5, 0.7, 1.0), size=4)
add_light("Side Fill L", 'POINT', V(14, -2, 8), 2000, (0.6, 0.8, 1.0), size=4)
add_light("Side Fill R", 'POINT', V(-14, -2, 8), 2000, (0.6, 0.8, 1.0), size=4)
CAMS = {
    "hero": (V(17, -19, 12), V(0, -0.5, 7.5), 35, (1200, 1000)),
    "front": (V(0, -36, 10), V(0, 0, 7.5), 50, (1000, 900)),
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
fbx_path = os.path.join(OUT, "FrostWyrmMine_Roblox.fbx")
bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=True, object_types={'MESH'}, use_triangles=True, mesh_smooth_type='FACE', apply_unit_scale=True)
print("[mine] exported", fbx_path)
for j in joined:bpy.data.objects.remove(j, do_unlink=True)
bpy.data.collections.remove(exp_coll)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FrostWyrmMine.blend"))
print("[mine] saved FrostWyrmMine.blend")
if RENDER:
    rdir = os.path.join(OUT, "renders");os.makedirs(rdir, exist_ok=True)
    for name in VIEWS.split(","):
        co, res = cam_objs[name];scene.camera = co
        scene.render.resolution_x, scene.render.resolution_y = res;scene.render.resolution_percentage = 100
        scene.render.filepath = os.path.join(rdir, f"{name}.png");bpy.ops.render.render(write_still=True);print("[mine] rendered", name)
