"""Sakura Shrine Mine - a red torii gate before a two-tier pagoda, a twisting cherry blossom tree, a koi pond
and stone lanterns; ore tumbles out of a bamboo water spout. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_SHRINE, C_TREE, C_POND, C_DETAIL = begin("SakuraShrineMine", ["Base", "Shrine", "Cherry Tree", "Pond", "Details"], seed=77)
DWOOD = M("Dark Wood (Wood)", (52, 34, 26), rough=0.6, rbx="WoodPlanks")
TRIM = M("Blossom Trim (Metal)", (255, 150, 190), rough=0.3, metal=0.4, glow=(255, 110, 170), glow_strength=1.0, rbx="Neon")
STONEF = M("Zen Stone (Marble)", (176, 176, 170), rough=0.6, marble=((166, 166, 160), (220, 210, 205)))
RED = M("Vermilion Lacquer", (205, 46, 30), rough=0.35)
BLACKL = M("Black Lacquer", (20, 18, 20), rough=0.3)
TILE = M("Roof Tiles", (54, 60, 76), rough=0.5, rbx="Slate", noise=((40, 46, 60), (72, 80, 98), 6.0, 0.3))
GOLD = M("Gold (Metal)", (236, 186, 70), rough=0.25, metal=1.0)
STONE = M("Lantern Stone", (150, 150, 144), rough=0.9, rbx="Slate", noise=((120, 120, 116), (176, 176, 170), 3.5, 0.4))
WARM = M("Lantern Glow", (255, 214, 140), rough=0.4, glow=(255, 180, 90), glow_strength=6.0, rbx="Neon", light=(9, 1.3))
BARK = M("Cherry Bark (Wood)", (74, 46, 38), rough=0.8, rbx="Wood")
BLOSSOM = M("Blossom", (255, 150, 196), rough=0.6, glow=(255, 140, 190), glow_strength=0.5, rbx="SmoothPlastic", noise=((240, 150, 190), (255, 206, 226), 4.0, 0.25))
PETAL = M("Petals", (255, 196, 220), rough=0.6, glow=(255, 160, 200), glow_strength=1.0, rbx="Neon")
BAMBOO = M("Bamboo", (150, 182, 82), rough=0.5, noise=((120, 150, 60), (180, 206, 110), 8.0, 0.1))
WATER = M("Pond Water", (60, 150, 180), rough=0.05, glow=(30, 120, 160), glow_strength=0.6, rbx="Glass", alpha=0.25)
KOI = M("Koi Orange", (255, 120, 40), rough=0.4)
KOIW = M("Koi White", (250, 246, 240), rough=0.4)
LEAF = M("Lily Pads", (70, 150, 70), rough=0.6)
ORE = M("Blossom Ore", (255, 190, 220), rough=0.15, glow=(255, 140, 200), glow_strength=2.2, rbx="Neon")

top = base_plinth(11.0, 11.0, DWOOD, TRIM, STONEF, C_BASE, c=1.0)

def roof(name, C, w, d, h, curl, coll):
    """Curved pagoda roof: hipped slab with upturned corners."""
    pts_lo = [C + V(-w / 2 - curl, -d / 2 - curl, curl * 0.6), C + V(w / 2 + curl, -d / 2 - curl, curl * 0.6),
              C + V(w / 2 + curl, d / 2 + curl, curl * 0.6), C + V(-w / 2 - curl, d / 2 + curl, curl * 0.6)]
    mid = [C + V(-w / 2, -d / 2, 0), C + V(w / 2, -d / 2, 0), C + V(w / 2, d / 2, 0), C + V(-w / 2, d / 2, 0)]
    up = [C + V(-w * 0.18, -d * 0.18, h), C + V(w * 0.18, -d * 0.18, h), C + V(w * 0.18, d * 0.18, h), C + V(-w * 0.18, d * 0.18, h)]
    bm = loft([[p + V(0, 0, -0.25) for p in pts_lo], pts_lo, mid, up], cap0=True, cap1=True, smooth_sides=False)
    finish(name, bm, TILE, coll, merge=0)
    for k, p in enumerate(pts_lo):
        dot(f"{name} Corner Bell {k + 1}", p + V(0, 0, -0.45), 0.14, GOLD, coll)

# ---- pagoda shrine (two tiers)
S = V(0, 2.2, top)
abox("Shrine Platform", S.x - 3.0, S.x + 3.0, S.y - 2.4, S.y + 2.4, top, top + 0.7, STONE, C_SHRINE)
for k in range(3):
    abox(f"Shrine Step {k + 1}", S.x - 1.2, S.x + 1.2, S.y - 2.4 - 0.35 * (k + 1), S.y - 2.4 - 0.35 * k, top, top + 0.7 - 0.23 * (k + 1), STONE, C_SHRINE)
for x in (-2.2, 2.2):
    for y in (-1.6, 1.6):
        cyl(f"Pillar {x}{y}", S + V(x, y, 0.7), S + V(x, y, 3.6), 0.22, 0.22, RED, C_SHRINE, n=10)
abox("Shrine Wall", S.x - 2.0, S.x + 2.0, S.y - 1.3, S.y + 1.5, top + 0.7, top + 3.5, DWOOD, C_SHRINE)
abox("Shrine Door Glow", S.x - 0.9, S.x + 0.9, S.y - 1.36, S.y - 1.28, top + 0.9, top + 2.9, WARM, C_SHRINE)
for k in range(3):
    abox(f"Door Lattice V{k + 1}", S.x - 0.6 + k * 0.6 - 0.04, S.x - 0.6 + k * 0.6 + 0.04, S.y - 1.42, S.y - 1.34, top + 0.9, top + 2.9, BLACKL, C_SHRINE)
    abox(f"Door Lattice H{k + 1}", S.x - 0.9, S.x + 0.9, S.y - 1.42, S.y - 1.34, top + 1.3 + k * 0.6 - 0.04, top + 1.3 + k * 0.6 + 0.04, BLACKL, C_SHRINE)
abox("Beam Ring", S.x - 2.5, S.x + 2.5, S.y - 1.9, S.y + 1.9, top + 3.55, top + 3.95, RED, C_SHRINE)
roof("Roof Lower", S + V(0, 0, 3.95), 5.4, 4.4, 1.7, 0.9, C_SHRINE)
abox("Upper Tier", S.x - 1.4, S.x + 1.4, S.y - 1.1, S.y + 1.1, top + 5.4, top + 7.0, RED, C_SHRINE)
abox("Upper Window", S.x - 0.6, S.x + 0.6, S.y - 1.16, S.y - 1.08, top + 5.8, top + 6.6, WARM, C_SHRINE)
roof("Roof Upper", S + V(0, 0, 7.0), 3.4, 2.9, 1.4, 0.7, C_SHRINE)
cyl("Finial Pole", S + V(0, 0, 8.3), S + V(0, 0, 10.0), 0.09, 0.06, GOLD, C_SHRINE, n=6)
for k in range(4):
    torus(f"Finial Ring {k + 1}", S + V(0, 0, 8.6 + k * 0.32), V(0, 0, 1), V(0, 1, 0), 0.3 - 0.05 * k, 0.05, GOLD, C_SHRINE, n_major=12, n_minor=4)
dot("Finial Jewel", S + V(0, 0, 10.1), 0.2, PETAL, C_SHRINE)

# ---- torii gate at the front
G = V(0, -2.9, top)
for side in (1, -1):
    cyl(f"Torii Post {side}", G + V(side * 2.4, 0, 0), G + V(side * 2.25, 0, 6.0), 0.32, 0.28, RED, C_SHRINE, n=12)
    cyl(f"Torii Foot {side}", G + V(side * 2.4, 0, 0), G + V(side * 2.4, 0, 0.6), 0.42, 0.42, BLACKL, C_SHRINE, n=12)
abox("Torii Nuki", G.x - 3.0, G.x + 3.0, G.y - 0.18, G.y + 0.18, top + 4.6, top + 5.0, RED, C_SHRINE)
abox("Torii Plaque", G.x - 0.45, G.x + 0.45, G.y - 0.22, G.y + 0.22, top + 5.0, top + 5.9, BLACKL, C_SHRINE)
bm = loft([[G + V(x, y, 6.0 + 0.35 * (abs(x) / 3.6) ** 2) for x, y in ((-3.6, -0.35), (3.6, -0.35), (3.6, 0.35), (-3.6, 0.35))],
           [G + V(x, y, 6.45 + 0.6 * (abs(x) / 3.6) ** 2) for x, y in ((-3.8, -0.4), (3.8, -0.4), (3.8, 0.4), (-3.8, 0.4))]], smooth_sides=False)
finish("Torii Kasagi", bm, BLACKL, C_SHRINE, merge=0)
abox("Torii Shimaki", G.x - 3.3, G.x + 3.3, G.y - 0.28, G.y + 0.28, top + 5.65, top + 6.0, RED, C_SHRINE)

# ---- bamboo spout (ore drop) under the gate
BS = G + V(0, 0.2, 2.6)
cyl("Bamboo Post", G + V(-0.9, 0.6, 0), G + V(-0.9, 0.6, 2.9), 0.18, 0.18, BAMBOO, C_DETAIL, n=10)
cyl("Bamboo Spout", G + V(-0.9, 1.4, 2.7), G + V(0.2, -0.6, 2.2), 0.2, 0.2, BAMBOO, C_DETAIL, n=10)
for k in range(3):
    torus(f"Bamboo Node {k + 1}", G + V(-0.9, 0.6, 0.8 + k * 0.8), V(0, 0, 1), V(0, 1, 0), 0.2, 0.04, BAMBOO, C_DETAIL, n_major=10, n_minor=4)
lathe("Stone Basin", G + V(0.3, -0.9, 0), [(0.9, 0), (1.0, 0.5), (0.95, 0.7), (0.75, 0.72), (0.7, 0.45)], STONE, C_DETAIL, n=14)
lathe("Basin Water", G + V(0.3, -0.9, 0.6), [(0.74, 0), (0.74, 0.03)], WATER, C_DETAIL, n=14)
ore_cube(G + V(0.3, -0.9, 1.5), ORE, C_DETAIL)

# ---- cherry blossom tree (left)
T0 = V(3.9, 3.4, top)
trunk = [T0, T0 + V(0.3, -0.2, 1.8), T0 + V(-0.4, -0.1, 3.6), T0 + V(0.2, 0.3, 5.2), T0 + V(0.6, 0.2, 6.4)]
path_tube("Cherry Trunk", trunk, [0.7, 0.55, 0.45, 0.38, 0.3], BARK, C_TREE, n=10)
rnd = random.Random(4)
for k, (d, l) in enumerate(((V(-1, -0.3, 0.6), 2.6), (V(0.6, 0.4, 0.5), 1.6), (V(-0.4, 1, 0.7), 1.6), (V(-0.3, -1, 0.6), 2.2), (V(-0.6, 0.2, 1), 1.8))):
    b0 = trunk[2 + k % 3];d = d.normalized()
    tip = b0 + d * l
    path_tube(f"Branch {k + 1}", [b0, (b0 + tip) / 2 + V(0, 0, 0.3), tip], [0.26, 0.18, 0.1], BARK, C_TREE, n=8)
    for j in range(3):
        c = tip + V(rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), rnd.uniform(0.0, 0.8))
        s_ = rnd.uniform(0.9, 1.4)
        rock_f(f"Blossom {k + 1}-{j + 1}", c, (s_, s_, s_ * 0.8), BLOSSOM, C_TREE, rough=0.18, subd=2)
for k in range(16):                                        # falling petals
    c = T0 + V(rnd.uniform(-4.5, 1.0), rnd.uniform(-6.5, -0.5), rnd.uniform(0.6, 6.0))
    a = rnd.uniform(0, 6.28)
    blade(f"Petal {k + 1}", [c, c + V(0.25 * math.cos(a), 0.25 * math.sin(a), 0.05), c + V(0.1, 0.1, 0.2)], 0.03, PETAL, C_TREE)

# ---- little maple bonsai back-left
B0 = V(-4.2, 3.8, top)
lathe("Bonsai Pot", B0, [(0.7, 0), (0.85, 0.5), (0.9, 0.55), (0.75, 0.55)], BLACKL, C_TREE, n=8, smooth=False)
path_tube("Bonsai Trunk", [B0 + V(0, 0, 0.5), B0 + V(0.3, 0, 1.3), B0 + V(-0.2, 0.1, 2.0)], [0.22, 0.16, 0.1], BARK, C_TREE, n=8)
for k, c in enumerate((V(-0.5, 0, 2.2), V(0.4, 0.2, 1.8), V(0, -0.2, 2.6))):
    rock_f(f"Bonsai Leaves {k + 1}", B0 + c, (0.7, 0.6, 0.45), RED, C_TREE, rough=0.2, subd=1)

# ---- koi pond (right) with lily pads
P = V(3.4, -0.6, top)
lathe("Pond Rim", P, [(2.0, 0), (2.05, 0.35), (1.7, 0.4), (1.6, 0.1)], STONE, C_POND, n=20, smooth=False)
lathe("Pond Water", P + V(0, 0, 0.25), [(1.7, 0), (1.7, 0.02)], WATER, C_POND, n=20)
for k, (dx, dy, ang, mat) in enumerate(((0.4, 0.5, 30, KOI), (-0.6, -0.2, 200, KOIW), (0.5, -0.7, 120, KOI))):
    c = P + V(dx, dy, 0.32);a = math.radians(ang);d = V(math.cos(a), math.sin(a), 0)
    path_tube(f"Koi {k + 1}", [c - d * 0.5, c - d * 0.1, c + d * 0.35, c + d * 0.55], [0.05, 0.2, 0.15, 0.05], mat, C_POND, n=8)
    blade(f"Koi Tail {k + 1}", [c - d * 0.5, c - d * 0.85 + V(-d.y, d.x, 0) * 0.2, c - d * 0.85 - V(-d.y, d.x, 0) * 0.2], 0.03, mat, C_POND)
for k, (dx, dy) in enumerate(((-0.8, 0.7), (0.9, -0.1), (-0.2, -1.0))):
    lathe(f"Lily Pad {k + 1}", P + V(dx, dy, 0.28), [(0.42, 0), (0.42, 0.03)], LEAF, C_POND, n=10)
dot("Lotus", P + V(-0.8, 0.7, 0.4), 0.16, PETAL, C_POND)

# ---- stone lanterns (toro) either side of the gate
for side in (1, -1):
    L0 = V(side * 4.2, -4.1, top)
    cyl(f"Toro Base {side}", L0, L0 + V(0, 0, 0.3), 0.6, 0.6, STONE, C_DETAIL, n=6)
    cyl(f"Toro Pole {side}", L0 + V(0, 0, 0.3), L0 + V(0, 0, 1.6), 0.25, 0.25, STONE, C_DETAIL, n=6)
    cyl(f"Toro Shelf {side}", L0 + V(0, 0, 1.6), L0 + V(0, 0, 1.85), 0.6, 0.55, STONE, C_DETAIL, n=6)
    cyl(f"Toro Light {side}", L0 + V(0, 0, 1.85), L0 + V(0, 0, 2.6), 0.4, 0.4, WARM, C_DETAIL, n=6)
    cyl(f"Toro Roof {side}", L0 + V(0, 0, 2.6), L0 + V(0, 0, 3.2), 0.8, 0.15, STONE, C_DETAIL, n=6)
    dot(f"Toro Knob {side}", L0 + V(0, 0, 3.3), 0.15, STONE, C_DETAIL)

finish_mine(bg=(0.02, 0.014, 0.024), tint=(1.0, 0.85, 0.9))
