"""Candy Oven Furnace - a pink bakery oven on a chocolate-bar base with a giant cupcake roof: conveyors feed ore straight
into the glowing oven door at ground level (no ramp). Candy canes, lollipops, gumdrops and sprinkles. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_OVEN, C_CAKE, C_CANDY = begin("CandyOvenFurnace", ["Chocolate", "Oven", "Cupcake", "Candy"], seed=91)
CHOC = M("Chocolate", (92, 52, 32), rough=0.4, rbx="SmoothPlastic")
CHOC2 = M("Milk Chocolate", (130, 80, 50), rough=0.4, rbx="SmoothPlastic")
PINK = M("Oven Pink", (255, 150, 190), rough=0.4)
ICING = M("Icing", (255, 248, 250), rough=0.5)
RED = M("Candy Red", (230, 40, 60), rough=0.3)
WHITE = M("Candy White", (250, 250, 250), rough=0.3)
OVEN = M("Oven Glow", (255, 150, 60), rough=0.3, glow=(255, 110, 30), glow_strength=4.0, rbx="Neon", light=(14, 1.8))
DARK = M("Oven Dark", (40, 20, 20), rough=0.6)
WRAP = M("Cupcake Wrapper", (120, 210, 255), rough=0.4)
FROST = M("Frosting", (255, 190, 220), rough=0.5)
CHERRY = M("Cherry", (210, 20, 40), rough=0.2, metal=0.2)
GUMS = [M("Gum Green", (90, 230, 120), rough=0.2, rbx="Glass", alpha=0.1), M("Gum Yellow", (255, 220, 60), rough=0.2, rbx="Glass", alpha=0.1),
        M("Gum Purple", (190, 110, 255), rough=0.2, rbx="Glass", alpha=0.1)]
SPR = [M("Sprinkle Blue", (60, 160, 255), rough=0.3, rbx="Neon"), M("Sprinkle Yellow", (255, 230, 60), rough=0.3, rbx="Neon"), M("Sprinkle Green", (80, 230, 120), rough=0.3, rbx="Neon")]
BURN = M("Burn Zone", (255, 160, 80), rough=0.2, glow=(255, 120, 40), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(91)

# ---- chocolate bar base
abox("Choc Slab", -6.2, 6.2, -5.6, 5.6, 0, 0.25, CHOC, C_BASE)
for i in range(4):
    for j in range(4):
        x0, y0 = -6.0 + i * 3.0, -5.4 + j * 2.75
        hexa(f"Choc Block {i}{j}", [V(x0, y0, 0.25), V(x0 + 2.8, y0, 0.25), V(x0 + 2.8, y0 + 2.55, 0.25), V(x0, y0 + 2.55, 0.25),
                                    V(x0 + 0.2, y0 + 0.2, 0.45), V(x0 + 2.6, y0 + 0.2, 0.45), V(x0 + 2.6, y0 + 2.35, 0.45), V(x0 + 0.2, y0 + 2.35, 0.45)], CHOC2, C_BASE)
# ---- oven body with a ground-level door
abox("Oven Back", -4.0, 4.0, -0.4, 3.2, 0.45, 5.0, PINK, C_OVEN)
for s in (-1, 1):
    abox(f"Oven Side {s}", min(s * 2.6, s * 4.0), max(s * 2.6, s * 4.0), -2.8, -0.4, 0.45, 5.0, PINK, C_OVEN)
abox("Oven Lintel", -2.6, 2.6, -2.8, -0.4, 2.8, 5.0, PINK, C_OVEN)
abox("Oven Interior", -2.6, 2.6, -0.45, -0.3, 0.45, 2.8, OVEN, C_OVEN)
abox("Oven Floor", -2.6, 2.6, -2.8, -0.3, 0.0, 0.45, DARK, C_OVEN)
for k in range(5):
    abox(f"Oven Rack {k}", -2.5, 2.5, -1.6 + k * 0.25, -1.55 + k * 0.25, 1.5, 1.55, WHITE, C_OVEN) if False else None
for k in range(14):                                         # candy-stripe arch round the door
    a0 = math.radians(k * 180 / 14);a1 = math.radians((k + 1) * 180 / 14)
    p = [V(r * math.cos(a), -2.85, 2.8 + r * math.sin(a) * 0.0) for r, a in ()]
for k in range(8):
    z0 = 0.45 + k * 0.3
    for s in (-1, 1):
        abox(f"Door Post {s}{k}", min(s * 2.6, s * 3.0), max(s * 2.6, s * 3.0), -2.95, -2.75, z0, z0 + 0.3, RED if k % 2 else WHITE, C_OVEN)
for k in range(14):
    x0 = -3.0 + k * (6.0 / 14)
    abox(f"Door Lintel {k}", x0, x0 + 6.0 / 14, -2.95, -2.75, 2.85, 3.25, RED if k % 2 else WHITE, C_OVEN)
burn_zone(BURN, -2.4, 2.4, -3.4, -0.6, 0.05, 2.6, C_OVEN)
for k in range(9):                                          # icing drips on the top edge
    x = -3.6 + k * 0.9
    ellip(f"Icing Drip {k}", V(x, -2.85, 4.75 - 0.25 * (k % 3)), 0.42, 0.18, 0.5 + 0.2 * (k % 3), ICING, C_OVEN, n=10, m=4)
abox("Icing Top", -4.1, 4.1, -2.9, 3.3, 5.0, 5.3, ICING, C_OVEN)
for s in (-1, 1):                                           # oven knobs + window
    for k in range(2):
        cyl(f"Knob {s}{k}", V(s * 3.3, -2.85, 3.6 - 0.8 * k), V(s * 3.3, -3.05, 3.6 - 0.8 * k), 0.25, 0.22, WHITE, C_OVEN, n=12, hint=Z_AX)
# ---- giant cupcake roof
CC = V(0, 1.4, 5.3)
lathe("Cupcake Wrapper", CC, [(2.6, 0), (3.2, 1.8), (3.25, 1.9), (0.01, 1.9)], WRAP, C_CAKE, n=20, smooth=False)
for k in range(20):
    a = 2 * math.pi * k / 20
    cyl(f"Wrapper Ridge {k}", CC + V(2.62 * math.cos(a), 2.62 * math.sin(a), 0.05), CC + V(3.22 * math.cos(a), 3.22 * math.sin(a), 1.85), 0.06, 0.06, WHITE, C_CAKE, n=4)
for k, (r, z) in enumerate(((3.1, 2.3), (2.6, 3.0), (2.0, 3.6), (1.35, 4.15), (0.75, 4.6))):
    torus(f"Frosting Swirl {k}", CC + V(0, 0, z), Z_AX, Y_AX, r * 0.8, r * 0.38, FROST, C_CAKE, n_major=24, n_minor=10)
cone("Frosting Tip", CC + V(0, 0, 4.7), CC + V(0, 0, 5.6), 0.5, FROST, C_CAKE, n=12)
dot("Cherry", CC + V(0, 0, 5.9), 0.5, CHERRY, C_CAKE)
path_tube("Cherry Stem", [CC + V(0, 0, 6.3), CC + V(0.3, 0.1, 6.9), CC + V(0.7, 0.2, 7.2)], [0.06, 0.05, 0.04], CHOC, C_CAKE, n=5)
for k in range(30):
    a = rnd.uniform(0, 6.28);z = rnd.uniform(2.3, 4.6);r = 3.0 * (1 - (z - 2.3) / 2.8) + 0.5
    p = CC + V(r * math.cos(a), r * math.sin(a), z)
    d = V(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 0.3)).normalized()
    cyl(f"Sprinkle {k}", p - d * 0.15, p + d * 0.15, 0.06, 0.06, SPR[k % 3], C_CAKE, n=4)
# ---- candy canes, lollipops, gumdrops
def cane(name, P, h, side):
    pts = [P + V(0, 0, h * t) for t in (0, 0.25, 0.5, 0.75, 1.0)]
    pts += [P + V(side * 0.6 * (1 - math.cos(a)), 0, h + 0.6 * math.sin(a)) for a in (0.6, 1.2, 1.9, 2.6, 3.1)]
    for k in range(len(pts) - 1):
        cyl(f"{name} {k}", pts[k], pts[k + 1], 0.25, 0.25, RED if k % 2 else WHITE, C_CANDY, n=10)
cane("Candy Cane L", V(-5.0, -4.2, 0.45), 3.2, 1)
cane("Candy Cane R", V(5.0, -4.2, 0.45), 3.2, -1)
for k, (x, y, h, mat) in enumerate(((-5.2, 2.6, 4.0, SPR[0]), (5.2, 2.6, 4.6, SPR[2]), (-4.6, 4.6, 3.0, SPR[1]))):
    cyl(f"Lolly Stick {k}", V(x, y, 0.45), V(x, y, h), 0.08, 0.08, WHITE, C_CANDY, n=6)
    cyl(f"Lolly Disc {k}", V(x, y - 0.15, h + 0.6), V(x, y + 0.15, h + 0.6), 0.8, 0.8, mat, C_CANDY, n=20, hint=Z_AX)
    pts = [V(x + 0.7 * t * math.cos(t * 12), y - 0.17, h + 0.6 + 0.7 * t * math.sin(t * 12)) for t in [i / 16 for i in range(17)]]
    path_tube(f"Lolly Swirl {k}", pts, [0.06] * 17, WHITE, C_CANDY, n=4)
for k, (x, y) in enumerate(((-3.4, -4.6), (3.4, -4.6), (5.4, -0.6), (-5.4, -0.8), (0.0, 4.8))):
    ellip(f"Gumdrop {k}", V(x, y, 0.45), 0.55, 0.55, 0.65, GUMS[k % 3], C_CANDY, n=12, m=4, half=True)

finish_mine(bg=(0.04, 0.02, 0.03), tint=(1.0, 0.9, 0.95))
write_furnace_lua("CandyOvenFurnace")
