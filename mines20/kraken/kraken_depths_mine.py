"""Kraken Depths Mine - a giant kraken coils round a brass diving bell; ore spills from the front porthole pipe.
Built with mine_kit (same pipeline as the other Ore Factory mines)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_BELL, C_KRAKEN, C_REEF, C_DETAIL = begin("KrakenDepthsMine", ["Base", "Bell", "Kraken", "Reef", "Details"], seed=8)
BLACK = M("Black", (8, 14, 20), rough=0.45)
TRIM = M("Teal Trim (Metal)", (30, 210, 200), rough=0.3, metal=0.5, glow=(20, 200, 190), glow_strength=0.8, rbx="Neon")
ABYSS = M("Abyss Marble (Marble)", (10, 24, 44), rough=0.25, marble=((8, 20, 38), (90, 230, 230)))
SAND = M("Sea Sand", (196, 176, 130), rough=0.9, rbx="Sand", noise=((170, 150, 108), (220, 204, 160), 4.0, 0.2))
BRASS = M("Brass (Metal)", (200, 150, 70), rough=0.28, metal=1.0, plate=12.0)
COPPER = M("Verdigris Copper (Metal)", (70, 150, 130), rough=0.5, metal=0.7, noise=((50, 120, 100), (110, 190, 160), 3.0, 0.2))
GLASS = M("Porthole Glass", (120, 240, 230), rough=0.05, glow=(60, 220, 210), glow_strength=3.5, rbx="Neon", light=(12, 1.4))
SKIN = M("Kraken Skin", (150, 50, 120), rough=0.55, rbx="SmoothPlastic", noise=((110, 34, 92), (190, 80, 150), 3.5, 0.3))
BELLY = M("Kraken Suckers", (240, 190, 200), rough=0.5)
EYE = M("Kraken Eye", (255, 220, 70), rough=0.3, glow=(255, 200, 40), glow_strength=4.0, rbx="Neon", light=(8, 1.2))
PUPIL = M("Pupil", (10, 6, 10), rough=0.3)
CORAL = M("Coral", (255, 110, 100), rough=0.6, noise=((220, 80, 80), (255, 150, 130), 5.0, 0.2))
CORAL2 = M("Glow Coral", (180, 120, 255), rough=0.4, glow=(150, 90, 255), glow_strength=2.5, rbx="Neon", light=(6, 0.8))
WEED = M("Seaweed", (40, 140, 80), rough=0.7)
BUBBLE = M("Bubbles", (200, 245, 255), rough=0.05, glow=(150, 230, 255), glow_strength=1.0, rbx="Glass", alpha=0.35)
IRON = M("Anchor Iron (Metal)", (50, 56, 64), rough=0.4, metal=0.9)
ORE = M("Pearl Ore", (230, 245, 255), rough=0.15, glow=(170, 230, 255), glow_strength=2.0, rbx="Neon")

top = base_plinth(10.5, 10.5, BLACK, TRIM, ABYSS, C_BASE, c=1.5)
lathe("Sand Mound", V(0, 0.6, top - 0.05), [(4.4, 0), (4.0, 0.35), (2.6, 0.7), (0.5, 0.8)], SAND, C_BASE, n=24)

# ---- brass diving bell with portholes and riveted bands
B = V(0, 0.8, top + 0.6)
lathe("Diving Bell", B, [(3.0, 0), (3.0, 0.5), (2.85, 2.5), (2.5, 4.6), (1.9, 6.2), (1.0, 7.1), (0.3, 7.35)], BRASS, C_BELL, n=32)
for i, z in enumerate((0.45, 3.2, 5.6)):
    r = {0: 3.02, 1: 2.72, 2: 2.13}[i]
    torus(f"Bell Band {i + 1}", B + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), r + 0.04, 0.13, COPPER, C_BELL, n_major=40, n_minor=6)
    for k in range(12):
        a = 2 * math.pi * k / 12
        dot(f"Rivet {i + 1}-{k + 1}", B + V((r + 0.16) * math.cos(a), (r + 0.16) * math.sin(a), z), 0.09, BRASS, C_BELL)
for k, ang in enumerate((-90, 30, 150)):                    # three glowing portholes
    a = math.radians(ang);n_ = V(math.cos(a), math.sin(a), 0.12).normalized()
    c = B + V(2.92 * math.cos(a), 2.92 * math.sin(a), 1.9)
    torus(f"Porthole Rim {k + 1}", c, n_, V(0, 0, 1), 0.85, 0.16, COPPER, C_BELL, n_major=24, n_minor=6)
    cyl(f"Porthole Glass {k + 1}", c - n_ * 0.05, c + n_ * 0.05, 0.72, 0.72, GLASS, C_BELL, n=20, hint=V(0, 0, 1))
    for j in range(4):
        aa = math.pi / 4 + j * math.pi / 2;u, v = perp_basis(n_, V(0, 0, 1))
        dot(f"Porthole Bolt {k + 1}-{j + 1}", c + (math.cos(aa) * u + math.sin(aa) * v) * 0.85 + n_ * 0.12, 0.1, BRASS, C_BELL)
lathe("Bell Hatch", B + V(0, 0, 7.2), [(0.7, 0), (0.75, 0.25), (0.45, 0.45), (0.0, 0.5)], COPPER, C_BELL, n=16)

# ---- the ore pipe out of the front porthole
P0 = B + V(0, -3.0, 1.9)
path_tube("Ore Pipe", [P0, P0 + V(0, -0.9, 0), P0 + V(0, -1.6, -0.4), P0 + V(0, -2.0, -1.0)], [0.38] * 4, BRASS, C_BELL, n=14)
SP = P0 + V(0, -2.0, -1.0)
torus("Pipe Collar", SP, V(0, -0.4, -1).normalized(), V(0, 1, 0), 0.48, 0.12, COPPER, C_BELL, n_major=16, n_minor=6)
torus("Pipe Glow", SP + V(0, -0.05, -0.12), V(0, -0.4, -1).normalized(), V(0, 1, 0), 0.38, 0.07, GLASS, C_BELL, n_major=16, n_minor=6)
ore_cube(SP + V(0, -0.6, -1.0), ORE, C_BELL)

# ---- the kraken: mantle on top of the bell, big eyes, tentacles wrapping down
K = B + V(0, 0.4, 7.0)
lathe("Kraken Mantle", K, [(1.6, 0), (2.4, 0.9), (2.6, 2.4), (2.3, 4.0), (1.6, 5.4), (0.7, 6.3), (0.0, 6.6)], SKIN, C_KRAKEN, n=24)
for k in range(10):                                         # spots
    a = 2 * math.pi * k / 10 + 0.3;z = 1.6 + (k % 3) * 1.3
    r = {0: 2.55, 1: 2.4, 2: 2.0}[k % 3]
    dot(f"Mantle Spot {k + 1}", K + V(r * math.cos(a), r * math.sin(a), z), 0.32, BELLY, C_KRAKEN)
for side, lab in ((1, "L"), (-1, "R")):
    E = K + V(side * 1.75, -1.55, 1.2)
    sphere(f"Eye Bulge {lab}", E, 0.95, SKIN, C_KRAKEN)
    sphere(f"Eye {lab}", E + V(side * 0.12, -0.45, 0.05), 0.7, EYE, C_KRAKEN)
    abox(f"Pupil {lab}", E.x + side * 0.12 - 0.1, E.x + side * 0.12 + 0.1, E.y - 1.12, E.y - 1.05, E.z - 0.45, E.z + 0.5, PUPIL, C_KRAKEN)
rnd = random.Random(3)
for t in range(8):                                          # tentacles spiral down round the bell onto the sand
    a0 = math.radians(-62 + t * 40 + (10 if t % 2 else 0))  # leaves the front pipe clear
    pts, rad = [], []
    turn = 0.9 + 0.35 * (t % 3)
    for i in range(22):
        f = i / 21
        a = a0 + f * turn * (1 if t % 2 else -1)
        r = 2.4 + 0.9 * math.sin(math.pi * f) + (1.8 * f ** 3 if f > 0.75 else 0)
        z = 7.2 - 7.0 * f ** 1.1
        pts.append(B + V(r * math.cos(a), r * math.sin(a), max(z, 0.35)))
        rad.append(0.62 * (1 - 0.85 * f) + 0.07)
    # curl the tip up off the sand
    tip = pts[-1]; d = (pts[-1] - pts[-2]).normalized()
    for k in range(1, 6):
        ang = k * 0.55
        pts.append(tip + d * 0.35 * k * math.cos(ang) + V(0, 0, 0.35 * k * math.sin(ang)))
        rad.append(0.09 * (1 - k / 7) + 0.02)
    path_tube(f"Tentacle {t + 1}", pts, rad, SKIN, C_KRAKEN, n=10)
    for i in range(3, len(pts) - 6, 2):                     # suckers on the underside
        d = (pts[i + 1] - pts[i - 1]).normalized()
        out = (pts[i] - B);out.z = 0;out = out.normalized()
        dot(f"Sucker {t + 1}-{i}", pts[i] - out * rad[i] * 0.75 - V(0, 0, rad[i] * 0.35), rad[i] * 0.35, BELLY, C_KRAKEN)

# ---- reef details: coral, glowing coral, seaweed, anchor, bubbles, clam
def coral(name, P, mat, h, seed):
    r_ = random.Random(seed)
    def branch(p, d, l, rr, depth):
        q = p + d * l
        cyl(f"{name} {depth}-{r_.randint(0, 99999)}", p, q, rr, rr * 0.7, mat, C_REEF, n=6)
        if depth < 3:
            for k in range(2):
                nd = (d + V(r_.uniform(-0.8, 0.8), r_.uniform(-0.8, 0.8), 0.6)).normalized()
                branch(q, nd, l * 0.72, rr * 0.7, depth + 1)
        else:
            sphere(f"{name} Tip {r_.randint(0, 99999)}", q, rr * 1.2, mat, C_REEF)
    branch(P, V(0, 0, 1), h, 0.28, 0)
coral("Coral A", V(-3.9, -3.6, top), CORAL, 1.4, 1)
coral("Coral B", V(3.7, 3.9, top), CORAL2, 1.6, 2)
coral("Coral C", V(-4.1, 3.2, top), CORAL2, 1.1, 3)
for k, (x, y) in enumerate(((3.9, -2.6), (4.2, -1.6), (-3.3, -4.3), (-4.3, 0.2))):
    pts = [V(x, y, top) + V(0.35 * math.sin(i * 1.3 + k), 0.25 * math.cos(i * 1.1 + k), i * 0.55) for i in range(8)]
    path_tube(f"Seaweed {k + 1}", pts, [0.16 - 0.015 * i for i in range(8)], WEED, C_REEF, n=6)
# anchor leaning on the bell (right side)
A0 = V(-3.4, -1.6, top)
cyl("Anchor Shank", A0 + V(0, 0, 0.4), A0 + V(0.5, 0.4, 4.2), 0.2, 0.2, IRON, C_DETAIL, n=8)
torus("Anchor Ring", A0 + V(0.56, 0.45, 4.6), V(0.7, -0.7, 0), V(0, 0, 1), 0.4, 0.09, IRON, C_DETAIL, n_major=16, n_minor=6)
cyl("Anchor Stock", A0 + V(0.25, -0.55, 3.6), A0 + V(0.65, 1.35, 3.8), 0.12, 0.12, IRON, C_DETAIL, n=6)
for side in (1, -1):
    path_tube(f"Anchor Arm {side}", [A0 + V(0, 0, 0.5), A0 + V(side * 0.9, -side * 0.6, 0.6), A0 + V(side * 1.4, -side * 0.95, 1.3)], [0.18, 0.16, 0.12], IRON, C_DETAIL, n=8)
    cone(f"Anchor Fluke {side}", A0 + V(side * 1.4, -side * 0.95, 1.3), A0 + V(side * 1.55, -side * 1.05, 1.9), 0.3, IRON, C_DETAIL, n=4)
# clam with a pearl
CL = V(3.6, -4.0, top + 0.15)
lathe("Clam Bottom", CL, [(0.0, 0), (0.9, 0.05), (1.0, 0.25)], BELLY, C_DETAIL, n=12)
lathe("Clam Top", CL + V(0, 0.25, 0.55), [(1.0, 0), (0.85, 0.3), (0.0, 0.42)], BELLY, C_DETAIL, n=12)
sphere("Pearl", CL + V(0, 0, 0.45), 0.32, ORE, C_DETAIL)
# bubbles rising from the hatch and the pipe
for k in range(5):
    dot(f"Bubble {k + 1}", K + V(0.3 * math.sin(k * 1.7), 0.2 * math.cos(k), 7.0 + k * 0.75), 0.18 + 0.05 * (k % 3), BUBBLE, C_DETAIL)
for k in range(4):
    dot(f"Pipe Bubble {k + 1}", SP + V(0.25 * math.sin(k * 2), -0.4, 0.5 + k * 0.6), 0.12 + 0.03 * k, BUBBLE, C_DETAIL)

finish_mine(bg=(0.004, 0.02, 0.035), tint=(0.55, 0.85, 1.0))
