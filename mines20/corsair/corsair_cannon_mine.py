"""Corsair Cannon Mine - a pirate galleon riding the waves, its great deck cannon firing ore out over the side.
Jolly Roger at the masthead, glowing stern windows, an open treasure chest on deck and a palm islet behind.
Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_HULL, C_RIG, C_GUNS, C_SEA = begin("CorsairCannonMine", ["Base", "Hull", "Rigging", "Guns", "Sea"], seed=17)
DARKWOOD = M("Ship Timber (Wood)", (86, 52, 32), rough=0.7, rbx="WoodPlanks", noise=((64, 38, 22), (110, 70, 44), 5.0, 0.3))
GOLD = M("Gold (Metal)", (240, 188, 66), rough=0.25, metal=1.0, rbx="Metal")
SEA = M("Sea Water", (30, 112, 150), rough=0.08, rbx="Glass", noise=((20, 88, 128), (54, 150, 182), 3.0, 0.25))
DECK = M("Deck Planks (Wood)", (164, 122, 78), rough=0.75, rbx="WoodPlanks", noise=((134, 96, 58), (186, 144, 96), 7.0, 0.25))
IRON = M("Cannon Iron", (40, 40, 44), rough=0.35, metal=0.85, rbx="Metal")
SAIL = M("Sailcloth (Fabric)", (236, 224, 196), rough=0.9, rbx="Fabric", noise=((214, 200, 168), (246, 238, 216), 2.5, 0.1))
STRIPE = M("Sail Red (Fabric)", (176, 34, 30), rough=0.9, rbx="Fabric")
FLAG = M("Flag Black (Fabric)", (16, 16, 18), rough=0.9, rbx="Fabric")
BONE = M("Skull White", (240, 236, 224), rough=0.6)
ROPE = M("Rope", (150, 120, 80), rough=0.9, rbx="Fabric")
WARM = M("Lantern Glow", (255, 210, 130), rough=0.4, glow=(255, 170, 70), glow_strength=5.0, rbx="Neon", light=(12, 1.4))
FLASH = M("Muzzle Flash", (255, 150, 40), rough=0.4, glow=(255, 110, 20), glow_strength=4.0, rbx="Neon", light=(10, 1.5))
SMOKE = M("Cannon Smoke", (200, 200, 204), rough=0.9, rbx="SmoothPlastic", alpha=0.2)
FOAM = M("Sea Foam", (236, 246, 250), rough=0.6)
ROCK = M("Islet Rock", (96, 92, 88), rough=0.9, rbx="Slate", noise=((70, 66, 64), (126, 120, 114), 3.0, 0.4))
BEACH = M("Islet Sand", (226, 200, 140), rough=0.95, rbx="Sand")
PALM = M("Palm Leaf", (64, 150, 64), rough=0.6)
TRUNK = M("Palm Trunk (Wood)", (130, 96, 60), rough=0.8, rbx="Wood")
GEM = M("Ruby", (220, 20, 50), rough=0.1, glow=(200, 10, 40), glow_strength=1.0, rbx="Glass", alpha=0.1)
ORE = M("Doubloon Ore", (255, 196, 60), rough=0.15, glow=(255, 150, 20), glow_strength=2.0, rbx="Neon")

top = base_plinth(15.0, 11.5, DARKWOOD, GOLD, SEA, C_BASE, c=1.2)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(17)

# ---- a thin pool of sea for the ship to float in (delete the SeaWater part in Roblox if you have your own water)
if not WITH_BASE:
    ellip("Sea Pool", V(0.2, 0, 0), 7.4, 5.3, 0.08, SEA, C_SEA, n=36, m=2, half=True)
    top = 0.08                                           # waterline

# ---- hull (bow toward +X)
XS = [-5.2, -4.6, -3.6, -2.4, -1.2, 0.0, 1.2, 2.4, 3.4, 4.2, 4.8, 5.3, 5.7]
def half_beam(x):
    if x <= 2.0:
        return 2.05 - 0.004 * (x + 1.0) ** 2 - (0.12 if x < -4.5 else 0.0)
    t = (x - 2.0) / 3.7
    return max(2.05 * (1 - t ** 1.8) - 0.004 * 9, 0.05)
def deck_z(x):
    return top + 2.0 + 0.035 * x * x
def section(x, w, dz):
    return [V(x, w, dz), V(x, w * 1.06, dz - 0.7), V(x, w * 1.0, dz - 1.3), V(x, w * 0.82, top - 0.1), V(x, w * 0.4, top - 0.45),
            V(x, 0, top - 0.6), V(x, -w * 0.4, top - 0.45), V(x, -w * 0.82, top - 0.1), V(x, -w * 1.0, dz - 1.3), V(x, -w * 1.06, dz - 0.7), V(x, -w, dz)]
rings = [section(x, half_beam(x), deck_z(x)) for x in XS]
bm = loft(rings, smooth_sides=True)
bm.faces.ensure_lookup_table()
n = len(rings[0])
for i in range(len(rings) - 1):
    bm.faces[i * n + n - 1].smooth = False
finish("Hull", bm, DARKWOOD, C_HULL, merge=0.0005)
deck_rings = [[V(x, -half_beam(x) * 0.95, deck_z(x)), V(x, half_beam(x) * 0.95, deck_z(x)), V(x, half_beam(x) * 0.95, deck_z(x) + 0.1),
               V(x, -half_beam(x) * 0.95, deck_z(x) + 0.1)] for x in XS[:-1]]
finish("Deck", loft(deck_rings, smooth_sides=False), DECK, C_HULL, merge=0)
for s in (-1, 1):
    bw = [[V(x, s * (half_beam(x) - 0.14), deck_z(x)), V(x, s * half_beam(x), deck_z(x)), V(x, s * half_beam(x), deck_z(x) + 0.75),
           V(x, s * (half_beam(x) - 0.14), deck_z(x) + 0.75)] for x in XS[:-1]]
    finish(f"Bulwark {s}", loft(bw, smooth_sides=False), DARKWOOD, C_HULL, merge=0)
    path_tube(f"Rail Cap {s}", [V(x, s * (half_beam(x) - 0.07), deck_z(x) + 0.8) for x in XS[:-1]], [0.09] * (len(XS) - 1), GOLD, C_HULL, n=6)
    for k, dz in enumerate((-0.72, -1.3)):
        path_tube(f"Wale {s}{k}", [V(x, s * half_beam(x) * (1.07 if k == 0 else 1.01), deck_z(x) + dz) for x in XS[:-1]] + [V(5.62, 0, deck_z(5.6) + dz)],
                  [0.07] * len(XS), GOLD if k == 0 else IRON, C_HULL, n=6)
    for k, x in enumerate((-2.9, -1.3, 0.3, 2.6)):        # gunports with small guns
        w = half_beam(x) * 1.05;z = deck_z(x) - 0.45
        obox(f"Gunport {s}{k}", V(x, s * w, z), (0.6, 0.12, 0.5), X_AX, Y_AX, Z_AX, IRON, C_GUNS)
        obox(f"Gunport Lid {s}{k}", V(x, s * (w + 0.2), z + 0.45), (0.62, 0.08, 0.5), X_AX, V(0, s * 0.6, 1), V(0, -1, s * 0.6), STRIPE, C_GUNS)
        cyl(f"Small Gun {s}{k}", V(x, s * (w - 0.1), z), V(x, s * (w + 0.55), z), 0.16, 0.13, IRON, C_GUNS, n=10, hint=Z_AX)
        torus(f"Small Gun Muzzle {s}{k}", V(x, s * (w + 0.55), z), Y_AX, Z_AX, 0.15, 0.05, IRON, C_GUNS, n_major=10, n_minor=4)

# ---- stern castle with glowing windows, lanterns and the ship's wheel
SZ = deck_z(-5.0)
hexa("Stern Castle", [V(-5.35, -1.95, top + 2.0), V(-2.7, -2.0, top + 2.0), V(-2.7, 2.0, top + 2.0), V(-5.35, 1.95, top + 2.0),
                      V(-5.5, -1.95, SZ + 1.3), V(-2.7, -2.0, SZ + 1.3), V(-2.7, 2.0, SZ + 1.3), V(-5.5, 1.95, SZ + 1.3)], DARKWOOD, C_HULL)
abox("Castle Deck", -5.5, -2.65, -2.0, 2.0, SZ + 1.3, SZ + 1.42, DECK, C_HULL)
for s in (-1, 1):
    abox(f"Castle Rail {s}", -5.5, -2.7, s * 1.95 - 0.06, s * 1.95 + 0.06, SZ + 1.95, SZ + 2.05, GOLD, C_HULL)
    for k in range(6):
        x = -5.4 + k * 0.52
        cyl(f"Castle Baluster {s}{k}", V(x, s * 1.95, SZ + 1.42), V(x, s * 1.95, SZ + 1.95), 0.05, 0.05, DARKWOOD, C_HULL, n=6)
for k, y in enumerate((-1.1, 0.0, 1.1)):
    abox(f"Stern Window {k + 1}", -5.56, -5.48, y - 0.32, y + 0.32, SZ + 0.25, SZ + 0.95, WARM, C_HULL)
    abox(f"Window Mullion {k + 1}", -5.6, -5.55, y - 0.03, y + 0.03, SZ + 0.25, SZ + 0.95, DARKWOOD, C_HULL)
abox("Stern Gallery", -5.75, -5.45, -1.9, 1.9, SZ + 0.1, SZ + 0.2, GOLD, C_HULL)
abox("Stern Name Board", -5.58, -5.5, -1.4, 1.4, SZ - 0.45, SZ - 0.1, GOLD, C_HULL)
for s in (-1, 1):
    P = V(-5.45, s * 1.75, SZ + 1.42)
    cyl(f"Stern Lantern Arm {s}", P, P + V(-0.35, 0, 0.6), 0.05, 0.05, IRON, C_HULL, n=6)
    lathe(f"Stern Lantern {s}", P + V(-0.4, 0, 0.6), [(0.2, -0.45), (0.28, -0.25), (0.28, 0.2), (0.12, 0.35)], WARM, C_HULL, n=8, smooth=False)
    cone(f"Stern Lantern Cap {s}", P + V(-0.4, 0, 0.95), P + V(-0.4, 0, 1.2), 0.2, GOLD, C_HULL, n=8)
W = V(-3.2, 0, SZ + 1.42)
cyl("Wheel Post", W, W + V(0, 0, 0.9), 0.12, 0.12, DARKWOOD, C_HULL, n=8)
WC = W + V(0.15, 0, 1.15)
torus("Ship Wheel", WC, X_AX, Z_AX, 0.55, 0.06, DARKWOOD, C_HULL, n_major=20, n_minor=5)
dot("Wheel Hub", WC, 0.12, GOLD, C_HULL)
for k in range(8):
    a = k * math.pi / 4;d = V(0, math.cos(a), math.sin(a))
    cyl(f"Wheel Spoke {k + 1}", WC, WC + d * 0.82, 0.035, 0.05, DARKWOOD, C_HULL, n=6)
for s in (-1, 1):                                        # stairs to the castle
    for k in range(4):
        abox(f"Castle Stair {s}{k}", -2.7 + 0.0, -2.7 + 0.35 * (4 - k), s * 1.35 - 0.4, s * 1.35 + 0.4, deck_z(-2.5), deck_z(-2.5) + 0.33 * (k + 1), DECK, C_HULL) if False else \
            abox(f"Castle Stair {s}{k}", -2.7 + 0.32 * k, -2.7 + 0.32 * (k + 1), s * 1.3 - 0.35, s * 1.3 + 0.35, deck_z(-2.0), SZ + 1.4 - 0.36 * (k + 1), DECK, C_HULL)

# ---- figurehead + bowsprit + anchor
BX = 5.55;BZ = deck_z(5.5)
cyl("Bowsprit", V(4.2, 0, BZ + 0.2), V(7.2, 0, BZ + 1.6), 0.16, 0.1, DARKWOOD, C_RIG, n=8)
for k in range(3):
    torus(f"Bowsprit Band {k}", V(4.9 + k * 0.6, 0, BZ + 0.53 + k * 0.28), V(1, 0, 0.46), Z_AX, 0.16, 0.04, GOLD, C_RIG, n_major=10, n_minor=4)
FH = V(5.85, 0, BZ - 0.4)
ellip("Figurehead Skull", FH, 0.42, 0.36, 0.42, GOLD, C_HULL, n=12, m=5)
ellip("Figurehead Jaw", FH + V(0.15, 0, -0.38), 0.3, 0.26, 0.15, GOLD, C_HULL, n=10, m=3)
for s in (-1, 1):
    dot(f"Figurehead Eye {s}", FH + V(0.33, s * 0.14, 0.05), 0.11, GEM, C_HULL)
AN = V(4.3, -1.75, deck_z(4.3) - 1.6)
cyl("Anchor Shank", AN, AN + V(0, 0, 1.2), 0.07, 0.07, IRON, C_HULL, n=8)
cyl("Anchor Stock", AN + V(-0.45, -0.05, 1.05), AN + V(0.45, -0.05, 1.05), 0.06, 0.06, IRON, C_HULL, n=6, hint=Z_AX)
path_tube("Anchor Arms", [AN + V(-0.55, -0.05, 0.4), AN + V(-0.3, -0.05, 0.02), AN + V(0, -0.05, -0.05), AN + V(0.3, -0.05, 0.02), AN + V(0.55, -0.05, 0.4)],
          [0.03, 0.07, 0.08, 0.07, 0.03], IRON, C_HULL, n=6)
for s in (-1, 1):
    cone(f"Anchor Fluke {s}", AN + V(s * 0.5, -0.05, 0.3), AN + V(s * 0.65, -0.05, 0.6), 0.12, IRON, C_HULL, n=4)
for k in range(4):
    torus(f"Anchor Chain {k + 1}", AN + V(0, 0.1 * k / 4, 1.35 + 0.22 * k), Z_AX if k % 2 else X_AX, Y_AX, 0.1, 0.03, IRON, C_HULL, n_major=8, n_minor=4)

# ---- masts, yards, sails, crow's nest, Jolly Roger
def sail(name, x, y0, y1, z0, z1, bulge, mat):
    rows = []
    for i in range(5):
        t = i / 4;z = z1 + (z0 - z1) * t
        wid = 1.0 + 0.12 * t
        rows.append([V(x + bulge * math.sin(math.pi * j / 6) * (0.4 + 0.6 * math.sin(math.pi * (0.15 + 0.85 * t))),
                       (y0 + (y1 - y0) * j / 6) * wid, z) for j in range(7)])
    bm = bmesh.new()
    vs = [[bm.verts.new(p) for p in r] for r in rows]
    for i in range(4):
        for j in range(6):
            bm.faces.new((vs[i][j], vs[i][j + 1], vs[i + 1][j + 1], vs[i + 1][j])).smooth = True
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.05)
    return finish(name, bm, mat, C_RIG, merge=0)

for mx, mh, yards in ((-0.6, 9.4, ((3.0, 2.0), (5.6, 1.6), (7.7, 1.15))), (3.0, 7.4, ((2.8, 1.6), (5.0, 1.25)))):
    D = deck_z(mx)
    cyl(f"Mast {mx}", V(mx, 0, D), V(mx, 0, D + mh), 0.24, 0.14, DARKWOOD, C_RIG, n=10)
    for k, (yz, half) in enumerate(yards):
        cyl(f"Yard {mx}-{k}", V(mx + 0.25, -half - 0.3, D + yz), V(mx + 0.25, half + 0.3, D + yz), 0.08, 0.08, DARKWOOD, C_RIG, n=6, hint=Z_AX)
        lower = yards[k - 1][0] + 0.25 if k else 1.3
        if k == 0 or True:
            zt = D + yz - 0.1;zb = D + (yards[k - 1][0] + 0.3 if k else 1.4)
            if k:
                sail(f"Sail {mx}-{k}", mx + 0.32, -half, half, zb, zt, 0.6, SAIL)
            else:
                sail(f"Sail {mx}-{k}", mx + 0.32, -half, half, D + 1.2, zt, 0.7, SAIL)
    for s in (-1, 1):                                    # shrouds
        for j in range(3):
            xx = mx - 0.5 + j * 0.45
            cyl(f"Shroud {mx}{s}{j}", V(xx, s * (half_beam(xx) - 0.05), deck_z(xx) + 0.8), V(mx, s * 0.12, D + mh * 0.78), 0.025, 0.025, ROPE, C_RIG, n=4)
D = deck_z(-0.6)
tube("Crows Nest", V(-0.6, 0, D + 8.35), Z_AX, X_AX, 0.65, 0.55, 0.55, DARKWOOD, C_RIG, n=14)
cyl("Crows Nest Floor", V(-0.6, 0, D + 8.07), V(-0.6, 0, D + 8.12), 0.62, 0.62, DARKWOOD, C_RIG, n=14)
torus("Crows Nest Band", V(-0.6, 0, D + 8.6), Z_AX, X_AX, 0.66, 0.04, GOLD, C_RIG, n_major=14, n_minor=4)
# Jolly Roger
FP = V(-0.6, 0, D + 9.3)
fl = [[FP + V(-0.05 - 1.9 * j / 5, 0.12 * math.sin(j * 1.3), -0.95 * i) for j in range(6)] for i in range(2)]
bm = bmesh.new()
vs = [[bm.verts.new(p) for p in r] for r in fl]
for j in range(5):
    bm.faces.new((vs[0][j], vs[0][j + 1], vs[1][j + 1], vs[1][j]))
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.04)
finish("Jolly Roger", bm, FLAG, C_RIG, merge=0)
SK = FP + V(-1.0, 0.0, -0.4)
for s in (-1, 1):
    ellip(f"Flag Skull {s}", SK + V(0, s * 0.1, 0.05), 0.26, 0.03, 0.24, BONE, C_RIG, n=12, m=3)
    for t in (-1, 1):
        dot(f"Flag Skull Eye {s}{t}", SK + V(t * 0.1, s * 0.13, 0.07), 0.06, FLAG, C_RIG)
    beam(f"Flag Bone A {s}", SK + V(-0.45, s * 0.1, -0.45), SK + V(0.45, s * 0.1, -0.15), 0.04, 0.08, Y_AX, BONE, C_RIG)
    beam(f"Flag Bone B {s}", SK + V(-0.45, s * 0.1, -0.15), SK + V(0.45, s * 0.1, -0.45), 0.04, 0.08, Y_AX, BONE, C_RIG)
# jib sail from bowsprit to foremast
blade("Jib Sail", [V(6.9, 0, BZ + 1.45), V(3.1, 0, deck_z(3.0) + 6.6), V(3.4, 0, deck_z(3.4) + 0.9)], 0.05, SAIL, C_RIG)
cyl("Forestay", V(7.1, 0, BZ + 1.55), V(3.0, 0, deck_z(3.0) + 7.0), 0.025, 0.025, ROPE, C_RIG, n=4)

# ---- the great cannon (fires ore over the side, toward -Y)
GX = 1.0;GD = deck_z(GX) + 0.1
abox("Gun Carriage", GX - 0.75, GX + 0.75, -1.5, 0.4, GD, GD + 0.7, DARKWOOD, C_GUNS)
abox("Carriage Step", GX - 0.75, GX + 0.75, -0.2, 0.9, GD, GD + 0.45, DARKWOOD, C_GUNS)
for sx in (-1, 1):
    for y in (-1.25, 0.55):
        cyl(f"Truck Wheel {sx}{y}", V(GX + sx * 0.8, y, GD + 0.3), V(GX + sx * 0.95, y, GD + 0.3), 0.3, 0.3, DARKWOOD, C_GUNS, n=12, hint=Z_AX)
    dot(f"Trunnion Cap {sx}", V(GX + sx * 0.78, -0.55, GD + 1.05), 0.14, GOLD, C_GUNS)
GZ = GD + 1.05
lathe_pts = [(0.62, -0.8), (0.6, 0.0), (0.56, 0.4), (0.5, 1.6), (0.46, 2.8), (0.44, 3.1), (0.56, 3.3), (0.58, 3.5), (0.42, 3.55)]
rings = [ring_pts(V(GX, 0.6 - z, GZ), Z_AX, X_AX, r, 22) for r, z in lathe_pts]
finish("Great Cannon", loft(rings, smooth_sides=True), IRON, C_GUNS, merge=0)
for k, y in enumerate((0.2, -0.95, -2.2)):
    cyl(f"Cannon Ring {k + 1}", V(GX, y + 0.08, GZ), V(GX, y - 0.08, GZ), 0.6 - 0.04 * k, 0.6 - 0.04 * k, GOLD, C_GUNS, n=22, hint=Z_AX)
dot("Cascabel", V(GX, 1.55, GZ), 0.22, GOLD, C_GUNS)
MZ = V(GX, -2.97, GZ)
cyl("Bore", MZ + V(0, 0.01, 0), MZ + V(0, -0.02, 0), 0.3, 0.3, FLAG, C_GUNS, n=16, hint=Z_AX)
for k in range(6):                                       # muzzle flash petals
    a = k * math.pi / 3;d = V(math.cos(a), 0, math.sin(a))
    cone(f"Muzzle Flash {k + 1}", MZ + d * 0.35 + V(0, -0.05, 0), MZ + d * 0.9 + V(0, -0.55, 0), 0.18, FLASH, C_GUNS, n=5)
for k, (dx, dy, dz, r) in enumerate(((0.3, -0.6, 0.5, 0.45), (-0.5, -0.4, 0.75, 0.55), (0.0, -0.1, 1.2, 0.5))):
    rock_f(f"Gun Smoke {k + 1}", MZ + V(dx, dy, dz), (r, r * 0.9, r * 0.8), SMOKE, C_GUNS, rough=0.18, subd=2)
ore_cube(MZ + V(0, -1.05, -0.05), ORE, C_GUNS, size=0.75)
for k, (dx, dy, dz) in enumerate(((0, 0, 0), (0.42, 0, 0), (0.84, 0, 0), (0.21, 0.36, 0), (0.63, 0.36, 0), (0.42, 0.18, 0.34))):
    dot(f"Cannonball {k + 1}", V(GX + 1.1 + dx, -1.1 + dy, GD + 0.21 + dz), 0.21, IRON, C_GUNS)

# ---- treasure chest, barrels, rope on deck
TC = V(-1.9, 0.6, deck_z(-1.9) + 0.1)
abox("Chest Body", TC.x - 0.55, TC.x + 0.55, TC.y - 0.38, TC.y + 0.38, TC.z, TC.z + 0.55, DARKWOOD, C_HULL)
for dx in (-0.4, 0.4):
    abox(f"Chest Strap {dx}", TC.x + dx - 0.06, TC.x + dx + 0.06, TC.y - 0.4, TC.y + 0.4, TC.z, TC.z + 0.57, GOLD, C_HULL)
hexa("Chest Lid", [V(TC.x - 0.55, TC.y + 0.38, TC.z + 0.55), V(TC.x + 0.55, TC.y + 0.38, TC.z + 0.55), V(TC.x + 0.55, TC.y + 0.5, TC.z + 0.55), V(TC.x - 0.55, TC.y + 0.5, TC.z + 0.55),
                   V(TC.x - 0.55, TC.y + 0.6, TC.z + 1.15), V(TC.x + 0.55, TC.y + 0.6, TC.z + 1.15), V(TC.x + 0.55, TC.y + 0.72, TC.z + 1.15), V(TC.x - 0.55, TC.y + 0.72, TC.z + 1.15)], DARKWOOD, C_HULL)
for k in range(16):
    dot(f"Coin {k + 1}", V(TC.x + rnd.uniform(-0.45, 0.45), TC.y + rnd.uniform(-0.3, 0.3), TC.z + 0.55 + rnd.uniform(0, 0.25)), 0.12, GOLD, C_HULL)
for k in range(6):
    p = V(TC.x + rnd.uniform(-0.9, 0.9), TC.y + rnd.uniform(-0.9, -0.45), TC.z + 0.05)
    cyl(f"Spilled Coin {k + 1}", p, p + V(0, 0, 0.04), 0.12, 0.12, GOLD, C_HULL, n=10)
crystal("Chest Ruby", V(TC.x + 0.15, TC.y, TC.z + 0.7), V(0.2, 0, 1), 0.45, 0.13, GEM, C_HULL)
for k, (x, y) in enumerate(((-2.2, -1.2), (-1.6, -1.35), (4.0, 0.6))):
    z = deck_z(x) + 0.1
    lathe(f"Barrel {k + 1}", V(x, y, z), [(0.28, 0), (0.34, 0.35), (0.34, 0.45), (0.28, 0.8)], DARKWOOD, C_HULL, n=12)
    for dz in (0.12, 0.68):
        torus(f"Barrel Hoop {k + 1}{dz}", V(x, y, z + dz), Z_AX, X_AX, 0.31, 0.03, IRON, C_HULL, n_major=12, n_minor=4)
torus("Rope Coil", V(2.2, 1.1, deck_z(2.2) + 0.15), Z_AX, X_AX, 0.32, 0.09, ROPE, C_HULL, n_major=14, n_minor=5)
torus("Rope Coil 2", V(2.2, 1.1, deck_z(2.2) + 0.3), Z_AX, X_AX, 0.24, 0.08, ROPE, C_HULL, n_major=14, n_minor=5)

# ---- sea: foam around the hull + palm islet + shark fin
for k, x in enumerate((-4.8, -3.0, -1.0, 1.0, 3.0, 4.6)):
    for s in (-1, 1):
        w = half_beam(x) * 1.0
        ellip(f"Foam {k}{s}", V(x, s * (w + 0.12), top + 0.02), 0.9, 0.25, 0.12, FOAM, C_SEA, n=10, m=2, half=True)
ellip("Bow Wave", V(5.6, 0, top + 0.02), 0.45, 1.1, 0.18, FOAM, C_SEA, n=12, m=2, half=True)
IS = V(-5.0, 3.9, top)
ellip("Islet Sand", IS, 1.9, 1.3, 0.4, BEACH, C_SEA, n=16, m=3, half=True)
for k in range(4):
    rock_f(f"Islet Rock {k + 1}", IS + V(rnd.uniform(-1.4, 1.4), rnd.uniform(-0.9, 0.9), 0.1), (0.45, 0.4, 0.4), ROCK, C_SEA, rough=0.3)
PT = [IS + V(0.3, 0, 0.3), IS + V(0.9, -0.2, 2.0), IS + V(1.7, -0.5, 3.4)]
path_tube("Palm Trunk", PT, [0.2, 0.16, 0.12], TRUNK, C_SEA, n=8)
for k in range(6):
    a = k * math.pi / 3
    d = V(math.cos(a), math.sin(a), 0)
    tipp = PT[-1] + d * 1.5 + V(0, 0, -0.6)
    blade(f"Palm Frond {k + 1}", [PT[-1], PT[-1] + d * 0.8 + V(-d.y, d.x, 0) * 0.32 + V(0, 0, 0.25), tipp, PT[-1] + d * 0.8 - V(-d.y, d.x, 0) * 0.32 + V(0, 0, 0.25)], 0.04, PALM, C_SEA)
for k in range(3):
    dot(f"Coconut {k + 1}", PT[-1] + V(0.15 * math.cos(k * 2.1), 0.15 * math.sin(k * 2.1), -0.15), 0.13, TRUNK, C_SEA)
SF = V(-4.6, -4.2, top)
blade("Shark Fin", [SF + V(-0.45, 0, 0), SF + V(0.4, 0, 0), SF + V(-0.25, 0, 0.85)], 0.1, IRON, C_SEA)
ellip("Fin Ripple", SF, 0.8, 0.35, 0.08, FOAM, C_SEA, n=12, m=2, half=True)
for k, (x, y) in enumerate(((6.0, -3.6), (-6.2, -1.0))):
    lathe(f"Floating Barrel {k + 1}", V(x, y, top - 0.15), [(0.3, 0), (0.36, 0.3), (0.3, 0.6)], DARKWOOD, C_SEA, n=10)

finish_mine(bg=(0.012, 0.02, 0.035), tint=(0.85, 0.92, 1.0))
