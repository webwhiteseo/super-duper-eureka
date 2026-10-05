"""Glowshroom Grove Mine - a giant glowing mushroom (with a tiny gnome door in its stalk) towers over smaller
mushrooms, roots and fairy lanterns; ore drips from a glowing spore pod under the cap.
Built with mine_kit (same pipeline as the other Ore Factory mines)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_SHROOM, C_SMALL, C_ROOTS, C_DETAIL = begin("GlowshroomGroveMine", ["Base", "Giant Mushroom", "Small Mushrooms", "Roots", "Details"], seed=33)
EARTH = M("Dark Earth", (34, 26, 22), rough=0.8)
TRIM = M("Spore Trim (Metal)", (60, 230, 200), rough=0.3, metal=0.4, glow=(40, 220, 190), glow_strength=1.0, rbx="Neon")
MOSSM = M("Moss Marble (Marble)", (24, 44, 30), rough=0.4, marble=((20, 38, 26), (110, 255, 210)))
STEM = M("Mushroom Stem", (232, 222, 196), rough=0.6, noise=((210, 198, 168), (246, 240, 220), 3.0, 0.25))
CAP = M("Violet Cap", (112, 62, 205), rough=0.45, noise=((84, 40, 170), (150, 96, 235), 2.5, 0.25))
CAP2 = M("Teal Cap", (40, 170, 160), rough=0.45, noise=((26, 130, 124), (70, 210, 196), 2.5, 0.25))
CAP3 = M("Magenta Cap", (220, 60, 160), rough=0.45, noise=((180, 40, 130), (250, 110, 200), 2.5, 0.25))
SPOT = M("Glow Spots", (150, 255, 240), rough=0.3, glow=(90, 255, 230), glow_strength=5.0, rbx="Neon", light=(9, 1.0))
GILL = M("Glowing Gills", (210, 160, 255), rough=0.4, glow=(170, 110, 255), glow_strength=3.0, rbx="Neon", light=(12, 1.4))
ROOT = M("Roots (Wood)", (92, 70, 50), rough=0.85, rbx="Wood")
MOSS = M("Moss", (64, 130, 56), rough=0.9, rbx="LeafyGrass", noise=((44, 100, 40), (90, 160, 72), 4.0, 0.3))
STONE = M("Mossy Stone", (88, 96, 92), rough=0.9, rbx="Slate", noise=((60, 70, 66), (116, 124, 118), 3.0, 0.5))
WOOD = M("Door Wood", (128, 82, 46), rough=0.7, rbx="WoodPlanks")
WARM = M("Window Glow", (255, 210, 130), rough=0.4, glow=(255, 170, 70), glow_strength=6.0, rbx="Neon", light=(8, 1.2))
FAIRY = M("Fairy Light", (240, 255, 160), rough=0.3, glow=(220, 255, 120), glow_strength=8.0, rbx="Neon", light=(6, 0.8))
VINE = M("Vine", (50, 110, 60), rough=0.8)
POD = M("Spore Pod", (190, 255, 220), rough=0.1, glow=(120, 255, 200), glow_strength=2.5, rbx="Glass", alpha=0.2)
ORE = M("Spore Ore", (180, 255, 225), rough=0.15, glow=(110, 255, 200), glow_strength=2.0, rbx="Neon")

top = base_plinth(10.5, 10.5, EARTH, TRIM, MOSSM, C_BASE, c=1.6)
lathe("Moss Mound", V(0, 0.8, top - 0.05), [(4.6, 0), (4.2, 0.3), (2.8, 0.6), (1.0, 0.7)], MOSS, C_BASE, n=20, smooth=False)

# ---- giant mushroom: curved stalk, wide cap, glowing spots and gills
S0 = V(0.2, 1.2, top + 0.5)
stalk = [S0 + V(0.35 * math.sin(t * 2.2), -0.25 * t, t * 9.0) for t in [i / 8 for i in range(9)]]
path_tube("Giant Stalk", stalk, [1.75, 1.55, 1.4, 1.3, 1.22, 1.18, 1.15, 1.18, 1.3], STEM, C_SHROOM, n=20)
lathe("Stalk Skirt", stalk[-3] + V(0, 0, 0.2), [(1.25, 0), (2.1, -0.6), (1.9, -0.75), (1.2, -0.25)], STEM, C_SHROOM, n=20)  # ring/annulus
CT = stalk[-1] + V(0, 0, 0.1)
lathe("Giant Cap", CT, [(0.9, -0.2), (4.9, 0.0), (5.3, 0.45), (4.9, 1.5), (3.9, 2.6), (2.4, 3.4), (0.9, 3.75), (0.0, 3.8)], CAP, C_SHROOM, n=32)
for k in range(28):                                         # gills under the cap
    a = 2 * math.pi * k / 28
    blade(f"Gill {k + 1}", [CT + V(1.0 * math.cos(a), 1.0 * math.sin(a), -0.15), CT + V(4.8 * math.cos(a), 4.8 * math.sin(a), 0.02),
                            CT + V(4.5 * math.cos(a), 4.5 * math.sin(a), 0.32), CT + V(1.0 * math.cos(a), 1.0 * math.sin(a), 0.3)], 0.06, GILL, C_SHROOM)
rnd = random.Random(5)
for k in range(26):                                         # glowing spots on the cap
    a = rnd.uniform(0, 2 * math.pi);t = rnd.uniform(0.15, 0.95)
    r = 4.9 * math.sin(math.pi / 2 * (1 - t)) + 0.4;z = 0.8 + 2.9 * t
    dot(f"Cap Spot {k + 1}", CT + V(r * math.cos(a), r * math.sin(a), z), rnd.uniform(0.22, 0.42), SPOT, C_SHROOM)
# gnome door, round window and steps in the stalk
D = V(stalk[0].x, stalk[0].y - 1.72, top + 1.75)
abox("Door", D.x - 0.55, D.x + 0.55, D.y - 0.1, D.y + 0.5, D.z - 1.15, D.z + 0.6, WOOD, C_SHROOM)
abox("Door Frame", D.x - 0.72, D.x + 0.72, D.y - 0.02, D.y + 0.55, D.z - 1.15, D.z + 0.62, ROOT, C_SHROOM)
torus("Door Arch", D + V(0, -0.12, 0.6), V(0, -1, 0), V(0, 0, 1), 0.56, 0.1, ROOT, C_SHROOM, n_major=16, n_minor=6)
dot("Door Knob", D + V(0.32, -0.2, -0.3), 0.08, WARM, C_SHROOM)
W = stalk[3] + V(0.4, -1.3, 0)
torus("Window Frame", W, V(0.2, -1, 0), V(0, 0, 1), 0.42, 0.09, WOOD, C_SHROOM, n_major=16, n_minor=6)
cyl("Window Glow", W - V(0.04, -0.2, 0), W + V(0.04, -0.12, 0), 0.36, 0.36, WARM, C_SHROOM, n=14, hint=V(0, 0, 1))
for k in range(3):
    abox(f"Step {k + 1}", D.x - 0.7, D.x + 0.7, D.y - 0.5 - k * 0.45, D.y - 0.1 - k * 0.45, top + 0.6 - k * 0.2, top + 0.85 - k * 0.2, STONE, C_SHROOM)

# ---- spore pod and drip (the ore drop) hanging at the front of the cap
PD = CT + V(0, -3.6, -0.6)
cyl("Pod Stem", CT + V(0, -3.4, 0.1), PD + V(0, 0, 0.6), 0.08, 0.08, VINE, C_DETAIL, n=6)
lathe("Spore Pod", PD + V(0, 0, -0.9), [(0.0, 0), (0.45, 0.2), (0.62, 0.7), (0.5, 1.2), (0.2, 1.5)], POD, C_DETAIL, n=14)
dot("Pod Core", PD - V(0, 0, 0.2), 0.3, SPOT, C_DETAIL)
for k in range(4):
    dot(f"Drip {k + 1}", PD - V(0, 0, 1.3 + 0.7 * k), 0.12 - 0.015 * k, POD, C_DETAIL)
ore_cube(V(PD.x, PD.y, top + 1.6), ORE, C_DETAIL)

# ---- smaller mushrooms around
def mushroom(name, P, h, rcap, cap_mat, lean=V(0, 0, 0), spots=6, seed=0):
    r_ = random.Random(seed)
    pts = [P + lean * (t * t) + V(0, 0, h * t) for t in [i / 4 for i in range(5)]]
    path_tube(f"{name} Stalk", pts, [rcap * 0.3, rcap * 0.26, rcap * 0.24, rcap * 0.24, rcap * 0.26], STEM, C_SMALL, n=12)
    c = pts[-1]
    lathe(f"{name} Cap", c, [(rcap * 0.25, -0.05), (rcap, 0.0), (rcap * 1.05, rcap * 0.12), (rcap * 0.85, rcap * 0.45), (rcap * 0.45, rcap * 0.68), (0, rcap * 0.72)], cap_mat, C_SMALL, n=20)
    lathe(f"{name} Gills", c + V(0, 0, -0.02), [(rcap * 0.25, 0), (rcap * 0.97, 0.01)], GILL, C_SMALL, n=20)
    for k in range(spots):
        a = r_.uniform(0, 2 * math.pi);t = r_.uniform(0.2, 0.8)
        rr = rcap * (1 - 0.6 * t);z = rcap * (0.15 + 0.5 * t)
        dot(f"{name} Spot {k + 1}", c + V(rr * math.cos(a), rr * math.sin(a), z), rcap * 0.12, SPOT, C_SMALL)
mushroom("Teal Shroom", V(-3.2, 2.4, top + 0.3), 5.2, 1.9, CAP2, lean=V(-0.6, 0.3, 0), seed=1)
mushroom("Magenta Shroom", V(3.4, 2.8, top + 0.3), 3.8, 1.5, CAP3, lean=V(0.5, 0.2, 0), seed=2)
mushroom("Tiny Shroom A", V(-3.9, -3.2, top + 0.1), 1.6, 0.7, CAP3, lean=V(-0.2, -0.1, 0), seed=3)
mushroom("Tiny Shroom B", V(-3.2, -3.9, top + 0.1), 1.1, 0.5, CAP2, seed=4)
mushroom("Tiny Shroom C", V(3.9, -3.5, top + 0.1), 1.4, 0.6, CAP, lean=V(0.2, -0.2, 0), seed=5)
mushroom("Tiny Shroom D", V(2.6, 4.3, top + 0.1), 1.2, 0.55, CAP2, seed=6)

# ---- roots spreading from the stalk, mossy stones
for k in range(7):
    a = math.radians(20 + k * 52)
    d = V(math.cos(a), math.sin(a), 0)
    pts = [S0 + d * 1.2 + V(0, 0, 0.6), S0 + d * 2.2 + V(0, 0, 0.25), S0 + d * 3.3 + V(0, 0, 0.05) + V(-d.y, d.x, 0) * 0.4, S0 + d * 4.2 + V(0, 0, -0.1)]
    path_tube(f"Root {k + 1}", pts, [0.45, 0.32, 0.22, 0.08], ROOT, C_ROOTS, n=8)
for k, (x, y, s) in enumerate(((4.1, 0.2, 0.7), (-4.2, -0.8, 0.8), (1.6, -4.3, 0.55), (-1.4, 4.4, 0.6))):
    rock_f(f"Mossy Stone {k + 1}", V(x, y, top + s * 0.35), (s, s * 0.85, s * 0.6), STONE, C_ROOTS)
    lathe(f"Moss Cap {k + 1}", V(x, y, top + s * 0.75), [(s * 0.7, 0), (s * 0.4, s * 0.2), (0, s * 0.25)], MOSS, C_ROOTS, n=10, smooth=False)

# ---- fairy lanterns hanging from the cap rim, fireflies
for k in range(7):
    a = math.radians(-60 + k * 52)
    c = CT + V(4.9 * math.cos(a), 4.9 * math.sin(a), 0.3)
    drop_len = 1.2 + 0.5 * (k % 3)
    cyl(f"Fairy Vine {k + 1}", c, c - V(0, 0, drop_len), 0.04, 0.04, VINE, C_DETAIL, n=4)
    lathe(f"Fairy Lantern {k + 1}", c - V(0, 0, drop_len + 0.5), [(0.0, 0), (0.22, 0.1), (0.25, 0.35), (0.12, 0.5)], FAIRY, C_DETAIL, n=8)
for k in range(10):
    a = rnd.uniform(0, 2 * math.pi);r = rnd.uniform(2.5, 5.2)
    dot(f"Firefly {k + 1}", V(r * math.cos(a), 0.8 + r * math.sin(a), top + rnd.uniform(2, 9)), 0.08, FAIRY, C_DETAIL)

finish_mine(bg=(0.01, 0.02, 0.03), tint=(0.7, 0.85, 1.0))
