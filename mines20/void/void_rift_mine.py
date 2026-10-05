"""Void Rift Mine - two obsidian monoliths hold open a swirling purple rift watched by an eldritch eye;
tentacles creep from its rim and void ore spills out. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_GATE, C_RIFT, C_HORROR, C_DETAIL = begin("VoidRiftMine", ["Base", "Monoliths", "Rift", "Horror", "Details"], seed=55)
OBS = M("Obsidian", (22, 16, 32), rough=0.15, rbx="Basalt", noise=((14, 10, 22), (44, 32, 62), 2.4, 0.4))
BLACK = M("Black", (8, 6, 12), rough=0.4)
TRIM = M("Void Trim (Metal)", (190, 70, 255), rough=0.3, metal=0.4, glow=(170, 50, 255), glow_strength=1.2, rbx="Neon")
VM = M("Void Marble (Marble)", (16, 10, 24), rough=0.2, marble=((12, 8, 20), (230, 80, 255)))
RUNE = M("Rune Glow", (230, 140, 255), rough=0.3, glow=(200, 80, 255), glow_strength=6.0, rbx="Neon", light=(8, 1.0))
SWIRL = M("Rift Swirl", (200, 90, 255), rough=0.3, glow=(170, 50, 255), glow_strength=9.0, rbx="Neon", light=(20, 2.4))
SWIRL2 = M("Rift Swirl Pink", (255, 120, 220), rough=0.3, glow=(255, 70, 200), glow_strength=7.0, rbx="Neon")
CORE = M("Void Core", (6, 2, 12), rough=0.2, rbx="SmoothPlastic")
EYEW = M("Eye White", (230, 240, 200), rough=0.3, glow=(200, 255, 140), glow_strength=2.0, rbx="Neon", light=(9, 1.2))
PUPIL = M("Pupil", (10, 0, 10), rough=0.3)
FLESH = M("Tentacle Flesh", (70, 30, 90), rough=0.5, noise=((50, 20, 66), (110, 50, 130), 4.0, 0.3))
SHARD = M("Void Shard", (120, 50, 220), rough=0.1, glow=(110, 40, 230), glow_strength=1.6, rbx="Glass", alpha=0.1, light=(6, 0.6))
IRON = M("Chain Iron (Metal)", (60, 58, 70), rough=0.4, metal=0.9)
ORE = M("Void Ore", (210, 130, 255), rough=0.15, glow=(180, 80, 255), glow_strength=2.4, rbx="Neon")

top = base_plinth(11.0, 10.5, BLACK, TRIM, VM, C_BASE, c=1.4)
R0 = V(0, 0.4, top)
torus("Rune Circle", R0 + V(0, 0, 0.05), V(0, 0, 1), V(0, 1, 0), 4.2, 0.09, RUNE, C_BASE, n_major=48, n_minor=4)
torus("Rune Circle Inner", R0 + V(0, 0, 0.05), V(0, 0, 1), V(0, 1, 0), 3.5, 0.06, RUNE, C_BASE, n_major=48, n_minor=4)
for k in range(12):
    a = 2 * math.pi * k / 12
    c = R0 + V(3.85 * math.cos(a), 3.85 * math.sin(a), 0.06)
    obox(f"Floor Rune {k + 1}", c, (0.42, 0.14, 0.06), V(-math.sin(a), math.cos(a), 0), V(math.cos(a), math.sin(a), 0), V(0, 0, 1), RUNE, C_BASE)

# ---- jagged obsidian monoliths
for side, lab in ((1, "L"), (-1, "R")):
    B = V(side * 4.0, 0.8, top)
    pts = [B + V(-0.9, -0.8, 0), B + V(0.9, -0.8, 0), B + V(0.9, 0.8, 0), B + V(-0.9, 0.8, 0),
           B + V(-0.5 + side * 0.4, -0.5, 9.8), B + V(0.5 + side * 0.4, -0.45, 10.4), B + V(0.5 + side * 0.4, 0.5, 9.6), B + V(-0.5 + side * 0.4, 0.45, 10.1)]
    hexa(f"Monolith {lab}", pts, OBS, C_GATE)
    hexa(f"Monolith Tip {lab}", [pts[4], pts[5], pts[6], pts[7], B + V(side * 0.6 - 0.05, -0.05, 11.8), B + V(side * 0.6 + 0.05, -0.05, 11.9), B + V(side * 0.6 + 0.05, 0.05, 11.8), B + V(side * 0.6 - 0.05, 0.05, 11.85)], OBS, C_GATE)
    for k in range(5):                                       # glowing runes down the inner face
        z = 1.5 + k * 1.7
        x = B.x - side * (0.86 - 0.04 * z / 1.7) 
        obox(f"Monolith Rune {lab} {k + 1}", V(x - side * 0.02, B.y - 0.2, top + z), (0.06, 0.55, 0.9), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), RUNE, C_GATE)
    for k in range(3):                                       # shards jutting out
        a = random.uniform(0, 2 * math.pi)
        crystal(f"Monolith Shard {lab} {k + 1}", B + V(side * 0.6, random.uniform(-0.5, 0.5), 2 + k * 2.8), V(side, math.cos(a) * 0.4, 0.5), 1.2, 0.3, SHARD, C_GATE, sides=4)
    rock_f(f"Monolith Rubble {lab}", B + V(side * 1.1, -1.2, 0.3), (0.8, 0.6, 0.5), OBS, C_GATE)

# ---- the rift: obsidian ring, glowing rings, swirl arms, black core
RC = V(0, 0.6, top + 5.6)
A = V(0, -1, 0)
torus("Rift Frame", RC, A, V(0, 0, 1), 3.0, 0.5, OBS, C_RIFT, n_major=48, n_minor=10)
torus("Rift Glow Outer", RC + V(0, -0.15, 0), A, V(0, 0, 1), 2.55, 0.18, SWIRL, C_RIFT, n_major=48, n_minor=8)
for k in range(10):                                         # frame spikes
    a = 2 * math.pi * k / 10 + 0.15
    d = V(math.cos(a), 0, math.sin(a))
    cone(f"Frame Spike {k + 1}", RC + d * 3.3, RC + d * (4.0 + 0.4 * (k % 2)), 0.28, OBS, C_RIFT, n=5)
cyl("Void Core", RC + V(0, 0.15, 0), RC + V(0, -0.05, 0), 2.45, 2.45, CORE, C_RIFT, n=40, hint=V(0, 0, 1))
for arm in range(5):                                        # spiral arms
    pts = []
    for i in range(14):
        t = i / 13
        ang = arm * 2 * math.pi / 5 + t * 3.3
        r = 0.25 + 2.2 * t
        pts.append(RC + V(r * math.cos(ang), -0.12 - 0.05 * t, r * math.sin(ang)))
    path_tube(f"Swirl Arm {arm + 1}", pts, [0.06 + 0.16 * math.sin(math.pi * (i / 13)) for i in range(14)], SWIRL if arm % 2 else SWIRL2, C_RIFT, n=6)
dot("Rift Heart", RC + V(0, -0.2, 0), 0.35, SWIRL2, C_RIFT)
for side in (1, -1):                                        # braces from monoliths to the ring
    beam(f"Rift Brace {side}", V(side * 3.5, 0.6, top + 5.6), RC + V(side * 3.1, 0, 0), 0.5, 0.4, V(0, 1, 0), OBS, C_RIFT)
    for k in range(4):                                      # chain links
        p = V(side * (3.8 - k * 0.0), 0.6, top + 9.0 - k * 0.55)
        torus(f"Chain {side}-{k + 1}", V(side * (3.6 - 0.3 * k), 0.6, top + 9.3 - 0.75 * k), V(1, 0, 0) if k % 2 else V(0, 1, 0), V(0, 0, 1), 0.28, 0.07, IRON, C_DETAIL, n_major=12, n_minor=4)

# ---- eldritch eye above the rift, tentacles from the rim
EY = RC + V(0, -0.2, 3.9)
lathe("Eye Socket", EY + V(0, 0.3, -1.0), [(0.0, 0), (1.1, 0.3), (1.25, 1.0), (1.1, 1.7), (0.0, 2.0)], FLESH, C_HORROR, n=18)
sphere("Eye", EY + V(0, -0.45, 0), 0.85, EYEW, C_HORROR)
abox("Eye Slit", -0.13, 0.13, EY.y - 1.32, EY.y - 1.22, EY.z - 0.6, EY.z + 0.6, PUPIL, C_HORROR)
for k, (ang, ln) in enumerate(((200, 3.0), (235, 3.6), (300, 3.2), (330, 2.6), (160, 2.8))):
    a = math.radians(ang)
    base = RC + V(2.6 * math.cos(a), -0.3, 2.6 * math.sin(a))
    out = V(math.cos(a), -0.6, math.sin(a)).normalized()
    pts = [base]
    for i in range(1, 10):
        t = i / 9
        pts.append(base + out * ln * t + V(0.6 * math.sin(t * 5 + k), -0.4 * t, -1.2 * t * t))
    path_tube(f"Tentacle {k + 1}", pts, [0.32 * (1 - 0.85 * i / 9) + 0.03 for i in range(10)], FLESH, C_HORROR, n=8)
    for i in range(2, 9, 2):
        dot(f"Tentacle Glow {k + 1}-{i}", pts[i] + V(0, -0.1, 0.0), 0.08, SWIRL2, C_HORROR)

# ---- ore spills from the rift down a void-stone ramp
hexa("Spill Ramp", [V(-0.9, RC.y - 0.5, top + 2.55), V(0.9, RC.y - 0.5, top + 2.55), V(0.9, RC.y - 3.6, top + 0.02), V(-0.9, RC.y - 3.6, top + 0.02),
                    V(-0.9, RC.y - 0.5, top + 2.85), V(0.9, RC.y - 0.5, top + 2.85), V(0.9, RC.y - 3.6, top + 0.3), V(-0.9, RC.y - 3.6, top + 0.3)], OBS, C_DETAIL)
beam("Spill Glow", V(0, RC.y - 0.6, top + 2.9), V(0, RC.y - 3.5, top + 0.35), 0.5, 0.05, V(0, 0, 1), SWIRL, C_DETAIL)
ore_cube(V(0, RC.y - 4.3, top + 0.8), ORE, C_DETAIL)
# floating shards around
rnd = random.Random(8)
for k in range(9):
    a = rnd.uniform(0, 2 * math.pi);r = rnd.uniform(3.6, 5.2)
    c = V(r * math.cos(a), 0.6 + r * math.sin(a) * 0.7, top + rnd.uniform(2.0, 10.5))
    crystal(f"Floating Shard {k + 1}", c, V(rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), 1), rnd.uniform(0.8, 1.6), rnd.uniform(0.2, 0.35), SHARD, C_DETAIL, sides=4)
for k, (x, y) in enumerate(((-4.4, -4.0), (4.4, -4.0))):    # rune braziers
    lathe(f"Brazier {k + 1}", V(x, y, top), [(0.5, 0), (0.3, 0.9), (0.55, 1.2), (0.6, 1.4)], OBS, C_DETAIL, n=10, smooth=False)
    lathe(f"Brazier Flame {k + 1}", V(x, y, top + 1.35), [(0.45, 0), (0.3, 0.45), (0.0, 1.0)], SWIRL2, C_DETAIL, n=8)

finish_mine(bg=(0.012, 0.004, 0.02), tint=(0.85, 0.6, 1.0))
