"""Generate five more Dragonglass-style mines from the Crimson Drake script (same body, head cannon, wing,
lantern, screen box, battery and crystals) - each with its own colours and a few of its own details.
Mines sit on the ground (no plinth); add --base when running a variant to get the plinth back.

    python3 make_drake_variants.py        -> writes ../<folder>/<name>_mine.py for each variant
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = open(os.path.join(HERE, "..", "crimson", "crimson_drake_mine.py")).read()


def cut(src, start, end, new):
    i = src.index(start)
    j = src.index(end, i)
    return src[:i] + new + src[j:]


MAT_HELPER = '''RBX = {}   # export name -> (Roblox material, rgb 0-255, transparency, light (r, g, b, range, brightness) or None)


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


'''

CLIP = '''

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


'''

LUA_TEMPLATE = open(os.path.join(HERE, "_lua_template.lua")).read()
assert "'''" not in LUA_TEMPLATE
LUA = r'''
# Roblox setup script: colours, materials, glow lights and a working dropper
LUA_TEMPLATE = r"""@@TEMPLATE@@"""


def write_roblox_setup(path, name, ore_key="Ore"):
    used = {ob.data.materials[0].name.split(" (")[0].replace(" ", "") for ob in MINE_OBJECTS}
    items = sorted((k, v) for k, v in RBX.items() if k in used)
    look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
    lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
    lua = LUA_TEMPLATE.replace("{NAME}", name).replace("{LOOK}", look).replace("{LIGHTS}", lights).replace("{ORE}", ore_key)
    with open(path, "w") as f:
        f.write(lua)
    print("[mine] wrote", path)


write_roblox_setup(os.path.join(OUT, "{MINE}_RobloxSetup.lua"), "{MINE}")

'''.replace("@@TEMPLATE@@", LUA_TEMPLATE)

VARIANTS = []

# =====================================================================================================
VARIANTS.append(dict(
    folder="sapphire", file="sapphire_tide_mine.py", mine="SapphireTideMine",
    doc="""Sapphire Tide Mine - ocean variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine with a deep-sea sapphire colour scheme and its own details:
a five-fin frill crown with catfish barbels, axolotl ear-fins, five-finger fin wings, a water-orb heart with
a pearl inside, a finned tail with a fluke, and a coral cluster by the lantern. Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (44, 112, 168), "Slate", rough=0.9, noise=((30, 84, 136), (74, 152, 204), 1.6, 0.25))
M_BLACK = MAT("Black", (8, 16, 24), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Deep Steel (DiamondPlate)", (18, 40, 70), "DiamondPlate", rough=0.35, metal=0.6, plate=9.0)
M_RIM = MAT("Aqua Trim (DiamondPlate)", (40, 220, 230), "Metal", rough=0.35, metal=0.5, glow=(40, 220, 230), strength=0.5, plate=14.0)
M_MARBLE = MAT("Abyss Marble", (10, 24, 40), "Marble", rough=0.25, marble=((8, 20, 34), (60, 200, 230)))
M_NEON = MAT("Neon (Glow)", (200, 250, 255), "Neon", rough=0.3, glow=(120, 230, 255), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Aquaglass)", (90, 220, 255), "Glass", rough=0.15, glow=(30, 180, 240), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (22, 34, 46), "Slate", rough=0.95, noise=((14, 24, 34), (44, 64, 82), 3.0, 0.5))
M_WING = MAT("Fin Membrane", (40, 150, 170), "Fabric", rough=0.75, noise=((26, 116, 140), (70, 190, 200), 2.2, 0.2))
M_BONE = MAT("Fin Bone", (16, 60, 90), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Flame", (150, 240, 255), "Neon", rough=0.5, glow=(80, 220, 255), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (170, 240, 255), "Neon", rough=0.3, glow=(100, 220, 255), strength=8.0)
M_PINK = MAT("Aqua LED", (80, 255, 220), "Neon", rough=0.3, glow=(40, 255, 210), strength=5.0)
M_BLUEBALL = MAT("Pearl Knob", (230, 240, 255), "Neon", rough=0.3, glow=(200, 230, 255), strength=1.5)
M_ORE = MAT("Ore", (170, 240, 255), "Neon", rough=0.2, glow=(100, 220, 255), strength=1.2)
M_HORN = MAT("Fin Spine", (12, 44, 70), "SmoothPlastic", rough=0.5)
M_WATER = MAT("Water Orb (Glass)", (60, 170, 230), "Glass", rough=0.05, glow=(30, 140, 220), strength=1.5, alpha=0.25, light=(14, 1.6))
M_PEARL = MAT("Pearl", (240, 240, 250), "SmoothPlastic", rough=0.2, metal=0.3)
M_CORAL = MAT("Coral", (255, 112, 104), "SmoothPlastic", rough=0.6, noise=((220, 80, 80), (255, 150, 130), 6.0, 0.3))
''',
    cogs=(8, 0.5, 0.34),
    crown='''# Frill crown: five swept fins over the top of the mouth, three barbels hanging below
F = V(0, -1, 0)
for i, th in enumerate((30, 60, 90, 120, 150)):
    r_ = radial(th)
    L = 3.7 if th == 90 else 3.1 if th in (60, 120) else 2.4
    d_ = (r_ * 0.85 - A * 0.55 + U * 0.15).normalized()
    b0, b1 = O + r_ * 2.95 - A * 0.55, O + r_ * 2.95 + A * 0.6
    blade(f"Frill Fin {i + 1}", [b1, b0, b0 + d_ * L, b1 + d_ * L * 0.45], 0.2, M_WING, C_HEAD)
    cyl(f"Frill Ray {i + 1}", (b0 + b1) / 2, b0 + d_ * L * 0.95, 0.12, 0.03, M_HORN, C_HEAD, n=6)
for i, th in enumerate((235, 270, 305)):
    r_ = radial(th)
    p0 = O + r_ * 2.9 + A * 0.3
    pts = [p0, p0 + A * 0.9 - U * 0.6 + r_ * 0.3, p0 + A * 1.3 - U * 1.6 + r_ * 0.5, p0 + A * 1.2 - U * 2.4 + r_ * 0.4]
    for k in range(3):
        cyl(f"Barbel {i + 1}-{k + 1}", pts[k], pts[k + 1], 0.16 * (1 - k / 3), 0.16 * (1 - (k + 1) / 3) + 0.02, M_BONE, C_HEAD, n=6)
    sphere(f"Barbel Tip {i + 1}", pts[-1], 0.13, M_PINK, C_HEAD)

''',
    horns='''# Axolotl-style ear fins either side of the head
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 0.9 + X_AXIS * side * 2.7 - A_ * 2.0
    for k, (up, back, L) in enumerate(((1.0, 0.3, 2.6), (0.45, 0.6, 2.9), (-0.1, 0.8, 2.4))):
        d_ = (X_AXIS * side * 0.8 + U_ * up - A_ * back).normalized()
        b0, b1 = c + U_ * (0.35 - 0.35 * k) - A_ * 0.2, c + U_ * (0.0 - 0.35 * k) + A_ * 0.35
        blade(f"Ear Fin {label} {k + 1}", [b0, b0 + d_ * L, b1 + d_ * L * 0.55, b1], 0.16, M_WING, C_HEAD)
        cyl(f"Ear Fin Spine {label} {k + 1}", (b0 + b1) / 2, b0 + d_ * L * 0.98, 0.11, 0.03, M_HORN, C_HEAD, n=6)

''',
    wings=('WRIST = (2.9, 16.9)\nTIPS = [(9.6, 13.0), (8.6, 10.6), (7.0, 8.8), (5.0, 8.0), (3.0, 8.6)]',
           'LEAD = [ROOT_TOP, (1.3, 16.1), WRIST, (4.8, 16.4), (6.6, 15.3), (8.2, 14.3), TIPS[0]]', 0.18),
    heart='''sphere("Water Orb", V(0, BY, 10.45), 1.02, M_WATER, C_DETAIL)
sphere("Orb Pearl", V(0, BY, 10.3), 0.38, M_PEARL, C_DETAIL)
for i, (dx, dy, dz, r) in enumerate(((0.35, -0.3, 0.55, 0.12), (-0.4, 0.2, 0.2, 0.1), (0.15, 0.45, 0.85, 0.08), (-0.2, -0.4, -0.4, 0.09))):
    sphere(f"Orb Bubble {i + 1}", V(dx, BY + dy, 10.45 + dz), r, M_NEON, C_DETAIL)
for i, z in enumerate((9.45, 11.45)):
    torus(f"Orb Band {i + 1}", V(0, BY, z), V(0, 0, 1), V(0, 1, 0), 0.92, 0.1, M_NAVY, C_DETAIL, n_major=24, n_minor=6)
''',
    tail='''# Finned tail curling round from the back, ending in a fluke
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.8 * (1 - i / 7), 0.8 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    if i < 5:
        a, b = tail[i] + V(0, 0, r0 * 0.6), tail[i + 1] + V(0, 0, r1 * 0.6)
        blade(f"Tail Fin {i + 1}", [a, b, b + V(0, 0, 0.4), (a + b) / 2 + V(0, 0, 1.1 - 0.12 * i)], 0.1, M_WING, C_DETAIL)
d_ = (tail[-1] - tail[-2]).normalized()
s_ = V(-d_.y, d_.x, 0)
for k, sgn in enumerate((1, -1)):
    blade(f"Tail Fluke {k + 1}", [tail[-1], tail[-1] + d_ * 1.6 + s_ * sgn * 1.3 + V(0, 0, 0.4), tail[-1] + d_ * 0.9 + s_ * sgn * 0.3], 0.12, M_WING, C_DETAIL)
# coral cluster beside the lantern
CB = V(5.1, 3.6, 2.45)
for k, (dx, dy, h, lean) in enumerate(((0, 0, 2.2, 0.0), (0.5, 0.3, 1.6, 0.5), (-0.4, 0.4, 1.4, -0.5), (0.2, -0.45, 1.2, 0.3))):
    b = CB + V(dx, dy, 0)
    t = b + V(lean, 0.1, h)
    cyl(f"Coral Stem {k + 1}", b, t, 0.2, 0.12, M_CORAL, C_DETAIL, n=8)
    for j, sgn in enumerate((1, -1)):
        m = b + (t - b) * (0.55 + 0.15 * j)
        cyl(f"Coral Branch {k + 1}-{j + 1}", m, m + V(sgn * 0.5, 0.15, 0.6), 0.1, 0.06, M_CORAL, C_DETAIL, n=6)
    sphere(f"Coral Tip {k + 1}", t, 0.15, M_CORAL, C_DETAIL)
for k, (dx, dy) in enumerate(((-0.9, -0.2), (0.9, 0.9))):
    sphere(f"Shell {k + 1}", CB + V(dx, dy, 0.15), 0.3, M_PEARL, C_DETAIL)
''',
    bg=(0.008, 0.025, 0.045), tint=(0.55, 0.85, 1.0), glow=(0.35, 0.75, 1.0), flame=(0.45, 0.9, 1.0),
))

# =====================================================================================================
VARIANTS.append(dict(
    folder="solar", file="solar_gold_mine.py", mine="SolarGoldMine",
    doc="""Solar Gold Mine - sun variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in sandstone and gold with its own details:
a twelve-ray sun crown, twelve slim mouth cogs, swept antelope horns with gold rings, feather-edged wings,
a blazing sun-core heart with rays, and a gold-banded tail ending in a sun flare. Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (206, 164, 84), "Sandstone", rough=0.9, noise=((168, 128, 58), (234, 198, 122), 1.6, 0.25))
M_BLACK = MAT("Black", (26, 20, 12), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Bronze Plate (DiamondPlate)", (112, 72, 30), "DiamondPlate", rough=0.35, metal=0.6, plate=9.0)
M_RIM = MAT("Sun Trim (DiamondPlate)", (255, 200, 60), "Metal", rough=0.35, metal=0.5, glow=(255, 200, 60), strength=0.5, plate=14.0)
M_MARBLE = MAT("White Marble", (230, 224, 210), "Marble", rough=0.25, marble=((222, 216, 202), (220, 170, 60)))
M_NEON = MAT("Neon (Glow)", (255, 240, 200), "Neon", rough=0.3, glow=(255, 220, 140), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Sunglass)", (255, 190, 60), "Glass", rough=0.15, glow=(255, 160, 20), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (72, 56, 38), "Slate", rough=0.95, noise=((52, 40, 26), (100, 80, 56), 3.0, 0.5))
M_WING = MAT("Wing Membrane", (236, 204, 130), "Fabric", rough=0.75, noise=((214, 178, 100), (250, 226, 160), 2.2, 0.2))
M_BONE = MAT("Wing Bone", (250, 240, 220), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Flame", (255, 250, 220), "Neon", rough=0.5, glow=(255, 230, 150), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (255, 230, 170), "Neon", rough=0.3, glow=(255, 210, 120), strength=8.0)
M_PINK = MAT("Sun LED", (255, 140, 40), "Neon", rough=0.3, glow=(255, 120, 20), strength=5.0)
M_BLUEBALL = MAT("Gold Knob", (255, 190, 40), "Neon", rough=0.3, glow=(255, 170, 20), strength=1.5)
M_ORE = MAT("Ore", (255, 220, 120), "Neon", rough=0.2, glow=(255, 190, 60), strength=1.2)
M_HORN = MAT("Gold Horn (Metal)", (240, 190, 70), "Metal", rough=0.25, metal=1.0)
M_SUN = MAT("Sun Core", (255, 220, 120), "Neon", rough=0.3, glow=(255, 180, 60), strength=9.0, light=(16, 2))
''',
    cogs=(12, 0.32, 0.18),
    crown='''# Sun crown: twelve rays all round the mouth, long stone rays between short gold ones
F = V(0, -1, 0)
for i in range(12):
    th = 90 + 30 * i
    r_ = radial(th)
    L = 3.4 if i % 2 == 0 else 2.1
    if math.sin(math.radians(th)) < -0.5:
        L *= 0.7
    d_ = (r_ * 0.85 + F * 0.35 + A * 0.1).normalized()
    b0, b1 = O + r_ * 2.95 - A * 0.35, O + r_ * 2.95 + A * 0.55
    blade(f"Sun Ray {i + 1}", [b0, (b0 + b1) / 2 + d_ * L, b1], 0.22, M_STONE if i % 2 == 0 else M_HORN, C_HEAD)

''',
    horns='''# Swept-back antelope horns with gold rings
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 2.3 + X_AXIS * side * 1.5 - A_ * 1.4
    pts = [c]
    for k in range(1, 8):
        t = k / 7
        pts.append(c + (-A_ * 1.0 + U_ * (0.75 - 0.35 * t) + X_AXIS * side * 0.22) * 4.6 * t)
    for k in range(7):
        cyl(f"Horn {label} {k + 1}", pts[k], pts[k + 1], 0.42 * (1 - 0.8 * k / 7), 0.42 * (1 - 0.8 * (k + 1) / 7) + 0.02, M_STONE, C_HEAD, n=8)
        if k < 5:
            d_ = (pts[k + 1] - pts[k]).normalized()
            torus(f"Horn Ring {label} {k + 1}", pts[k + 1], d_, perp_basis(d_)[0], 0.42 * (1 - 0.8 * (k + 1) / 7) + 0.05, 0.05, M_HORN, C_HEAD, n_major=12, n_minor=4)

''',
    wings=('WRIST = (2.9, 17.0)\nTIPS = [(9.4, 12.4), (8.0, 10.0), (6.2, 8.6), (4.2, 8.2)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.4), (6.8, 15.2), (8.3, 13.9), TIPS[0]]', 0.12),
    heart='''sphere("Sun Core", V(0, BY, 10.45), 0.95, M_SUN, C_DETAIL)
for i, ang in enumerate((-40, -20, 0, 20, 40, 140, 160, 180, 200, 220)):
    a_ = math.radians(ang)
    d_ = V(math.cos(a_), 0, math.sin(a_))
    cyl(f"Sun Spike {i + 1}", V(0, BY + 0.25, 10.45) + d_ * 0.95, V(0, BY + 0.25, 10.45) + d_ * 1.75, 0.16, 0.0, M_HORN, C_DETAIL, n=6)
torus("Sun Ring", V(0, BY, 10.45), V(0, 1, 0), V(0, 0, 1), 1.12, 0.07, M_HORN, C_DETAIL, n_major=28, n_minor=5)
''',
    tail='''# Gold-banded tail curling round from the back, ending in a sun flare
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.9 * (1 - i / 7), 0.9 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    d_ = (tail[i + 1] - tail[i]).normalized()
    torus(f"Tail Band {i + 1}", tail[i + 1], d_, V(0, 0, 1), max(r1, 0.12) + 0.04, 0.07, M_HORN, C_DETAIL, n_major=12, n_minor=4)
d_ = (tail[-1] - tail[-2]).normalized()
s_ = V(-d_.y, d_.x, 0)
for k, ang in enumerate((-0.9, -0.45, 0.0, 0.45, 0.9)):
    dd = (d_ * math.cos(ang) + s_ * math.sin(ang)).normalized()
    blade(f"Tail Flare {k + 1}", [tail[-1] + s_ * 0.18, tail[-1] + dd * (1.4 if k % 2 == 0 else 1.0) + V(0, 0, 0.15), tail[-1] - s_ * 0.18], 0.1,
          M_HORN if k % 2 == 0 else M_STONE, C_DETAIL)
''',
    bg=(0.035, 0.026, 0.012), tint=(1.0, 0.88, 0.62), glow=(1.0, 0.8, 0.45), flame=(1.0, 0.9, 0.6),
))

# =====================================================================================================
VARIANTS.append(dict(
    folder="shadow", file="shadow_amethyst_mine.py", mine="ShadowAmethystMine",
    doc="""Shadow Amethyst Mine - shadow variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in black-violet with its own details:
a jagged nine-spike crown, six heavy mouth cogs, four bone horns, tattered wings on white bone fingers,
a void-eye heart in a chain cage, and iron chains staked to rune posts. Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (54, 38, 78), "Slate", rough=0.9, noise=((36, 24, 54), (80, 58, 108), 1.6, 0.25))
M_BLACK = MAT("Black", (8, 6, 12), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Shadow Iron (DiamondPlate)", (28, 20, 40), "DiamondPlate", rough=0.35, metal=0.6, plate=9.0)
M_RIM = MAT("Violet Trim (DiamondPlate)", (170, 80, 255), "Metal", rough=0.35, metal=0.5, glow=(170, 80, 255), strength=0.5, plate=14.0)
M_MARBLE = MAT("Void Marble", (12, 8, 20), "Marble", rough=0.25, marble=((10, 6, 16), (180, 100, 255)))
M_NEON = MAT("Neon (Glow)", (230, 200, 255), "Neon", rough=0.3, glow=(190, 130, 255), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Amethyst)", (190, 110, 255), "Glass", rough=0.15, glow=(150, 60, 255), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (26, 20, 34), "Slate", rough=0.95, noise=((16, 12, 22), (46, 36, 58), 3.0, 0.5))
M_WING = MAT("Wing Membrane", (72, 40, 112), "Fabric", rough=0.75, noise=((50, 26, 84), (100, 62, 146), 2.2, 0.2))
M_BONE = MAT("Wing Bone", (222, 214, 198), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Flame", (220, 140, 255), "Neon", rough=0.5, glow=(190, 80, 255), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (220, 170, 255), "Neon", rough=0.3, glow=(180, 110, 255), strength=8.0)
M_PINK = MAT("Violet LED", (255, 90, 255), "Neon", rough=0.3, glow=(255, 60, 255), strength=5.0)
M_BLUEBALL = MAT("Void Knob", (130, 70, 255), "Neon", rough=0.3, glow=(110, 50, 255), strength=1.5)
M_ORE = MAT("Ore", (220, 180, 255), "Neon", rough=0.2, glow=(170, 110, 255), strength=1.2)
M_HORN = MAT("Bone Horn", (222, 214, 198), "SmoothPlastic", rough=0.5)
M_VOID = MAT("Void Eye", (14, 8, 22), "SmoothPlastic", rough=0.1, metal=0.4)
M_IRIS = MAT("Iris Glow", (210, 110, 255), "Neon", rough=0.3, glow=(180, 70, 255), strength=8.0, light=(14, 1.6))
M_CHAIN = MAT("Chain (Metal)", (64, 60, 74), "Metal", rough=0.35, metal=0.9)
''',
    cogs=(6, 0.62, 0.42),
    crown='''# Jagged crown: nine uneven spikes, the longest straight up
F = V(0, -1, 0)
rnd_c = random.Random(13)
for i, th in enumerate([90 + 360 * k / 9 for k in range(9)]):
    th = th % 360
    if 240 < th < 300:
        continue
    r_ = radial(th)
    L = 4.4 if abs(th - 90) < 1 else rnd_c.uniform(2.2, 3.6) * (0.75 if math.sin(math.radians(th)) < 0 else 1.0)
    d_ = (A * 0.3 + F * 0.5 + r_ * 0.75).normalized()
    b0, b1 = O + r_ * 2.95 - A * 0.45, O + r_ * 2.95 + A * 0.95
    mid = (b0 + b1) / 2 + d_ * L * 0.55 + tangent(th) * 0.35
    blade(f"Jagged Spike {i + 1}", [b0, mid, (b0 + b1) / 2 + d_ * L, b1], 0.28, M_STONE, C_HEAD)

''',
    horns='''# Four bone horns: a tall pair on top and a lower pair sweeping out
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    for j, (c, d_, L, r) in enumerate(((O_ + U_ * 2.5 + X_AXIS * side * 1.1 - A_ * 1.0, -A_ * 0.75 + U_ * 0.65 + X_AXIS * side * 0.25, 4.2, 0.5),
                                       (O_ + U_ * 1.0 + X_AXIS * side * 2.5 - A_ * 1.4, -A_ * 0.8 + U_ * 0.15 + X_AXIS * side * 0.55, 3.2, 0.42))):
        d_ = d_.normalized()
        pts = [c + d_ * L * k / 5 + U_ * 0.35 * math.sin(math.pi * k / 5) for k in range(6)]
        for k in range(5):
            cyl(f"Bone Horn {label}{j + 1} {k + 1}", pts[k], pts[k + 1], r * (1 - 0.85 * k / 5), r * (1 - 0.85 * (k + 1) / 5) + 0.02, M_HORN, C_HEAD, n=8)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.8, 14.0), (8.4, 10.0), (6.0, 8.2), (3.6, 8.4)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.9), (7.0, 16.2), (8.6, 15.3), TIPS[0]]', 0.62),
    heart='''sphere("Void Eye", V(0, BY, 10.45), 1.0, M_VOID, C_DETAIL)
torus("Void Iris", V(0, BY + 0.86, 10.45), V(0, 1, 0), V(0, 0, 1), 0.48, 0.12, M_IRIS, C_DETAIL, n_major=24, n_minor=6)
obox("Void Pupil", V(0, BY + 0.98, 10.45), (0.14, 0.06, 0.75), X_AXIS, V(0, 1, 0), V(0, 0, 1), M_IRIS, C_DETAIL)
for i in range(6):
    a_ = 2 * math.pi * i / 6 + 0.5
    for k in range(4):
        z = 9.35 + k * 0.62
        torus(f"Cage Chain {i + 1}-{k + 1}", V(1.06 * math.cos(a_), BY + 1.06 * math.sin(a_), z), V(0, 0, 1) if k % 2 else V(math.cos(a_), math.sin(a_), 0),
              V(-math.sin(a_), math.cos(a_), 0) if k % 2 else V(0, 0, 1), 0.2, 0.06, M_CHAIN, C_DETAIL, n_major=8, n_minor=4)
''',
    tail='''# Bone-spiked tail curling round from the back
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.9 * (1 - i / 7), 0.9 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    mid = (tail[i] + tail[i + 1]) / 2
    cyl(f"Tail Spike {i + 1}", mid + V(0, 0, r0 * 0.6), mid + V(0, 0, r0 * 0.6 + 1.1), 0.22, 0.0, M_HORN, C_DETAIL, n=6)
cyl("Tail Blade", tail[-1], tail[-1] + V(-0.6, -1.5, 0.1), 0.35, 0.0, M_HORN, C_DETAIL, n=6)
# chains from the back plate staked to rune posts in the ground
for side in (1, -1):
    post = V(side * 4.6, 4.4, 2.45)
    abox(f"Rune Post {side}", post.x - 0.35, post.x + 0.35, post.y - 0.35, post.y + 0.35, post.z - 0.5, post.z + 1.6, M_ROCK, C_DETAIL)
    abox(f"Post Rune {side}", post.x - 0.37, post.x + 0.37, post.y - 0.08, post.y + 0.08, post.z + 0.4, post.z + 1.2, M_IRIS, C_DETAIL)
    a = V(side * 2.45, 1.0, 12.4)
    b = post + V(0, 0, 1.6)
    n_ = 13
    for k in range(n_ + 1):
        t = k / n_
        p = a + (b - a) * t - V(0, 0, 1.6 * math.sin(math.pi * t))
        q = a + (b - a) * min(1, t + 0.05) - V(0, 0, 1.6 * math.sin(math.pi * min(1, t + 0.05)))
        d_ = (q - p).normalized()
        u_ = perp_basis(d_)[0]
        torus(f"Chain {side} {k + 1}", p, u_ if k % 2 else d_.cross(u_), d_, 0.2, 0.055, M_CHAIN, C_DETAIL, n_major=8, n_minor=4)
''',
    bg=(0.02, 0.012, 0.035), tint=(0.78, 0.6, 1.0), glow=(0.7, 0.4, 1.0), flame=(0.8, 0.45, 1.0),
))

# =====================================================================================================
VARIANTS.append(dict(
    folder="venom", file="venom_drake_mine.py", mine="VenomDrakeMine",
    doc="""Venom Drake Mine - toxic variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in swamp green and toxic lime with its own details:
a double row of crown spikes, eight fanged mouth cogs, hooked viper horns, mottled wings,
a glass venom canister heart with hazard bands, venom drips, a stinger tail and a leaking toxic barrel.
Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (72, 98, 46), "Slate", rough=0.9, noise=((50, 72, 30), (100, 130, 64), 1.6, 0.25))
M_BLACK = MAT("Black", (10, 14, 8), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Rusted Iron (DiamondPlate)", (56, 48, 30), "DiamondPlate", rough=0.35, metal=0.6, plate=9.0)
M_RIM = MAT("Toxic Trim (DiamondPlate)", (160, 255, 40), "Metal", rough=0.35, metal=0.5, glow=(160, 255, 40), strength=0.5, plate=14.0)
M_MARBLE = MAT("Sludge Marble", (14, 20, 10), "Marble", rough=0.25, marble=((12, 16, 8), (140, 255, 60)))
M_NEON = MAT("Neon (Glow)", (220, 255, 190), "Neon", rough=0.3, glow=(170, 255, 100), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Toxiglass)", (150, 255, 60), "Glass", rough=0.15, glow=(100, 230, 20), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (30, 36, 24), "Slate", rough=0.95, noise=((20, 26, 16), (52, 60, 40), 3.0, 0.5))
M_WING = MAT("Wing Membrane", (122, 150, 42), "Fabric", rough=0.75, noise=((86, 116, 22), (170, 196, 80), 3.4, 0.25))
M_BONE = MAT("Wing Bone", (40, 52, 20), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Flame", (180, 255, 80), "Neon", rough=0.5, glow=(120, 255, 30), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (200, 255, 150), "Neon", rough=0.3, glow=(150, 255, 90), strength=8.0)
M_PINK = MAT("Hazard LED", (255, 210, 30), "Neon", rough=0.3, glow=(255, 190, 10), strength=5.0)
M_BLUEBALL = MAT("Toxic Knob", (150, 255, 40), "Neon", rough=0.3, glow=(120, 255, 20), strength=1.5)
M_ORE = MAT("Ore", (190, 255, 120), "Neon", rough=0.2, glow=(130, 255, 60), strength=1.2)
M_HORN = MAT("Horn", (30, 30, 24), "SmoothPlastic", rough=0.5)
M_SLIME = MAT("Venom (Glow)", (140, 255, 50), "Neon", rough=0.3, glow=(100, 255, 20), strength=6.0, light=(12, 1.4))
M_HAZ = MAT("Hazard Yellow", (240, 200, 20), "SmoothPlastic", rough=0.45)
M_GLASS = MAT("Canister Glass", (200, 255, 200), "Glass", rough=0.05, alpha=0.45)
''',
    cogs=(8, 0.46, 0.08),
    crown='''# Double crown: seven main spikes with a back row of short ones between them
F = V(0, -1, 0)
for i, th in enumerate([90 + 360 * k / 7 for k in range(7)]):
    th = th % 360
    r_ = radial(th)
    L = 3.6 if abs(th - 90) < 1 else 2.9 if math.sin(math.radians(th)) > 0 else 2.3
    d_ = (A * 0.4 + F * 0.6 + r_ * 0.6).normalized()
    b0, b1 = O + r_ * 2.95 - A * 0.4, O + r_ * 2.95 + A * 1.0
    blade(f"Spike {i + 1}", [b0, (b0 + b1) / 2 + d_ * L, b1], 0.3, M_STONE, C_HEAD)
    th2 = th + 360 / 14
    r2 = radial(th2)
    d2 = (A * 0.1 + F * 0.3 + r2 * 0.9).normalized()
    c0, c1 = O + r2 * 2.9 - A * 0.75, O + r2 * 2.9 - A * 0.05
    blade(f"Back Spike {i + 1}", [c0, (c0 + c1) / 2 + d2 * 1.6, c1], 0.22, M_HORN, C_HEAD)
# venom dripping from the lower lip
for k in range(4):
    sphere(f"Venom Drip {k + 1}", O + A * 0.55 - U * (3.05 + 0.4 * k) + X_AXIS * (0.5 if k % 2 else -0.4), 0.16 - 0.025 * k, M_SLIME, C_HEAD)

''',
    horns='''# Hooked viper horns curving back and down
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 2.0 + X_AXIS * side * 2.0 - A_ * 1.3
    pts = []
    for k in range(11):
        t = k / 10
        ang = math.radians(10 + 150 * t)
        rad = 2.3 * (1 - 0.35 * t)
        pts.append(c + X_AXIS * side * (0.7 * t) + (math.cos(ang) * U_ + math.sin(ang) * (-A_)) * rad - U_ * 2.3 * (1 - 0.0))
    pts = [p + U_ * 2.3 for p in pts]
    for k in range(10):
        cyl(f"Viper Horn {label} {k + 1}", pts[k], pts[k + 1], 0.5 * (1 - 0.85 * k / 10), 0.5 * (1 - 0.85 * (k + 1) / 10), M_HORN, C_HEAD, n=8)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.8, 13.2), (8.2, 9.6), (5.8, 8.2), (3.4, 8.6)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.6), (6.9, 15.7), (8.6, 14.6), TIPS[0]]', 0.4),
    heart='''cyl("Venom Canister", V(0, BY, 9.15), V(0, BY, 11.7), 1.0, 1.0, M_GLASS, C_DETAIL)
cyl("Venom Fluid", V(0, BY, 9.2), V(0, BY, 11.1), 0.78, 0.78, M_SLIME, C_DETAIL)
for i, (dx, dy, dz) in enumerate(((0.3, -0.2, 11.3), (-0.25, 0.3, 11.45), (0.05, 0.1, 11.55))):
    sphere(f"Venom Bubble {i + 1}", V(dx, BY + dy, dz), 0.09, M_SLIME, C_DETAIL)
for i, z in enumerate((9.35, 11.5)):
    tube(f"Hazard Band {i + 1}", V(0, BY, z), V(0, 0, 1), V(0, 1, 0), 1.06, 0.98, 0.3, M_HAZ, C_DETAIL, n=28)
    for k in range(8):
        a_ = 2 * math.pi * k / 8
        obox(f"Hazard Stripe {i + 1}-{k + 1}", V(1.07 * math.cos(a_), BY + 1.07 * math.sin(a_), z), (0.04, 0.16, 0.32),
             V(math.cos(a_), math.sin(a_), 0), V(-math.sin(a_), math.cos(a_), 0), V(0.3, 0, 1).normalized(), M_BLACK, C_DETAIL)
''',
    tail='''# Spiked tail curling round from the back, ending in a dripping stinger
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.9 * (1 - i / 7), 0.9 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    mid = (tail[i] + tail[i + 1]) / 2
    cyl(f"Tail Spike {i + 1}", mid + V(0, 0, r0 * 0.6), mid + V(0, 0, r0 * 0.6 + 0.8), 0.22, 0.0, M_HORN, C_DETAIL, n=6)
S0 = tail[-1]
cyl("Stinger Bulb", S0, S0 + V(-0.3, -0.7, 0.5), 0.45, 0.3, M_STONE, C_DETAIL, n=10)
cyl("Stinger", S0 + V(-0.3, -0.7, 0.5), S0 + V(-0.5, -1.0, 1.7), 0.3, 0.0, M_HORN, C_DETAIL, n=8)
sphere("Stinger Drop", S0 + V(-0.52, -1.05, 1.45), 0.12, M_SLIME, C_DETAIL)
# leaking toxic barrel beside the screen box with a puddle
TB = V(-4.4, -2.2, 2.45)
cyl("Toxic Barrel", TB, TB + V(0, 0, 1.7), 0.7, 0.7, M_HAZ, C_DETAIL, n=16)
for z in (0.35, 1.35):
    torus(f"Barrel Hoop {z}", TB + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 0.71, 0.06, M_BLACK, C_DETAIL, n_major=16, n_minor=4)
cyl("Barrel Lid", TB + V(0, 0, 1.7), TB + V(0, 0, 1.78), 0.6, 0.6, M_SLIME, C_DETAIL, n=16)
sphere("Barrel Drip", TB + V(0.65, -0.3, 1.2), 0.12, M_SLIME, C_DETAIL)
cyl("Toxic Puddle", TB + V(0.8, -0.9, 0.0), TB + V(0.8, -0.9, 0.05), 1.1, 1.1, M_SLIME, C_DETAIL, n=18)
''',
    bg=(0.014, 0.03, 0.01), tint=(0.75, 1.0, 0.55), glow=(0.6, 1.0, 0.3), flame=(0.6, 1.0, 0.3),
))

# =====================================================================================================
VARIANTS.append(dict(
    folder="storm", file="storm_drake_mine.py", mine="StormDrakeMine",
    doc="""Storm Drake Mine - thunder variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in storm grey and electric yellow with its own details:
a crown of lightning-bolt spikes, nine mouth cogs, zig-zag horns with glowing tips, a copper tesla-coil heart,
a lightning-rod tail and a storm cloud striking the crystals with a bolt. Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (104, 112, 130), "Slate", rough=0.9, noise=((78, 86, 104), (138, 148, 168), 1.6, 0.25))
M_BLACK = MAT("Black", (14, 16, 22), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Storm Steel (DiamondPlate)", (40, 46, 62), "DiamondPlate", rough=0.35, metal=0.6, plate=9.0)
M_RIM = MAT("Volt Trim (DiamondPlate)", (255, 220, 40), "Metal", rough=0.35, metal=0.5, glow=(255, 220, 40), strength=0.5, plate=14.0)
M_MARBLE = MAT("Storm Marble", (18, 22, 34), "Marble", rough=0.25, marble=((14, 18, 28), (255, 220, 80)))
M_NEON = MAT("Neon (Glow)", (255, 250, 210), "Neon", rough=0.3, glow=(255, 236, 140), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Voltglass)", (140, 220, 255), "Glass", rough=0.15, glow=(90, 190, 255), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (40, 44, 54), "Slate", rough=0.95, noise=((28, 32, 40), (64, 70, 84), 3.0, 0.5))
M_WING = MAT("Wing Membrane", (72, 82, 106), "Fabric", rough=0.75, noise=((52, 60, 82), (104, 114, 138), 2.2, 0.2))
M_BONE = MAT("Wing Bone", (30, 34, 46), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Flame", (150, 220, 255), "Neon", rough=0.5, glow=(100, 190, 255), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (255, 240, 170), "Neon", rough=0.3, glow=(255, 220, 100), strength=8.0)
M_PINK = MAT("Volt LED", (255, 230, 40), "Neon", rough=0.3, glow=(255, 210, 20), strength=5.0)
M_BLUEBALL = MAT("Spark Knob", (120, 200, 255), "Neon", rough=0.3, glow=(80, 180, 255), strength=1.5)
M_ORE = MAT("Ore", (255, 240, 150), "Neon", rough=0.2, glow=(255, 220, 80), strength=1.2)
M_HORN = MAT("Horn", (30, 34, 46), "SmoothPlastic", rough=0.5)
M_BOLT = MAT("Lightning (Glow)", (255, 240, 120), "Neon", rough=0.3, glow=(255, 220, 60), strength=6.0, light=(12, 1.5))
M_COPPER = MAT("Copper Coil (Metal)", (200, 110, 60), "Metal", rough=0.3, metal=1.0)
M_CLOUD = MAT("Storm Cloud", (92, 98, 112), "SmoothPlastic", rough=0.9)
''',
    cogs=(9, 0.42, 0.22),
    crown='''# Crown of lightning-bolt spikes (the top one glows)
F = V(0, -1, 0)
BOLT = [(0.0, -0.5), (0.55, -0.12), (0.47, -0.42), (1.0, 0.0), (0.4, 0.2), (0.5, 0.48), (0.0, 0.5)]
for i, th in enumerate([90 + 360 * k / 7 for k in range(7)]):
    th = th % 360
    r_ = radial(th)
    L = 4.0 if abs(th - 90) < 1 else 3.1 if math.sin(math.radians(th)) > 0 else 2.5
    d_ = (A * 0.4 + F * 0.6 + r_ * 0.6).normalized()
    base = O + r_ * 2.95 + A * 0.3
    w_ = (A - d_ * A.dot(d_)).normalized()
    blade(f"Bolt Spike {i + 1}", [base + d_ * L * a + w_ * 1.4 * b for a, b in BOLT], 0.26, M_BOLT if abs(th - 90) < 1 else M_STONE, C_HEAD)

''',
    horns='''# Zig-zag horns with glowing tips
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 2.2 + X_AXIS * side * 1.8 - A_ * 1.2
    zig = [V(0, 0, 0), (-A_ * 0.6 + U_ * 1.0 + X_AXIS * side * 0.4), (-A_ * 1.4 + U_ * 1.3 + X_AXIS * side * 0.1),
           (-A_ * 1.9 + U_ * 2.3 + X_AXIS * side * 0.6), (-A_ * 2.8 + U_ * 2.6 + X_AXIS * side * 0.3), (-A_ * 3.2 + U_ * 3.6 + X_AXIS * side * 0.7)]
    pts = [c + z for z in zig]
    for k in range(5):
        cyl(f"Zig Horn {label} {k + 1}", pts[k], pts[k + 1], 0.45 * (1 - 0.7 * k / 5), 0.45 * (1 - 0.7 * (k + 1) / 5), M_HORN if k < 4 else M_BOLT, C_HEAD, n=8)
        sphere(f"Zig Joint {label} {k + 1}", pts[k + 1], 0.45 * (1 - 0.7 * (k + 1) / 5), M_HORN if k < 3 else M_BOLT, C_HEAD)

''',
    wings=('WRIST = (3.0, 17.1)\nTIPS = [(9.9, 13.6), (8.3, 9.8), (5.6, 8.0), (3.2, 8.6)]',
           'LEAD = [ROOT_TOP, (1.3, 16.3), WRIST, (5.0, 16.7), (7.0, 15.9), (8.7, 14.8), TIPS[0]]', 0.34),
    heart='''sphere("Tesla Core", V(0, BY, 10.45), 0.55, M_BOLT, C_DETAIL)
for k in range(7):
    torus(f"Tesla Coil {k + 1}", V(0, BY, 9.4 + k * 0.34), V(0, 0, 1), V(0, 1, 0), 0.92, 0.09, M_COPPER, C_DETAIL, n_major=24, n_minor=6)
for i in range(3):
    a_ = 2 * math.pi * i / 3 + 0.3
    beam(f"Coil Bar {i + 1}", V(1.04 * math.cos(a_), BY + 1.04 * math.sin(a_), 9.15), V(1.04 * math.cos(a_), BY + 1.04 * math.sin(a_), 11.7),
         0.14, 0.14, V(math.cos(a_), math.sin(a_), 0), M_NAVY, C_DETAIL)
''',
    tail='''# Spiked tail curling round from the back, ending in a lightning rod
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.9 * (1 - i / 7), 0.9 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    mid = (tail[i] + tail[i + 1]) / 2
    cyl(f"Tail Spike {i + 1}", mid + V(0, 0, r0 * 0.6), mid + V(0, 0, r0 * 0.6 + 0.9), 0.25, 0.0, M_HORN, C_DETAIL, n=6)
R0 = tail[-1]
cyl("Lightning Rod", R0, R0 + V(-0.2, -0.4, 2.4), 0.1, 0.07, M_COPPER, C_DETAIL, n=8)
sphere("Rod Ball", R0 + V(-0.2, -0.4, 2.5), 0.22, M_BOLT, C_DETAIL)
# storm cloud over the crystals striking them with a bolt
CL = V(0.2, 2.6, 20.2)
for k, (dx, dy, dz, r) in enumerate(((0, 0, 0, 1.3), (1.4, 0.2, -0.2, 1.0), (-1.4, -0.1, -0.15, 1.05), (0.6, 0.6, 0.6, 0.9), (-0.7, 0.4, 0.5, 0.85), (2.4, 0.1, -0.35, 0.7))):
    rock(f"Cloud Puff {k + 1}", CL + V(dx, dy, dz), (r * 1.2, r, r * 0.75), M_CLOUD, C_DETAIL, rough=0.08)
zz = [CL + V(0, -0.3, -0.9), V(0.6, 2.4, 19.0), V(-0.3, 2.3, 18.3), V(0.3, 2.4, 17.6), V(-0.4, 2.35, 17.0)]
for k in range(len(zz) - 1):
    cyl(f"Strike {k + 1}", zz[k], zz[k + 1], 0.12, 0.09, M_BOLT, C_DETAIL, n=6)
for k in range(3):
    sphere(f"Rain Drop {k + 1}", CL + V(-1.6 + k * 1.2, -0.6, -1.3 - 0.4 * (k % 2)), 0.08, M_CRYSTAL, C_DETAIL)
''',
    bg=(0.015, 0.018, 0.03), tint=(0.75, 0.82, 1.0), glow=(0.9, 0.85, 0.5), flame=(0.5, 0.8, 1.0),
))


def build(v):
    s = TEMPLATE
    s = cut(s, '"""Crimson Drake Mine', "\nRun from a terminal:", '"""' + v["doc"] + "\n")
    s = s.replace("CrimsonDrakeMine", v["mine"]).replace("crimson_drake_mine.py", v["file"])
    s = s.replace('SAMPLES = int(arg("--samples", 32))', 'SAMPLES = int(arg("--samples", 32))\nWITH_BASE = bool(arg("--base", False))  # no plinth by default\nBASE_H = 2.45')
    s = cut(s, "STONE_RGB = (168, 58, 52)", "\n# ------", MAT_HELPER + v["mats"])
    # base only with --base, and the ground clip helper
    i = s.index('slab("Base Slab"');j = s.index("M_MARBLE, C_BASE)", i) + len("M_MARBLE, C_BASE)")
    block = s[i:j]
    s = s[:i] + "if WITH_BASE:\n" + "\n".join("    " + ln for ln in block.split("\n")) + s[j:]
    s = s.replace("# --------------------------------------------------------------------------\n# BASE", CLIP.strip("\n") + "\n\n\n# --------------------------------------------------------------------------\n# BASE", 1)
    # mouth cogs
    n, w0, w1 = v["cogs"]
    s = s.replace("for k in range(10):\n    th = 18 + 36 * k", f"for k in range({n}):\n    th = {180 / n:g} + {360 / n:g} * k")
    s = s.replace("[c0 - t_ * 0.4 - A * 0.36, c0 + t_ * 0.4 - A * 0.36, c0 + t_ * 0.4 + A * 0.36, c0 - t_ * 0.4 + A * 0.36,",
                  f"[c0 - t_ * {w0} - A * 0.36, c0 + t_ * {w0} - A * 0.36, c0 + t_ * {w0} + A * 0.36, c0 - t_ * {w0} + A * 0.36,")
    s = s.replace("c1 - t_ * 0.22 - A * 0.36, c1 + t_ * 0.22 - A * 0.36, c1 + t_ * 0.22 + A * 0.36, c1 - t_ * 0.22 + A * 0.36],",
                  f"c1 - t_ * {w1} - A * 0.36, c1 + t_ * {w1} - A * 0.36, c1 + t_ * {w1} + A * 0.36, c1 - t_ * {w1} + A * 0.36],")
    s = cut(s, "# Crown of broad, flat spikes around the mouth", "# Curled ram horns", v["crown"])
    s = cut(s, "# Curled ram horns", "# The glowing ore cube", v["horns"])
    wr, lead, k = v["wings"]
    s = s.replace("WRIST = (3.0, 17.2)\nTIPS = [(10.0, 13.8), (8.4, 9.4), (4.8, 8.0)]", wr)
    s = s.replace("LEAD = [ROOT_TOP, (1.3, 16.3), WRIST, (5.0, 16.8), (7.0, 16.0), (8.8, 15.0), TIPS[0]]", lead)
    s = s.replace("k=0.48 if Pb != ROOT_BOT else 0.22", f"k={k} if Pb != ROOT_BOT else 0.22")
    s = cut(s, 'sphere("Magma Heart"', 'cyl("Battery Cap Top"', v["heart"])
    s = cut(s, "# Spiked tail curling round the base from the back", "# Lantern with flame", v["tail"] + "\n")
    # sit on the ground: drop everything by the plinth height and trim what goes below
    s = s.replace("# --------------------------------------------------------------------------\n# Tidy",
                  "if not WITH_BASE:\n    for ob in MINE_OBJECTS:\n        ob.data.transform(Matrix.Translation(V(0, 0, -BASE_H)))\n    clip_to_ground()\n\n"
                  "# --------------------------------------------------------------------------\n# Tidy", 1)
    # stage colours
    bg, t, g, f = v["bg"], v["tint"], v["glow"], v["flame"]
    s = s.replace("bg.inputs[\"Color\"].default_value = (0.04, 0.012, 0.012, 1)", f"bg.inputs[\"Color\"].default_value = ({bg[0]}, {bg[1]}, {bg[2]}, 1)")
    s = cut(s, 'add_light("Moon"', "\n# Bloom", f'''LZ = 0 if WITH_BASE else BASE_H
add_light("Moon", 'SUN', V(0, 0, 30), 1.2, {t}, rot=Euler((math.radians(50), 0, math.radians(30))))
add_light("Mine Glow", 'POINT', V(0, -4.0, 20), 7000, {g}, size=3)
add_light("Front Fill", 'POINT', V(0, -16, 9), 4000, {t}, size=4)
add_light("Back Fill", 'POINT', V(0, 15, 10), 3000, {t}, size=4)
add_light("Side Fill L", 'POINT', V(14, -2, 8), 2200, {t}, size=4)
add_light("Side Fill R", 'POINT', V(-14, -2, 8), 2200, {t}, size=4)
add_light("Flame Light", 'POINT', V(LX, LY, 7.0 - LZ), 120, {f}, size=0.3)
''')
    s = s.replace("}\ncam_objs = {}", "}\nif not WITH_BASE:\n    CAMS = {k: (l - V(0, 0, BASE_H), t - V(0, 0, BASE_H), ln, r) for k, (l, t, ln, r) in CAMS.items()}\ncam_objs = {}", 1)
    s = s.replace("\nif RENDER:\n", LUA.replace("{MINE}", v["mine"]) + "if RENDER:\n", 1)
    folder = os.path.join(HERE, "..", v["folder"])
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, v["file"])
    open(out, "w").write(s)
    print("wrote", os.path.relpath(out, HERE))


for v in VARIANTS:
    build(v)
