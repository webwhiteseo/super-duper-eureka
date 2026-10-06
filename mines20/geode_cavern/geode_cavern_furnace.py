"""Geode Cavern Furnace - a giant split geode on a rocky cave floor; the ramp carries ore into the geode's glowing
crystal-liquid heart, ringed by amethyst crystals inside the shell. Stalagmites, glowing mushrooms, crystal clusters.
mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_GEODE, C_CAVE = begin("GeodeCavernFurnace", ["Cave Floor", "Geode", "Cave"], seed=201)
CAVE = M("Cave Rock", (70, 64, 72), rough=0.9, rbx="Slate", noise=((50, 46, 54), (96, 88, 100), 3.0, 0.5))
SHELL = M("Geode Shell", (150, 136, 120), rough=0.85, rbx="Rock", noise=((120, 106, 92), (176, 160, 142), 4.0, 0.4))
BAND = M("Agate Band", (230, 220, 240), rough=0.4)
AMETH = M("Amethyst", (180, 100, 255), rough=0.05, glow=(150, 60, 255), glow_strength=1.6, rbx="Glass", alpha=0.15, light=(10, 1.2))
AMETH2 = M("Pale Amethyst", (230, 190, 255), rough=0.05, glow=(200, 150, 255), glow_strength=1.0, rbx="Glass", alpha=0.15)
POOL = M("Crystal Liquid", (210, 150, 255), rough=0.05, glow=(180, 100, 255), glow_strength=4.0, rbx="Neon", light=(16, 2.2))
SHROOM = M("Glow Mushroom", (100, 230, 255), rough=0.3, glow=(60, 210, 255), glow_strength=3.0, rbx="Neon", light=(6, 0.8))
STEM = M("Mushroom Stem", (220, 220, 230), rough=0.6)
CONVM = M("Conveyor", (60, 54, 64), rough=0.6, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (210, 150, 255), rough=0.2, glow=(180, 100, 255), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(201)
# irregular cave floor
N = 16
rad = [6.8 + rnd.uniform(-0.6, 0.6) for _ in range(N)]
out = [V(rad[k] * math.cos(2 * math.pi * k / N), 0.6 + rad[k] * math.sin(2 * math.pi * k / N), 0) for k in range(N)]
finish("Cave Floor", loft([out, [p + V(0, 0, 0.5) for p in out], [V(p.x * 0.92, 0.6 + (p.y - 0.6) * 0.92, 0.7) for p in out]], smooth_sides=False), CAVE, C_BASE, merge=0)
conveyor_ramp(CONVM, AMETH2, CAVE, AMETH, y_end=-2.4, coll=C_BASE)
# geode: two half shells split open (back half standing, front half low ring)
G = V(0, 0.6, 1.0)
for k in range(16):
    a0 = math.radians(-20 + k * 13.75);a1 = a0 + math.radians(13.75)
    for j, (z0, z1, r0, r1) in enumerate(((0.0, 1.6, 3.4, 3.9), (1.6, 3.4, 3.2, 3.7), (3.4, 4.8, 2.6, 3.1), (4.8, 5.8, 1.6, 2.2))):
        if j > 0 and not (0 < math.degrees(a0) % 360 < 180 or 180 < math.degrees(a1) % 360 < 181):
            continue
        p = [G + V(r * math.cos(a), r * math.sin(a), z) for r, a, z in ((r0, a0, z0), (r1, a0, z0), (r1, a1, z0), (r0, a1, z0))]
        q = [G + V(r * math.cos(a) * (r1 / r0 if False else 1), r * math.sin(a), z1) for r, a in ((r0 - (0.4 if j else 0), a0), (r1 - (0.4 if j else 0), a0), (r1 - (0.4 if j else 0), a1), (r0 - (0.4 if j else 0), a1))]
        hexa(f"Shell {k}{j}", p + q, SHELL, C_GEODE)
        if j == 0 and k % 2 == 0:
            m = (a0 + a1) / 2
            crystal(f"Rim Crystal {k}", G + V(3.3 * math.cos(m), 3.3 * math.sin(m), 1.4), V(-math.cos(m) * 0.6, -math.sin(m) * 0.6, 1), 1.0, 0.25, AMETH, C_GEODE, sides=6)
torus("Agate Band", G + V(0, 0, 1.62), Z_AX, Y_AX, 3.65, 0.08, BAND, C_GEODE, n_major=40, n_minor=4)
lathe("Crystal Pool", G + V(0, 0, -0.2), [(3.3, 0), (3.3, 0.45)], POOL, C_GEODE, n=28)
burn_zone(BURN, -2.4, 2.4, -2.4, 2.6, 0.3 + 1.0 - 0.95, 2.0, C_GEODE)
for k in range(22):                                          # crystals lining the inside of the back shell
    a = math.radians(rnd.uniform(15, 165));z = rnd.uniform(1.8, 5.0)
    r = 3.0 - 0.25 * (z - 1.8)
    p = G + V(r * math.cos(a), r * math.sin(a), z)
    crystal(f"Inner Crystal {k}", p, V(-math.cos(a), -math.sin(a), rnd.uniform(-0.3, 0.4)), rnd.uniform(0.6, 1.3), rnd.uniform(0.15, 0.28), AMETH if k % 3 else AMETH2, C_GEODE, sides=6)
crystal_cluster("Heart Cluster", G + V(0, 1.6, 0.3), 6, 0.55, AMETH, SHELL, C_GEODE, seed=4)
# stalagmites, mushrooms, side clusters
for k, (x, y, h) in enumerate(((-5.4, 3.0, 3.2), (-4.6, 4.6, 2.2), (5.2, 3.4, 3.6), (4.4, 5.0, 2.4), (-5.8, -1.0, 1.8), (5.8, -0.6, 2.0))):
    cone(f"Stalagmite {k}", V(x, y, 0.5), V(x + 0.1, y, 0.5 + h), 0.6, CAVE, C_CAVE, n=7)
for k, (x, y) in enumerate(((-4.2, -3.6), (4.2, -3.8), (-5.2, 1.4), (5.4, 1.6))):
    for j in range(3):
        P = V(x + 0.5 * (j - 1), y + 0.3 * (j % 2), 0.5)
        h = 0.6 + 0.35 * j
        cyl(f"Shroom Stem {k}{j}", P, P + V(0, 0, h), 0.1, 0.08, STEM, C_CAVE, n=6)
        ellip(f"Shroom Cap {k}{j}", P + V(0, 0, h), 0.4 - 0.05 * j, 0.4 - 0.05 * j, 0.22, SHROOM, C_CAVE, n=10, m=3, half=True)
for k, (x, y) in enumerate(((-3.8, 5.0), (3.6, 5.4))):
    crystal_cluster(f"Side Cluster {k}", V(x, y, 0.6), 5, 0.5, AMETH2, CAVE, C_CAVE, seed=k + 9)
finish_mine(bg=(0.016, 0.01, 0.03), tint=(0.85, 0.78, 1.0))
write_furnace_lua("GeodeCavernFurnace")
