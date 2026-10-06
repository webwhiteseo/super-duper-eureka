"""Classic Incinerator Furnace - an original take on the classic Miner's Haven furnace: a chunky diamond-plate box
with a glowing lava pit, its front open at conveyor height so a conveyor runs straight in. Corner posts with neon
caps, side vents, small chimneys with flames, warning lights. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BOX, C_PIT, C_DETAIL = begin("ClassicIncineratorFurnace", ["Box", "Pit", "Details"], seed=511)
P = M("Dark Plate (DiamondPlate)", (70, 72, 80), rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
P2 = M("Steel Plate (DiamondPlate)", (128, 132, 142), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
BLACK = M("Black", (16, 16, 20), rough=0.5)
LAVA = M("Lava Pit", (255, 110, 30), rough=0.2, glow=(255, 80, 10), glow_strength=4.5, rbx="Neon", light=(18, 2.4))
NEON = M("Orange Neon", (255, 150, 50), rough=0.3, glow=(255, 120, 20), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
FLAME = M("Flame", (255, 190, 80), rough=0.3, glow=(255, 150, 30), glow_strength=5.0, rbx="Neon")
WARN = M("Warning Red", (255, 40, 30), rough=0.3, glow=(255, 20, 10), glow_strength=5.0, rbx="Neon", light=(6, 0.8))
HAZ = M("Hazard Yellow", (240, 196, 20), rough=0.45)
BURN = M("Burn Zone", (255, 130, 40), rough=0.2, glow=(255, 100, 20), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
CZ = 1.0                                                     # conveyor height at the front
slab("Foot", chamfer_rect(10.0, 10.0, 1.0), 0.0, chamfer_rect(9.6, 9.6, 0.9), 0.4, P2, C_BOX)
# box walls (front opening at conveyor height)
abox("Back Wall", -4.2, 4.2, 2.8, 4.2, 0.4, 4.0, P, C_BOX)
for s in (-1, 1):
    abox(f"Side Wall {s}", min(s * 2.8, s * 4.2), max(s * 2.8, s * 4.2), -4.2, 2.8, 0.4, 4.0, P, C_BOX)
abox("Front Lip", -2.8, 2.8, -4.2, -3.4, 0.4, CZ, P2, C_BOX)
abox("Front Header", -2.8, 2.8, -4.2, -3.4, 3.0, 4.0, P, C_BOX)
for k in range(7):                                           # hazard stripes on the header
    obox(f"Header Stripe {k}", V(-2.4 + k * 0.8, -4.22, 3.5), (0.3, 0.04, 0.9), (X_AX + Z_AX).normalized(), Y_AX, (Z_AX - X_AX).normalized(), HAZ, C_BOX)
abox("Pit Floor", -2.8, 2.8, -3.4, 2.8, 0.4, 0.6, BLACK, C_PIT)
abox("Lava Pit", -2.7, 2.7, -3.3, 2.7, 0.6, 0.85, LAVA, C_PIT)
burn_zone(BURN, -2.6, 2.6, -3.4, 2.6, 0.85, 2.8, C_PIT)
for s in (-1, 1):
    abox(f"Inner Glow {s}", min(s * 2.78, s * 2.82), max(s * 2.78, s * 2.82), -3.2, 2.6, 1.2, 2.6, NEON, C_PIT)
abox("Back Glow", -2.6, 2.6, 2.76, 2.8, 1.2, 2.6, NEON, C_PIT)
# chunky corner posts with neon caps
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * 4.0, sy * 4.0
        abox(f"Corner Post {sx}{sy}", x - 0.8, x + 0.8, y - 0.8, y + 0.8, 0.4, 5.0, P2, C_DETAIL)
        abox(f"Post Cap {sx}{sy}", x - 0.6, x + 0.6, y - 0.6, y + 0.6, 5.0, 5.3, NEON, C_DETAIL)
        abox(f"Post Band {sx}{sy}", x - 0.84, x + 0.84, y - 0.84, y + 0.84, 2.4, 2.6, BLACK, C_DETAIL)
abox("Roof Rim Back", -4.2, 4.2, 2.8, 4.2, 4.0, 4.4, P2, C_DETAIL)
for s in (-1, 1):
    abox(f"Roof Rim {s}", min(s * 2.8, s * 4.2), max(s * 2.8, s * 4.2), -4.2, 2.8, 4.0, 4.4, P2, C_DETAIL)
    for k in range(3):
        abox(f"Side Vent {s}{k}", min(s * 4.2, s * 4.24), max(s * 4.2, s * 4.24), -2.4 + k * 1.6, -1.4 + k * 1.6, 1.4, 2.8, NEON, C_DETAIL)
    C = V(s * 2.4, 3.5, 4.4)
    cyl(f"Chimney {s}", C, C + V(0, 0, 2.8), 0.5, 0.45, P, C_DETAIL, n=12)
    tube(f"Chimney Lip {s}", C + V(0, 0, 2.9), Z_AX, Y_AX, 0.65, 0.42, 0.3, P2, C_DETAIL, n=12)
    lathe(f"Chimney Flame {s}", C + V(0, 0, 3.0), [(0.4, 0), (0.3, 0.6), (0.0, 1.5)], FLAME, C_DETAIL, n=10)
    dot(f"Warning Light {s}", V(s * 3.0, -4.25, 3.5), 0.22, WARN, C_DETAIL)
finish_mine(bg=(0.02, 0.016, 0.014), tint=(1.0, 0.9, 0.82))
write_furnace_lua("ClassicIncineratorFurnace")
