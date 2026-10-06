"""Abyss Maw Furnace - a giant angler fish lying on the seabed with its jaws open at ground level: conveyors feed
ore straight into the glowing throat (no ramp). Glowing lure, eyes, fins, coral, shells and seaweed. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_FISH, C_DETAIL = begin("AbyssMawFurnace", ["Seabed", "Angler", "Details"], seed=81)
SAND = M("Seabed Sand", (196, 176, 130), rough=0.95, rbx="Sand", noise=((170, 150, 106), (220, 202, 160), 5.0, 0.3))
SKIN = M("Angler Skin", (46, 64, 92), rough=0.6, rbx="Slate", noise=((30, 44, 70), (70, 92, 124), 6.0, 0.25))
BELLY = M("Angler Belly", (120, 136, 150), rough=0.6)
VOID = M("Throat Dark", (6, 10, 16), rough=0.6)
THROAT = M("Throat Glow", (80, 255, 220), rough=0.2, glow=(40, 255, 200), glow_strength=4.0, rbx="Neon", light=(14, 2.0))
LURE = M("Lure Glow", (180, 255, 240), rough=0.2, glow=(120, 255, 230), glow_strength=8.0, rbx="Neon", light=(16, 2.2))
TOOTH = M("Teeth", (236, 232, 214), rough=0.4)
EYE = M("Eye Glow", (255, 230, 120), rough=0.2, glow=(255, 210, 60), glow_strength=5.0, rbx="Neon", light=(6, 0.8))
FIN = M("Fin Membrane", (60, 140, 160), rough=0.6, rbx="Fabric", alpha=0.1)
CORAL = M("Coral", (255, 110, 120), rough=0.6, glow=(255, 70, 110), glow_strength=0.4)
WEED = M("Seaweed", (50, 150, 80), rough=0.6)
SHELL = M("Shell", (240, 220, 210), rough=0.4, metal=0.2)
BUB = M("Bubbles", (190, 240, 255), rough=0.05, rbx="Glass", alpha=0.5)
BURN = M("Burn Zone", (80, 255, 220), rough=0.2, glow=(40, 255, 200), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(81)

ellip("Seabed", V(0, 0.8, 0), 7.2, 6.6, 0.45, SAND, C_BASE, n=28, m=3, half=True)
# ---- angler head/body
B = V(0, 2.4, 2.6)
ellip("Angler Body", B, 4.2, 4.6, 3.0, SKIN, C_FISH, n=24, m=8)
ellip("Angler Belly", B + V(0, -0.6, -1.3), 3.6, 3.8, 1.6, BELLY, C_FISH, n=20, m=6)
ellip("Upper Jaw", V(0, -1.4, 2.2), 3.6, 2.2, 1.5, SKIN, C_FISH, n=24, m=6)
ellip("Mouth Cavity", V(0, -2.2, 1.15), 2.9, 1.6, 1.25, VOID, C_FISH, n=24, m=6)
ellip("Throat Light", V(0, -3.0, 1.05), 1.9, 0.75, 0.85, THROAT, C_FISH, n=18, m=5)
ellip("Lower Jaw", V(0, -2.6, 0.0), 3.4, 2.2, 0.22, BELLY, C_FISH, n=24, m=3, half=True)
for k in range(11):                                        # teeth: upper (down) and lower (up)
    a = math.radians(200 + k * 14)
    p = V(2.8 * math.cos(a), -2.2 + 1.5 * math.sin(a) * 0.9, 0)
    L = 1.0 if k % 2 else 0.7
    cone(f"Upper Tooth {k}", V(p.x, p.y, 2.05), V(p.x * 0.95, p.y + 0.15, 2.05 - L), 0.18, TOOTH, C_FISH, n=5)
    if 2 <= k <= 8 and k % 3 != 1:
        cone(f"Lower Tooth {k}", V(p.x, p.y - 0.15, 0.15), V(p.x * 0.95, p.y, 0.15 + L * 0.8), 0.16, TOOTH, C_FISH, n=5)
burn_zone(BURN, -2.4, 2.4, -3.6, -1.2, 0.05, 2.0, C_FISH)
for s in (-1, 1):                                          # eyes
    E = V(s * 2.6, -0.4, 3.9)
    dot(f"Eye {s}", E, 0.55, EYE, C_FISH)
    dot(f"Pupil {s}", E + V(s * 0.2, -0.35, 0.05), 0.25, VOID, C_FISH)
    torus(f"Eye Rim {s}", E, V(s * 0.6, -0.8, 0).normalized(), Z_AX, 0.58, 0.1, SKIN, C_FISH, n_major=16, n_minor=4)
    # pectoral fins
    r0 = V(s * 3.9, 1.4, 1.6)
    blade(f"Pectoral Fin {s}", [r0, r0 + V(s * 2.4, -0.6, 0.6), r0 + V(s * 2.2, 1.4, -0.4), r0 + V(s * 0.3, 1.6, -0.6)], 0.08, FIN, C_FISH)
    for j in range(3):
        cyl(f"Fin Ray {s}{j}", r0, r0 + V(s * 2.3, -0.6 + 1.0 * j, 0.6 - 0.5 * j), 0.06, 0.03, SKIN, C_FISH, n=5)
# dorsal spines + tail
for k in range(5):
    p = B + V(0, -0.6 + k * 1.1, 2.7 - 0.25 * k)
    cone(f"Dorsal Spine {k}", p, p + V(0, 0.6, 1.4 - 0.15 * k), 0.16, SKIN, C_FISH, n=5)
blade("Dorsal Fin", [B + V(0, -0.6, 2.8), B + V(0, 0.2, 4.0), B + V(0, 3.6, 3.0), B + V(0, 3.6, 2.2)], 0.08, FIN, C_FISH)
T0 = B + V(0, 4.3, 0.2)
blade("Tail Fin", [T0, T0 + V(0, 2.2, 2.2), T0 + V(0, 1.4, 0.0), T0 + V(0, 2.2, -1.8)], 0.1, FIN, C_FISH)
# glowing lure on a curved rod
rod = [B + V(0, -1.6, 2.7), B + V(0, -2.4, 4.6), V(0, -3.6, 6.8), V(0, -5.0, 6.6), V(0, -5.6, 5.4)]
path_tube("Lure Rod", rod, [0.16, 0.13, 0.1, 0.08, 0.05], SKIN, C_FISH, n=6)
dot("Lure Bulb", V(0, -5.6, 5.0), 0.5, LURE, C_FISH)
torus("Lure Ring", V(0, -5.6, 5.0), Z_AX, Y_AX, 0.55, 0.05, SHELL, C_FISH, n_major=14, n_minor=4)

# ---- coral, seaweed, shells, bubbles
for k, (x, y) in enumerate(((-5.4, 3.6), (5.2, 4.2), (-5.6, -1.6), (5.6, -1.2))):
    for j in range(3):
        b = V(x + rnd.uniform(-0.5, 0.5), y + rnd.uniform(-0.5, 0.5), 0.2)
        t = b + V(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), rnd.uniform(1.0, 2.0))
        cyl(f"Coral {k}{j}", b, t, 0.18, 0.1, CORAL, C_DETAIL, n=6)
        cyl(f"Coral Branch {k}{j}", (b + t) / 2, (b + t) / 2 + V(0.5, 0.2, 0.6), 0.1, 0.06, CORAL, C_DETAIL, n=5)
        dot(f"Coral Tip {k}{j}", t, 0.14, CORAL, C_DETAIL)
for k in range(8):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(4.6, 6.4)
    if math.sin(a) < -0.5 and abs(math.cos(a)) < 0.6:
        continue
    b = V(r * math.cos(a), 0.8 + r * math.sin(a), 0.2);h = rnd.uniform(1.5, 3.0)
    blade(f"Seaweed {k}", [b + V(-0.15, 0, 0), b + V(0.15, 0, 0), b + V(0.35, 0.1, h * 0.5), b + V(0.0, 0.05, h), b + V(-0.2, 0, h * 0.5)], 0.05, WEED, C_DETAIL)
for k, (x, y) in enumerate(((-3.8, -3.6), (3.6, -3.9), (-4.6, 0.6))):
    ellip(f"Shell {k}", V(x, y, 0.3), 0.45, 0.4, 0.25, SHELL, C_DETAIL, n=10, m=3, half=True)
    dot(f"Pearl {k}", V(x, y - 0.15, 0.45), 0.13, LURE, C_DETAIL)
for k in range(8):
    dot(f"Bubble {k}", V(rnd.uniform(-1.5, 1.5), -2.0 + rnd.uniform(-0.5, 0.5), 3.2 + k * 0.6), 0.12 + 0.02 * (k % 3), BUB, C_DETAIL)

finish_mine(bg=(0.006, 0.02, 0.035), tint=(0.6, 0.85, 1.0))
write_furnace_lua("AbyssMawFurnace")
