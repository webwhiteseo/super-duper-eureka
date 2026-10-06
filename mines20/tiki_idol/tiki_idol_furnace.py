"""Tiki Idol Furnace - a giant carved jungle idol head on a mossy temple step; ore rolls straight into its glowing open
mouth at ground level (no ramp). Tiki torches, vines, ferns, stone steps, carved totems. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_IDOL, C_JUNGLE = begin("TikiIdolFurnace", ["Temple Step", "Idol", "Jungle"], seed=191)
JSTONE = M("Temple Stone", (120, 118, 96), rough=0.9, rbx="Cobblestone", noise=((92, 90, 70), (148, 146, 120), 3.0, 0.5))
WOOD = M("Idol Wood (Wood)", (120, 74, 40), rough=0.8, rbx="Wood", noise=((96, 56, 28), (146, 94, 54), 5.0, 0.3))
DWOOD = M("Dark Carving (Wood)", (60, 36, 20), rough=0.8, rbx="Wood")
PAINT = M("Teal Paint", (40, 170, 160), rough=0.6)
RED = M("Red Paint", (200, 50, 40), rough=0.6)
GLOW = M("Idol Fire", (255, 140, 40), rough=0.3, glow=(255, 100, 10), glow_strength=4.5, rbx="Neon", light=(16, 2.0))
EYE = M("Idol Eyes", (120, 255, 120), rough=0.3, glow=(80, 255, 80), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
LEAF = M("Jungle Leaf", (50, 140, 60), rough=0.7)
VINE = M("Vine", (60, 110, 40), rough=0.8)
MOSS = M("Moss", (80, 130, 50), rough=0.9, rbx="Grass")
TORCH = M("Torch Flame", (255, 180, 60), rough=0.3, glow=(255, 140, 20), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
BURN = M("Burn Zone", (255, 140, 40), rough=0.2, glow=(255, 100, 10), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(191)
# stepped temple platform (steps behind; ground level in front for the conveyor)
for k, (w, l, y0, z) in enumerate(((13.0, 9.0, -3.2, 0.0), (10.0, 6.5, -0.6, 0.6), (7.0, 4.5, 1.4, 1.2))):
    abox(f"Temple Step {k}", -w / 2, w / 2, y0, y0 + l, z, z + 0.6, JSTONE, C_BASE)
for k in range(8):
    ellip(f"Moss {k}", V(rnd.uniform(-6, 6), rnd.uniform(-3, 5), 0.6 + 0.6 * (k % 3)), 0.8, 0.6, 0.12, MOSS, C_BASE, n=8, m=2, half=True)
# the idol head (mouth opening at ground level at the front)
abox("Idol Back", -3.4, 3.4, -0.6, 3.0, 0.0, 9.0, WOOD, C_IDOL)
for s in (-1, 1):
    abox(f"Idol Cheek {s}", min(s * 2.4, s * 3.4), max(s * 2.4, s * 3.4), -3.0, -0.6, 0.0, 9.0, WOOD, C_IDOL)
abox("Upper Lip", -2.4, 2.4, -3.2, -0.6, 2.6, 3.4, DWOOD, C_IDOL)
abox("Brow Block", -3.5, 3.5, -3.3, -0.6, 6.4, 7.2, DWOOD, C_IDOL)
abox("Face Upper", -2.4, 2.4, -3.0, -0.6, 3.4, 6.4, WOOD, C_IDOL)
abox("Mouth Fire", -2.4, 2.4, -0.75, -0.6, 0.0, 2.6, GLOW, C_IDOL)
abox("Mouth Floor", -2.4, 2.4, -3.0, -0.6, 0.0, 0.05, DWOOD, C_IDOL)
burn_zone(BURN, -2.2, 2.2, -3.6, -0.8, 0.05, 2.4, C_IDOL)
for k in range(6):                                          # carved teeth
    x = -2.0 + k * 0.8
    abox(f"Tooth {k}", x - 0.25, x + 0.25, -3.25, -2.9, 2.0, 2.6, PAINT if k % 2 else JSTONE, C_IDOL)
for s in (-1, 1):
    abox(f"Eye Socket {s}", s * 1.2 - 0.8, s * 1.2 + 0.8, -3.1, -2.95, 4.4, 5.6, DWOOD, C_IDOL)
    abox(f"Eye Glow {s}", s * 1.2 - 0.45, s * 1.2 + 0.45, -3.15, -3.05, 4.7, 5.3, EYE, C_IDOL)
    hexa(f"Ear {s}", [V(s * 3.4, -1.6, 3.6), V(s * 4.4, -1.6, 4.0), V(s * 4.4, -0.4, 4.0), V(s * 3.4, -0.4, 3.6),
                      V(s * 3.4, -1.6, 6.4), V(s * 4.2, -1.6, 6.0), V(s * 4.2, -0.4, 6.0), V(s * 3.4, -0.4, 6.4)], DWOOD, C_IDOL)
    abox(f"Cheek Paint {s}", s * 2.9 - 0.3, s * 2.9 + 0.3, -3.05, -3.0, 3.8, 5.8, RED, C_IDOL)
hexa("Nose", [V(-0.6, -3.0, 3.4), V(0.6, -3.0, 3.4), V(0.6, -3.0, 5.4), V(-0.6, -3.0, 5.4),
              V(-0.7, -3.8, 3.4), V(0.7, -3.8, 3.4), V(0.4, -3.4, 5.4), V(-0.4, -3.4, 5.4)], DWOOD, C_IDOL)
for k in range(7):                                          # feather/leaf crown
    a = math.radians(30 + k * 20)
    d = V(math.cos(a), 0, math.sin(a))
    b0 = V(0, 0.6, 9.0) + d * 0.6
    blade(f"Crown Leaf {k}", [b0 - V(0, 0, 0) + V(-math.sin(a), 0, math.cos(a)) * 0.4, b0 + d * 3.0, b0 + V(math.sin(a), 0, -math.cos(a)) * 0.4], 0.12,
          PAINT if k % 2 else RED, C_IDOL)
abox("Head Band", -3.5, 3.5, -3.1, 3.1, 8.6, 9.2, PAINT, C_IDOL)
# vines hanging off the idol
for k in range(4):
    x = -3.0 + k * 2.0
    pts = [V(x, -1.0 + 0.4 * k, 9.1), V(x + 0.3, -3.2, 8.0), V(x - 0.2, -3.25, 6.2), V(x + 0.2, -3.3, 4.8 - 0.4 * k)]
    path_tube(f"Vine {k}", pts, [0.08] * 4, VINE, C_JUNGLE, n=5)
    for j in range(3):
        blade(f"Vine Leaf {k}{j}", [pts[j + 1], pts[j + 1] + V(0.4, -0.15, 0.2), pts[j + 1] + V(0.15, -0.1, 0.5)], 0.03, LEAF, C_JUNGLE)
# tiki torches, totems, ferns
for s in (-1, 1):
    T = V(s * 4.8, -3.0, 0.0)
    cyl(f"Torch Pole {s}", T, T + V(0, 0, 3.4), 0.13, 0.11, DWOOD, C_JUNGLE, n=6)
    lathe(f"Torch Cup {s}", T + V(0, 0, 3.3), [(0.15, 0), (0.4, 0.5), (0.42, 0.6)], WOOD, C_JUNGLE, n=8, smooth=False)
    lathe(f"Torch Flame {s}", T + V(0, 0, 3.85), [(0.35, 0), (0.22, 0.45), (0.0, 1.0)], TORCH, C_JUNGLE, n=8)
    P = V(s * 5.6, 3.6, 0.6)
    for j in range(3):
        abox(f"Totem {s}{j}", P.x - 0.55, P.x + 0.55, P.y - 0.55, P.y + 0.55, P.z + j * 1.2, P.z + j * 1.2 + 1.15, WOOD if j % 2 else DWOOD, C_JUNGLE)
        abox(f"Totem Eyes {s}{j}", P.x - 0.35, P.x + 0.35, P.y - 0.58, P.y - 0.55, P.z + j * 1.2 + 0.6, P.z + j * 1.2 + 0.8, EYE if j == 2 else PAINT, C_JUNGLE)
for k in range(9):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(4.6, 6.4)
    if math.sin(a) < -0.5 and abs(math.cos(a)) < 0.6: continue
    F = V(r * math.cos(a), 0.6 + r * math.sin(a) * 0.7, 0.0)
    for j in range(5):
        b = j * 2 * math.pi / 5 + rnd.uniform(0, 0.5)
        d = V(math.cos(b), math.sin(b), 0)
        blade(f"Fern {k}{j}", [F, F + d * 0.6 + V(0, 0, 0.8) + V(-d.y, d.x, 0) * 0.25, F + d * 1.4 + V(0, 0, 0.5), F + d * 0.6 + V(0, 0, 0.8) - V(-d.y, d.x, 0) * 0.25], 0.03, LEAF, C_JUNGLE)
finish_mine(bg=(0.016, 0.03, 0.016), tint=(0.95, 1.0, 0.85))
write_furnace_lua("TikiIdolFurnace")
