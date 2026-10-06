"""Solar Crucible Furnace - a white marble octagon with gold inlays; a ramp leads ore into a golden crucible of molten
gold, lit by six mirror towers beaming sunlight into it under a floating sun disc. Obelisks and gold braziers.
mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_CRUC, C_MIRROR, C_SUN = begin("SolarCrucibleFurnace", ["Marble", "Crucible", "Mirrors", "Sun"], seed=121)
MARBLE = M("White Marble (Marble)", (238, 234, 226), rough=0.3, marble=((228, 224, 214), (200, 170, 110)))
GOLD = M("Gold (Metal)", (240, 190, 70), rough=0.22, metal=1.0, rbx="Metal")
MOLTEN = M("Molten Gold", (255, 200, 70), rough=0.2, glow=(255, 170, 30), glow_strength=4.0, rbx="Neon", light=(16, 2.2))
MIRROR = M("Mirror (Glass)", (200, 220, 240), rough=0.02, metal=1.0, rbx="Glass")
BEAM = M("Sun Beam", (255, 240, 170), rough=0.3, glow=(255, 220, 120), glow_strength=5.0, rbx="Neon", alpha=0.3)
SUN = M("Sun Core", (255, 230, 140), rough=0.3, glow=(255, 190, 60), glow_strength=8.0, rbx="Neon", light=(22, 2.6))
LAPIS = M("Lapis", (40, 70, 170), rough=0.3)
CONVM = M("Conveyor", (180, 170, 150), rough=0.5, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (255, 200, 80), rough=0.2, glow=(255, 170, 40), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)

# ---- marble octagon with gold inlays
lathe("Octagon Base", V(0, 0.8, 0), [(7.0, 0), (7.0, 0.5), (6.6, 0.75), (0.01, 0.75)], MARBLE, C_BASE, n=8, smooth=False)
lathe("Octagon Inlay", V(0, 0.8, 0.75), [(6.0, 0), (6.0, 0.03), (5.7, 0.03), (5.7, 0)], GOLD, C_BASE, n=8, smooth=False)
for k in range(8):
    a = 2 * math.pi * k / 8 + math.pi / 8
    if 240 < math.degrees(a) % 360 < 300:
        continue
    d = V(math.cos(a), math.sin(a), 0)
    beam(f"Inlay Ray {k}", V(0, 0.8, 0.76) + d * 3.8, V(0, 0.8, 0.76) + d * 5.7, 0.2, 0.04, Z_AX, GOLD, C_BASE)
# ---- crucible (rim open at the front for the ramp)
CC = V(0, 0.0, 0.75)
lathe("Molten Pool", CC, [(2.8, 0), (2.8, 0.45)], MOLTEN, C_CRUC, n=24)
for k in range(12):
    a0 = math.radians(-55 + k * 24.2);a1 = a0 + math.radians(23)
    p = [V(r * math.cos(a), r * math.sin(a), 0) for r, a in ((2.85, a0), (3.5, a0), (3.5, a1), (2.85, a1))]
    hexa(f"Crucible Rim {k}", [CC + q for q in p] + [CC + q + V(0, 0, 1.0) for q in p], GOLD, C_CRUC)
    if k % 3 == 1:
        m = (a0 + a1) / 2
        dot(f"Rim Gem {k}", CC + V(3.5 * math.cos(m), 3.5 * math.sin(m), 0.6), 0.22, LAPIS, C_CRUC)
burn_zone(BURN, -2.5, 2.5, -2.6, 2.6, 1.15, 2.0, C_CRUC)
conveyor_ramp(CONVM, GOLD, MARBLE, GOLD, y_end=-2.6, coll=C_BASE)
# ---- mirror towers beaming into the crucible
TGT = CC + V(0, 0, 0.6)
for k in range(6):
    a = math.radians(15 + k * 30)
    P = V(5.4 * math.cos(a), 0.8 + 5.2 * math.sin(a), 0.75)
    h = 4.2 + 0.6 * math.sin(a)
    cyl(f"Mirror Post {k}", P, P + V(0, 0, h), 0.2, 0.15, GOLD, C_MIRROR, n=8)
    M0 = P + V(0, 0, h + 0.7)
    n_ = (TGT - M0 + V(0, 0, 9.0)).normalized()          # bisector between sun and crucible
    u, v = perp_basis(n_)
    obox(f"Mirror {k}", M0, (1.6, 1.6, 0.08), u, v, n_, MIRROR, C_MIRROR)
    obox(f"Mirror Frame {k}", M0 - n_ * 0.07, (1.8, 1.8, 0.06), u, v, n_, GOLD, C_MIRROR)
    cyl(f"Sun Beam {k}", M0, TGT + (M0 - TGT).normalized() * 0.4, 0.09, 0.14, BEAM, C_MIRROR, n=6)
# ---- floating sun disc with rays + obelisks
SC = V(0, 2.4, 10.4)
dot("Sun Core", SC, 1.3, SUN, C_SUN)
torus("Sun Ring", SC, V(0, -1, 0.2).normalized(), Z_AX, 1.7, 0.12, GOLD, C_SUN, n_major=32, n_minor=5)
for k in range(12):
    a = 2 * math.pi * k / 12
    d = V(math.cos(a), 0, math.sin(a))
    blade(f"Sun Ray {k}", [SC + d * 1.85 + V(-math.sin(a), 0, math.cos(a)) * 0.25, SC + d * (3.0 if k % 2 else 2.4), SC + d * 1.85 - V(-math.sin(a), 0, math.cos(a)) * 0.25], 0.12, GOLD, C_SUN)
for k in range(3):
    cyl(f"Sun Beam Down {k}", SC + V(-0.6 + 0.6 * k, 0, -1.3), TGT + V(-0.6 + 0.6 * k, 0, 0.4), 0.06, 0.06, BEAM, C_SUN, n=6)
for s in (-1, 1):
    O = V(s * 5.6, -3.2, 0.75)
    hexa(f"Obelisk {s}", [O + V(-0.5, -0.5, 0), O + V(0.5, -0.5, 0), O + V(0.5, 0.5, 0), O + V(-0.5, 0.5, 0),
                          O + V(-0.3, -0.3, 4.2), O + V(0.3, -0.3, 4.2), O + V(0.3, 0.3, 4.2), O + V(-0.3, 0.3, 4.2)], MARBLE, C_SUN)
    cone(f"Obelisk Tip {s}", O + V(0, 0, 4.2), O + V(0, 0, 4.9), 0.42, GOLD, C_SUN, n=4)
    abox(f"Obelisk Glyph {s}", O.x - 0.12, O.x + 0.12, O.y - 0.47, O.y - 0.43, 1.0, 3.6, LAPIS, C_SUN)
    B = V(s * 3.9, -5.4, 0.0)
    lathe(f"Brazier {s}", B, [(0.5, 0), (0.3, 0.3), (0.25, 1.3), (0.55, 1.6), (0.6, 1.8), (0.45, 1.8)], GOLD, C_SUN, n=8, smooth=False)
    lathe(f"Brazier Flame {s}", B + V(0, 0, 1.75), [(0.38, 0), (0.25, 0.5), (0.0, 1.0)], MOLTEN, C_SUN, n=8)

finish_mine(bg=(0.03, 0.026, 0.016), tint=(1.0, 0.95, 0.85))
write_furnace_lua("SolarCrucibleFurnace")
