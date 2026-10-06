"""Tesla Cage Furnace - a concrete pad with a hazard ring; the ramp carries ore into a caged plasma pit zapped by two
tall tesla towers with lightning arcs. Control box, cables, warning lights. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_CAGE, C_TOWER, C_DETAIL = begin("TeslaCageFurnace", ["Pad", "Cage", "Towers", "Details"], seed=141)
CONC = M("Concrete", (150, 150, 146), rough=0.9, rbx="Concrete", noise=((124, 124, 120), (172, 172, 168), 4.0, 0.3))
HAZ = M("Hazard Yellow", (240, 196, 20), rough=0.45)
BLACK = M("Black", (16, 16, 20), rough=0.5)
STEEL = M("Steel (Metal)", (130, 136, 146), rough=0.3, metal=0.9, rbx="Metal")
COPPER = M("Copper Coil (Metal)", (200, 110, 60), rough=0.3, metal=1.0, rbx="Metal")
PLASMA = M("Plasma Pool", (150, 200, 255), rough=0.05, glow=(110, 170, 255), glow_strength=4.0, rbx="Neon", light=(16, 2.2))
BOLT = M("Lightning", (220, 230, 255), rough=0.3, glow=(170, 200, 255), glow_strength=7.0, rbx="Neon", light=(10, 1.4))
WARN = M("Warning Light", (255, 60, 40), rough=0.3, glow=(255, 30, 20), glow_strength=5.0, rbx="Neon", light=(6, 1.0))
CONVM = M("Conveyor", (40, 42, 48), rough=0.5, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (150, 200, 255), rough=0.2, glow=(110, 170, 255), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(141)
lathe("Concrete Pad", V(0, 0.8, 0), [(7.0, 0), (7.0, 0.5), (0.01, 0.5)], CONC, C_BASE, n=32, smooth=False)
for k in range(24):
    a0 = 2 * math.pi * k / 24;a1 = a0 + 2 * math.pi / 24
    p = [V(r * math.cos(a), 0.8 + r * math.sin(a), 0.5) for r, a in ((6.2, a0), (6.8, a0), (6.8, a1), (6.2, a1))]
    hexa(f"Hazard Ring {k}", p + [q + V(0, 0, 0.04) for q in p], HAZ if k % 2 else BLACK, C_BASE)
conveyor_ramp(CONVM, HAZ, STEEL, HAZ, y_end=-2.8, coll=C_BASE)
abox("Pit Base", -2.8, 2.8, -2.8, 2.6, 0.0, 1.1, STEEL, C_CAGE)
abox("Plasma Pool", -2.5, 2.5, -2.7, 2.3, 1.0, 1.2, PLASMA, C_CAGE)
burn_zone(BURN, -2.4, 2.4, -2.7, 2.3, 1.2, 2.0, C_CAGE)
for x in (-2.7, -1.35, 0.0, 1.35, 2.7):                    # cage bars (top + back, front open)
    beam(f"Cage Arch {x}", V(x, -2.7, 4.6), V(x, 2.5, 4.6), 0.14, 0.14, Z_AX, STEEL, C_CAGE)
for y in (-2.7, -0.9, 0.9, 2.5):
    for s in (-1, 1):
        beam(f"Cage Post {y}{s}", V(s * 2.7, y, 1.1), V(s * 2.7, y, 4.6), 0.16, 0.16, X_AX, STEEL, C_CAGE)
    beam(f"Cage Top {y}", V(-2.7, y, 4.6), V(2.7, y, 4.6), 0.14, 0.14, Z_AX, STEEL, C_CAGE)
for x in (-1.8, -0.6, 0.6, 1.8):
    beam(f"Cage Back {x}", V(x, 2.5, 1.1), V(x, 2.5, 4.6), 0.1, 0.1, Y_AX, STEEL, C_CAGE)
# tesla towers
for s in (-1, 1):
    T = V(s * 4.6, 1.4, 0.5)
    lathe(f"Tower Base {s}", T, [(1.2, 0), (1.2, 0.8), (0.6, 1.0)], CONC, C_TOWER, n=12, smooth=False)
    cyl(f"Tower Column {s}", T + V(0, 0, 1.0), T + V(0, 0, 6.4), 0.45, 0.35, BLACK, C_TOWER, n=12)
    for k in range(12):
        torus(f"Coil {s}{k}", T + V(0, 0, 1.4 + k * 0.38), Z_AX, Y_AX, 0.55, 0.08, COPPER, C_TOWER, n_major=14, n_minor=4)
    torus(f"Toroid {s}", T + V(0, 0, 7.0), Z_AX, Y_AX, 1.0, 0.42, STEEL, C_TOWER, n_major=24, n_minor=8)
    dot(f"Tower Orb {s}", T + V(0, 0, 7.5), 0.35, BOLT, C_TOWER)
    pts = [T + V(-s * 1.0, -0.4, 7.0)]
    for j in range(5):
        t = (j + 1) / 5
        pts.append(T + V(-s * 1.0, -0.4, 7.0) + (V(0, 0, 3.0) - T - V(-s * 1.0, -0.4, 7.0) + V(s * 0.6, 0.6, 0)) * t + V(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3)) * (1 if j < 4 else 0))
    for j in range(len(pts) - 1):
        cyl(f"Arc {s}{j}", pts[j], pts[j + 1], 0.09, 0.07, BOLT, C_TOWER, n=5)
abox("Control Box", -5.6, -4.2, -3.6, -2.4, 0.5, 2.4, STEEL, C_DETAIL)
abox("Control Screen", -5.62, -4.18, -3.65, -3.6, 1.4, 2.1, PLASMA, C_DETAIL)
abox("Lever Base", -5.0, -4.8, -3.7, -3.6, 0.9, 1.1, BLACK, C_DETAIL)
cyl("Lever", V(-4.9, -3.7, 1.0), V(-4.9, -4.1, 1.6), 0.05, 0.05, STEEL, C_DETAIL, n=6)
dot("Lever Knob", V(-4.9, -4.1, 1.65), 0.12, WARN, C_DETAIL)
for k, (x, y) in enumerate(((5.2, -3.4), (-5.6, 3.8), (5.6, 4.0))):
    cyl(f"Warning Post {k}", V(x, y, 0.5), V(x, y, 2.6), 0.1, 0.1, BLACK, C_DETAIL, n=6)
    dot(f"Warning Light {k}", V(x, y, 2.8), 0.25, WARN, C_DETAIL)
for s in (-1, 1):
    path_tube(f"Cable {s}", [V(s * 4.6, 2.2, 0.55), V(s * 3.6, 3.2, 0.55), V(s * 2.0, 3.2, 0.55), V(s * 1.0, 2.6, 1.0)], [0.12] * 4, BLACK, C_DETAIL, n=6)
finish_mine(bg=(0.014, 0.016, 0.03), tint=(0.85, 0.9, 1.0))
write_furnace_lua("TeslaCageFurnace")
