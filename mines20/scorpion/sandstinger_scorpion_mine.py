"""Sandstinger Mine - a bronze clockwork scorpion crouched on a desert dune among sandstone ruins.
Topaz crystals grow from its armoured back, its tail curls over its head and ore drips from the glowing stinger.
Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_BODY, C_LEGS, C_TAIL, C_DESERT = begin("SandstingerMine", ["Base", "Body", "Legs", "Tail", "Desert"], seed=16)
SANDSTONE = M("Sandstone (Slate)", (176, 128, 82), rough=0.9, rbx="Sandstone", noise=((146, 102, 62), (204, 160, 112), 4.0, 0.5))
GOLD = M("Gold Trim (Metal)", (240, 186, 70), rough=0.25, metal=1.0, rbx="Metal")
SAND = M("Dune Sand", (226, 186, 128), rough=0.95, rbx="Sand", noise=((206, 164, 106), (240, 206, 150), 6.0, 0.3))
BRONZE = M("Bronze Armour", (178, 104, 46), rough=0.3, metal=0.85, rbx="Metal", noise=((140, 78, 34), (200, 128, 64), 5.0, 0.15))
DARKST = M("Joint Steel", (54, 48, 46), rough=0.4, metal=0.8, rbx="DiamondPlate")
TOPAZ = M("Topaz Crystal", (255, 140, 10), rough=0.1, glow=(255, 110, 0), glow_strength=1.2, rbx="Glass", alpha=0.15, light=(10, 1.2))
VENOM = M("Venom Glow", (255, 110, 10), rough=0.3, glow=(255, 80, 0), glow_strength=4.0, rbx="Neon", light=(14, 1.8))
EYE = M("Eye Glow", (255, 40, 20), rough=0.3, glow=(255, 20, 10), glow_strength=4.0, rbx="Neon", light=(6, 1.0))
CACTUS = M("Cactus", (70, 128, 66), rough=0.7, noise=((52, 104, 50), (96, 156, 86), 9.0, 0.2))
BONE = M("Bleached Bone", (232, 222, 196), rough=0.7)
ROCK = M("Desert Rock", (140, 92, 62), rough=0.9, rbx="Slate")
BLOOM = M("Cactus Bloom", (255, 90, 140), rough=0.5, glow=(255, 60, 120), glow_strength=1.2, rbx="Neon")
ORE = M("Topaz Ore", (255, 170, 40), rough=0.15, glow=(255, 130, 10), glow_strength=2.0, rbx="Neon")

top = base_plinth(12.5, 12.5, SANDSTONE, GOLD, SAND, C_BASE, c=1.2)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(16)

# ---- dunes
for k, (x, y, sx, sy, sz) in enumerate(((-3.8, 3.2, 2.6, 2.0, 0.9), (3.6, 3.6, 2.2, 1.8, 0.7), (-4.0, -3.4, 1.8, 1.5, 0.5),
                                        (0.5, 1.0, 3.6, 3.4, 0.55), (4.2, -2.0, 1.6, 2.0, 0.45))):
    ellip(f"Dune {k + 1}", V(x, y, top - 0.05), sx, sy, sz, SAND, C_DESERT, n=18, m=4, half=True)

# ---- scorpion body (faces -Y)
BZ = top + 1.9
ellip("Cephalothorax", V(0, -1.9, BZ), 1.55, 1.3, 0.75, BRONZE, C_BODY, n=20, m=6)
ellip("Head Crest", V(0, -2.0, BZ + 0.45), 0.9, 0.9, 0.45, BRONZE, C_BODY, n=16, m=4, half=True)
for s in (-1, 1):
    for k, (dx, dy, r) in enumerate(((0.28, -2.75, 0.17), (0.55, -2.55, 0.12), (0.12, -2.35, 0.1))):
        dot(f"Eye {s}{k}", V(s * dx, dy, BZ + 0.6 - k * 0.08), r, EYE, C_BODY)
    path_tube(f"Chelicera {s}", [V(s * 0.35, -3.0, BZ - 0.1), V(s * 0.4, -3.45, BZ - 0.25), V(s * 0.2, -3.7, BZ - 0.45)], [0.18, 0.12, 0.03], DARKST, C_BODY, n=8)
SEG = ((-0.75, 1.7, 0.72), (0.2, 1.75, 0.7), (1.15, 1.65, 0.66), (2.05, 1.45, 0.6), (2.85, 1.2, 0.52))
for k, (y, rx, rz) in enumerate(SEG):
    ellip(f"Abdomen Plate {k + 1}", V(0, y, BZ - 0.05 * k), rx, 0.6, rz, BRONZE, C_BODY, n=20, m=5)
    ellip(f"Plate Rim {k + 1}", V(0, y - 0.4, BZ - 0.05 * k), rx * 0.97, 0.07, rz * 0.97, GOLD, C_BODY, n=20, m=4)
    for s in (-1, 1):
        dot(f"Plate Rivet {k}{s}", V(s * rx * 0.62, y - 0.25, BZ + rz * 0.55 - 0.05 * k), 0.08, GOLD, C_BODY)
    if k < 4:                                               # topaz crystals on the back
        for j in range(2):
            a = rnd.uniform(-0.6, 0.6)
            crystal(f"Back Crystal {k + 1}-{j + 1}", V(rnd.uniform(-0.5, 0.5), y + rnd.uniform(-0.15, 0.15), BZ + rz * 0.75 - 0.05 * k),
                    V(math.sin(a), rnd.uniform(-0.3, 0.3), 1.0), rnd.uniform(0.9, 1.5), rnd.uniform(0.16, 0.24), TOPAZ, C_BODY)
ellip("Belly", V(0, 0.4, BZ - 0.45), 1.3, 3.0, 0.4, DARKST, C_BODY, n=16, m=4)

# ---- legs: 4 per side
for s in (-1, 1):
    for k, (y, sw) in enumerate(((-1.6, -0.6), (-0.6, -0.2), (0.4, 0.25), (1.4, 0.7))):
        hip = V(s * 1.3, y, BZ - 0.1)
        knee = V(s * 2.9, y + sw * 0.6, BZ + 0.9)
        ank = V(s * 4.0, y + sw * 1.2, top + 0.7)
        foot = V(s * 4.35, y + sw * 1.4, top + 0.02)
        path_tube(f"Leg {k + 1}{s} Femur", [hip, (hip + knee) / 2 + V(0, 0, 0.2), knee], [0.28, 0.24, 0.2], BRONZE, C_LEGS, n=10)
        path_tube(f"Leg {k + 1}{s} Tibia", [knee, (knee + ank) / 2 + V(s * 0.15, 0, 0.1), ank], [0.2, 0.17, 0.13], BRONZE, C_LEGS, n=10)
        cone(f"Leg {k + 1}{s} Claw", ank, foot, 0.13, DARKST, C_LEGS, n=8)
        dot(f"Leg {k + 1}{s} Hip Joint", hip, 0.3, DARKST, C_LEGS)
        dot(f"Leg {k + 1}{s} Knee Joint", knee, 0.25, GOLD, C_LEGS)
        dot(f"Leg {k + 1}{s} Ankle Joint", ank, 0.16, DARKST, C_LEGS)

# ---- pincers
for s in (-1, 1):
    sh = V(s * 1.0, -2.7, BZ - 0.1)
    el = V(s * 2.5, -3.2, BZ + 0.5)
    wr = V(s * 2.4, -4.3, BZ + 0.2)
    path_tube(f"Arm {s} Upper", [sh, (sh + el) / 2 + V(0, 0, 0.2), el], [0.32, 0.3, 0.26], BRONZE, C_LEGS, n=12)
    path_tube(f"Arm {s} Fore", [el, (el + wr) / 2, wr], [0.26, 0.28, 0.3], BRONZE, C_LEGS, n=12)
    dot(f"Elbow {s}", el, 0.32, GOLD, C_LEGS)
    dot(f"Wrist {s}", wr, 0.3, DARKST, C_LEGS)
    H = V(s * 2.3, -4.95, BZ + 0.25)
    ellip(f"Claw Hand {s}", H, 0.62, 0.85, 0.5, BRONZE, C_LEGS, n=16, m=6)
    torus(f"Claw Band {s}", H + V(0, 0.45, 0), Y_AX, Z_AX, 0.5, 0.06, GOLD, C_LEGS, n_major=16, n_minor=4)
    fx = H + V(-s * 0.25, -0.7, 0)
    path_tube(f"Fixed Finger {s}", [fx, fx + V(-s * 0.15, -0.6, 0.0), fx + V(s * 0.05, -1.2, 0.05)], [0.24, 0.16, 0.02], BRONZE, C_LEGS, n=10)
    mv = H + V(s * 0.25, -0.65, 0.05)
    path_tube(f"Moving Finger {s}", [mv, mv + V(s * 0.35, -0.5, 0.1), mv + V(s * 0.15, -1.15, 0.12)], [0.22, 0.15, 0.02], BRONZE, C_LEGS, n=10)
    for j in range(3):                                      # serrations
        cone(f"Claw Tooth {s}{j}", fx + V(-s * 0.05, -0.25 - j * 0.3, 0), fx + V(s * 0.12, -0.3 - j * 0.3, 0), 0.06, GOLD, C_LEGS, n=4)

# ---- tail arching over the head; ore drips from the stinger
TP = [V(0, 3.25, BZ - 0.1), V(0, 4.45, BZ + 0.9), V(0, 5.0, BZ + 2.6), V(0, 4.6, BZ + 4.3), V(0, 3.5, BZ + 5.5),
      V(0, 1.9, BZ + 6.1), V(0, 0.2, BZ + 6.0), V(0, -1.2, BZ + 5.4)]
for k in range(len(TP) - 1):
    a, b = TP[k], TP[k + 1]
    d = (b - a);L = d.length;mid = (a + b) / 2
    side = X_AX
    up = d.normalized().cross(side).normalized()
    r = 0.62 - 0.045 * k
    ellip(f"Tail Segment {k + 1}", mid, r, L * 0.62, r * 0.9, BRONZE, C_TAIL, n=16, m=5, ax=side, ay=d, az=up * -1)
    torus(f"Tail Ring {k + 1}", a, d, side, r * 0.85, 0.07, GOLD, C_TAIL, n_major=16, n_minor=4)
    crystal(f"Tail Spike {k + 1}", mid - up * r * 0.75, -up + d.normalized() * 0.3, 0.6, 0.11, DARKST, C_TAIL, sides=4)
SB = V(0, -2.0, BZ + 4.75)
d = (SB - TP[-1]).normalized()
ellip("Venom Bulb", SB, 0.62, 0.85, 0.62, TOPAZ, C_TAIL, n=16, m=6, ax=X_AX, ay=d, az=d.cross(X_AX))
torus("Bulb Collar", TP[-1] + d * 0.25, d, X_AX, 0.5, 0.09, GOLD, C_TAIL, n_major=16, n_minor=4)
dot("Venom Core", SB, 0.42, VENOM, C_TAIL)
tip = SB + V(0, -0.85, -1.05)
path_tube("Stinger", [SB + V(0, -0.45, -0.35), SB + V(0, -0.75, -0.65), tip], [0.26, 0.15, 0.02], DARKST, C_TAIL, n=10)
for k in range(3):
    dot(f"Venom Drip {k + 1}", tip + V(0, -0.05, -0.3 - k * 0.32), 0.09 - 0.02 * k, VENOM, C_TAIL)
ore_cube(tip + V(0, -0.2, -1.75), ORE, C_TAIL, size=0.8)

# ---- sandstone ruins (back-left)
R0 = V(-4.4, 3.9, top)
for k, (dx, h) in enumerate(((-0.9, 5.2), (1.4, 3.6))):
    for j in range(int(h // 1.2)):
        cyl(f"Ruin Drum {k}{j}", R0 + V(dx, 0, j * 1.2), R0 + V(dx, 0, j * 1.2 + 1.15), 0.55 - 0.02 * j, 0.53 - 0.02 * j, SANDSTONE, C_DESERT, n=10)
    lathe(f"Ruin Capital {k}", R0 + V(dx, 0, (h // 1.2) * 1.2), [(0.55, 0), (0.75, 0.3), (0.75, 0.45), (0.55, 0.45)], SANDSTONE, C_DESERT, n=10, smooth=False)
obox("Ruin Lintel", R0 + V(-0.4, 0, 5.15), (2.4, 1.0, 0.6), V(1, 0, -0.15), Y_AX, V(0.15, 0, 1), SANDSTONE, C_DESERT)
cyl("Fallen Drum", R0 + V(1.7, -2.0, 0.5), R0 + V(2.7, -2.4, 0.45), 0.5, 0.5, SANDSTONE, C_DESERT, n=10)
for k in range(5):
    rock_f(f"Rubble {k + 1}", R0 + V(rnd.uniform(-1.2, 2.5), rnd.uniform(-2.0, 0.6), 0.1), (0.35, 0.3, 0.25), SANDSTONE, C_DESERT, rough=0.3)

# ---- cacti
def saguaro(name, P, h, arms):
    path_tube(f"{name} Trunk", [P, P + V(0, 0, h * 0.5), P + V(0, 0, h)], [0.38, 0.36, 0.3], CACTUS, C_DESERT, n=10)
    dot(f"{name} Top", P + V(0, 0, h), 0.3, CACTUS, C_DESERT)
    for k, (dx, z0, hh) in enumerate(arms):
        a0 = P + V(0, 0, z0);a1 = a0 + V(dx * 0.9, 0, 0.15);a2 = a1 + V(dx * 0.1, 0, hh)
        path_tube(f"{name} Arm {k + 1}", [a0, a1, a2], [0.24, 0.22, 0.2], CACTUS, C_DESERT, n=8)
        dot(f"{name} Arm Tip {k + 1}", a2, 0.2, CACTUS, C_DESERT)
    dot(f"{name} Bloom", P + V(0, 0, h + 0.25), 0.16, BLOOM, C_DESERT)
saguaro("Saguaro A", V(4.4, 3.4, top + 0.3), 4.2, ((1, 1.6, 1.4), (-1, 2.3, 1.1)))
saguaro("Saguaro B", V(-4.7, -1.2, top + 0.2), 2.6, ((1, 1.0, 0.9),))
for k, (x, y) in enumerate(((3.2, 4.6), (-3.5, -4.3))):
    for j in range(3):
        ellip(f"Barrel Cactus {k}{j}", V(x + j * 0.45 - 0.45, y + (j % 2) * 0.3, top + 0.25), 0.3, 0.3, 0.4 + 0.1 * j, CACTUS, C_DESERT, n=10, m=4)

# ---- bleached bones (front-right): ribcage + skull
B0 = V(3.9, -3.9, top + 0.1)
path_tube("Spine", [B0 + V(-1.4, 0.4, 0.15), B0 + V(0, 0, 0.3), B0 + V(1.2, -0.3, 0.15)], [0.1, 0.12, 0.08], BONE, C_DESERT, n=6)
for k in range(5):
    x = -1.1 + k * 0.5
    for s in (-1, 1):
        path_tube(f"Rib {k}{s}", [B0 + V(x, -0.1 * x, 0.3), B0 + V(x + 0.05, -0.1 * x + s * 0.55, 0.85 - 0.06 * k), B0 + V(x + 0.1, -0.1 * x + s * 0.75, 0.05)],
                  [0.06, 0.06, 0.04], BONE, C_DESERT, n=6)
S0 = B0 + V(1.7, -0.6, 0.25)
ellip("Skull", S0, 0.45, 0.38, 0.32, BONE, C_DESERT, n=12, m=4)
ellip("Skull Snout", S0 + V(0.45, -0.1, -0.08), 0.32, 0.22, 0.18, BONE, C_DESERT, n=10, m=3)
for s in (-1, 1):
    dot(f"Eye Socket {s}", S0 + V(0.25, s * 0.22, 0.12), 0.1, DARKST, C_DESERT)
    path_tube(f"Skull Horn {s}", [S0 + V(-0.1, s * 0.3, 0.2), S0 + V(-0.2, s * 0.75, 0.45), S0 + V(0.1, s * 0.95, 0.75)], [0.08, 0.06, 0.01], BONE, C_DESERT, n=6)
for k in range(6):
    rock_f(f"Desert Rock {k + 1}", V(rnd.uniform(-5, 5), rnd.uniform(-5, -3.6), top + 0.05), (0.4, 0.35, 0.25), ROCK, C_DESERT, rough=0.3) if k < 3 else \
        rock_f(f"Desert Rock {k + 1}", V(rnd.uniform(1.8, 5), rnd.uniform(0.5, 2.5), top + 0.05), (0.35, 0.3, 0.22), ROCK, C_DESERT, rough=0.3)

finish_mine(bg=(0.03, 0.02, 0.015), tint=(1.0, 0.85, 0.65))
