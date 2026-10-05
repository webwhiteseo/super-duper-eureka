"""Magma Golem Forge - a lava-cracked rock golem kneels on a basalt plinth and pours molten ore from a crucible.
Built with mine_kit (same pipeline as the other Ore Factory mines)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_BODY, C_ARMS, C_FORGE, C_DETAIL = begin("MagmaGolemForge", ["Base", "Body", "Arms", "Forge", "Details"], seed=4)
BASALT = M("Basalt (Slate)", (58, 50, 48), rough=0.95, rbx="Basalt", noise=((36, 30, 30), (86, 76, 70), 2.6, 0.6))
OBSID = M("Cooled Lava (Marble)", (22, 14, 12), rough=0.3, rbx="CrackedLava", marble=((18, 10, 8), (255, 110, 30)))
LAVA = M("Lava Glow", (255, 120, 40), rough=0.5, glow=(255, 100, 20), glow_strength=9, light=(10, 1.2))
CORE = M("Magma Core", (255, 190, 90), rough=0.4, glow=(255, 150, 40), glow_strength=14, light=(18, 2.5))
TRIM = M("Ember Trim (Metal)", (255, 96, 30), rough=0.35, metal=0.5, glow=(255, 80, 20), glow_strength=0.8, rbx="Neon")
BLACK = M("Black", (16, 12, 12), rough=0.45)
IRON = M("Forge Iron (Metal)", (64, 62, 68), rough=0.35, metal=0.9, plate=10.0)
GOLD = M("Brass (Metal)", (205, 150, 60), rough=0.3, metal=1.0)
FIREC = M("Fire Crystal", (255, 150, 60), rough=0.12, glow=(255, 110, 30), glow_strength=1.6, rbx="Glass", alpha=0.1, light=(7, 0.6))
WOOD = M("Charred Wood", (60, 36, 24), rough=0.85, rbx="Wood")
ORE = M("Ember Ore", (255, 160, 90), rough=0.2, glow=(255, 120, 50), glow_strength=2.0, rbx="Neon")

top = base_plinth(10.5, 10.5, BLACK, TRIM, OBSID, C_BASE, c=1.6)
for i, (x, y) in enumerate(((4.3, 4.3), (-4.3, 4.3), (4.3, -4.3), (-4.3, -4.3))):
    rock_f(f"Corner Boulder {i + 1}", V(x, y, top + 0.2), (0.9, 0.85, 0.6), BASALT, C_BASE)

# ---- body: kneeling legs, hips, chest with a glowing magma heart, head with burning eyes
G = V(0, 1.4, 0)
for side, lab in ((1, "L"), (-1, "R")):
    rock_f(f"Thigh {lab}", G + V(side * 1.9, -0.6, top + 1.6), (1.3, 1.9, 1.2), BASALT, C_BODY)
    rock_f(f"Shin {lab}", G + V(side * 2.0, 1.4, top + 0.7), (1.2, 1.9, 0.8), BASALT, C_BODY)
    rock_f(f"Foot {lab}", G + V(side * 2.0, 3.0, top + 0.4), (1.0, 0.9, 0.5), BASALT, C_BODY)
    torus(f"Knee Joint {lab}", G + V(side * 2.0, -1.4, top + 1.3), V(1, 0, 0), V(0, 0, 1), 0.85, 0.16, LAVA, C_BODY, n_major=20, n_minor=6)
rock_f("Hips", G + V(0, 0, top + 2.6), (2.6, 1.8, 1.2), BASALT, C_BODY)
rock_f("Belly", G + V(0, -0.2, top + 4.0), (2.4, 1.7, 1.3), BASALT, C_BODY)
rock_f("Chest", G + V(0, -0.4, top + 6.3), (3.4, 2.3, 2.0), BASALT, C_BODY)
sphere("Magma Heart", G + V(0, -2.2, top + 6.2), 1.05, CORE, C_BODY)
torus("Heart Ring", G + V(0, -2.35, top + 6.2), V(0, -1, 0), V(0, 0, 1), 1.2, 0.14, LAVA, C_BODY, n_major=24, n_minor=6)
for k in range(6):                                         # cracks radiating from the heart
    a = math.radians(30 + 60 * k)
    p0 = G + V(1.2 * math.cos(a), -2.25, top + 6.2 + 1.2 * math.sin(a))
    p1 = G + V(2.4 * math.cos(a + 0.2), -1.9, top + 6.2 + 2.0 * math.sin(a + 0.2))
    beam(f"Lava Crack {k + 1}", p0, p1, 0.16, 0.1, V(0, -1, 0), LAVA, C_BODY)
for side, lab in ((1, "L"), (-1, "R")):
    rock_f(f"Shoulder {lab}", G + V(side * 3.6, -0.2, top + 7.3), (1.6, 1.5, 1.4), BASALT, C_BODY)
    torus(f"Shoulder Joint {lab}", G + V(side * 3.3, -0.2, top + 6.5), V(side, 0, 0.2), V(0, 1, 0), 1.0, 0.15, LAVA, C_BODY, n_major=20, n_minor=6)
    for k in range(3):                                     # shoulder spikes of cooled lava
        cone(f"Shoulder Spike {lab} {k + 1}", G + V(side * (3.4 + 0.5 * k), -0.4 + 0.5 * k, top + 8.3),
             G + V(side * (3.9 + 0.8 * k), -0.2 + 0.6 * k, top + 10.0 - 0.3 * k), 0.38, BASALT, C_BODY, n=6)
rock_f("Neck", G + V(0, -0.6, top + 8.4), (1.1, 1.0, 0.6), BASALT, C_BODY)
rock_f("Head", G + V(0, -1.1, top + 9.6), (1.45, 1.3, 1.2), BASALT, C_BODY)
rock_f("Brow", G + V(0, -2.0, top + 10.2), (1.3, 0.5, 0.35), BASALT, C_BODY)
for side, lab in ((1, "L"), (-1, "R")):
    sphere(f"Eye {lab}", G + V(side * 0.55, -2.25, top + 9.7), 0.22, CORE, C_BODY)
    cone(f"Horn {lab}", G + V(side * 0.9, -1.1, top + 10.5), G + V(side * 1.7, -0.4, top + 12.0), 0.35, BASALT, C_BODY, n=6)
beam("Mouth Glow", G + V(-0.45, -2.35, top + 9.0), G + V(0.45, -2.35, top + 9.0), 0.12, 0.12, V(0, -1, 0), LAVA, C_BODY)

# ---- arms reaching forward, hands gripping a tilted crucible
CR = V(0, -3.6, top + 5.4)                                 # crucible centre
for side, lab in ((1, "L"), (-1, "R")):
    elbow = G + V(side * 3.9, -2.6, top + 5.0)
    rock_f(f"Upper Arm {lab}", (G + V(side * 3.6, -0.2, top + 6.6) + elbow) / 2, (1.0, 1.3, 1.0), BASALT, C_ARMS)
    torus(f"Elbow Joint {lab}", elbow, V(0, -1, 0.3), V(0, 0, 1), 0.75, 0.14, LAVA, C_ARMS, n_major=20, n_minor=6)
    hand = CR + V(side * 2.0, 0, 0.1)
    rock_f(f"Forearm {lab}", (elbow + hand) / 2, (0.9, 1.2, 0.85), BASALT, C_ARMS)
    rock_f(f"Hand {lab}", hand, (0.75, 0.8, 0.7), BASALT, C_ARMS)
lathe("Crucible", CR - V(0, 0, 1.1), [(0.9, 0), (1.35, 0.4), (1.55, 1.3), (1.6, 2.0), (1.45, 2.05)], IRON, C_FORGE, n=24)
lathe("Crucible Melt", CR + V(0, 0, 0.75), [(1.45, 0), (1.45, 0.08)], LAVA, C_FORGE, n=24)
for side in (1, -1):
    cyl(f"Crucible Handle {side}", CR + V(side * 1.6, 0, 0.5), CR + V(side * 2.1, 0, 0.3), 0.18, 0.18, IRON, C_FORGE, n=8)
lip = CR + V(0, -1.55, 0.85)
cyl("Pour Spout", CR + V(0, -1.3, 0.75), lip, 0.35, 0.25, IRON, C_FORGE, n=10)
path_tube("Molten Stream", [lip, lip + V(0, -0.5, -0.8), lip + V(0, -0.7, -2.0), lip + V(0, -0.75, -3.2)], [0.22, 0.2, 0.18, 0.16], LAVA, C_FORGE, n=8)
ore_cube(lip + V(0, -0.8, -4.1), ORE, C_FORGE)

# ---- glowing lava cracks over the body, lava pool where the ore lands
rnd = random.Random(9)
for k, (c, sc) in enumerate(((G + V(0, -0.4, top + 6.3), (3.4, 2.3, 2.0)), (G + V(0, 0, top + 2.6), (2.6, 1.8, 1.2)),
                             (G + V(1.9, -0.6, top + 1.6), (1.3, 1.9, 1.2)), (G + V(-1.9, -0.6, top + 1.6), (1.3, 1.9, 1.2)),
                             (G + V(3.6, -0.2, top + 7.3), (1.6, 1.5, 1.4)), (G + V(-3.6, -0.2, top + 7.3), (1.6, 1.5, 1.4)))):
    for j in range(2):
        a = rnd.uniform(-2.6, -0.5);b = rnd.uniform(-0.5, 0.5)  # front-facing side
        d = V(math.cos(a) * math.cos(b), math.sin(a) * math.cos(b) - 0.4, math.sin(b)).normalized()
        p0 = c + V(d.x * sc[0], d.y * sc[1], d.z * sc[2]) * 0.8
        t = d.cross(V(0, 0, 1)).normalized() if abs(d.z) < 0.9 else V(1, 0, 0)
        p1 = p0 + (t * rnd.uniform(0.5, 0.9) + V(0, 0, rnd.uniform(-0.4, 0.4)))
        p0 -= d * 0.1; p1 -= d * 0.25
        beam(f"Body Crack {k + 1}-{j + 1}", p0, p1, 0.16, 0.5, d, LAVA, C_BODY)
pool = lip + V(0, -0.8, 0) ;pool.z = top
lathe("Lava Pool Rim", pool, [(1.25, 0), (1.25, 0.18), (0.95, 0.22)], BASALT, C_FORGE, n=16, smooth=False)
lathe("Lava Pool", pool + V(0, 0, 0.12), [(0.98, 0), (0.98, 0.04)], LAVA, C_FORGE, n=16)

# ---- forge details: anvil, hammer, volcanic vents, fire crystals, bellows
A0 = V(3.3, -3.6, top)
abox("Anvil Foot", A0.x - 0.8, A0.x + 0.8, A0.y - 0.6, A0.y + 0.6, top, top + 0.5, IRON, C_DETAIL)
abox("Anvil Waist", A0.x - 0.45, A0.x + 0.45, A0.y - 0.35, A0.y + 0.35, top + 0.5, top + 1.3, IRON, C_DETAIL)
abox("Anvil Face", A0.x - 1.3, A0.x + 1.0, A0.y - 0.55, A0.y + 0.55, top + 1.3, top + 1.85, IRON, C_DETAIL)
cone("Anvil Horn", V(A0.x + 1.0, A0.y, top + 1.6), V(A0.x + 2.2, A0.y, top + 1.75), 0.32, IRON, C_DETAIL, n=8)
abox("Hot Ingot", A0.x - 0.6, A0.x + 0.2, A0.y - 0.25, A0.y + 0.25, top + 1.85, top + 2.1, LAVA, C_DETAIL)
cyl("Hammer Handle", V(A0.x - 0.9, A0.y + 0.9, top), V(A0.x - 0.4, A0.y + 0.5, top + 2.4), 0.12, 0.12, WOOD, C_DETAIL, n=6)
abox("Hammer Head", A0.x - 0.75, A0.x - 0.05, A0.y + 0.25, A0.y + 0.75, top + 2.3, top + 2.8, IRON, C_DETAIL)
for i, (x, y, h) in enumerate(((-3.6, 3.4, 2.6), (3.4, 3.6, 2.0), (-1.8, 4.2, 1.6))):
    lathe(f"Vent {i + 1}", V(x, y, top), [(1.0, 0), (0.8, h * 0.6), (0.45, h), (0.38, h)], BASALT, C_DETAIL, n=10, smooth=False)
    lathe(f"Vent Glow {i + 1}", V(x, y, top + h - 0.05), [(0.38, 0), (0.3, 0.2), (0.0, 0.25)], LAVA, C_DETAIL, n=10)
crystal_cluster("Fire Crystals L", V(-3.8, -3.4, top + 0.1), 4, 0.85, FIREC, BASALT, C_DETAIL, seed=3)
crystal_cluster("Fire Crystals B", V(0.4, 4.3, top + 0.1), 3, 0.7, FIREC, BASALT, C_DETAIL, seed=5)
# bellows on the left
B0 = V(-3.9, 0.4, top + 1.3)
lathe("Bellows Bag", B0, [(0.2, -0.9), (1.0, -0.6), (1.15, 0), (1.0, 0.6), (0.2, 0.9)], WOOD, C_DETAIL, n=12)
for k, z in enumerate((-0.35, 0.0, 0.35)):
    torus(f"Bellows Rib {k + 1}", B0 + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 1.08 - 0.15 * abs(k - 1), 0.07, GOLD, C_DETAIL, n_major=16, n_minor=4)
cyl("Bellows Nozzle", B0 + V(0.6, -0.4, 0), B0 + V(2.1, -1.4, 0.2), 0.2, 0.12, GOLD, C_DETAIL, n=8)

finish_mine(bg=(0.03, 0.012, 0.01), tint=(1.0, 0.72, 0.55))
