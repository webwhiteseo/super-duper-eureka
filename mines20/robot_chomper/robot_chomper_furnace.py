"""Robot Chomper Furnace - a giant robot head sits on a tracked metal base; the ramp carries ore into its wide open
jaw where a glowing grinder eats it. LED screen eyes, antenna, ear speakers, piston jaw, warning stripes.
mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_HEAD, C_DETAIL = begin("RobotChomperFurnace", ["Tracked Base", "Robot Head", "Details"], seed=211)
STEEL = M("Robot Steel (Metal)", (170, 176, 186), rough=0.25, metal=0.9, rbx="Metal")
BLUE = M("Robot Blue", (40, 110, 220), rough=0.35, metal=0.3)
DARK = M("Dark Panel", (30, 32, 40), rough=0.4)
TREAD = M("Tread Rubber", (26, 26, 30), rough=0.8)
HAZ = M("Hazard Yellow", (240, 196, 20), rough=0.45)
EYE = M("LED Eyes", (80, 255, 255), rough=0.2, glow=(30, 240, 255), glow_strength=6.0, rbx="Neon", light=(10, 1.4))
MOUTH = M("Grinder Glow", (255, 80, 60), rough=0.2, glow=(255, 50, 30), glow_strength=4.5, rbx="Neon", light=(16, 2.0))
TEETH = M("Steel Teeth (Metal)", (220, 224, 230), rough=0.2, metal=1.0, rbx="Metal")
ANT = M("Antenna Light", (255, 60, 60), rough=0.3, glow=(255, 30, 30), glow_strength=6.0, rbx="Neon", light=(6, 1.0))
CONVM = M("Conveyor", (40, 42, 50), rough=0.5, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (255, 80, 60), rough=0.2, glow=(255, 50, 30), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
# tracked base: two crawler tracks + a deck
for s in (-1, 1):
    ring = [V(s * 5.2, -4.8 + 0.7 * math.cos(a) if False else 0, 0) for a in ()]
    pts = []
    for k in range(10):
        a = math.pi / 2 + math.pi * k / 9
        pts.append(V(0, -4.4 + 0.75 * math.cos(a), 0.75 + 0.75 * math.sin(a)))
    for k in range(10):
        a = -math.pi / 2 + math.pi * k / 9
        pts.append(V(0, 4.4 + 0.75 * math.cos(a), 0.75 + 0.75 * math.sin(a)))
    r0 = [p + V(s * 4.6, 0, 0) for p in pts];r1 = [p + V(s * 6.2, 0, 0) for p in pts]
    finish(f"Track {s}", loft([r0, r1], smooth_sides=False), TREAD, C_BASE, merge=0)
    for k in range(5):
        y = -4.4 + k * 2.2
        cyl(f"Road Wheel {s}{k}", V(s * 4.55, y, 0.75), V(s * 6.25, y, 0.75), 0.5, 0.5, STEEL, C_BASE, n=12, hint=Z_AX)
    for k in range(9):
        y = -4.6 + k * 1.15
        abox(f"Track Stripe {s}{k}", min(s * 4.6, s * 6.2), max(s * 4.6, s * 6.2), y - 0.1, y + 0.1, 1.5, 1.56, HAZ, C_BASE)
abox("Base Deck", -4.6, 4.6, -4.2, 5.0, 0.3, 1.3, DARK, C_BASE)
for k in range(10):
    x = -4.4 + k * 0.95
    obox(f"Deck Stripe {k}", V(x, -4.22, 0.8), (0.35, 0.04, 1.0), (X_AX + Z_AX * 0.8).normalized(), Y_AX, (Z_AX - X_AX * 0.8).normalized(), HAZ, C_BASE)
conveyor_ramp(CONVM, HAZ, STEEL, EYE, y_front=-9.2, y_lip=-5.0, y_end=-2.4, coll=C_BASE)
# robot head with a hinged open jaw (ramp runs into the mouth)
abox("Head Back", -4.0, 4.0, 0.8, 4.6, 1.3, 9.0, BLUE, C_HEAD)
for s in (-1, 1):
    abox(f"Head Side {s}", min(s * 2.8, s * 4.0), max(s * 2.8, s * 4.0), -2.6, 0.8, 1.3, 9.0, BLUE, C_HEAD)
abox("Face Plate", -2.8, 2.8, -2.6, 0.8, 4.4, 9.0, STEEL, C_HEAD)
abox("Mouth Back Glow", -2.8, 2.8, 0.65, 0.8, 1.3, 4.4, MOUTH, C_HEAD)
abox("Mouth Floor", -2.8, 2.8, -2.6, 0.8, 1.25, 1.3, DARK, C_HEAD)
burn_zone(BURN, -2.4, 2.4, -2.4, 0.6, 1.3, 2.4, C_HEAD)
for k in range(5):                                          # top teeth (lower jaw is the ramp lip)
    x = -2.2 + k * 1.1
    cone(f"Top Tooth {k}", V(x, -2.4, 4.4), V(x, -2.4, 3.5), 0.4, TEETH, C_HEAD, n=4)
for k in range(3):
    cyl(f"Grinder {k}", V(-2.6, -0.4 + k * 0.5, 3.6 - k * 0.2), V(2.6, -0.4 + k * 0.5, 3.6 - k * 0.2), 0.25, 0.25, TEETH, C_HEAD, n=10, hint=Z_AX)
for s in (-1, 1):                                           # screen eyes + brows + ear speakers + jaw pistons
    abox(f"Eye Screen {s}", s * 1.3 - 0.9, s * 1.3 + 0.9, -2.68, -2.6, 6.2, 7.6, DARK, C_HEAD)
    abox(f"Eye LED {s}", s * 1.3 - 0.55, s * 1.3 + 0.55, -2.72, -2.68, 6.5, 7.3, EYE, C_HEAD)
    hexa(f"Brow {s}", [V(s * 0.4, -2.75, 8.1), V(s * 2.3, -2.75, 7.8), V(s * 2.3, -2.65, 7.8), V(s * 0.4, -2.65, 8.1),
                       V(s * 0.4, -2.75, 8.5), V(s * 2.3, -2.75, 8.2), V(s * 2.3, -2.65, 8.2), V(s * 0.4, -2.65, 8.5)], DARK, C_HEAD)
    cyl(f"Ear Speaker {s}", V(s * 4.0, 1.4, 6.0), V(s * 4.5, 1.4, 6.0), 1.1, 1.1, STEEL, C_HEAD, n=20, hint=Z_AX)
    for j in range(3):
        torus(f"Speaker Ring {s}{j}", V(s * 4.52, 1.4, 6.0), X_AX, Z_AX, 0.3 + j * 0.3, 0.05, DARK, C_HEAD, n_major=16, n_minor=4)
    cyl(f"Jaw Piston {s}", V(s * 3.4, -2.0, 1.4), V(s * 3.4, -2.0, 4.4), 0.25, 0.25, STEEL, C_HEAD, n=10)
    cyl(f"Piston Sleeve {s}", V(s * 3.4, -2.0, 1.4), V(s * 3.4, -2.0, 2.8), 0.35, 0.35, DARK, C_HEAD, n=10)
for k in range(6):
    abox(f"Face Vent {k}", -1.5 + k * 0.6 - 0.12, -1.5 + k * 0.6 + 0.12, -2.65, -2.6, 4.7, 5.6, DARK, C_HEAD)
abox("Head Top", -4.1, 4.1, -2.7, 4.7, 9.0, 9.4, STEEL, C_HEAD)
cyl("Antenna", V(0, 1.0, 9.4), V(0, 1.0, 12.0), 0.1, 0.07, STEEL, C_HEAD, n=8)
for k in range(2):
    torus(f"Antenna Ring {k}", V(0, 1.0, 10.4 + k * 0.7), Z_AX, Y_AX, 0.25 - 0.06 * k, 0.05, BLUE, C_HEAD, n_major=12, n_minor=4)
dot("Antenna Light", V(0, 1.0, 12.2), 0.3, ANT, C_HEAD)
for s in (-1, 1):
    abox(f"Exhaust {s}", s * 2.6 - 0.35, s * 2.6 + 0.35, 3.0, 3.7, 9.4, 10.6, DARK, C_DETAIL)
    abox(f"Exhaust Glow {s}", s * 2.6 - 0.25, s * 2.6 + 0.25, 3.1, 3.6, 10.6, 10.65, MOUTH, C_DETAIL)
finish_mine(bg=(0.012, 0.016, 0.03), tint=(0.88, 0.92, 1.0))
write_furnace_lua("RobotChomperFurnace")
