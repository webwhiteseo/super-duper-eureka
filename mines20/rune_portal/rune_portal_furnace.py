"""Rune Portal Furnace - an ancient stone portal ring standing on a mossy stone circle, its swirling gateway touching
the ground at the front so conveyors run ore straight into it (no ramp). Standing stones with glowing runes,
floating rocks and crystals. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_PORTAL, C_STONES, C_DETAIL = begin("RunePortalFurnace", ["Stone Circle", "Portal", "Standing Stones", "Details"], seed=101)
STONE = M("Ancient Stone", (120, 118, 112), rough=0.9, rbx="Slate", noise=((90, 88, 84), (150, 148, 140), 3.0, 0.5))
DARKST = M("Dark Stone", (70, 70, 74), rough=0.85, rbx="Slate", noise=((50, 50, 54), (94, 94, 98), 4.0, 0.4))
MOSS = M("Moss", (70, 120, 50), rough=0.9, rbx="Grass")
RUNE = M("Rune Glow", (90, 255, 210), rough=0.3, glow=(40, 255, 190), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
PORTAL = M("Portal Swirl", (120, 200, 255), rough=0.2, glow=(70, 170, 255), glow_strength=3.5, rbx="Neon", light=(18, 2.2))
PORTAL2 = M("Portal Arms", (220, 255, 255), rough=0.2, glow=(170, 255, 255), glow_strength=6.0, rbx="Neon")
CRYS = M("Rune Crystal", (120, 255, 220), rough=0.05, glow=(60, 230, 190), glow_strength=1.2, rbx="Glass", alpha=0.2)
GOLD = M("Old Bronze (Metal)", (170, 130, 70), rough=0.4, metal=0.8, rbx="Metal")
BURN = M("Burn Zone", (100, 200, 255), rough=0.2, glow=(60, 170, 255), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(101)

# ---- mossy stone circle (flagstones)
lathe("Circle Base", V(0, 1.0, 0), [(6.8, 0), (6.8, 0.2), (6.5, 0.3), (0.01, 0.3)], DARKST, C_BASE, n=24, smooth=False)
for ring, (r0, r1, n) in enumerate(((1.4, 3.6, 8), (3.7, 6.3, 14))):
    for k in range(n):
        a0 = 2 * math.pi * k / n + 0.03;a1 = 2 * math.pi * (k + 1) / n - 0.03
        p = [V(r * math.cos(a), 1.0 + r * math.sin(a), 0) for r, a in ((r0, a0), (r1, a0), (r1, a1), (r0, a1))]
        hexa(f"Flagstone {ring}{k}", [q + V(0, 0, 0.3) for q in p] + [q + V(0, 0, 0.42) for q in p], STONE, C_BASE)
for k in range(7):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(2, 6)
    ellip(f"Moss {k}", V(r * math.cos(a), 1.0 + r * math.sin(a), 0.42), rnd.uniform(0.5, 1.0), rnd.uniform(0.4, 0.8), 0.12, MOSS, C_BASE, n=10, m=2, half=True)

# ---- portal ring standing at the front, opening down to the ground
PC = V(0, -2.4, 2.6);PR = 2.9
tube("Portal Ring", PC, Y_AX, Z_AX, PR + 0.9, PR, 1.0, STONE, C_PORTAL, n=36)
cyl("Portal Surface", PC + V(0, 0.08, 0), PC + V(0, -0.08, 0), PR, PR, PORTAL, C_PORTAL, n=36, hint=Z_AX)
for k in range(6):
    pts = []
    for i in range(10):
        t = i / 9;a = 2 * math.pi * k / 6 + t * 3.2;r = 0.15 + (PR - 0.25) * t
        pts.append(PC + V(r * math.cos(a), -0.12, r * math.sin(a)))
    path_tube(f"Portal Arm {k}", pts, [0.05 + 0.07 * (i / 9) for i in range(10)], PORTAL2, C_PORTAL, n=5)
for k in range(12):                                         # rune stones set into the ring face
    a = 2 * math.pi * k / 12 + math.pi / 12
    d = V(math.cos(a), 0, math.sin(a));t = V(-math.sin(a), 0, math.cos(a))
    obox(f"Ring Rune {k}", PC + d * (PR + 0.45) + V(0, -0.52, 0), (0.45, 0.06, 0.55), t, Y_AX, d, RUNE, C_PORTAL)
    if k % 3 == 0:
        obox(f"Ring Keystone {k}", PC + d * (PR + 1.0), (0.9, 1.2, 0.6), t, Y_AX, d, DARKST, C_PORTAL)
for s in (-1, 1):                                           # buttress pillars holding the ring
    abox(f"Ring Pillar {s}", s * (PR + 0.6) - 0.6, s * (PR + 0.6) + 0.6, -3.2, -1.6, 0.3, 4.2, DARKST, C_PORTAL)
    abox(f"Pillar Cap {s}", s * (PR + 0.6) - 0.75, s * (PR + 0.6) + 0.75, -3.35, -1.45, 4.2, 4.6, STONE, C_PORTAL)
    crystal(f"Pillar Crystal {s}", V(s * (PR + 0.6), -2.4, 4.6), Z_AX, 1.4, 0.35, CRYS, C_PORTAL, sides=5)
    abox(f"Pillar Rune {s}", s * (PR + 0.6) - 0.15, s * (PR + 0.6) + 0.15, -3.22, -3.18, 1.0, 3.4, RUNE, C_PORTAL)
burn_zone(BURN, -2.4, 2.4, -3.0, -1.8, 0.05, 2.6, C_PORTAL)

# ---- standing stones in a half circle behind
for k in range(7):
    a = math.radians(20 + k * 23.3)
    c = V(5.3 * math.cos(a), 1.0 + 5.3 * math.sin(a), 0)
    h = 3.6 + 1.2 * math.sin(a)
    t = V(-math.sin(a), math.cos(a), 0)
    obox(f"Standing Stone {k}", c + V(0, 0, h / 2 + 0.3), (1.1, 0.6, h), t, V(math.cos(a), math.sin(a), 0), Z_AX, STONE, C_STONES)
    obox(f"Stone Rune {k}", c + V(0, 0, h * 0.55 + 0.3) - V(math.cos(a), math.sin(a), 0) * 0.31, (0.2, 0.04, h * 0.5), t, V(math.cos(a), math.sin(a), 0), Z_AX, RUNE, C_STONES)
    if k in (2, 4):                                         # lintel stones
        a2 = math.radians(20 + (k + 1) * 23.3)
        c2 = V(5.3 * math.cos(a2), 1.0 + 5.3 * math.sin(a2), 0)
        beam(f"Lintel {k}", c + V(0, 0, h + 0.6), c2 + V(0, 0, 3.6 + 1.2 * math.sin(a2) + 0.6), 0.7, 0.6, Z_AX, DARKST, C_STONES)
# ---- altar, floating rocks, crystals, braziers
abox("Altar", -1.2, 1.2, 2.2, 3.6, 0.42, 1.4, DARKST, C_DETAIL)
crystal_cluster("Altar Crystals", V(0, 2.9, 1.4), 5, 0.4, CRYS, STONE, C_DETAIL, seed=3)
for k in range(5):
    a = rnd.uniform(0, 6.28)
    p = V(3.2 * math.cos(a), 0.0 + 1.6 * math.sin(a), rnd.uniform(6.5, 8.5))
    rock_f(f"Floating Rock {k}", p, (0.5, 0.45, 0.4), STONE, C_DETAIL, rough=0.3)
    cone(f"Rock Drip {k}", p + V(0, 0, -0.3), p + V(0, 0, -1.0), 0.2, RUNE, C_DETAIL, n=4)
for s in (-1, 1):
    B = V(s * 4.4, -4.6, 0)
    lathe(f"Brazier {s}", B, [(0.5, 0), (0.3, 0.3), (0.25, 1.4), (0.55, 1.7), (0.6, 1.9), (0.45, 1.9)], GOLD, C_DETAIL, n=8, smooth=False)
    lathe(f"Brazier Flame {s}", B + V(0, 0, 1.85), [(0.4, 0), (0.25, 0.5), (0.0, 1.0)], RUNE, C_DETAIL, n=8)

finish_mine(bg=(0.014, 0.024, 0.03), tint=(0.8, 0.95, 1.0))
write_furnace_lua("RunePortalFurnace")
