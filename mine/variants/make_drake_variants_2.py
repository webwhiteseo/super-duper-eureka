"""Five more Dragonglass-style drakes with bigger changes in look (second batch).
Uses the same generator as make_drake_variants.py.     python3 make_drake_variants_2.py"""
from make_drake_variants import build

V2 = []

# =====================================================================================================
V2.append(dict(
    folder="cyber", file="cyber_neon_mine.py", mine="CyberNeonMine",
    doc="""Cyber Neon Mine - tech variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in black carbon and chrome with cyan and magenta neon:
an antenna-array crown with glowing tips, twin antenna masts and a radar dish, angular panel wings on glowing
struts, a stacked power-core heart, a cable tail ending in a plug, and a hologram projector. Renders use Cycles.""",
    mats='''M_STONE = MAT("Carbon Shell", (34, 36, 46), "Metal", rough=0.35, metal=0.5, noise=((24, 26, 34), (52, 54, 66), 6.0, 0.12))
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
''',
    cogs=(8, 0.3, 0.3),
    crown='''# Antenna-array crown: thin chrome masts with glowing magenta tips
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

''',
    horns='''# Twin antenna towers and a radar dish
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

''',
    wings=('WRIST = (3.0, 17.2)\nTIPS = [(10.2, 14.4), (9.0, 11.0), (6.6, 8.4), (3.8, 8.2)]',
           'LEAD = [ROOT_TOP, (1.3, 16.3), WRIST, (6.0, 16.6), (8.6, 15.6), TIPS[0]]', 0.0),
    heart='''cyl("Power Core", V(0, BY, 9.15), V(0, BY, 11.7), 0.45, 0.45, M_NEON, C_DETAIL, n=16)
for k in range(5):
    torus(f"Core Ring {k + 1}", V(0, BY, 9.45 + k * 0.5), V(0, 0, 1), V(0, 1, 0), 0.82, 0.12, M_MAG if k % 2 else M_NAVY, C_DETAIL, n_major=24, n_minor=6)
for i in range(4):
    a_ = 2 * math.pi * i / 4 + math.pi / 4
    beam(f"Core Rail {i + 1}", V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), 9.15), V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), 11.7),
         0.14, 0.14, V(math.cos(a_), math.sin(a_), 0), M_BLACK, C_DETAIL)
''',
    tail='''# Cable tail with glowing rings, ending in a plug
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
''',
    bg=(0.008, 0.01, 0.025), tint=(0.6, 0.85, 1.0), glow=(0.9, 0.3, 1.0), flame=(1.0, 0.3, 0.9),
))

# =====================================================================================================
V2.append(dict(
    folder="jade", file="jade_emperor_mine.py", mine="JadeEmperorMine",
    doc="""Jade Emperor Mine - eastern-dragon variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in polished jade with red lacquer and gold:
a flowing red-and-gold mane, golden deer antlers, long golden whiskers, red silk wings on gold bones,
a glowing dragon pearl held in golden claws, a tasselled tail and a red paper lantern. Renders use Cycles.""",
    mats='''M_STONE = MAT("Jade (Marble)", (62, 152, 112), "Marble", rough=0.35, noise=((40, 120, 86), (112, 192, 152), 2.2, 0.12))
M_BLACK = MAT("Black", (16, 10, 8), "SmoothPlastic", rough=0.4)
M_NAVY = MAT("Red Lacquer", (176, 30, 26), "SmoothPlastic", rough=0.3, metal=0.2)
M_RIM = MAT("Gold Trim (DiamondPlate)", (236, 186, 70), "Metal", rough=0.3, metal=0.9, plate=14.0)
M_MARBLE = MAT("White Jade", (226, 236, 222), "Marble", rough=0.25, marble=((214, 228, 212), (90, 170, 120)))
M_NEON = MAT("Neon (Glow)", (255, 236, 190), "Neon", rough=0.3, glow=(255, 210, 130), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Jadeglass)", (120, 255, 180), "Glass", rough=0.15, glow=(60, 220, 140), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (44, 42, 38), "Slate", rough=0.95, noise=((30, 28, 26), (66, 62, 56), 3.0, 0.5))
M_WING = MAT("Red Silk (Fabric)", (196, 36, 30), "Fabric", rough=0.7, noise=((160, 24, 20), (226, 60, 50), 2.2, 0.15))
M_BONE = MAT("Gold Bone (Metal)", (236, 186, 70), "Metal", rough=0.25, metal=1.0)
M_FLAME = MAT("Flame", (255, 190, 90), "Neon", rough=0.5, glow=(255, 150, 50), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (255, 220, 150), "Neon", rough=0.3, glow=(255, 190, 100), strength=8.0)
M_PINK = MAT("Gold LED", (255, 200, 60), "Neon", rough=0.3, glow=(255, 180, 40), strength=5.0)
M_BLUEBALL = MAT("Pearl Knob", (245, 245, 235), "Neon", rough=0.3, glow=(255, 250, 230), strength=1.2)
M_ORE = MAT("Ore", (160, 255, 200), "Neon", rough=0.2, glow=(90, 240, 160), strength=1.2)
M_HORN = MAT("Gold Antler (Metal)", (236, 186, 70), "Metal", rough=0.25, metal=1.0)
M_PEARL = MAT("Dragon Pearl", (255, 250, 232), "Neon", rough=0.2, glow=(255, 240, 200), strength=4.0, light=(14, 1.6))
M_LANTERN = MAT("Paper Lantern", (224, 44, 32), "Neon", rough=0.6, glow=(255, 70, 30), strength=1.8, light=(10, 1.2))
''',
    cogs=(8, 0.5, 0.34),
    crown='''# Flowing mane: curved flame-shaped locks in red lacquer and gold, swept back
F = V(0, -1, 0)
for i, th in enumerate([90 + 360 * k / 11 for k in range(11)]):
    th = th % 360
    if 235 < th < 305:
        continue
    r_ = radial(th)
    t_ = tangent(th)
    L = 3.6 if abs(th - 90) < 1 else 3.0 if math.sin(math.radians(th)) > 0 else 2.2
    d_ = (r_ * 0.8 - A * 0.6).normalized()
    b0 = O + r_ * 2.9 - A * 0.2
    pts = [b0 - t_ * 0.45, b0 + d_ * L * 0.45 - t_ * 0.15 + r_ * 0.2, b0 + d_ * L + t_ * 0.35, b0 + d_ * L * 0.5 + t_ * 0.35, b0 + t_ * 0.45]
    blade(f"Mane Lock {i + 1}", pts, 0.2, M_NAVY if i % 2 else M_HORN, C_HEAD)

''',
    horns='''# Golden deer antlers and long whiskers
O_, A_, U_ = HEAD_FRAME
for side, label in ((1, "L"), (-1, "R")):
    b = O_ + U_ * 2.4 + X_AXIS * side * 1.4 - A_ * 1.5
    main = [b, b + U_ * 1.4 - A_ * 0.7 + X_AXIS * side * 0.3, b + U_ * 2.6 - A_ * 1.7 + X_AXIS * side * 0.6, b + U_ * 3.3 - A_ * 3.0 + X_AXIS * side * 0.7]
    for k in range(3):
        cyl(f"Antler {label} {k + 1}", main[k], main[k + 1], 0.3 - 0.07 * k, 0.23 - 0.07 * k, M_HORN, C_HEAD, n=8)
    for k, (f_, tip) in enumerate(((1, U_ * 1.3 + A_ * 0.2 + X_AXIS * side * 0.2), (2, U_ * 1.1 + A_ * 0.1 + X_AXIS * side * 0.4))):
        cyl(f"Antler Tine {label} {k + 1}", main[f_], main[f_] + tip, 0.15, 0.04, M_HORN, C_HEAD, n=6)
    w0 = O_ + U_ * 0.9 + X_AXIS * side * 0.9 + A_ * 3.2
    wpts = [w0]
    for k in range(1, 9):
        t = k / 8
        wpts.append(w0 + X_AXIS * side * (2.6 * t) - A_ * (1.8 * t) - U_ * (3.4 * t * t) + U_ * 0.8 * math.sin(math.pi * t))
    for k in range(8):
        cyl(f"Whisker {label} {k + 1}", wpts[k], wpts[k + 1], 0.12 * (1 - 0.8 * k / 8), 0.12 * (1 - 0.8 * (k + 1) / 8) + 0.01, M_HORN, C_HEAD, n=6)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.6, 13.2), (8.4, 10.0), (6.2, 8.4), (3.6, 8.4)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.6), (6.9, 15.6), (8.5, 14.5), TIPS[0]]', 0.3),
    heart='''sphere("Dragon Pearl", V(0, BY, 10.45), 0.85, M_PEARL, C_DETAIL)
for i in range(4):
    a_ = 2 * math.pi * i / 4 + math.pi / 4
    pts = [V(0.6 * math.cos(a_), BY + 0.6 * math.sin(a_), 9.15), V(1.15 * math.cos(a_), BY + 1.15 * math.sin(a_), 10.0),
           V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), 10.9), V(0.55 * math.cos(a_), BY + 0.55 * math.sin(a_), 11.35)]
    for k in range(3):
        cyl(f"Pearl Claw {i + 1}-{k + 1}", pts[k], pts[k + 1], 0.16 - 0.03 * k, 0.13 - 0.03 * k, M_HORN, C_DETAIL, n=8)
    cyl(f"Pearl Talon {i + 1}", pts[-1], pts[-1] + V(-0.25 * math.cos(a_), -0.25 * math.sin(a_), 0.1), 0.08, 0.0, M_BLACK, C_DETAIL, n=6)
''',
    tail='''# Jade tail with gold rings and a red silk tassel
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.9 * (1 - i / 7), 0.9 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    mid = (tail[i] + tail[i + 1]) / 2
    blade(f"Tail Fin {i + 1}", [mid + V(0, 0, r0 * 0.5) - (tail[i + 1] - tail[i]) * 0.3, mid + V(0, 0, r0 * 0.5 + 0.7), mid + V(0, 0, r0 * 0.5) + (tail[i + 1] - tail[i]) * 0.3], 0.1, M_NAVY, C_DETAIL)
d_ = (tail[-1] - tail[-2]).normalized()
T0 = tail[-1] + d_ * 0.1
cyl("Tassel Cap", T0, T0 + d_ * 0.4, 0.2, 0.25, M_HORN, C_DETAIL, n=10)
cyl("Tassel", T0 + d_ * 0.4, T0 + d_ * 1.7 + V(0, 0, -0.2), 0.32, 0.12, M_WING, C_DETAIL, n=10)
# red paper lantern on a gold hook (by the screen side)
LP = V(-4.4, -1.6, 2.45)
cyl("Lantern Pole", LP, LP + V(0, 0, 4.6), 0.1, 0.08, M_HORN, C_DETAIL, n=8)
cyl("Lantern Hook", LP + V(0, 0, 4.6), LP + V(0.0, -1.0, 4.6), 0.06, 0.06, M_HORN, C_DETAIL, n=6, hint=V(0, 0, 1))
PL = LP + V(0, -1.0, 3.55)
rock("Paper Lantern Body", PL, (0.62, 0.62, 0.5), M_LANTERN, C_DETAIL, rough=0.0)
for dz, r in ((0.5, 0.3), (-0.5, 0.3)):
    cyl(f"Lantern Cap {dz}", PL + V(0, 0, dz - 0.06), PL + V(0, 0, dz + 0.06), r, r, M_HORN, C_DETAIL, n=12)
cyl("Lantern String", PL + V(0, 0, 0.56), PL + V(0, 0, 1.05), 0.03, 0.03, M_BLACK, C_DETAIL, n=4)
cyl("Lantern Tassel", PL + V(0, 0, -0.56), PL + V(0, 0, -1.2), 0.08, 0.14, M_WING, C_DETAIL, n=8)
''',
    bg=(0.012, 0.03, 0.022), tint=(0.85, 1.0, 0.85), glow=(1.0, 0.8, 0.5), flame=(1.0, 0.75, 0.4),
))

# =====================================================================================================
V2.append(dict(
    folder="necro", file="bone_necro_mine.py", mine="BoneNecroMine",
    doc="""Bone Necro Mine - undead variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in bleached bone with ghostly soul-green fire:
a ribcage crown, dark cracked horns with glowing eye sockets, ghost-membrane wings on bone fingers,
a soul flame caged in ribs, a vertebrae tail, and gravestones with skulls. Renders use Cycles.""",
    mats='''M_STONE = MAT("Bone (Slate)", (214, 204, 180), "Limestone", rough=0.8, noise=((186, 174, 146), (234, 226, 206), 2.0, 0.3))
M_BLACK = MAT("Black", (12, 14, 12), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Grave Iron (DiamondPlate)", (46, 52, 46), "DiamondPlate", rough=0.4, metal=0.6, plate=9.0)
M_RIM = MAT("Soul Trim (DiamondPlate)", (90, 255, 140), "Metal", rough=0.35, metal=0.5, glow=(90, 255, 140), strength=0.5, plate=14.0)
M_MARBLE = MAT("Grave Marble", (20, 24, 20), "Marble", rough=0.25, marble=((16, 20, 16), (90, 255, 140)))
M_NEON = MAT("Neon (Glow)", (190, 255, 210), "Neon", rough=0.3, glow=(90, 255, 150), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Soulglass)", (100, 255, 170), "Glass", rough=0.15, glow=(40, 230, 120), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (42, 46, 40), "Slate", rough=0.95, noise=((28, 32, 26), (64, 70, 60), 3.0, 0.5))
M_WING = MAT("Ghost Membrane", (120, 255, 170), "Glass", rough=0.5, glow=(60, 220, 120), strength=0.8, alpha=0.45)
M_BONE = MAT("Wing Bone", (228, 220, 198), "SmoothPlastic", rough=0.6)
M_FLAME = MAT("Soul Flame", (150, 255, 190), "Neon", rough=0.5, glow=(60, 255, 130), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (160, 255, 190), "Neon", rough=0.3, glow=(80, 255, 140), strength=8.0)
M_PINK = MAT("Soul LED", (90, 255, 140), "Neon", rough=0.3, glow=(60, 255, 120), strength=5.0)
M_BLUEBALL = MAT("Soul Knob", (120, 255, 170), "Neon", rough=0.3, glow=(80, 255, 140), strength=1.5)
M_ORE = MAT("Ore", (170, 255, 200), "Neon", rough=0.2, glow=(90, 255, 150), strength=1.2)
M_HORN = MAT("Dark Horn", (42, 38, 34), "SmoothPlastic", rough=0.5)
M_SOUL = MAT("Soul Fire", (120, 255, 160), "Neon", rough=0.3, glow=(60, 255, 120), strength=7.0, light=(14, 1.6))
M_GRAVE = MAT("Gravestone", (96, 100, 96), "Slate", rough=0.9, noise=((72, 76, 72), (120, 126, 120), 3.0, 0.4))
''',
    cogs=(10, 0.4, 0.06),
    crown='''# Ribcage crown: curved ribs arching back over the head
F = V(0, -1, 0)
for i, th in enumerate((20, 45, 70, 90, 110, 135, 160)):
    r_ = radial(th)
    L = 3.8 if th == 90 else 3.3 if th in (70, 110) else 2.7
    p0 = O + r_ * 2.95 - A * 0.1
    pts = [p0]
    for k in range(1, 6):
        t = k / 5
        pts.append(p0 + r_ * L * 0.55 * math.sin(math.pi * t * 0.8) - A * L * t + F * 0.0)
    for k in range(5):
        cyl(f"Rib {i + 1}-{k + 1}", pts[k], pts[k + 1], 0.2 * (1 - 0.6 * k / 5), 0.2 * (1 - 0.6 * (k + 1) / 5), M_STONE, C_HEAD, n=8)
    sphere(f"Rib Knuckle {i + 1}", p0, 0.24, M_STONE, C_HEAD)
# glowing eye sockets on top of the head
for side in (1, -1):
    e = O + U * 2.2 + X_AXIS * side * 1.25 - A * 0.9
    sphere(f"Eye Socket {side}", e, 0.48, M_BLACK, C_HEAD)
    sphere(f"Soul Eye {side}", e + A * 0.3 + U * 0.05, 0.24, M_SOUL, C_HEAD)

''',
    horns='''# Dark cracked horns curling down past the jaw
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 1.8 + X_AXIS * side * 2.5 - A_ * 1.6
    pts = []
    for k in range(11):
        t = k / 10
        ang = math.radians(30 - 200 * t)
        rad = 1.8 * (1 - 0.35 * t)
        pts.append(c + X_AXIS * side * (0.9 * t) + (math.cos(ang) * U_ + math.sin(ang) * (-A_)) * rad)
    for k in range(10):
        cyl(f"Dark Horn {label} {k + 1}", pts[k], pts[k + 1], 0.5 * (1 - 0.8 * k / 10), 0.5 * (1 - 0.8 * (k + 1) / 10), M_HORN, C_HEAD, n=8)
        if k % 3 == 1:
            torus(f"Horn Crack {label} {k + 1}", pts[k + 1], (pts[k + 1] - pts[k]).normalized(), X_AXIS, 0.5 * (1 - 0.8 * (k + 1) / 10) + 0.02, 0.03, M_SOUL, C_HEAD, n_major=10, n_minor=4)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.8, 14.2), (8.6, 10.4), (6.2, 8.2), (3.6, 8.4)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.9), (7.0, 16.3), (8.6, 15.4), TIPS[0]]', 0.72),
    heart='''sphere("Soul Flame Core", V(0, BY, 10.45), 0.6, M_SOUL, C_DETAIL)
for i in range(6):
    a_ = 2 * math.pi * i / 6
    pts = [V(0.35 * math.cos(a_), BY + 0.35 * math.sin(a_), 9.15)]
    for k in range(1, 5):
        t = k / 4
        r = 0.35 + 0.75 * math.sin(math.pi * t)
        pts.append(V(r * math.cos(a_), BY + r * math.sin(a_), 9.15 + 2.55 * t))
    for k in range(4):
        cyl(f"Heart Rib {i + 1}-{k + 1}", pts[k], pts[k + 1], 0.11, 0.11, M_STONE, C_DETAIL, n=6)
''',
    tail='''# Vertebrae tail: bone discs with spines
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0 = 0.8 * (1 - i / 7)
    cyl(f"Spine Cord {i + 1}", tail[i], tail[i + 1], max(r0 * 0.4, 0.1), max(r0 * 0.35, 0.08), M_STONE, C_DETAIL, n=8)
    d_ = (tail[i + 1] - tail[i]).normalized()
    for k in range(3):
        p = tail[i] + (tail[i + 1] - tail[i]) * (k + 0.5) / 3
        cyl(f"Vertebra {i + 1}-{k + 1}", p - d_ * 0.18, p + d_ * 0.18, max(r0, 0.18), max(r0, 0.18) * 0.85, M_STONE, C_DETAIL, n=10)
        cyl(f"Vertebra Spine {i + 1}-{k + 1}", p + V(0, 0, max(r0, 0.18) * 0.7), p + V(0, 0, max(r0, 0.18) + 0.5) - d_ * 0.25, 0.1, 0.0, M_STONE, C_DETAIL, n=5)
# gravestones and skulls
for k, (x, y, rot) in enumerate(((5.0, 3.4, 0.2), (-4.6, 3.8, -0.15), (-4.7, -2.6, 0.1))):
    G = V(x, y, 2.45)
    d_ = V(math.sin(rot), -math.cos(rot), 0)
    s_ = V(math.cos(rot), math.sin(rot), 0)
    obox(f"Gravestone {k + 1}", G + V(0, 0, 0.7), (1.1, 0.3, 1.9), s_, d_, V(0, 0, 1), M_GRAVE, C_DETAIL)
    cyl(f"Gravestone Top {k + 1}", G + V(0, 0, 1.65) - d_ * 0.15, G + V(0, 0, 1.65) + d_ * 0.15, 0.55, 0.55, M_GRAVE, C_DETAIL, n=16, hint=V(0, 0, 1))
    obox(f"Grave Cross {k + 1}", G + V(0, 0, 1.35) + d_ * 0.16, (0.12, 0.04, 0.7), s_, d_, V(0, 0, 1), M_SOUL, C_DETAIL)
    obox(f"Grave Cross Bar {k + 1}", G + V(0, 0, 1.5) + d_ * 0.16, (0.45, 0.04, 0.12), s_, d_, V(0, 0, 1), M_SOUL, C_DETAIL)
for k, (x, y) in enumerate(((4.2, -3.6), (-3.6, 4.6), (5.6, 1.0))):
    S = V(x, y, 2.75)
    sphere(f"Skull {k + 1}", S, 0.32, M_STONE, C_DETAIL)
    obox(f"Skull Jaw {k + 1}", S + V(0, -0.12, -0.25), (0.36, 0.3, 0.14), X_AXIS, V(0, 1, 0), V(0, 0, 1), M_STONE, C_DETAIL)
    for s in (-1, 1):
        sphere(f"Skull Eye {k + 1}{s}", S + V(s * 0.12, -0.26, 0.04), 0.08, M_SOUL, C_DETAIL)
''',
    bg=(0.01, 0.02, 0.014), tint=(0.8, 1.0, 0.85), glow=(0.5, 1.0, 0.6), flame=(0.5, 1.0, 0.6),
))

# =====================================================================================================
V2.append(dict(
    folder="rose", file="rose_quartz_mine.py", mine="RoseQuartzMine",
    doc="""Rose Quartz Mine - crystal variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in pastel pink and rose gold:
a crown of rose-quartz crystals, crystal-cluster horns, rose-gold wings, a glowing heart gem in a
rose-gold ring, a crystal-spiked tail with a heart tip, crystal flowers and floating hearts. Renders use Cycles.""",
    mats='''M_STONE = MAT("Stone (Slate)", (236, 172, 192), "Slate", rough=0.8, noise=((214, 146, 170), (250, 198, 214), 1.6, 0.2))
M_BLACK = MAT("Black", (46, 22, 34), "SmoothPlastic", rough=0.4)
M_NAVY = MAT("Rose Gold (Metal)", (232, 162, 142), "Metal", rough=0.22, metal=0.95)
M_RIM = MAT("Pink Trim (DiamondPlate)", (255, 120, 190), "Metal", rough=0.3, metal=0.6, glow=(255, 120, 190), strength=0.5, plate=14.0)
M_MARBLE = MAT("White Marble", (248, 240, 244), "Marble", rough=0.25, marble=((240, 230, 236), (255, 140, 190)))
M_NEON = MAT("Neon (Glow)", (255, 232, 245), "Neon", rough=0.3, glow=(255, 170, 220), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Rose Quartz)", (255, 150, 205), "Glass", rough=0.1, glow=(255, 100, 180), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Rock", (206, 186, 214), "Slate", rough=0.9, noise=((180, 160, 192), (226, 210, 232), 3.0, 0.4))
M_WING = MAT("Wing Membrane", (255, 204, 228), "Fabric", rough=0.7, noise=((246, 178, 210), (255, 226, 240), 2.0, 0.15))
M_BONE = MAT("Wing Bone (Metal)", (232, 162, 142), "Metal", rough=0.22, metal=0.95)
M_FLAME = MAT("Flame", (255, 160, 225), "Neon", rough=0.5, glow=(255, 100, 200), strength=10.0, light=(12, 2))
M_SCREEN = MAT("Screen", (255, 200, 235), "Neon", rough=0.3, glow=(255, 140, 210), strength=8.0)
M_PINK = MAT("Heart LED", (255, 60, 140), "Neon", rough=0.3, glow=(255, 30, 120), strength=5.0)
M_BLUEBALL = MAT("Lilac Knob", (205, 150, 255), "Neon", rough=0.3, glow=(180, 120, 255), strength=1.5)
M_ORE = MAT("Ore", (255, 190, 230), "Neon", rough=0.2, glow=(255, 130, 200), strength=1.2)
M_HORN = MAT("Lilac Crystal", (200, 160, 255), "Glass", rough=0.1, glow=(170, 120, 255), strength=0.8, alpha=0.15)
M_HEART = MAT("Heart Gem", (255, 46, 116), "Neon", rough=0.2, glow=(255, 20, 90), strength=3.0, light=(14, 1.6))
''',
    cogs=(8, 0.5, 0.5),
    crown='''# Crown of rose-quartz crystals
F = V(0, -1, 0)
rnd_c = random.Random(21)
for i, th in enumerate([90 + 360 * k / 10 for k in range(10)]):
    th = th % 360
    if 240 < th < 300:
        continue
    r_ = radial(th)
    L = 3.6 if abs(th - 90) < 1 else rnd_c.uniform(2.0, 3.0)
    d_ = (A * 0.3 + F * 0.5 + r_ * 0.7).normalized()
    crystal(f"Crown Crystal {i + 1}", O + r_ * 2.9 + A * 0.2, d_, L, 0.42 if abs(th - 90) < 1 else 0.33, M_CRYSTAL if i % 2 == 0 else M_HORN, C_HEAD)

''',
    horns='''# Crystal-cluster horns
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 2.3 + X_AXIS * side * 1.5 - A_ * 1.5
    for k, (d_, L, r) in enumerate(((-A_ * 0.6 + U_ * 0.8 + X_AXIS * side * 0.2, 3.4, 0.45), (-A_ * 0.9 + U_ * 0.4 + X_AXIS * side * 0.5, 2.6, 0.36),
                                    (-A_ * 0.3 + U_ * 0.9 + X_AXIS * side * 0.6, 2.0, 0.3))):
        crystal(f"Horn Crystal {label} {k + 1}", c, d_.normalized(), L, r, M_HORN if k == 0 else M_CRYSTAL, C_HEAD)
    rock(f"Horn Base {label}", c, (0.55, 0.55, 0.35), M_NAVY, C_HEAD, rough=0.05)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.6, 13.0), (8.4, 9.8), (6.2, 8.4), (3.6, 8.4)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (4.9, 16.6), (6.9, 15.6), (8.5, 14.4), TIPS[0]]', 0.15),
    heart='''HT = [V(0.055 * 16 * math.sin(t) ** 3, 0, 0.055 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)))
      for t in [2 * math.pi * k / 28 for k in range(28)]]
blade("Heart Gem", [V(0, BY + 0.55, 10.5) + p for p in HT], 0.5, M_HEART, C_DETAIL)
blade("Heart Gem Back", [V(0, BY - 0.1, 10.5) + p * 0.9 for p in HT], 0.5, M_HEART, C_DETAIL)
torus("Heart Ring", V(0, BY, 10.45), V(0, 1, 0), V(0, 0, 1), 1.1, 0.09, M_NAVY, C_DETAIL, n_major=28, n_minor=6)
for k in range(4):
    a_ = math.pi / 4 + k * math.pi / 2
    sphere(f"Ring Pearl {k + 1}", V(1.1 * math.cos(a_), BY, 10.45 + 1.1 * math.sin(a_)), 0.15, M_NEON, C_DETAIL)
''',
    tail='''# Tail with crystal spikes and a heart tip
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.85 * (1 - i / 7), 0.85 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.15), max(r1, 0.12), M_STONE, C_DETAIL, n=10)
    mid = (tail[i] + tail[i + 1]) / 2
    crystal(f"Tail Crystal {i + 1}", mid + V(0, 0, r0 * 0.5), V(0.1, 0.1, 1), 0.6 + r0, 0.16 + r0 * 0.1, M_CRYSTAL if i % 2 else M_HORN, C_DETAIL)
d_ = (tail[-1] - tail[-2]).normalized()
s_ = V(-d_.y, d_.x, 0)
HT2 = [d_ * (0.06 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))) * -1 + s_ * 0.06 * 16 * math.sin(t) ** 3
       for t in [2 * math.pi * k / 24 for k in range(24)]]
blade("Tail Heart", [tail[-1] + d_ * 0.9 + V(0, 0, 0.3) + p for p in HT2], 0.22, M_HEART, C_DETAIL)
# crystal flowers on the ground and floating hearts
rnd_f = random.Random(5)
for k, (x, y) in enumerate(((5.2, 3.3), (-4.5, 3.9), (-4.6, -2.8), (5.3, -1.0))):
    for j in range(3):
        a = rnd_f.uniform(0, 6.28)
        crystal(f"Flower Crystal {k + 1}-{j + 1}", V(x, y, 2.45), V(math.cos(a) * 0.5, math.sin(a) * 0.5, 1), rnd_f.uniform(0.7, 1.3), 0.2, M_CRYSTAL if j else M_HORN, C_DETAIL)
for k, (x, y, z, sc) in enumerate(((4.4, -1.2, 9.5, 0.6), (-3.8, 1.0, 12.5, 0.5), (3.2, 4.6, 14.0, 0.45))):
    blade(f"Floating Heart {k + 1}", [V(x, y, z) + p * sc for p in HT], 0.15, M_HEART, C_DETAIL)
''',
    bg=(0.03, 0.016, 0.026), tint=(1.0, 0.82, 0.92), glow=(1.0, 0.55, 0.8), flame=(1.0, 0.5, 0.85),
))

# =====================================================================================================
V2.append(dict(
    folder="steampunk", file="copper_steam_mine.py", mine="CopperSteamMine",
    doc="""Copper Steam Mine - steampunk variant of the Dragonglass-style mine, for Blender 5.x.

Same build as the Dragonglass / Crimson Drake mine in riveted copper and brass:
a crown of exhaust pipes puffing steam, brass pipe horns ending in valve wheels, canvas glider wings on wooden
spars, a riveted boiler heart with a pressure gauge, a geared tail with a propeller, and a smokestack.
Renders use Cycles.""",
    mats='''M_STONE = MAT("Copper Plate (Metal)", (186, 104, 58), "Metal", rough=0.35, metal=0.75, noise=((150, 80, 40), (216, 132, 80), 3.0, 0.15))
M_BLACK = MAT("Black", (22, 18, 16), "SmoothPlastic", rough=0.45)
M_NAVY = MAT("Brass (Metal)", (212, 162, 70), "Metal", rough=0.25, metal=1.0)
M_RIM = MAT("Brass Trim (DiamondPlate)", (212, 162, 70), "Metal", rough=0.3, metal=0.9, plate=14.0)
M_MARBLE = MAT("Walnut Marble", (60, 40, 28), "Marble", rough=0.3, marble=((48, 32, 22), (212, 162, 70)))
M_NEON = MAT("Neon (Glow)", (255, 222, 160), "Neon", rough=0.3, glow=(255, 180, 90), strength=2.4, light=(10, 1))
M_CRYSTAL = MAT("Crystal (Amber)", (255, 160, 50), "Glass", rough=0.15, glow=(255, 120, 20), strength=1.0, alpha=0.15, light=(8, 0.6))
M_ROCK = MAT("Coal", (32, 30, 30), "Slate", rough=0.7, metal=0.2)
M_WING = MAT("Wing Canvas (Fabric)", (198, 172, 130), "Fabric", rough=0.85, noise=((172, 146, 104), (220, 196, 156), 2.5, 0.15))
M_BONE = MAT("Wing Spar (Wood)", (102, 66, 40), "Wood", rough=0.7)
M_FLAME = MAT("Flame", (255, 180, 80), "Neon", rough=0.5, glow=(255, 140, 40), strength=12.0, light=(12, 2))
M_SCREEN = MAT("Screen", (255, 210, 140), "Neon", rough=0.3, glow=(255, 170, 80), strength=8.0)
M_PINK = MAT("Amber LED", (255, 170, 40), "Neon", rough=0.3, glow=(255, 150, 20), strength=5.0)
M_BLUEBALL = MAT("Valve Red", (196, 40, 30), "SmoothPlastic", rough=0.4)
M_ORE = MAT("Ore", (255, 200, 120), "Neon", rough=0.2, glow=(255, 160, 60), strength=1.2)
M_HORN = MAT("Iron (Metal)", (54, 52, 54), "Metal", rough=0.4, metal=0.9)
M_GAUGE = MAT("Gauge Face", (240, 234, 216), "SmoothPlastic", rough=0.5)
M_STEAM = MAT("Steam", (232, 232, 236), "SmoothPlastic", rough=0.9, alpha=0.3)
M_PATINA = MAT("Patina", (92, 170, 150), "SmoothPlastic", rough=0.7)
''',
    cogs=(14, 0.26, 0.2),
    crown='''# Crown of brass exhaust pipes puffing steam, two big side gears
F = V(0, -1, 0)
def gear(name, C, axis, up, r, teeth, th, mat):
    tube(name, C, axis, up, r, r * 0.45, th, mat, C_HEAD, n=max(24, teeth * 2))
    a_ = axis.normalized();u_ = up.normalized();v_ = a_.cross(u_).normalized()
    for k in range(teeth):
        ang = 2 * math.pi * k / teeth
        rr = math.cos(ang) * v_ + math.sin(ang) * u_;tt = -math.sin(ang) * v_ + math.cos(ang) * u_
        obox(f"{name} Tooth {k + 1}", C + rr * (r + 0.12), (th, 0.26, 0.3), a_, rr, tt, mat, C_HEAD)
    cyl(f"{name} Hub", C - a_ * th * 0.7, C + a_ * th * 0.7, r * 0.2, r * 0.2, M_HORN, C_HEAD, n=12, hint=u_)
for i, th in enumerate((45, 67, 90, 113, 135)):
    r_ = radial(th)
    p0 = O + r_ * 2.9 - A * 0.4
    L = 3.4 if th == 90 else 2.8 if th in (67, 113) else 2.2
    d_ = (r_ * 0.7 - A * 0.7).normalized()
    cyl(f"Exhaust Pipe {i + 1}", p0, p0 + d_ * L, 0.28, 0.28, M_NAVY, C_HEAD, n=10)
    tube(f"Exhaust Flare {i + 1}", p0 + d_ * (L + 0.1), d_, perp_basis(d_)[0], 0.4, 0.26, 0.25, M_NAVY, C_HEAD, n=12)
    if i % 2 == 0:
        rock(f"Steam Puff {i + 1}", p0 + d_ * (L + 0.7), (0.45, 0.45, 0.4), M_STEAM, C_HEAD, rough=0.15)
for side in (1, -1):
    gear(f"Side Gear {side}", O + X_AXIS * side * 2.9 - A * 1.6 + U * 0.6, X_AXIS * side, U, 1.0, 12, 0.22, M_NAVY)

''',
    horns='''# Brass pipe horns ending in red valve wheels
for side, label in ((1, "L"), (-1, "R")):
    O_, A_, U_ = HEAD_FRAME
    c = O_ + U_ * 1.6 + X_AXIS * side * 2.6 - A_ * 1.2
    pts = []
    for k in range(9):
        t = k / 8
        ang = math.radians(-40 + 220 * t)
        rad = 1.7 * (1 - 0.3 * t)
        pts.append(c + X_AXIS * side * (0.8 * t) + (math.cos(ang) * U_ + math.sin(ang) * (-A_)) * rad)
    for k in range(8):
        cyl(f"Pipe Horn {label} {k + 1}", pts[k], pts[k + 1], 0.32, 0.32, M_NAVY if k % 2 else M_STONE, C_HEAD, n=10)
        if k % 2 == 1:
            torus(f"Pipe Joint {label} {k + 1}", pts[k + 1], (pts[k + 1] - pts[k]).normalized(), X_AXIS, 0.36, 0.06, M_HORN, C_HEAD, n_major=12, n_minor=4)
    dv = (pts[-1] - pts[-2]).normalized()
    W = pts[-1] + dv * 0.35
    cyl(f"Valve Stem {label}", pts[-1], W, 0.08, 0.08, M_HORN, C_HEAD, n=6)
    torus(f"Valve Wheel {label}", W, dv, perp_basis(dv)[0], 0.45, 0.07, M_BLUEBALL, C_HEAD, n_major=16, n_minor=5)
    for k in range(4):
        a_ = k * math.pi / 2
        u_, v_ = perp_basis(dv)
        cyl(f"Valve Spoke {label} {k + 1}", W, W + (math.cos(a_) * u_ + math.sin(a_) * v_) * 0.43, 0.04, 0.04, M_BLUEBALL, C_HEAD, n=5)

''',
    wings=('WRIST = (3.0, 17.0)\nTIPS = [(9.8, 13.6), (8.8, 11.0), (7.2, 9.0), (5.2, 8.0), (3.2, 8.4)]',
           'LEAD = [ROOT_TOP, (1.3, 16.2), WRIST, (5.0, 16.6), (7.0, 15.8), (8.6, 14.8), TIPS[0]]', 0.15),
    heart='''cyl("Boiler", V(0, BY, 9.15), V(0, BY, 11.7), 1.0, 1.0, M_STONE, C_DETAIL, n=24)
for z in (9.4, 11.45):
    for k in range(12):
        a_ = 2 * math.pi * k / 12
        sphere(f"Boiler Rivet {z}-{k + 1}", V(1.0 * math.cos(a_), BY + 1.0 * math.sin(a_), z), 0.07, M_NAVY, C_DETAIL)
G0 = V(0, BY + 1.0, 10.45)
cyl("Gauge Body", G0, G0 + V(0, 0.25, 0), 0.5, 0.5, M_NAVY, C_DETAIL, n=20, hint=V(0, 0, 1))
cyl("Gauge Face", G0 + V(0, 0.25, 0), G0 + V(0, 0.28, 0), 0.42, 0.42, M_GAUGE, C_DETAIL, n=20, hint=V(0, 0, 1))
beam("Gauge Needle", G0 + V(0, 0.3, 0), G0 + V(0.25, 0.3, 0.22), 0.04, 0.04, V(0, 1, 0), M_BLUEBALL, C_DETAIL)
for k in range(8):
    a_ = math.radians(200 - k * 31)
    sphere(f"Gauge Tick {k + 1}", G0 + V(0.34 * math.cos(a_), 0.29, 0.34 * math.sin(a_)), 0.035, M_BLACK, C_DETAIL)
cyl("Pressure Pipe", V(0.7, BY + 0.7, 11.2), V(1.3, BY + 1.3, 11.9), 0.1, 0.1, M_PATINA, C_DETAIL, n=6)
''',
    tail='''# Geared copper tail ending in a propeller, plus a smokestack
tail = [V(0, 3.9, 3.3), V(1.8, 5.0, 2.9), V(3.8, 4.8, 2.7), V(4.9, 3.0, 2.6), V(5.0, 0.2, 2.6), V(4.5, -2.6, 2.55), V(3.4, -4.6, 2.5)]
for i in range(len(tail) - 1):
    r0, r1 = 0.85 * (1 - i / 7), 0.85 * (1 - (i + 1) / 7)
    cyl(f"Tail {i + 1}", tail[i], tail[i + 1], max(r0, 0.18), max(r1, 0.15), M_STONE, C_DETAIL, n=10)
    d_ = (tail[i + 1] - tail[i]).normalized()
    torus(f"Tail Band {i + 1}", tail[i + 1], d_, V(0, 0, 1), max(r1, 0.15) + 0.04, 0.07, M_NAVY, C_DETAIL, n_major=12, n_minor=4)
d_ = (tail[-1] - tail[-2]).normalized()
H0 = tail[-1] + d_ * 0.35
cyl("Prop Shaft", tail[-1], H0, 0.1, 0.1, M_HORN, C_DETAIL, n=6)
sphere("Prop Hub", H0, 0.2, M_NAVY, C_DETAIL)
u_, v_ = perp_basis(d_)
for k in range(3):
    a_ = 2 * math.pi * k / 3 + 0.4
    r_ = math.cos(a_) * u_ + math.sin(a_) * v_
    t_ = -math.sin(a_) * u_ + math.cos(a_) * v_
    blade(f"Prop Blade {k + 1}", [H0 + r_ * 0.15 - t_ * 0.12, H0 + r_ * 1.1 - t_ * 0.25 + d_ * 0.05, H0 + r_ * 1.2 + t_ * 0.15, H0 + r_ * 0.15 + t_ * 0.12], 0.05, M_BONE, C_DETAIL)
SS = V(-1.3, 0.3, 15.2)
cyl("Smokestack", SS, SS + V(0, 0, 3.2), 0.38, 0.32, M_HORN, C_DETAIL, n=12)
cyl("Smokestack Crown", SS + V(0, 0, 3.2), SS + V(0, 0, 3.55), 0.42, 0.52, M_NAVY, C_DETAIL, n=12)
for k, (dx, dz, r) in enumerate(((0.1, 4.1, 0.45), (-0.4, 4.7, 0.6), (-1.1, 5.2, 0.7))):
    rock(f"Stack Smoke {k + 1}", SS + V(dx, 0.1 * k, dz), (r, r, r * 0.85), M_STEAM, C_DETAIL, rough=0.15)
''',
    bg=(0.03, 0.02, 0.012), tint=(1.0, 0.88, 0.72), glow=(1.0, 0.7, 0.4), flame=(1.0, 0.7, 0.35),
))

if __name__ == "__main__":
    for v in V2:
        build(v)
