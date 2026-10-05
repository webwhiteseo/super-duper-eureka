"""Cyber Neon Mine - tech variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in black carbon and chrome with cyan and magenta neon:
an antenna-array crown with glowing tips, twin antenna masts and a radar dish, angular panel wings on glowing
struts, a stacked power-core heart, a cable tail ending in a plug, and a hologram projector. Renders use Cycles.

Run from a terminal:
    blender -b --factory-startup -P cyber_neon_mine.py -- --out <folder> [--render] [--views front,left]
    (or: python3 cyber_neon_mine.py -- --out <folder> --render  with the bpy module)

Builds the model, saves CyberNeonMine.blend, exports CyberNeonMine_Roblox.fbx
(one mesh per material, ready for Roblox's 3D importer) and optionally renders
preview images that match the reference screenshot angles.

Units: 1 Blender unit = 1 Roblox stud. The mine faces -Y, +Z is up,
+X is the mine's left (lantern side), -X its right (screen box side).
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
VIEWS = arg("--views", "front,left,right,back,top,hero")
SAMPLES = int(arg("--samples", 32))
WITH_BASE = bool(arg("--base", False))  # no plinth by default
BASE_H = 2.45
random.seed(7)

V = lambda *a: Vector(a)
X_AXIS = V(1, 0, 0)

# --------------------------------------------------------------------------
# Scene reset
# --------------------------------------------------------------------------
scene = bpy.context.scene
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)

root_coll = bpy.data.collections.new("CyberNeonMine")
scene.collection.children.link(root_coll)
stage_coll = bpy.data.collections.new("Stage (not exported)")
scene.collection.children.link(stage_coll)


def sub_coll(name):
    c = bpy.data.collections.new(name)
    root_coll.children.link(c)
    return c


C_BASE, C_BODY, C_HEAD, C_WINGS, C_DETAIL = (sub_coll(n) for n in ("Base", "Body", "Head", "Wings", "Details"))
MINE_OBJECTS = []

# --------------------------------------------------------------------------
# Materials
# --------------------------------------------------------------------------


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


RBX = {}   # export name -> (Roblox material, rgb 0-255, transparency, light (r, g, b, range, brightness) or None)


def MAT(name, rgb, rbx, rough=0.6, metal=0.0, glow=None, strength=0.0, alpha=0.0, light=None, noise=None, marble=None, plate=None):
    m = new_mat(name, lin(rgb), rough=rough, metal=metal, emit=lin(glow) if glow else None, emit_strength=strength)
    if noise:
        add_noise(m, lin(noise[0]), lin(noise[1]), scale=noise[2], bump=noise[3])
    if marble:
        add_marble(m, lin(marble[0]), lin(marble[1]))
    if plate:
        add_plate_bump(m, scale=plate)
    g = glow or rgb
    RBX[name.split(" (")[0].replace(" ", "")] = (rbx, rgb, alpha, (g[0], g[1], g[2], light[0], light[1]) if light else None)
    return m


M_STONE = MAT("Carbon Shell", (34, 36, 46), "Metal", rough=0.35, metal=0.5, noise=((24, 26, 34), (52, 54, 66), 6.0, 0.12))
M_BLACK = MAT("Black", (6, 6, 10), "SmoothPlastic", rough=0.4)
M_NAVY = MAT("Chrome (Metal)", (156, 162, 176), "Metal", rough=0.18, metal=0.95)
M_RIM = MAT("Cyan Trim (DiamondPlate)", (0, 240, 255), "Neon", rough=0.35, metal=0.5, glow=(0, 240, 255), strength=0.8, plate=14.0)
M_MARBLE = MAT("Circuit Marble", (10, 12, 18), "Marble", rough=0.25, marble=((8, 10, 14), (0, 220, 255)))
M_NEON = MAT("Neon (Glow)", (130, 250, 255), "Neon", rough=0.3, glow=(0, 230, 255), strength=2.6, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Holo)", (255, 70, 225), "Glass", rough=0.1, glow=(255, 30, 210), strength=1.2, alpha=0.2, light=(8, 0.7))
M_ROCK = MAT("Server Block", (24, 26, 34), "SmoothPlastic", rough=0.4, metal=0.3)
M_WING = MAT("Wing Panel", (18, 20, 28), "SmoothPlastic", rough=0.3, metal=0.4, noise=((12, 14, 20), (34, 38, 50), 9.0, 0.08))
M_BONE = MAT("Wing Strut", (0, 230, 255), "Neon", rough=0.3, glow=(0, 220, 255), strength=3.0)
M_FLAME = MAT("Flame", (255, 90, 235), "Neon", rough=0.5, glow=(255, 40, 220), strength=10.0, light=(12, 2))
M_SCREEN = MAT("Screen", (120, 255, 255), "Neon", rough=0.3, glow=(0, 230, 255), strength=8.0)
M_PINK = MAT("Magenta LED", (255, 40, 200), "Neon", rough=0.3, glow=(255, 20, 190), strength=5.0)
M_BLUEBALL = MAT("Cyan Knob", (0, 240, 255), "Neon", rough=0.3, glow=(0, 220, 255), strength=2.0)
M_ORE = MAT("Ore", (130, 255, 255), "Neon", rough=0.2, glow=(0, 230, 255), strength=1.4)
M_HORN = MAT("Antenna (Metal)", (156, 162, 176), "Metal", rough=0.18, metal=0.95)
M_MAG = MAT("Magenta (Glow)", (255, 50, 210), "Neon", rough=0.3, glow=(255, 30, 200), strength=5.0, light=(10, 1.2))
M_HOLO = MAT("Hologram (Glass)", (90, 240, 255), "ForceField", rough=0.1, glow=(40, 220, 255), strength=1.5, alpha=0.5)

# --------------------------------------------------------------------------
# Geometry helpers (everything is built directly in world space)
# --------------------------------------------------------------------------


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


def clip_to_ground(z0=0.0):
    """Cut every part flat at the ground and cap the cut, so the mine sits on whatever it is placed on."""
    for ob in list(MINE_OBJECTS):
        me = ob.data
        if min(v.co.z for v in me.vertices) >= z0 - 1e-4:
            continue
        if max(v.co.z for v in me.vertices) <= z0 + 1e-3:
            MINE_OBJECTS.remove(ob)
            bpy.data.objects.remove(ob, do_unlink=True)
            continue
        bm = bmesh.new()
        bm.from_mesh(me)
        res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-5,
                                     plane_co=V(0, 0, z0), plane_no=V(0, 0, 1), clear_inner=True)
        cut = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge) and e.is_valid and e.is_boundary]
        if cut:
            for f in bmesh.ops.holes_fill(bm, edges=cut, sides=0)["faces"]:
                f.smooth = False
        bm.to_mesh(me)
        bm.free()
        me.update()


# --------------------------------------------------------------------------
# BASE  (9 x 11.3 studs footprint)
# --------------------------------------------------------------------------
BW, BL = 9.0, 11.3
if WITH_BASE:
    slab("Base Slab", chamfer_rect(BW, BL, 1.0), 0.0, chamfer_rect(BW, BL, 1.0), 1.8, M_BLACK, C_BASE)
    slab("Base Trim", chamfer_rect(BW + 0.08, BL + 0.08, 1.03), 1.8, chamfer_rect(BW + 0.08, BL + 0.08, 1.03), 2.0,
         M_RIM, C_BASE)
    slab("Base Top", chamfer_rect(BW - 0.4, BL - 0.4, 0.92), 2.0, chamfer_rect(BW - 1.1, BL - 1.1, 0.75), 2.5,
         M_MARBLE, C_BASE)

# --------------------------------------------------------------------------
# BODY
# --------------------------------------------------------------------------
TW = 2.95  # torso half-width
profile_x("Torso", [(-3.75, 2.45), (1.2, 2.45), (1.2, 8.3), (-3.15, 8.3)], -TW, TW, M_STONE, C_BODY)
profile_x("Haunch", [(0.8, 2.45), (4.2, 2.45), (4.2, 5.8), (1.9, 7.9), (0.8, 7.9)], -TW - 0.05, TW + 0.05,
          M_STONE, C_BODY)
profile_x("Back Plate", [(-1.3, 7.6), (1.7, 7.6), (1.7, 15.5), (1.2, 16.1), (-1.3, 14.1)], -2.4, 2.4,
          M_STONE, C_BODY)

# --------------------------------------------------------------------------
# HEAD - a pipe that bends down 30 deg in two glowing 15 deg joints
# --------------------------------------------------------------------------
HR, ZC, NSEG = 2.7, 11.0, 40
C = V(0, -0.9, ZC)
d = V(0, -1, 0)
u = V(0, 0, 1)
stone_rings, glow_rings = [], []
C1 = C + d * 1.2
stone_rings.append([ring_pts(C, u, X_AXIS, HR, NSEG), ring_pts(C1, u, X_AXIS, HR, NSEG)])
C = C1
for wedge_deg, seg_len in ((15, 1.4), (15, 0.8)):
    pivot = C - u * HR
    rings = []
    for i in range(5):
        R = Matrix.Rotation(math.radians(wedge_deg) * i / 4, 3, 'X')
        rings.append(ring_pts(pivot + R @ (C - pivot), R @ u, X_AXIS, HR - 0.07, NSEG))
    glow_rings.append(rings)
    R = Matrix.Rotation(math.radians(wedge_deg), 3, 'X')
    C, u, d = pivot + R @ (C - pivot), R @ u, R @ d
    C1 = C + d * seg_len
    stone_rings.append([ring_pts(C, u, X_AXIS, HR, NSEG), ring_pts(C1, u, X_AXIS, HR, NSEG)])
    C = C1

bm = bmesh.new()
for rings in stone_rings:
    loft(rings, bm=bm)
finish("Head Segments", bm, M_STONE, C_HEAD)
bm = bmesh.new()
for rings in glow_rings:
    loft(rings, bm=bm)
finish("Head Glow Strips", bm, M_NEON, C_HEAD, merge=0.002)

# Local frame at the mouth: O = ring centre, A = forward axis, U = up, X = lateral
A, U = d.normalized(), u.normalized()
O = C + A * 0.1
HEAD_FRAME = (O.copy(), A.copy(), U.copy())


def radial(theta_deg):
    t = math.radians(theta_deg)
    return math.cos(t) * X_AXIS + math.sin(t) * U


def tangent(theta_deg):
    t = math.radians(theta_deg)
    return -math.sin(t) * X_AXIS + math.cos(t) * U


# Mouth ring: dark navy faces, a glowing band round the outside showing between
# 8 black cogs, and a thin glowing line on the inner edge
tube("Mouth Ring Glow", O, A, U, 3.02, 2.66, 0.5, M_NEON, C_HEAD)
tube("Mouth Ring Rim Back", O - A * 0.3, A, U, 3.18, 2.55, 0.16, M_NAVY, C_HEAD)
tube("Mouth Ring Rim Front", O + A * 0.3, A, U, 3.18, 2.55, 0.16, M_NAVY, C_HEAD)
torus("Mouth Inner Glow", O + A * 0.4, A, U, 2.58, 0.07, M_NEON, C_HEAD)
for k in range(8):
    th = 22.5 + 45 * k
    r_, t_ = radial(th), tangent(th)
    c0, c1 = O + r_ * 2.95, O + r_ * 3.55
    hexa(f"Mouth Cog {k + 1}",
         [c0 - t_ * 0.3 - A * 0.36, c0 + t_ * 0.3 - A * 0.36, c0 + t_ * 0.3 + A * 0.36, c0 - t_ * 0.3 + A * 0.36,
          c1 - t_ * 0.3 - A * 0.36, c1 + t_ * 0.3 - A * 0.36, c1 + t_ * 0.3 + A * 0.36, c1 - t_ * 0.3 + A * 0.36],
         M_BLACK, C_HEAD)

# Face plate (disc + shallow dome) inside the ring
cap_r, cap_h = 2.6, 0.6
Rs = (cap_r ** 2 + cap_h ** 2) / (2 * cap_h)
V_ = A.cross(U).normalized() * -1
rings = [ring_pts(O - A * 0.2, U, V_, cap_r, NSEG), ring_pts(O + A * 0.35, U, V_, cap_r, NSEG)]
for i in range(1, 6):
    z = cap_h * i / 6
    rings.append(ring_pts(O + A * (0.35 + z), U, V_, math.sqrt(max(Rs ** 2 - (Rs - cap_h + z) ** 2, 0)), NSEG))
rings.append([O + A * (0.35 + cap_h)] * NSEG)
finish("Face Plate", loft(rings, cap1=False), M_STONE, C_HEAD, merge=0.001)

# Inner ring with black clamps
IR = O + A * 1.05
tube("Inner Ring Rim", IR, A, U, 1.88, 1.72, 0.42, M_NAVY, C_HEAD)
tube("Inner Ring Glow", IR, A, U, 1.72, 1.45, 0.34, M_NEON, C_HEAD)
for i, th in enumerate((0, 65, 115, 180, 245, 295)):
    r_, t_ = radial(th), tangent(th)
    c0, c1 = IR + r_ * 1.8, IR + r_ * 2.3
    hexa(f"Inner Clamp {i + 1}",
         [c0 - t_ * 0.24 - A * 0.28, c0 + t_ * 0.24 - A * 0.28, c0 + t_ * 0.24 + A * 0.28, c0 - t_ * 0.24 + A * 0.28,
          c1 - t_ * 0.24 - A * 0.28, c1 + t_ * 0.24 - A * 0.28, c1 + t_ * 0.24 + A * 0.28, c1 - t_ * 0.24 + A * 0.28],
         M_BLACK, C_HEAD)

# Struts converging on the spout
NZ = O + A * 3.6
for i, th in enumerate((0, 90, 180, 270)):
    r_ = radial(th)
    beam(f"Spout Strut {i + 1}", O + r_ * 2.2 + A * 0.35, NZ + r_ * 0.95 - A * 0.15, 0.4, 0.4, tangent(th),
         M_STONE, C_HEAD)

# Spout / nozzle
tube("Spout Collar", NZ, A, U, 1.15, 0.78, 0.42, M_NAVY, C_HEAD, n=32)
torus("Spout Glow", NZ + A * 0.24, A, U, 0.97, 0.1, M_NEON, C_HEAD, n_major=32, n_minor=8)
cyl("Spout Tip", NZ - A * 0.4, NZ + A * 0.9, 0.78, 0.0, M_STONE, C_HEAD, n=20, hint=U)

# Antenna-array crown: thin chrome masts with glowing magenta tips
F = V(0, -1, 0)
for i, th in enumerate([90 + 360 * k / 7 for k in range(7)]):
    th = th % 360
    r_ = radial(th)
    L = 4.2 if abs(th - 90) < 1 else 3.3 if math.sin(math.radians(th)) > 0 else 2.6
    d_ = (A * 0.4 + F * 0.6 + r_ * 0.6).normalized()
    p0 = O + r_ * 2.95 + A * 0.3
    cyl(f"Mast {i + 1}", p0, p0 + d_ * L, 0.16, 0.06, M_HORN, C_HEAD, n=6)
    for k in range(2):
        q = p0 + d_ * L * (0.45 + 0.25 * k)
        torus(f"Mast Ring {i + 1}-{k + 1}", q, d_, perp_basis(d_)[0], 0.16, 0.04, M_NEON, C_HEAD, n_major=10, n_minor=4)
    sphere(f"Mast Tip {i + 1}", p0 + d_ * L, 0.17, M_MAG, C_HEAD)

# Twin antenna towers and a radar dish
O_, A_, U_ = HEAD_FRAME
for side, label in ((1, "L"), (-1, "R")):
    b = O_ + U_ * 2.4 + X_AXIS * side * 1.7 - A_ * 1.6
    t = b + U_ * 3.4 - A_ * 1.0 + X_AXIS * side * 0.3
    cyl(f"Antenna Tower {label}", b, t, 0.22, 0.08, M_HORN, C_HEAD, n=8)
    for k in range(3):
        q = b + (t - b) * (0.3 + 0.25 * k)
        torus(f"Tower Ring {label} {k + 1}", q, (t - b).normalized(), X_AXIS, 0.26 - 0.05 * k, 0.05, M_MAG if k % 2 else M_NEON, C_HEAD, n_major=12, n_minor=4)
    sphere(f"Tower Beacon {label}", t, 0.22, M_MAG, C_HEAD)
D = O_ + U_ * 1.6 + X_AXIS * 2.9 - A_ * 2.2
cyl("Radar Arm", D, D + X_AXIS * 0.6 + U_ * 0.5, 0.1, 0.1, M_HORN, C_HEAD, n=6)
dn = (X_AXIS * 0.7 + U_ * 0.6 + F * 0.0 - A_ * 0.2).normalized() if False else (X_AXIS * 0.7 + U_ * 0.6 - A_ * 0.2).normalized()
Dc = D + X_AXIS * 0.6 + U_ * 0.5
rings = [ring_pts(Dc + dn * z, perp_basis(dn)[0], perp_basis(dn)[1], r, 16) for z, r in ((0.0, 0.15), (0.12, 0.6), (0.3, 0.95), (0.36, 1.0))]
finish("Radar Dish", loft(rings, cap0=True, cap1=False), M_NAVY, C_HEAD, merge=0.0005)
cyl("Radar Feed", Dc, Dc + dn * 0.9, 0.05, 0.05, M_HORN, C_HEAD, n=6)
sphere("Radar Feed Tip", Dc + dn * 0.95, 0.1, M_NEON, C_HEAD)

# The glowing ore cube that sits at the spout (delete if you don't want it)
ore_rot = Euler((0.3, 0.2, 0.5)).to_matrix()
obox("Ore (optional)", O + A * 5.1 - U * 0.9, (0.95, 0.95, 0.95),
     ore_rot @ X_AXIS, ore_rot @ V(0, 1, 0), ore_rot @ V(0, 0, 1), M_ORE, C_HEAD)

# --------------------------------------------------------------------------
# WINGS - vertical bat wings, swept back
# --------------------------------------------------------------------------
WRIST = (3.0, 17.2)
TIPS = [(10.2, 14.4), (9.0, 11.0), (6.6, 8.4), (3.8, 8.2)]
ROOT_TOP, ROOT_BOT = (0.0, 15.0), (0.3, 11.0)
LEAD = [ROOT_TOP, (1.3, 16.3), WRIST, (6.0, 16.6), (8.6, 15.6), TIPS[0]]


def scallop(Pa, Pb, k=0.3, steps=5):
    mid = ((Pa[0] + Pb[0]) / 2, (Pa[1] + Pb[1]) / 2)
    ctrl = (mid[0] + (WRIST[0] - mid[0]) * k, mid[1] + (WRIST[1] - mid[1]) * k)
    out = []
    for i in range(1, steps):
        t = i / steps
        out.append(tuple((1 - t) ** 2 * Pa[j] + 2 * (1 - t) * t * ctrl[j] + t * t * Pb[j] for j in range(2)))
    return out


OUTLINE = LEAD[:]
for Pa, Pb in zip(TIPS, TIPS[1:] + [ROOT_BOT]):
    OUTLINE += scallop(Pa, Pb, k=0.0 if Pb != ROOT_BOT else 0.22) + [Pb]


def build_wing(side, label):
    sweep = math.radians(32)
    h = V(side * math.cos(sweep), math.sin(sweep), 0)
    root = V(side * 2.3, 0.6, 0)
    n = h.cross(V(0, 0, 1)).normalized()

    def P(s, z, off=0.0):
        return root + h * s + V(0, 0, z) + n * off

    bm = bmesh.new()
    fr = [bm.verts.new(P(s, z, 0.05)) for s, z in OUTLINE]
    bk = [bm.verts.new(P(s, z, -0.05)) for s, z in OUTLINE]
    bm.faces.new(fr)
    bm.faces.new(list(reversed(bk)))
    for j in range(len(fr)):
        k = (j + 1) % len(fr)
        bm.faces.new((fr[k], fr[j], bk[j], bk[k]))
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
    finish(f"Wing {label} Membrane", bm, M_WING, C_WINGS)
    cyl(f"Wing {label} Arm", P(0.0, 13.4), P(*WRIST), 0.24, 0.15, M_BONE, C_WINGS, n=10)
    for i, tip in enumerate(TIPS):
        cyl(f"Wing {label} Finger {i + 1}", P(*WRIST), P(*tip), 0.13, 0.04, M_BONE, C_WINGS, n=8)
    cyl(f"Wing {label} Claw", P(*WRIST), P(WRIST[0] - 0.5, WRIST[1] + 1.6), 0.22, 0.0, M_HORN, C_WINGS, n=8)


build_wing(+1, "L")
build_wing(-1, "R")

# --------------------------------------------------------------------------
# DETAILS
# --------------------------------------------------------------------------
# Battery on the back, between two crystal clusters
BY = 2.75
cyl("Battery Cap Bottom", V(0, BY, 8.0), V(0, BY, 9.15), 1.12, 1.12, M_NAVY, C_DETAIL)
cyl("Power Core", V(0, BY, 9.15), V(0, BY, 11.7), 0.45, 0.45, M_NEON, C_DETAIL, n=16)
for k in range(5):
    torus(f"Core Ring {k + 1}", V(0, BY, 9.45 + k * 0.5), V(0, 0, 1), V(0, 1, 0), 0.82, 0.12, M_MAG if k % 2 else M_NAVY, C_DETAIL, n_major=24, n_minor=6)
for i in range(4):
    a_ = 2 * math.pi * i / 4 + math.pi / 4
    beam(f"Core Rail {i + 1}", V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), 9.15), V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), 11.7),
         0.14, 0.14, V(math.cos(a_), math.sin(a_), 0), M_BLACK, C_DETAIL)
cyl("Battery Cap Top", V(0, BY, 11.7), V(0, BY, 12.9), 1.12, 1.12, M_NAVY, C_DETAIL)
for zc in (8.57, 12.3):
    for i, ang in enumerate((-50, 0, 50)):
        a_ = math.radians(ang)
        sphere(f"Battery Stud {zc:.0f}-{i + 1}", V(1.12 * math.sin(a_), BY + 1.12 * math.cos(a_), zc),
               0.17 if ang == 0 else 0.12, M_NEON, C_DETAIL)

rock("Crystal Rock Top", V(0, 2.45, 13.75), (1.5, 1.05, 0.9), M_ROCK, C_DETAIL)
crystal("Crystal Top 1", V(-0.5, 2.35, 14.1), V(-0.3, 0.2, 1), 3.1, 0.78, M_CRYSTAL, C_DETAIL)
crystal("Crystal Top 2", V(0.65, 2.5, 14.05), V(0.5, 0.3, 1), 2.5, 0.7, M_CRYSTAL, C_DETAIL)
crystal("Crystal Top 3", V(0.05, 3.15, 13.6), V(0.1, 1, 0.15), 1.7, 0.68, M_CRYSTAL, C_DETAIL)
crystal("Crystal Top 4", V(-0.9, 2.9, 13.6), V(-0.8, 0.8, 0.5), 1.4, 0.55, M_CRYSTAL, C_DETAIL)

rock("Crystal Rock Bottom", V(0, 4.15, 6.95), (1.6, 1.1, 0.95), M_ROCK, C_DETAIL)
crystal("Crystal Bottom 1", V(0.05, 4.25, 7.3), V(0, 0.3, 1), 2.2, 0.85, M_CRYSTAL, C_DETAIL)
crystal("Crystal Bottom 2", V(-0.95, 4.4, 6.9), V(-1, 0.7, 0.1), 1.7, 0.72, M_CRYSTAL, C_DETAIL)
crystal("Crystal Bottom 3", V(1.0, 4.4, 6.8), V(1, 0.7, -0.1), 1.6, 0.72, M_CRYSTAL, C_DETAIL)
crystal("Crystal Bottom 4", V(0.2, 4.9, 6.6), V(0.2, 1, -0.2), 1.3, 0.6, M_CRYSTAL, C_DETAIL)

# Cable tail with glowing rings, ending in a plug
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.75 * (1 - i / 9), 0.75 * (1 - (i + 1) / 9)
    cyl(f"Cable {i + 1}", tail[i], tail[i + 1], max(r0, 0.2), max(r1, 0.2), M_STONE, C_DETAIL, n=10)
    d_ = (tail[i + 1] - tail[i]).normalized()
    torus(f"Cable Ring {i + 1}", tail[i + 1], d_, V(0, 0, 1), max(r1, 0.2) + 0.04, 0.06, M_NEON if i % 2 else M_MAG, C_DETAIL, n_major=12, n_minor=4)
d_ = (tail[-1] - tail[-2]).normalized()
s_ = V(-d_.y, d_.x, 0)
P0 = tail[-1] + d_ * 0.35
obox("Plug", P0, (0.7, 0.6, 0.5), d_, s_, V(0, 0, 1), M_NAVY, C_DETAIL)
for sgn in (1, -1):
    cyl(f"Plug Prong {sgn}", P0 + d_ * 0.35 + s_ * sgn * 0.15, P0 + d_ * 0.8 + s_ * sgn * 0.15, 0.05, 0.05, M_NEON, C_DETAIL, n=6)
# hologram projector beside the lantern
HP = V(5.0, 3.6, 2.45)
cyl("Holo Projector", HP, HP + V(0, 0, 0.5), 0.45, 0.35, M_NAVY, C_DETAIL, n=12)
cyl("Holo Lens", HP + V(0, 0, 0.5), HP + V(0, 0, 0.58), 0.25, 0.25, M_NEON, C_DETAIL, n=12)
cyl("Holo Beam", HP + V(0, 0, 0.6), HP + V(0, 0, 2.2), 0.2, 0.7, M_HOLO, C_DETAIL, n=12)
crystal("Holo Gem", HP + V(0, 0, 2.3), V(0, 0, 1), 0.9, 0.35, M_CRYSTAL, C_DETAIL, sides=6)
crystal("Holo Gem Base", HP + V(0, 0, 2.3), V(0, 0, -1), 0.5, 0.35, M_CRYSTAL, C_DETAIL, sides=6)

# Lantern with flame (+X side, at the back)
LX, LY = 3.65, 2.3
cyl("Lantern Base", V(LX, LY, 2.05), V(LX, LY, 3.5), 0.74, 0.74, M_NAVY, C_DETAIL)
cyl("Lantern Glass", V(LX, LY, 3.5), V(LX, LY, 5.0), 0.6, 0.6, M_NEON, C_DETAIL)
tube("Lantern Cup", V(LX, LY, 5.45), V(0, 0, 1), V(0, 1, 0), 0.74, 0.5, 0.9, M_NAVY, C_DETAIL, n=24)
cyl("Lantern Cup Floor", V(LX, LY, 5.0), V(LX, LY, 5.55), 0.52, 0.52, M_BLACK, C_DETAIL)
flame_u, flame_v = V(0, 1, 0), V(1, 0, 0)
flame_rings = [ring_pts(V(LX, LY, 5.5 + z), flame_u, flame_v, r, 12)
               for z, r in ((0.0, 0.18), (0.15, 0.34), (0.4, 0.4), (0.7, 0.36), (1.0, 0.27), (1.35, 0.12))]
flame_rings.append([V(LX, LY, 7.2)] * 12)
finish("Lantern Flame", loft(flame_rings, cap1=False), M_FLAME, C_DETAIL, smooth=True, merge=0.001)

# Screen box (-X side)
SX = -TW
abox("Screen Box", SX - 0.2, SX + 0.05, -0.8, 3.5, 3.4, 5.9, M_BLACK, C_DETAIL)
abox("Screen Display", SX - 0.25, SX - 0.1, 1.25, 3.05, 3.8, 5.4, M_SCREEN, C_DETAIL)
abox("Screen Slot 1", SX - 0.25, SX - 0.12, 0.15, 0.8, 3.75, 5.25, M_NAVY, C_DETAIL)
abox("Screen Slot 2", SX - 0.25, SX - 0.12, -0.65, 0.0, 3.75, 5.25, M_NAVY, C_DETAIL)
sphere("Screen Button 1", V(SX - 0.25, 0.47, 3.98), 0.14, M_BLUEBALL, C_DETAIL)
sphere("Screen Button 2", V(SX - 0.25, -0.33, 5.0), 0.14, M_BLUEBALL, C_DETAIL)

# Valve knob (-X side, behind the screen box)
KC = V(-TW - 0.05, 3.85, 5.5)
cyl("Knob", KC, KC + V(-0.45, 0, 0), 0.28, 0.28, M_NAVY, C_DETAIL, n=12, hint=V(0, 1, 0))
for i, dz in enumerate((0.8, -0.8)):
    end = KC + V(-0.45, 0, 0) + V(-0.45, 0, dz * 0.6)
    cyl(f"Knob Handle {i + 1}", KC + V(-0.4, 0, 0), end, 0.05, 0.05, M_BLACK, C_DETAIL, n=6)
    sphere(f"Knob Ball {i + 1}", end, 0.15, M_BLUEBALL, C_DETAIL)

# Vent panel (+X side)
VX = TW
abox("Vent Frame", VX - 0.02, VX + 0.13, -2.0, 0.6, 3.6, 5.4, M_BLACK, C_DETAIL)
abox("Vent Slat Top", VX, VX + 0.16, -1.8, 0.4, 4.68, 5.2, M_STONE, C_DETAIL)
abox("Vent Slat Bottom", VX, VX + 0.16, -1.8, 0.4, 3.8, 4.32, M_STONE, C_DETAIL)
abox("Vent Bar", VX, VX + 0.17, -1.8, 0.4, 4.4, 4.6, M_BLACK, C_DETAIL)
abox("Vent Clip", VX, VX + 0.19, -0.85, -0.55, 4.1, 4.9, M_NAVY, C_DETAIL)

# Radio + antenna (-X side, on the back plate)
abox("Radio", -2.68, -2.4, -0.75, -0.2, 8.5, 9.6, M_BLACK, C_DETAIL)
abox("Radio LED", -2.72, -2.65, -0.55, -0.4, 8.7, 8.85, M_PINK, C_DETAIL)
cyl("Antenna", V(-2.54, -0.48, 9.6), V(-2.54, -0.48, 12.4), 0.045, 0.045, M_BLACK, C_DETAIL, n=6)
sphere("Antenna Tip", V(-2.54, -0.48, 12.45), 0.1, M_PINK, C_DETAIL)

if not WITH_BASE:
    for ob in MINE_OBJECTS:
        ob.data.transform(Matrix.Translation(V(0, 0, -BASE_H)))
    clip_to_ground()

# --------------------------------------------------------------------------
# Tidy: origins at each part's centre, parent everything to one empty
# --------------------------------------------------------------------------
root_empty = bpy.data.objects.new("CyberNeonMine", None)
root_empty.empty_display_type = 'PLAIN_AXES'
root_empty.empty_display_size = 3
root_coll.objects.link(root_empty)
for ob in MINE_OBJECTS:
    me = ob.data
    c = sum((v.co for v in me.vertices), Vector()) / max(len(me.vertices), 1)
    me.transform(Matrix.Translation(-c))
    ob.location = c
    ob.parent = root_empty

tris = sum(len(p.vertices) - 2 for ob in MINE_OBJECTS for p in ob.data.polygons)
print(f"[mine] parts={len(MINE_OBJECTS)} triangles={tris}")

# --------------------------------------------------------------------------
# Stage: ground, lights, cameras, glow (for preview renders only)
# --------------------------------------------------------------------------
scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
for vt in ("Standard", "AgX"):
    try:
        scene.view_settings.view_transform = vt
        break
    except Exception:
        pass

world = bpy.data.worlds.new("Night")
scene.world = world
try:
    world.use_nodes = True
except Exception:
    pass
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.008, 0.01, 0.025, 1)
    bg.inputs["Strength"].default_value = 1.0

ground_me = bpy.data.meshes.new("Ground")
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=120)
bm.to_mesh(ground_me)
bm.free()
ground = bpy.data.objects.new("Ground", ground_me)
ground.location.z = -0.01
stage_coll.objects.link(ground)
M_GROUND = new_mat("Ground", lin((95, 92, 100)), rough=0.95)
add_noise(M_GROUND, lin((78, 76, 84)), lin((118, 115, 124)), scale=1.4, bump=0.08)
ground_me.materials.append(M_GROUND)


def add_light(name, kind, loc, energy, color, size=0.5, rot=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    if kind == 'SUN':
        ld.angle = math.radians(10)
    else:
        ld.shadow_soft_size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    if rot:
        ob.rotation_euler = rot
    stage_coll.objects.link(ob)
    return ob


LZ = 0 if WITH_BASE else BASE_H
add_light("Moon", 'SUN', V(0, 0, 30), 1.2, (0.6, 0.85, 1.0), rot=Euler((math.radians(50), 0, math.radians(30))))
add_light("Mine Glow", 'POINT', V(0, -4.0, 20), 7000, (0.9, 0.3, 1.0), size=3)
add_light("Front Fill", 'POINT', V(0, -16, 9), 4000, (0.6, 0.85, 1.0), size=4)
add_light("Back Fill", 'POINT', V(0, 15, 10), 3000, (0.6, 0.85, 1.0), size=4)
add_light("Side Fill L", 'POINT', V(14, -2, 8), 2200, (0.6, 0.85, 1.0), size=4)
add_light("Side Fill R", 'POINT', V(-14, -2, 8), 2200, (0.6, 0.85, 1.0), size=4)
add_light("Flame Light", 'POINT', V(LX, LY, 7.0 - LZ), 120, (1.0, 0.3, 0.9), size=0.3)

# Bloom so the neon parts glow like Roblox Neon
try:
    scene.render.use_compositing = True
    ng = bpy.data.node_groups.new("Glow", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    rl = ng.nodes.new("CompositorNodeRLayers")
    gl = ng.nodes.new("CompositorNodeGlare")
    out = ng.nodes.new("NodeGroupOutput")
    for k, v in (("Type", "Bloom"), ("Threshold", 1.5), ("Strength", 0.3), ("Size", 0.45)):
        try:
            gl.inputs[k].default_value = v
        except Exception as e:
            print("[mine] glare", k, e)
    ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
    ng.links.new(gl.outputs["Image"], out.inputs[0])
    scene.compositing_node_group = ng
except Exception as e:
    print("[mine] glow setup skipped:", e)

# Cameras roughly matching the reference screenshots
CAMS = {
    #        location            look-at            lens  resolution
    "front": (V(0, -38, 11.5), V(0, 0, 8.2), 56, (1028, 854)),
    "left": (V(-35, -2.0, 16.0), V(0, -2.0, 7.8), 52, (898, 726)),
    "right": (V(35, -1.0, 19.0), V(0, -1.0, 7.8), 50, (1012, 766)),
    "back": (V(-1.6, 35, 22.0), V(-1.6, 0, 8.4), 47, (1042, 742)),
    "top": (V(0, -18.1, 52.0), V(0, -1.0, 5.0), 64, (726, 666)),
    "hero": (V(21, -22, 12), V(0, -2.0, 9.5), 35, (1200, 1000)),
}
if not WITH_BASE:
    CAMS = {k: (l - V(0, 0, BASE_H), t - V(0, 0, BASE_H), ln, r) for k, (l, t, ln, r) in CAMS.items()}
cam_objs = {}
for name, (loc, tgt, lens, res) in CAMS.items():
    cd = bpy.data.cameras.new(f"Cam {name}")
    cd.lens = lens
    co = bpy.data.objects.new(f"Cam {name}", cd)
    co.location = loc
    co.rotation_euler = (tgt - loc).to_track_quat('-Z', 'Y').to_euler()
    stage_coll.objects.link(co)
    cam_objs[name] = (co, res)
scene.camera = cam_objs["hero"][0]

# --------------------------------------------------------------------------
# Save, export, render
# --------------------------------------------------------------------------
os.makedirs(OUT, exist_ok=True)

# Roblox export: one mesh per material so each becomes a single MeshPart
exp_coll = bpy.data.collections.new("_export")
scene.collection.children.link(exp_coll)
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
        exp_coll.objects.link(dd)
        dups.append(dd)
    with bpy.context.temp_override(active_object=dups[0], selected_editable_objects=dups, selected_objects=dups):
        bpy.ops.object.join()
    j = dups[0]
    j.name = mname.split(" (")[0].replace(" ", "")
    joined.append(j)
for o in bpy.context.view_layer.objects:
    o.select_set(False)
for j in joined:
    j.select_set(True)
    t = sum(len(p.vertices) - 2 for p in j.data.polygons)
    print(f"[mine] export part {j.name}: {t} tris")
fbx_path = os.path.join(OUT, "CyberNeonMine_Roblox.fbx")
bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=True, object_types={'MESH'},
                         use_triangles=True, mesh_smooth_type='FACE', apply_unit_scale=True)
print("[mine] exported", fbx_path)
for j in joined:
    bpy.data.objects.remove(j, do_unlink=True)
bpy.data.collections.remove(exp_coll)

blend_path = os.path.join(OUT, "CyberNeonMine.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("[mine] saved", blend_path)

# Roblox setup script: colours, materials, glow lights and a working dropper
LUA_TEMPLATE = r"""-- {NAME}: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import {NAME}_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
{LOOK}
}
local LIGHTS = {
{LIGHTS}
}
local ORE_PART = "{ORE}"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("{NAME}_Roblox", true) or workspace:FindFirstChild("{NAME}", true) end
assert(model, "Select the imported {NAME} model first.")
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
print(("[{NAME}] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
"""


def write_roblox_setup(path, name, ore_key="Ore"):
    used = {ob.data.materials[0].name.split(" (")[0].replace(" ", "") for ob in MINE_OBJECTS}
    items = sorted((k, v) for k, v in RBX.items() if k in used)
    look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
    lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
    lua = LUA_TEMPLATE.replace("{NAME}", name).replace("{LOOK}", look).replace("{LIGHTS}", lights).replace("{ORE}", ore_key)
    with open(path, "w") as f:
        f.write(lua)
    print("[mine] wrote", path)


write_roblox_setup(os.path.join(OUT, "CyberNeonMine_RobloxSetup.lua"), "CyberNeonMine")

if RENDER:
    rdir = os.path.join(OUT, "renders")
    os.makedirs(rdir, exist_ok=True)
    for name in VIEWS.split(","):
        co, res = cam_objs[name]
        scene.camera = co
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.resolution_percentage = 100
        scene.render.filepath = os.path.join(rdir, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("[mine] rendered", name)
