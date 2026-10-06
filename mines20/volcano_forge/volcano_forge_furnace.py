"""Volcano Forge Furnace - a rocky island base with lava cracks, a lava cave mouth that sells the ore, a smoking
volcano behind with lava streams, obsidian spikes, anvils and embers. Conveyor ramp straight into the lava.
mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_CAVE, C_VOLC, C_DETAIL = begin("VolcanoForgeFurnace", ["Island", "Cave", "Volcano", "Details"], seed=61)
BASALT = M("Basalt Rock", (54, 44, 42), rough=0.9, rbx="Basalt", noise=((36, 28, 26), (80, 66, 60), 3.0, 0.5))
CRUST = M("Cooled Lava", (30, 22, 22), rough=0.8, rbx="CrackedLava", noise=((20, 14, 14), (52, 38, 34), 5.0, 0.4))
OBS = M("Obsidian", (24, 16, 30), rough=0.15, metal=0.3, rbx="Glass")
LAVA = M("Lava", (255, 110, 20), rough=0.3, glow=(255, 80, 0), glow_strength=4.0, rbx="Neon", light=(16, 2.0))
GLOW = M("Lava Neon", (255, 150, 40), rough=0.3, glow=(255, 110, 10), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
SMOKE = M("Smoke", (70, 66, 68), rough=0.9, rbx="SmoothPlastic", alpha=0.2)
IRON = M("Forge Iron (Metal)", (60, 58, 62), rough=0.4, metal=0.9, rbx="Metal")
CONVM = M("Conveyor", (44, 34, 32), rough=0.6, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (255, 140, 40), rough=0.2, glow=(255, 100, 20), glow_strength=1.0, rbx="ForceField", alpha=0.6)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(61)

# ---- irregular rocky island base with glowing cracks
N = 18
rad = [6.6 + rnd.uniform(-0.7, 0.7) for _ in range(N)]
outline = [(rad[k] * math.cos(2 * math.pi * k / N), 0.4 + rad[k] * math.sin(2 * math.pi * k / N)) for k in range(N)]
inner = [(x * 0.9, 0.4 + (y - 0.4) * 0.9) for x, y in outline]
bm = loft([[V(x, y, 0) for x, y in outline], [V(x, y, 0.7) for x, y in outline], [V(x, y, 1.0) for x, y in inner]], smooth_sides=False)
finish("Island Slab", bm, CRUST, C_BASE, merge=0)
for k in range(N):
    if 230 < (360 * k / N) < 310:
        continue
    x, y = outline[k]
    rock_f(f"Shore Rock {k}", V(x, y, 0.5), (rnd.uniform(0.7, 1.1), rnd.uniform(0.6, 0.9), rnd.uniform(0.5, 0.8)), BASALT, C_BASE, rough=0.3)
for k in range(6):
    a = rnd.uniform(0, 6.28)
    pts = [V(3.6 * math.cos(a), 0.4 + 3.6 * math.sin(a), 1.0)]
    for j in range(3):
        a += rnd.uniform(-0.3, 0.3)
        pts.append(pts[-1] + V(0.9 * math.cos(a), 0.9 * math.sin(a), 0))
    if all(abs(p.x) > 2.9 or p.y > 3.0 for p in pts):
        path_tube(f"Lava Crack {k}", pts, [0.06, 0.08, 0.06, 0.03], GLOW, C_BASE, n=5)

# ---- lava cave mouth: rocky arch over a lava pool
lathe("Lava Pool", V(0, 0, 0.9), [(2.8, 0), (2.8, 0.38)], LAVA, C_CAVE, n=24)
for k in range(13):
    a = math.radians(-15 + k * 15)
    p = V(3.3 * math.cos(a), 0.2, 1.0 + 3.6 * math.sin(a))
    rock_f(f"Arch Rock {k}", p, (0.8, 1.4, 0.75), BASALT, C_CAVE, rough=0.25)
for k in range(9):
    a = math.radians(-60 + k * 30)
    if -110 < math.degrees(a) - 270 + 360 < -70:
        continue
    p = V(3.4 * math.cos(a), 3.4 * math.sin(a), 1.2)
    if p.y < -1.8:
        continue
    rock_f(f"Pool Rock {k}", p, (0.8, 0.7, 0.5), BASALT, C_CAVE, rough=0.3)
for k in range(5):
    cone(f"Stalactite {k}", V(-2.0 + k, 0.2, 4.4 - 0.3 * abs(k - 2)), V(-2.0 + k, 0.2, 3.5 - 0.3 * abs(k - 2)), 0.22, CRUST, C_CAVE, n=5)
burn_zone(BURN, -2.5, 2.5, -2.6, 2.4, 1.15, 2.0, C_CAVE)
conveyor_ramp(CONVM, GLOW, BASALT, GLOW, y_end=-2.6, coll=C_BASE)

# ---- volcano behind
VC = V(0, 4.4, 0.9)
lathe("Volcano", VC, [(4.6, 0), (4.0, 1.5), (2.9, 4.0), (1.9, 6.4), (1.6, 7.0), (1.2, 6.8), (0.01, 6.0)], BASALT, C_VOLC, n=16, smooth=False)
lathe("Crater Lava", VC + V(0, 0, 6.55), [(1.25, 0), (1.25, 0.15)], LAVA, C_VOLC, n=16)
for k, a in enumerate((200, 250, 300, 340, 20)):
    a = math.radians(a)
    pts = [VC + V(1.5 * math.cos(a), 1.5 * math.sin(a), 6.7)]
    for j in range(1, 6):
        t = j / 5
        r = 1.5 + 3.0 * t
        aa = a + 0.25 * math.sin(j + k)
        pts.append(VC + V(r * math.cos(aa), r * math.sin(aa), 6.7 - 6.2 * t + 0.25))
    path_tube(f"Lava Stream {k}", pts, [0.32, 0.3, 0.28, 0.25, 0.22, 0.2], LAVA, C_VOLC, n=8)
for k, (dx, dz, r) in enumerate(((0, 7.8, 1.0), (0.6, 8.9, 1.3), (-0.4, 10.1, 1.5), (0.5, 11.3, 1.2))):
    rock_f(f"Smoke {k}", VC + V(dx, 0.3 * k, dz), (r, r, r * 0.8), SMOKE, C_VOLC, rough=0.2, subd=2)
for k in range(10):
    dot(f"Ember {k}", VC + V(rnd.uniform(-2.5, 2.5), rnd.uniform(-1.5, 1.5), rnd.uniform(7.5, 11)), 0.09, GLOW, C_VOLC)

# ---- obsidian spikes, anvil, braziers
for k, (x, y) in enumerate(((-5.2, 1.6), (5.2, 1.6), (-4.4, 4.6), (4.4, 4.6), (-5.4, -1.8), (5.4, -1.8))):
    for j in range(3):
        crystal(f"Obsidian Spike {k}{j}", V(x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), 0.9),
                V(rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 1), rnd.uniform(1.2, 2.6), 0.28, OBS, C_DETAIL, sides=4)
A = V(-4.0, -2.4, 1.0)
abox("Anvil Base", A.x - 0.4, A.x + 0.4, A.y - 0.3, A.y + 0.3, A.z, A.z + 0.6, IRON, C_DETAIL)
abox("Anvil Top", A.x - 0.7, A.x + 0.6, A.y - 0.35, A.y + 0.35, A.z + 0.6, A.z + 0.95, IRON, C_DETAIL)
cone("Anvil Horn", V(A.x + 0.6, A.y, A.z + 0.8), V(A.x + 1.3, A.y, A.z + 0.85), 0.25, IRON, C_DETAIL, n=8)
for s in (-1, 1):
    B = V(s * 3.7, -5.0, 0.0)
    lathe(f"Brazier {s}", B, [(0.5, 0), (0.3, 0.4), (0.25, 1.6), (0.6, 1.9), (0.65, 2.2), (0.5, 2.2)], IRON, C_DETAIL, n=8, smooth=False)
    lathe(f"Brazier Fire {s}", B + V(0, 0, 2.1), [(0.45, 0), (0.3, 0.5), (0.0, 1.1)], GLOW, C_DETAIL, n=8)

finish_mine(bg=(0.03, 0.014, 0.01), tint=(1.0, 0.8, 0.65))
write_furnace_lua("VolcanoForgeFurnace")
