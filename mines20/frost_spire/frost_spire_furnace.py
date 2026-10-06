"""Frost Spire Furnace - round tiered ice base, a frozen well that sells the ore, a giant floating ice spire with
orbit rings and shards, ice pillars and frost lanterns. Conveyor ramp straight into the well. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_WELL, C_SPIRE, C_DETAIL = begin("FrostSpireFurnace", ["Base", "Well", "Spire", "Details"], seed=51)
ICE = M("Packed Ice", (170, 214, 240), rough=0.25, rbx="Ice", noise=((140, 190, 226), (210, 236, 250), 2.5, 0.15))
SNOW = M("Snow", (242, 248, 255), rough=0.8, rbx="Snow")
STEEL = M("Frost Steel (Metal)", (120, 140, 168), rough=0.3, metal=0.85, rbx="Metal")
DARK = M("Deep Ice", (30, 60, 110), rough=0.2, rbx="Glacier")
WELL = M("Frost Well", (140, 230, 255), rough=0.05, glow=(80, 210, 255), glow_strength=3.0, rbx="Neon", light=(16, 2.0))
GLOW = M("Frost Neon", (160, 240, 255), rough=0.3, glow=(100, 220, 255), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
CRYS = M("Ice Crystal", (170, 230, 255), rough=0.05, glow=(110, 200, 255), glow_strength=1.0, rbx="Glass", alpha=0.2, light=(10, 1.0))
CORE = M("Spire Core", (230, 250, 255), rough=0.2, glow=(170, 235, 255), glow_strength=7.0, rbx="Neon", light=(20, 2.4))
CONVM = M("Conveyor", (60, 84, 116), rough=0.4, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (150, 230, 255), rough=0.2, glow=(100, 210, 255), glow_strength=1.0, rbx="ForceField", alpha=0.6)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(51)

# ---- round tiered ice base
lathe("Ice Disc Low", V(0, 0.5, 0), [(7.2, 0), (7.2, 0.35), (6.8, 0.6), (0.01, 0.6)], ICE, C_BASE, n=28, smooth=False)
lathe("Ice Disc Top", V(0, 0.5, 0.6), [(6.0, 0), (6.0, 0.3), (5.7, 0.5), (0.01, 0.5)], DARK, C_BASE, n=28, smooth=False)
torus("Disc Glow", V(0, 0.5, 0.62), Z_AX, Y_AX, 6.35, 0.06, GLOW, C_BASE, n_major=40, n_minor=4)
for k in range(12):
    a = 2 * math.pi * k / 12 + 0.2
    if -2.2 < math.degrees(a) % 360 - 270 < 2.2 or 250 < math.degrees(a) % 360 < 290:
        continue
    ellip(f"Snow Drift {k}", V(6.4 * math.cos(a), 0.5 + 6.4 * math.sin(a), 0.6), 1.0, 0.7, 0.35, SNOW, C_BASE, n=12, m=3, half=True)

# ---- frozen well (rim open at the front for the ramp)
WC = V(0, 0.0, 1.1)
lathe("Well Liquid", WC + V(0, 0, -0.2), [(2.9, 0), (2.9, 0.35)], WELL, C_WELL, n=28)
for k in range(14):
    a0 = math.radians(-60 + k * (300 / 14));a1 = math.radians(-60 + (k + 1) * (300 / 14))
    if True:
        p = [V(r * math.cos(a), r * math.sin(a), 0) for r, a in ((2.95, a0), (3.6, a0), (3.6, a1), (2.95, a1))]
        hexa(f"Well Rim {k}", [WC + q for q in p] + [WC + q + V(0, 0, 0.9) for q in p], ICE, C_WELL)
        if k % 2 == 0:
            m = (a0 + a1) / 2
            crystal(f"Rim Crystal {k}", WC + V(3.3 * math.cos(m), 3.3 * math.sin(m), 0.85), V(math.cos(m) * 0.3, math.sin(m) * 0.3, 1), 1.0, 0.2, CRYS, C_WELL, sides=5)
torus("Well Glow", WC + V(0, 0, 0.92), Z_AX, Y_AX, 3.28, 0.05, GLOW, C_WELL, n_major=40, n_minor=4)
burn_zone(BURN, -2.5, 2.5, -2.6, 2.6, 1.15, 2.0, C_WELL)
conveyor_ramp(CONVM, GLOW, STEEL, GLOW, y_end=-2.6, coll=C_BASE)

# ---- floating ice spire with orbit rings
SP = V(0, 3.6, 7.6)
crystal("Spire Up", SP, Z_AX, 5.2, 1.0, CRYS, C_SPIRE, sides=6)
crystal("Spire Down", SP, -Z_AX, 3.0, 1.0, CRYS, C_SPIRE, sides=6)
dot("Spire Core", SP + V(0, 0, 0.6), 0.6, CORE, C_SPIRE)
for k, (ax, R) in enumerate(((V(0.3, -0.2, 1), 2.4), (V(1, 0.4, 0.5), 2.9), (V(-0.6, 1, 0.4), 3.3))):
    torus(f"Orbit Ring {k}", SP + V(0, 0, 0.6), ax, perp_basis(ax.normalized())[0], R, 0.07, STEEL if k % 2 else GLOW, C_SPIRE, n_major=40, n_minor=4)
for k in range(8):
    a = 2 * math.pi * k / 8
    c = SP + V(3.8 * math.cos(a), 3.8 * math.sin(a) * 0.6, 0.6 + 1.2 * math.sin(2 * a))
    crystal(f"Orbit Shard {k}a", c, V(math.cos(a), math.sin(a), 0.6), 0.6, 0.18, CRYS, C_SPIRE, sides=4)
    crystal(f"Orbit Shard {k}b", c, -V(math.cos(a), math.sin(a), 0.6), 0.4, 0.18, CRYS, C_SPIRE, sides=4)
# cradle claws holding the spire
for k in range(3):
    a = math.radians(90 + 120 * k)
    d = V(math.cos(a), math.sin(a), 0)
    pts = [SP + d * 3.2 + V(0, 0, -4.6), SP + d * 2.6 + V(0, 0, -3.4), SP + d * 1.8 + V(0, 0, -2.2), SP + d * 1.3 + V(0, 0, -1.4)]
    pts[0] = V(pts[0].x, pts[0].y, 1.1)
    path_tube(f"Cradle Claw {k}", pts, [0.32, 0.26, 0.2, 0.08], STEEL, C_SPIRE, n=8)
    dot(f"Claw Light {k}", pts[2], 0.18, GLOW, C_SPIRE)

# ---- ice pillars + frost lanterns + snowflake emblems
for k, (x, y, h) in enumerate(((-4.6, 2.6, 4.8), (4.6, 2.6, 4.8), (-5.0, -1.8, 3.2), (5.0, -1.8, 3.2))):
    crystal(f"Ice Pillar {k}", V(x, y, 1.0), V(0.05 * x, 0.05 * y, 1), h, 0.55, ICE, C_DETAIL, sides=6)
    crystal(f"Pillar Shard {k}", V(x + 0.4, y, 1.0), V(0.4, 0.1, 1), h * 0.5, 0.3, CRYS, C_DETAIL, sides=5)
    dot(f"Pillar Glow {k}", V(x, y, 1.0 + h * 0.65), 0.25, GLOW, C_DETAIL)
for s in (-1, 1):
    P = V(s * 3.6, -4.6, 0.6)
    post_lantern(f"Frost Lantern {s}", P, 1.8, STEEL, GLOW, ICE, C_DETAIL, r=0.32)
    F = V(s * 4.6, -0.3, 1.6)
    for k in range(6):
        a = k * math.pi / 3
        d = V(0, math.cos(a), math.sin(a)) * 0 + V(math.cos(a) * 0.0, 0, 0)
    for k in range(6):
        a = k * math.pi / 3
        d = V(0.0, math.cos(a), math.sin(a))
        beam(f"Flake Arm {s}{k}", F, F + d * 0.7, 0.08, 0.06, X_AX, GLOW, C_DETAIL)

finish_mine(bg=(0.012, 0.02, 0.04), tint=(0.75, 0.88, 1.0))
write_furnace_lua("FrostSpireFurnace")
