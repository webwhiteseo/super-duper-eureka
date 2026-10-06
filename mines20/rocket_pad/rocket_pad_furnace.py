"""Rocket Launchpad Furnace - a launch pad with a rocket standing on its gantry; the ramp feeds ore into the flame
trench beneath the rocket's roaring engines. Gantry tower, fuel tanks, flood lights, smoke. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_ROCKET, C_GANTRY, C_DETAIL = begin("RocketPadFurnace", ["Pad", "Rocket", "Gantry", "Details"], seed=171)
PAD = M("Launch Pad", (120, 122, 128), rough=0.8, rbx="Concrete", noise=((96, 98, 104), (146, 148, 152), 4.0, 0.3))
STRIPE = M("Pad Stripe", (240, 196, 20), rough=0.5)
WHITE = M("Rocket White", (238, 240, 244), rough=0.35)
RED = M("Rocket Red", (220, 40, 40), rough=0.35)
STEEL = M("Gantry Steel (Metal)", (140, 60, 40), rough=0.4, metal=0.6, rbx="Metal")
DARK = M("Engine Dark (Metal)", (50, 52, 58), rough=0.4, metal=0.9, rbx="Metal")
FLAME = M("Rocket Flame", (255, 170, 60), rough=0.3, glow=(255, 130, 20), glow_strength=5.0, rbx="Neon", light=(18, 2.4))
BLUE = M("Flame Core", (140, 200, 255), rough=0.3, glow=(100, 170, 255), glow_strength=6.0, rbx="Neon")
SMOKE = M("Smoke", (200, 200, 204), rough=0.9, rbx="SmoothPlastic", alpha=0.2)
WIN = M("Porthole", (120, 200, 255), rough=0.1, glow=(80, 170, 255), glow_strength=2.0, rbx="Neon")
LAMP = M("Flood Light", (255, 250, 220), rough=0.3, glow=(255, 240, 190), glow_strength=5.0, rbx="Neon", light=(10, 1.2))
CONVM = M("Conveyor", (50, 52, 58), rough=0.5, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (255, 170, 60), rough=0.2, glow=(255, 130, 20), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(171)
slab("Launch Pad", chamfer_rect(14.0, 12.5, 2.4), 0.0, chamfer_rect(13.4, 11.9, 2.2), 0.6, PAD, C_BASE)
for k in range(8):
    a = 2 * math.pi * k / 8
    beam(f"Pad Mark {k}", V(0, 0.4, 0.61) + V(math.cos(a), math.sin(a), 0) * 3.6, V(0, 0.4, 0.61) + V(math.cos(a), math.sin(a), 0) * 5.0, 0.3, 0.02, Z_AX, STRIPE, C_BASE)
conveyor_ramp(CONVM, STRIPE, DARK, STRIPE, y_end=-2.6, coll=C_BASE)
abox("Flame Trench", -2.8, 2.8, -2.6, 2.8, 0.0, 1.1, DARK, C_BASE)
abox("Trench Fire", -2.5, 2.5, -2.5, 2.5, 1.0, 1.25, FLAME, C_BASE)
burn_zone(BURN, -2.4, 2.4, -2.5, 2.5, 1.25, 2.0, C_BASE)
for s in (-1, 1):                                           # launch clamps holding the rocket
    abox(f"Launch Clamp {s}", min(s * 2.8, s * 3.6), max(s * 2.8, s * 3.6), -0.6, 1.4, 0.6, 3.4, DARK, C_GANTRY)
    beam(f"Clamp Arm {s}", V(s * 3.2, 0.4, 3.4), V(s * 1.6, 0.4, 4.4), 0.3, 0.3, Y_AX, DARK, C_GANTRY)
# rocket
R0 = V(0, 0.4, 3.6)
for k in range(4):                                          # engine bells + flames
    a = math.pi / 4 + k * math.pi / 2
    E = R0 + V(0.75 * math.cos(a), 0.75 * math.sin(a), 0)
    lathe(f"Engine Bell {k}", E + V(0, 0, -0.9), [(0.45, 0), (0.3, 0.6), (0.22, 0.9)], DARK, C_ROCKET, n=12)
    lathe(f"Engine Flame {k}", E + V(0, 0, -2.3), [(0.01, 0), (0.3, 0.6), (0.42, 1.35)], FLAME, C_ROCKET, n=10)
    lathe(f"Flame Core {k}", E + V(0, 0, -1.6), [(0.01, 0), (0.18, 0.4), (0.22, 0.7)], BLUE, C_ROCKET, n=8)
lathe("Rocket Body", R0, [(1.5, 0), (1.5, 6.5), (1.4, 7.5), (1.1, 8.6), (0.6, 9.6), (0.01, 10.2)], WHITE, C_ROCKET, n=24)
for z in (1.4, 4.6):
    torus(f"Body Band {z}", R0 + V(0, 0, z), Z_AX, Y_AX, 1.52, 0.18, RED, C_ROCKET, n_major=24, n_minor=4)
lathe("Nose Cone", R0 + V(0, 0, 8.6), [(1.12, 0), (0.62, 1.0), (0.01, 1.6)], RED, C_ROCKET, n=24)
for k in range(3):
    cyl(f"Porthole {k}", R0 + V(0, -1.45, 6.0 - k * 1.2), R0 + V(0, -1.58, 6.0 - k * 1.2), 0.3, 0.3, WIN, C_ROCKET, n=14, hint=Z_AX)
    torus(f"Porthole Rim {k}", R0 + V(0, -1.55, 6.0 - k * 1.2), Y_AX, Z_AX, 0.32, 0.06, DARK, C_ROCKET, n_major=14, n_minor=4)
for k in range(4):
    a = k * math.pi / 2
    d = V(math.cos(a), math.sin(a), 0)
    blade(f"Fin {k}", [R0 + d * 1.45 + V(0, 0, 0.2), R0 + d * 1.45 + V(0, 0, 2.6), R0 + d * 2.7 + V(0, 0, 0.2), R0 + d * 2.5 + V(0, 0, -0.4)], 0.15, RED, C_ROCKET)
# gantry tower beside
G = V(4.4, 2.6, 0.6)
for sx in (-1, 1):
    for sy in (-1, 1):
        beam(f"Gantry Leg {sx}{sy}", G + V(sx * 0.8, sy * 0.8, 0), G + V(sx * 0.8, sy * 0.8, 12.0), 0.22, 0.22, X_AX, STEEL, C_GANTRY)
for k in range(8):
    z = 1.0 + k * 1.5
    for (a, b) in (((-0.8, -0.8), (0.8, -0.8)), ((0.8, -0.8), (0.8, 0.8)), ((0.8, 0.8), (-0.8, 0.8)), ((-0.8, 0.8), (-0.8, -0.8))):
        beam(f"Gantry Girt {k}{a}{b}", G + V(a[0], a[1], z), G + V(b[0], b[1], z), 0.12, 0.12, Z_AX, STEEL, C_GANTRY)
    beam(f"Gantry Brace {k}", G + V(-0.8, -0.8, z), G + V(0.8, -0.8, z + 1.5), 0.08, 0.08, Y_AX, STEEL, C_GANTRY)
for k, z in enumerate((5.0, 8.4)):
    beam(f"Access Arm {k}", G + V(-0.8, -0.4, z), R0 + V(1.5, 0.2, z - 0.6), 0.6, 0.3, Z_AX, STEEL, C_GANTRY)
dot("Gantry Beacon", G + V(0, 0, 12.3), 0.3, FLAME, C_GANTRY)
# fuel tanks, flood lights, smoke
for k, x in enumerate((-4.4, -5.6)):
    cyl(f"Fuel Tank {k}", V(x, 3.4, 0.6), V(x, 3.4, 3.6), 0.6, 0.6, WHITE, C_DETAIL, n=16)
    lathe(f"Tank Dome {k}", V(x, 3.4, 3.6), [(0.6, 0), (0.4, 0.3), (0.01, 0.45)], WHITE, C_DETAIL, n=16)
    torus(f"Tank Band {k}", V(x, 3.4, 2.0), Z_AX, Y_AX, 0.62, 0.06, RED, C_DETAIL, n_major=16, n_minor=4)
for s in (-1, 1):
    P = V(s * 5.6, -4.4, 0.6)
    cyl(f"Flood Pole {s}", P, P + V(0, 0, 4.0), 0.1, 0.1, DARK, C_DETAIL, n=6)
    obox(f"Flood Lamp {s}", P + V(0, 0, 4.2), (0.9, 0.3, 0.6), X_AX, (V(-s * 0.6, 0.8, -0.3)).normalized(), V(0, 0.3, 0.95).normalized(), LAMP, C_DETAIL)
for k in range(6):
    a = rnd.uniform(0, 6.28)
    rock_f(f"Launch Smoke {k}", V(3.2 * math.cos(a), 0.4 + 2.4 * math.sin(a) + 1.0, 1.0 + rnd.uniform(0, 0.6)), (0.9, 0.8, 0.6), SMOKE, C_DETAIL, rough=0.2, subd=2)
finish_mine(bg=(0.012, 0.016, 0.03), tint=(0.9, 0.92, 1.0))
write_furnace_lua("RocketPadFurnace")
