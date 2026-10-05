"""Phoenix Nest Mine - a phoenix bursts up out of a woven twig nest, wings of flame spread wide;
ore drops from a cracked golden egg at the nest's edge. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_NEST, C_BIRD, C_WINGS, C_FIRE = begin("PhoenixNestMine", ["Base", "Nest", "Phoenix", "Wings", "Fire"], seed=66)
CHAR = M("Charcoal", (30, 24, 22), rough=0.6)
TRIM = M("Fire Trim (Metal)", (255, 110, 30), rough=0.3, metal=0.5, glow=(255, 90, 20), glow_strength=1.2, rbx="Neon")
EMB = M("Ember Marble (Marble)", (34, 18, 12), rough=0.3, marble=((28, 14, 10), (255, 140, 40)))
ROCK = M("Volcanic Rock", (62, 50, 46), rough=0.9, rbx="Slate", noise=((40, 32, 30), (90, 74, 66), 3.0, 0.5))
TWIG = M("Twigs (Wood)", (112, 78, 46), rough=0.85, rbx="Wood")
TWIG2 = M("Dark Twigs (Wood)", (78, 52, 32), rough=0.85, rbx="Wood")
RED = M("Phoenix Red", (190, 28, 18), rough=0.5, rbx="SmoothPlastic")
ORANGE = M("Phoenix Orange", (255, 100, 20), rough=0.4, glow=(255, 80, 10), glow_strength=1.4, rbx="Neon", light=(10, 1.2))
YELLOW = M("Flame Yellow", (255, 190, 40), rough=0.4, glow=(255, 160, 20), glow_strength=2.6, rbx="Neon", light=(12, 1.6))
GOLD = M("Gold (Metal)", (240, 190, 70), rough=0.25, metal=1.0, glow=(120, 70, 10), glow_strength=0.3)
EYE = M("Eye Glow", (255, 255, 220), rough=0.3, glow=(255, 240, 160), glow_strength=10.0, rbx="Neon")
EGG = M("Egg Shell", (235, 190, 90), rough=0.25, metal=0.6, rbx="Metal")
ORE = M("Phoenix Ore", (255, 190, 90), rough=0.15, glow=(255, 150, 40), glow_strength=2.4, rbx="Neon")

top = base_plinth(10.5, 10.5, CHAR, TRIM, EMB, C_BASE, c=1.6)
for k in range(5):
    a = math.radians(30 + 72 * k)
    rock_f(f"Pedestal Rock {k + 1}", V(1.6 * math.cos(a), 0.8 + 1.6 * math.sin(a), top + 0.8), (1.6, 1.3, 1.1), ROCK, C_NEST)

# ---- woven nest: rings of twigs
N = V(0, 0.8, top + 2.0)
rnd = random.Random(6)
for k in range(46):
    r0 = rnd.uniform(2.4, 3.6);a0 = rnd.uniform(0, 2 * math.pi);span = rnd.uniform(0.7, 1.4)
    z0 = rnd.uniform(-0.5, 1.2)
    pts = []
    for i in range(6):
        t = i / 5;a = a0 + span * t;r = r0 + 0.35 * math.sin(t * 3 + k)
        pts.append(N + V(r * math.cos(a), r * math.sin(a), z0 + 0.4 * math.sin(t * math.pi + k) * (1 if k % 2 else -1)))
    path_tube(f"Twig {k + 1}", pts, [0.13] * 6, TWIG if k % 3 else TWIG2, C_NEST, n=5, cap=True)
lathe("Nest Bowl", N + V(0, 0, -0.6), [(1.2, 0), (2.9, 0.5), (3.3, 1.4), (2.9, 1.5), (2.4, 0.9), (0.0, 0.7)], TWIG2, C_NEST, n=20, smooth=False)
for k in range(4):                                          # loose sticks poking out
    a = rnd.uniform(0, 2 * math.pi)
    p = N + V(3.2 * math.cos(a), 3.2 * math.sin(a), rnd.uniform(0, 1))
    cyl(f"Stray Stick {k + 1}", p, p + V(1.3 * math.cos(a + 0.4), 1.3 * math.sin(a + 0.4), rnd.uniform(-0.4, 0.8)), 0.09, 0.06, TWIG, C_NEST, n=5)

# ---- the phoenix
B = N + V(0, 0.2, 2.4)
lathe("Phoenix Body", B, [(0.4, 0), (1.1, 0.6), (1.35, 1.6), (1.15, 2.7), (0.75, 3.5), (0.55, 3.9)], RED, C_BIRD, n=18)
lathe("Phoenix Chest", B + V(0, -0.45, 0.6), [(0.0, 0), (0.85, 0.3), (1.0, 1.2), (0.7, 2.2), (0.0, 2.5)], ORANGE, C_BIRD, n=14)
for k in range(12):                                         # golden chest scales
    z = 0.9 + (k // 3) * 0.5;a = math.radians(-90 + (k % 3 - 1) * 28)
    c = B + V(1.15 * math.cos(a), 1.15 * math.sin(a) - 0.2, z)
    blade(f"Chest Scale {k + 1}", [c + V(-0.22, 0, 0.18), c + V(0.22, 0, 0.18), c + V(0, -0.08, -0.25)], 0.05, GOLD, C_BIRD)
Hd = B + V(0, -0.35, 4.6)
lathe("Phoenix Head", Hd + V(0, 0, -0.7), [(0.5, 0), (0.85, 0.4), (0.8, 1.0), (0.4, 1.35), (0.0, 1.4)], RED, C_BIRD, n=14)
cone("Beak", Hd + V(0, -0.65, 0.05), Hd + V(0, -1.55, -0.35), 0.28, GOLD, C_BIRD, n=8)
for side in (1, -1):
    dot(f"Eye {side}", Hd + V(side * 0.42, -0.62, 0.25), 0.12, EYE, C_BIRD)
for k in range(5):                                          # crest of flame feathers
    a = math.radians(-50 + k * 25)
    base = Hd + V(0, 0.1, 0.5)
    tip = base + V(0.55 * math.sin(a), 1.2 + 0.2 * k * 0, 1.8 - abs(k - 2) * 0.35)
    blade(f"Crest {k + 1}", [base + V(-0.15, 0, 0), base + V(0.15, 0, 0), tip], 0.08, YELLOW if k % 2 else ORANGE, C_BIRD)

# ---- wings: layered flame feathers sweeping up and out
for side, lab in ((1, "L"), (-1, "R")):
    sh = B + V(side * 1.1, 0.3, 2.9)
    for row, (mat, L0, spread) in enumerate(((RED, 3.8, 1.0), (ORANGE, 3.0, 0.82), (YELLOW, 2.0, 0.62))):
        for k in range(8):
            t = k / 7
            ang = math.radians(10 + 75 * t)                  # from sideways up to near vertical
            d = V(side * math.cos(ang) * spread, 0.35 + 0.2 * t, math.sin(ang) * 0.95 + 0.25).normalized()
            root = sh + V(side * 0.4 * t, 0.1 * row, 0.3 * t)
            L = L0 * (0.75 + 0.45 * math.sin(math.pi * (0.2 + 0.8 * t)))
            w = 0.38 - 0.06 * row
            perp = d.cross(V(0, 1, 0)).normalized()
            blade(f"Wing {lab} R{row + 1} F{k + 1}", [root - perp * w, root + perp * w, root + d * L * 0.7 + perp * w * 0.6, root + d * L, root + d * L * 0.7 - perp * w * 0.3], 0.07, mat, C_WINGS)
    path_tube(f"Wing Arm {lab}", [sh, sh + V(side * 1.4, 0.3, 0.9), sh + V(side * 2.4, 0.5, 2.0)], [0.28, 0.2, 0.1], RED, C_WINGS, n=8)

# ---- flowing flame tail curling down over the nest
for k in range(5):
    off = (k - 2) * 0.45
    pts = [B + V(off * 0.4, 1.0, 0.8)]
    for i in range(1, 10):
        t = i / 9
        pts.append(B + V(off * (0.4 + 1.6 * t), 1.0 + 3.0 * t, 0.8 - 2.6 * t + 1.2 * math.sin(t * math.pi)))
    path_tube(f"Tail Plume {k + 1}", pts, [0.3 * (1 - 0.8 * i / 9) + 0.04 for i in range(10)], [RED, ORANGE, YELLOW, ORANGE, RED][k], C_WINGS, n=8)
    blade(f"Tail Tip {k + 1}", [pts[-1] + V(-0.3, 0, 0), pts[-1] + V(0.3, 0, 0), pts[-1] + V(off * 0.5, 0.9, -0.4)], 0.06, YELLOW, C_WINGS)

# ---- flames round the nest, embers, cracked golden egg (ore drop) at the front
for k in range(9):
    a = math.radians(-70 + k * 40)
    p = N + V(3.4 * math.cos(a), 3.4 * math.sin(a), 0.6)
    h = 1.2 + 0.6 * (k % 3)
    lathe(f"Flame {k + 1}", p, [(0.42, 0), (0.36, h * 0.35), (0.2, h * 0.75), (0.0, h)], ORANGE if k % 2 else YELLOW, C_FIRE, n=8)
for k in range(14):
    a = rnd.uniform(0, 2 * math.pi);r = rnd.uniform(1.5, 5.0)
    dot(f"Ember {k + 1}", V(r * math.cos(a), 0.8 + r * math.sin(a), top + rnd.uniform(3, 12)), rnd.uniform(0.06, 0.12), YELLOW, C_FIRE)
EG = N + V(0, -3.4, -0.2)
lathe("Golden Egg", EG + V(0, 0, -0.9), [(0.0, 0), (0.6, 0.25), (0.78, 0.8), (0.66, 1.35), (0.0, 1.75)], EGG, C_FIRE, n=16)
for k in range(4):
    a = math.radians(-120 + 50 * k)
    beam(f"Egg Crack {k + 1}", EG + V(0.75 * math.cos(a), -0.2 + 0.55 * math.sin(a) * 0, 0.2 + 0.25 * k), EG + V(0.7 * math.cos(a + 0.5), -0.55, 0.5 + 0.2 * k), 0.07, 0.05, V(0, -1, 0), YELLOW, C_FIRE)
ore_cube(EG + V(0, -1.4, -0.8), ORE, C_FIRE)

finish_mine(bg=(0.03, 0.012, 0.006), tint=(1.0, 0.7, 0.5))
