"""Singularity Furnace - a hexagonal hover platform on glowing pads, a swirling accretion vortex that sells the ore,
and a black hole held in golden claws above with a blazing accretion ring, orbit rings and stardust streaming down.
Conveyor ramp straight into the vortex. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_VORTEX, C_HOLE, C_DETAIL = begin("SingularityFurnace", ["Hover Platform", "Vortex", "Black Hole", "Details"], seed=71)
HULL = M("Hull Plate (DiamondPlate)", (34, 30, 48), rough=0.35, metal=0.7, rbx="DiamondPlate", plate=8.0)
GOLD = M("Gold (Metal)", (236, 186, 70), rough=0.25, metal=1.0, rbx="Metal")
VOIDM = M("Event Horizon", (4, 2, 8), rough=0.05, metal=0.4)
DISK = M("Accretion Glow", (255, 170, 90), rough=0.3, glow=(255, 130, 60), glow_strength=5.0, rbx="Neon", light=(18, 2.2))
PURP = M("Void Neon", (190, 110, 255), rough=0.3, glow=(160, 70, 255), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
VORT = M("Vortex Swirl", (150, 80, 255), rough=0.2, glow=(130, 50, 255), glow_strength=3.0, rbx="Neon", light=(14, 1.8))
DUST = M("Stardust", (255, 230, 200), rough=0.3, glow=(255, 210, 160), glow_strength=4.0, rbx="Neon")
CONVM = M("Conveyor", (40, 34, 58), rough=0.4, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (170, 110, 255), rough=0.2, glow=(140, 70, 255), glow_strength=1.0, rbx="ForceField", alpha=0.6)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(71)

# ---- hexagonal hover platform on glowing pads
HC = V(0, 0.6, 0)
lathe("Hex Deck", HC + V(0, 0, 0.45), [(6.6, 0), (6.9, 0.3), (6.9, 0.55), (6.4, 0.65), (0.01, 0.65)], HULL, C_BASE, n=6, smooth=False)
lathe("Hex Trim", HC + V(0, 0, 0.83), [(6.95, 0), (6.95, 0.1)], GOLD, C_BASE, n=6, smooth=False)
for k in range(6):
    a = 2 * math.pi * k / 6
    P = HC + V(5.3 * math.cos(a), 5.3 * math.sin(a), 0)
    cyl(f"Hover Leg {k}", P + V(0, 0, 0.0), P + V(0, 0, 0.5), 0.55, 0.45, HULL, C_BASE, n=10)
    cyl(f"Hover Pad {k}", P, P + V(0, 0, 0.08), 0.75, 0.75, PURP, C_BASE, n=14)
    abox(f"Deck Light {k}", P.x - 0.25, P.x + 0.25, P.y - 0.25, P.y + 0.25, 1.1, 1.14, PURP, C_BASE)

# ---- accretion vortex intake (open front for the ramp)
VC = V(0, 0.0, 1.1)
lathe("Vortex Dish", VC + V(0, 0, -0.25), [(2.8, 0.35), (1.6, 0.1), (0.4, -0.2), (0.01, -0.25)], VOIDM, C_VORTEX, n=28)
for k in range(6):
    pts = []
    for i in range(10):
        t = i / 9;a = 2 * math.pi * k / 6 + t * 3.0;r = 0.3 + 2.4 * t
        pts.append(VC + V(r * math.cos(a), r * math.sin(a), -0.35 + 0.4 * t))
    path_tube(f"Swirl Arm {k}", pts, [0.06 + 0.1 * (i / 9) for i in range(10)], VORT, C_VORTEX, n=5)
for k in range(10):
    a0 = math.radians(-50 + k * 28);a1 = a0 + math.radians(26)
    p = [V(r * math.cos(a), r * math.sin(a), 0) for r, a in ((2.9, a0), (3.5, a0), (3.5, a1), (2.9, a1))]
    hexa(f"Vortex Rim {k}", [VC + q for q in p] + [VC + q + V(0, 0, 0.6) for q in p], HULL, C_VORTEX)
    m = (a0 + a1) / 2
    abox(f"Rim Light {k}", VC.x + 3.2 * math.cos(m) - 0.12, VC.x + 3.2 * math.cos(m) + 0.12, VC.y + 3.2 * math.sin(m) - 0.12, VC.y + 3.2 * math.sin(m) + 0.12, 1.7, 1.75, PURP, C_VORTEX)
burn_zone(BURN, -2.5, 2.5, -2.6, 2.6, 1.0, 1.9, C_VORTEX)
conveyor_ramp(CONVM, PURP, HULL, GOLD, y_end=-2.6, coll=C_BASE)

# ---- black hole held by golden claws
BH = V(0, 3.4, 8.2)
dot("Event Horizon", BH, 1.5, VOIDM, C_HOLE) if False else sphere("Event Horizon", BH, 1.5, VOIDM, C_HOLE)
tube("Accretion Ring", BH, V(0.15, -0.35, 1).normalized(), Y_AX, 3.3, 1.75, 0.12, DISK, C_HOLE, n=48)
torus("Photon Ring", BH, V(0, -1, 0.1).normalized(), Z_AX, 1.65, 0.07, DUST, C_HOLE, n_major=36, n_minor=4)
for k, (ax, R) in enumerate(((V(1, 0.2, 0.3), 4.0), (V(-0.4, 1, 0.6), 4.4))):
    torus(f"Orbit Ring {k}", BH, ax.normalized(), perp_basis(ax.normalized())[0], R, 0.06, GOLD, C_HOLE, n_major=48, n_minor=4)
for k in range(3):
    a = math.radians(90 + 120 * k)
    d = V(math.cos(a), math.sin(a), 0)
    base = V(BH.x + d.x * 4.6, BH.y + d.y * 3.2, 1.1)
    pts = [base, base + V(0, 0, 2.5) - d * 0.3, BH + d * 3.2 + V(0, 0, -2.4), BH + d * 2.4 + V(0, 0, -1.2), BH + d * 1.9 + V(0, 0, 0.3)]
    path_tube(f"Gold Claw {k}", pts, [0.4, 0.34, 0.28, 0.2, 0.06], GOLD, C_HOLE, n=8)
    dot(f"Claw Gem {k}", pts[2], 0.25, PURP, C_HOLE)
for k in range(9):                                           # stardust spiralling down into the vortex
    t = k / 8
    a = t * 4.0
    p = BH + (VC + V(0, 0, 0.6) - BH) * t + V(1.3 * (1 - t) * math.cos(a), 1.3 * (1 - t) * math.sin(a), 0)
    dot(f"Stardust {k}", p, 0.16 - 0.08 * t, DUST, C_HOLE)

# ---- pylons with orbs + floating debris
for k, (x, y) in enumerate(((-4.4, 3.6), (4.4, 3.6), (-5.0, -1.2), (5.0, -1.2))):
    cyl(f"Pylon {k}", V(x, y, 1.1), V(x, y, 4.2), 0.25, 0.15, HULL, C_DETAIL, n=6)
    torus(f"Pylon Ring {k}", V(x, y, 3.0), Z_AX, Y_AX, 0.32, 0.06, GOLD, C_DETAIL, n_major=12, n_minor=4)
    dot(f"Pylon Orb {k}", V(x, y, 4.5), 0.35, PURP, C_DETAIL)
for k in range(6):
    a = rnd.uniform(0, 6.28)
    rock_f(f"Debris {k}", BH + V(5.2 * math.cos(a), 2.0 * math.sin(a), rnd.uniform(-1.5, 2.5)), (0.35, 0.3, 0.25), HULL, C_DETAIL, rough=0.35)

finish_mine(bg=(0.012, 0.008, 0.03), tint=(0.85, 0.75, 1.0))
write_furnace_lua("SingularityFurnace")
