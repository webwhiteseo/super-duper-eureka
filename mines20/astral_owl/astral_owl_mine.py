"""Astral Owl Mine - FUSION of the Clockwork Owl and the Astral Orrery.
A star-plated night-metal owl with starlight lens eyes perches in a golden crescent moon on an orrery column. Its chest
window holds a tiny solar system, planets ride gold arms round the column, and stardust pours from its chest
through a funnel and spout to drop the ore. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_ORRERY, C_OWL, C_WINGS, C_DETAIL = begin("AstralOwlMine", ["Base", "Orrery", "Owl", "Wings", "Details"], seed=20)
BLACK = M("Black", (10, 10, 20), rough=0.5, rbx="SmoothPlastic")
GOLD = M("Gold Trim (Metal)", (232, 182, 72), rough=0.25, metal=1.0, rbx="Metal")
STARM = M("Star Marble (Marble)", (22, 24, 56), rough=0.3, marble=((18, 20, 48), (120, 130, 210)))
NIGHT = M("Night Metal", (28, 36, 86), rough=0.3, metal=0.7, rbx="Metal", plate=11.0)
PURPLE = M("Dusk Feathers", (74, 52, 146), rough=0.35, metal=0.5, rbx="Metal")
NEON = M("Starlight", (190, 245, 255), rough=0.3, glow=(160, 235, 255), glow_strength=5.0, rbx="Neon", light=(8, 0.9))
LENS = M("Lens Glow", (120, 230, 255), rough=0.1, glow=(90, 210, 255), glow_strength=6.0, rbx="Neon", light=(10, 1.4))
CORE = M("Star Core", (255, 228, 180), rough=0.3, glow=(255, 190, 110), glow_strength=8.0, rbx="Neon", light=(14, 1.8))
PLR = M("Planet Red", (220, 90, 60), rough=0.5)
PLT = M("Planet Teal", (60, 190, 170), rough=0.5)
PLP = M("Planet Purple", (140, 90, 210), rough=0.5)
MOON = M("Moon Silver", (214, 214, 226), rough=0.6, rbx="SmoothPlastic", noise=((176, 176, 190), (236, 236, 244), 5.0, 0.3))
CRYSTAL = M("Starglass Crystal", (175, 135, 255), rough=0.05, glow=(150, 100, 255), glow_strength=1.2, rbx="Glass", alpha=0.15)
ROCK = M("Meteor Rock", (38, 34, 52), rough=0.85, rbx="Slate")
INK = M("Pupil", (8, 8, 14), rough=0.4)
ORE = M("Starfeather Ore", (205, 225, 255), rough=0.15, glow=(170, 200, 255), glow_strength=2.2, rbx="Neon")

top = base_plinth(11.5, 11.5, BLACK, GOLD, STARM, C_BASE, c=1.2)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(20)
for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):
    dot(f"Corner Star {i + 1}", V(sx * 4.75, sy * 4.75, top + 0.15), 0.3, NEON, C_BASE)

def gear(name, C, axis, up, r, teeth, th, mat, coll, hub=None):
    tube(name, C, axis, up, r, r * 0.45, th, mat, coll, n=max(24, teeth * 2))
    a_ = axis.normalized();u = up.normalized();v = a_.cross(u).normalized()
    for k in range(teeth):
        ang = 2 * math.pi * k / teeth
        rr = math.cos(ang) * v + math.sin(ang) * u;tt = -math.sin(ang) * v + math.cos(ang) * u
        obox(f"{name} Tooth {k + 1}", C + rr * (r + 0.12), (th, 0.26, 0.3), a_, rr, tt, mat, coll)
    if hub:
        cyl(f"{name} Hub", C - a_ * th * 0.7, C + a_ * th * 0.7, r * 0.2, r * 0.2, hub, coll, n=12, hint=u)

# ---- orrery pedestal: stepped plinths, gear ring, column
PC = V(0, 0.9, top)
cyl("Plinth 1", PC, PC + V(0, 0, 0.8), 3.1, 2.9, NIGHT, C_ORRERY, n=32)
tube("Plinth Band", PC + V(0, 0, 0.65), Z_AX, Y_AX, 3.0, 2.6, 0.22, GOLD, C_ORRERY, n=32)
cyl("Plinth 2", PC + V(0, 0, 0.8), PC + V(0, 0, 1.8), 2.4, 2.1, NIGHT, C_ORRERY, n=32)
gear("Orrery Gear", PC + V(0, 0, 1.35), Z_AX, Y_AX, 3.0, 22, 0.3, GOLD, C_ORRERY)
MC = PC + V(0, 0, 8.2);MR = 3.6
cyl("Column", PC + V(0, 0, 1.8), MC + V(0, 0, -MR + 0.2), 0.95, 0.75, NIGHT, C_ORRERY, n=24)
for z in (2.8, 3.9):
    torus(f"Column Ring {z}", PC + V(0, 0, z), Z_AX, Y_AX, 0.92 - 0.04 * (z - 2.8), 0.12, GOLD, C_ORRERY, n_major=24, n_minor=6)
lathe("Column Cup", MC + V(0, 0, -MR - 0.6), [(0.75, 0), (1.25, 0.45), (1.3, 0.6), (0.9, 0.7)], GOLD, C_ORRERY, n=24)

# ---- crescent moon cradle (horns up)
D_ = 1.6
r2 = math.hypot(D_, MR)
outer = [MC + MR * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in range(180, 361, 12)]
a_tip = math.degrees(math.atan2(-D_, MR))
a_end = 180 - a_tip
inner = [MC + V(0, 0, D_) + r2 * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in [a_tip - (a_tip - (a_end - 360)) * k / 12 for k in range(1, 12)]]
blade("Crescent Moon", outer + inner, 0.8, MOON, C_ORRERY)
for s in (-1, 1):
    pts = [MC + MR * 1.0 * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in range(180, 361, 12)]
    path_tube(f"Crescent Rim {s}", [p + V(0, s * 0.42, 0) for p in pts], [0.08] * len(pts), GOLD, C_ORRERY, n=6)
    dot(f"Horn Star {s}", MC + V(s * MR, 0, 0.25), 0.22, NEON, C_ORRERY)
for k in range(5):                                          # craters on the moon face
    a = math.radians(200 + k * 35)
    p = MC + (MR - 0.45) * V(math.cos(a), 0, math.sin(a)) + V(0, -0.41, 0)
    cyl(f"Moon Crater {k + 1}", p + V(0, 0.03, 0), p + V(0, -0.02, 0), 0.18 - 0.02 * (k % 2), 0.13, ROCK, C_ORRERY, n=10, hint=Z_AX)
PERCH = MC.z - MR + (MR - (r2 - D_))

# ---- planets on curved gold arms round the column
for k, (ang, R, h, mat, pr) in enumerate(((210, 3.9, 3.2, PLR, 0.5), (330, 4.3, 4.3, PLT, 0.62), (90, 4.0, 5.4, PLP, 0.7))):
    a = math.radians(ang);d = V(math.cos(a), math.sin(a), 0)
    pts = [PC + V(0, 0, 2.2 + (h - 2.2) * t) + d * (0.9 + (R - 0.9) * math.sin(math.pi / 2 * t)) for t in [i / 5 for i in range(6)]]
    path_tube(f"Planet Arm {k + 1}", pts, [0.12] * 6, GOLD, C_ORRERY, n=8)
    P = pts[-1] + V(0, 0, pr + 0.1)
    sphere(f"Planet {k + 1}", P, pr, mat, C_ORRERY)
    if k == 1:
        torus("Planet Ring", P, V(0.3, 0.2, 1), Y_AX, pr * 1.7, 0.07, GOLD, C_ORRERY, n_major=24, n_minor=4)
    if k == 2:
        sphere("Little Moon", P + V(0.7, -0.6, 0.6), 0.2, MOON, C_ORRERY)

# ---- the owl
O = V(PC.x, PC.y, PERCH + 2.2)
lathe("Owl Body", O + V(0, 0, -2.2), [(0.6, 0), (1.5, 0.4), (1.95, 1.4), (2.0, 2.4), (1.7, 3.3), (1.2, 3.8)], NIGHT, C_OWL, n=20)
for k in range(5):                                          # gold star-plates on the belly
    z = -1.6 + k * 0.62
    for j in range(5):
        a = math.radians(-90 + (j - 2) * 22 + (11 if k % 2 else 0))
        r = 1.85 + 0.15 * math.sin(k)
        c = O + V(r * math.cos(a), r * math.sin(a) + 0.05, z)
        blade(f"Belly Plate {k + 1}-{j + 1}", [c + V(-0.28 * math.sin(a), 0.28 * math.cos(a), 0.25), c + V(0.28 * math.sin(a), -0.28 * math.cos(a), 0.25),
                                               c + V(0, 0, -0.35) + V(math.cos(a), math.sin(a), 0) * 0.12], 0.06, GOLD if (k + j) % 2 else PURPLE, C_OWL)
# chest window: a tiny solar system
CW = O + V(0, -1.97, 0.6)
torus("Chest Window Rim", CW, V(0, -1, 0), Z_AX, 0.85, 0.1, GOLD, C_OWL, n_major=24, n_minor=6)
cyl("Chest Window Back", CW + V(0, 0.12, 0), CW + V(0, 0.07, 0), 0.8, 0.8, BLACK, C_OWL, n=20, hint=Z_AX)
dot("Chest Sun", CW + V(0, -0.05, 0), 0.3, CORE, C_OWL)
torus("Chest Orbit", CW + V(0, -0.05, 0), V(0, -1, 0.35), Z_AX, 0.6, 0.03, GOLD, C_OWL, n_major=20, n_minor=4)
for k, (a, mat) in enumerate(((0.6, PLT), (3.6, PLR))):
    dot(f"Chest Planet {k + 1}", CW + V(0.6 * math.cos(a), -0.05 - 0.1 * math.sin(a), 0.6 * math.sin(a) * 0.95), 0.1, mat, C_OWL)
H = O + V(0, -0.15, 2.4)
lathe("Owl Head", H + V(0, 0, -0.9), [(1.25, 0), (1.75, 0.5), (1.85, 1.2), (1.55, 1.85), (0.9, 2.15), (0.0, 2.25)], NIGHT, C_OWL, n=20)
for side, lab in ((1, "L"), (-1, "R")):
    E = H + V(side * 0.78, -1.78, 0.42)
    torus(f"Eye Rim {lab}", E, V(side * 0.25, -1, 0).normalized(), Z_AX, 0.74, 0.15, GOLD, C_OWL, n_major=24, n_minor=6)
    torus(f"Eye Inner Rim {lab}", E + V(0, -0.05, 0), V(side * 0.25, -1, 0).normalized(), Z_AX, 0.4, 0.06, PURPLE, C_OWL, n_major=20, n_minor=4)
    cyl(f"Eye Lens {lab}", E + V(0, 0.3, 0), E + V(0, -0.06, 0), 0.66, 0.66, LENS, C_OWL, n=20, hint=Z_AX)
    dot(f"Pupil {lab}", E + V(0, -0.1, 0), 0.18, INK, C_OWL)
    for j in range(4):                                      # starburst ticks round each eye
        b = math.radians(45 + 90 * j)
        p = E + V(0.95 * math.cos(b), -0.05, 0.95 * math.sin(b))
        cone(f"Eye Ray {lab}{j}", p, p + V(0.3 * math.cos(b), 0, 0.3 * math.sin(b)), 0.08, GOLD, C_OWL, n=4)
    crystal(f"Ear Tuft {lab}", H + V(side * 1.1, -0.2, 1.3), V(side * 0.45, 0.2, 1), 1.7, 0.36, CRYSTAL, C_OWL, sides=4)
    gear(f"Ear Gear {lab}", H + V(side * 1.8, 0.1, 0.6), V(side, 0, 0), Z_AX, 0.42, 9, 0.14, GOLD, C_OWL, hub=PURPLE)
cone("Beak", H + V(0, -1.75, -0.2), H + V(0, -2.3, -0.85), 0.34, GOLD, C_OWL, n=6)
dot("Brow Star", H + V(0, -1.6, 1.05), 0.2, NEON, C_OWL)
for side in (1, -1):                                        # talons gripping the moon
    for j in range(3):
        a = math.radians(-90 + (j - 1) * 30)
        base = V(O.x + side * 0.8 + 0.15 * math.cos(a), O.y, PERCH + 0.35)
        path_tube(f"Talon {side}-{j + 1}", [base, base + V(0.2 * math.cos(a), 0.4 * math.sin(a), -0.05), base + V(0.25 * math.cos(a), 0.45 * math.sin(a), -0.5)], [0.12, 0.1, 0.03], GOLD, C_OWL, n=6)
# halo of stars above the head
HH = H + V(0, 0.1, 2.75)
torus("Star Halo", HH, V(0, -0.25, 1), Y_AX, 1.1, 0.05, GOLD, C_OWL, n_major=28, n_minor=4)
for k in range(5):
    a = 2 * math.pi * k / 5
    p = HH + V(1.1 * math.cos(a), 1.1 * math.sin(a) * 0.97, -0.27 * math.sin(a))
    crystal(f"Halo Star {k + 1}a", p, Z_AX, 0.28, 0.12, NEON, C_OWL, sides=4)
    crystal(f"Halo Star {k + 1}b", p, -Z_AX, 0.28, 0.12, NEON, C_OWL, sides=4)
# wind-up key on the back (with a star bow)
K = O + V(0, 1.9, 0.6)
cyl("Key Shaft", K, K + V(0, 1.3, 0), 0.16, 0.16, GOLD, C_OWL, n=10, hint=Z_AX)
for side in (1, -1):
    torus(f"Key Bow {side}", K + V(side * 0.6, 1.45, 0), Y_AX, Z_AX, 0.5, 0.14, GOLD, C_OWL, n_major=18, n_minor=6)

# ---- star-feather wings
for side, lab in ((1, "L"), (-1, "R")):
    sh = O + V(side * 1.7, 0.85, 1.0)
    elbow = sh + V(side * 2.4, 1.0, 1.1)
    tip = elbow + V(side * 2.6, 1.0, -0.6)
    cyl(f"Wing Bone {lab} 1", sh, elbow, 0.2, 0.16, GOLD, C_WINGS, n=8)
    cyl(f"Wing Bone {lab} 2", elbow, tip, 0.16, 0.08, GOLD, C_WINGS, n=8)
    gear(f"Wing Gear {lab}", sh, V(side, 0.2, 0).normalized(), Z_AX, 0.45, 10, 0.16, PURPLE, C_WINGS, hub=GOLD)
    dot(f"Elbow Star {lab}", elbow, 0.3, NEON, C_WINGS)
    for k in range(9):
        t = k / 8
        root = sh + (elbow - sh) * min(1, t * 2) + (tip - elbow) * max(0, t * 2 - 1)
        L = 1.6 + 1.6 * math.sin(math.pi * t) + 0.6 * t
        d = V(side * 0.35 * t, 0.3, -1).normalized()
        w = 0.32
        u = V(side, 0.4, 0).normalized()
        blade(f"Feather {lab} {k + 1}", [root - u * w, root + u * w, root + d * L + u * w * 0.4, root + d * (L + 0.35), root + d * L - u * w * 0.4],
              0.06, NIGHT if k % 2 else PURPLE, C_WINGS)
        cone(f"Feather Tip {lab} {k + 1}", root + d * (L - 0.05), root + d * (L + 0.42), 0.14, GOLD, C_WINGS, n=4)
        dot(f"Feather Star {lab} {k + 1}", root + d * (L * 0.55) + V(0, -0.06, 0), 0.07 + 0.03 * (k % 3 == 0), NEON, C_WINGS)

# ---- stardust stream from the chest window into a funnel, spout drops the ore
F0 = V(PC.x, PC.y - 2.75, PERCH - 0.9)
for k in range(5):
    dot(f"Stardust {k + 1}", CW + V(0, -0.3 - 0.11 * k, -0.6 - 0.48 * k), 0.13 - 0.012 * k, NEON, C_DETAIL)
cyl("Funnel Cup", F0, F0 + V(0, 0, -1.1), 0.9, 0.35, NIGHT, C_DETAIL, n=20)
torus("Funnel Rim", F0, Z_AX, Y_AX, 0.9, 0.08, GOLD, C_DETAIL, n_major=24, n_minor=5)
beam("Funnel Bracket", F0 + V(0, 0.75, -0.4), V(PC.x, PC.y - 0.45, PERCH - 0.9), 0.18, 0.18, X_AX, GOLD, C_DETAIL)
pipe = [F0 + V(0, 0, -1.1), F0 + V(0, -0.4, -2.0), F0 + V(0, -1.3, -2.5)]
for i in range(2):
    cyl(f"Spout Pipe {i + 1}", pipe[i], pipe[i + 1], 0.35, 0.35, NIGHT, C_DETAIL, n=16)
dot("Spout Elbow", pipe[1], 0.35, NIGHT, C_DETAIL)
SP = pipe[-1]
tube("Spout Collar", SP, V(0, -1, 0), Z_AX, 0.55, 0.3, 0.3, GOLD, C_DETAIL, n=20)
torus("Spout Glow", SP + V(0, -0.17, 0), V(0, -1, 0), Z_AX, 0.43, 0.06, NEON, C_DETAIL, n_major=20, n_minor=5)
ore_cube(SP + V(0, -0.85, -0.75), ORE, C_DETAIL, size=0.8)

# ---- telescope, gears, meteor crystals, lamps
TB = V(3.9, -3.2, top)
for k, (dx, dy) in enumerate(((0.5, 0.4), (-0.5, 0.4), (0, -0.6))):
    beam(f"Tripod Leg {k + 1}", TB + V(dx, dy, 0), TB + V(0, 0, 2.4), 0.11, 0.11, Z_AX, GOLD, C_DETAIL)
tdir = V(-0.35, 0.3, 0.88).normalized()
TP = TB + V(0, 0, 2.4)
cyl("Telescope Tube", TP - tdir * 1.1, TP + tdir * 1.5, 0.28, 0.38, NIGHT, C_DETAIL, n=16)
tube("Telescope Band", TP, tdir, perp_basis(tdir)[0], 0.36, 0.27, 0.22, GOLD, C_DETAIL, n=16)
cyl("Telescope Lens", TP + tdir * 1.5, TP + tdir * 1.56, 0.34, 0.34, LENS, C_DETAIL, n=16)
gear("Floor Gear", V(-3.7, -3.4, top + 0.12), Z_AX, Y_AX, 0.95, 13, 0.2, GOLD, C_DETAIL, hub=PURPLE)
gear("Floor Gear Small", V(-2.3, -4.3, top + 0.12), Z_AX, Y_AX, 0.5, 8, 0.2, PURPLE, C_DETAIL, hub=GOLD)
for i, (c, n_, sz) in enumerate(((V(-3.9, 3.6, top), 4, 0.8), (V(3.9, 3.7, top), 3, 0.7))):
    rock(f"Meteor {i + 1}", c, (sz * 1.1, sz * 0.9, sz * 0.6), ROCK, C_DETAIL)
    for k in range(n_):
        a = rnd.uniform(0, 2 * math.pi)
        crystal(f"Starglass {i + 1}-{k + 1}", c + V(math.cos(a), math.sin(a), 0) * sz * 0.4, V(math.cos(a) * 0.5, math.sin(a) * 0.5, 1),
                sz * rnd.uniform(1.6, 2.5), sz * rnd.uniform(0.32, 0.45), CRYSTAL, C_DETAIL)
for k, (x, y) in enumerate(((-4.5, 0.6), (4.5, 0.6))):
    post_lantern(f"Star Lamp {k + 1}", V(x, y, top), 2.2, NIGHT, NEON, GOLD, C_DETAIL, r=0.3)
for k in range(5):                                          # floating rune stones
    a = 2 * math.pi * k / 5 + 0.5
    c = PC + V(3.4 * math.cos(a), 3.4 * math.sin(a), 2.6 + 0.4 * math.sin(3 * a))
    rr = Euler((0.6, 0.3, a)).to_matrix()
    obox(f"Rune Stone {k + 1}", c, (0.3, 0.22, 0.45), rr @ X_AX, rr @ Y_AX, rr @ Z_AX, CRYSTAL, C_DETAIL)

finish_mine(bg=(0.008, 0.008, 0.03), tint=(0.8, 0.82, 1.0))
