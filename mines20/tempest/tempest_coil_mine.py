"""Tempest Coil Mine - a towering Tesla coil under a storm cloud arcs lightning to three side coils;
charged ore drops from the capacitor chute. Built with mine_kit (same pipeline as the other Ore Factory mines)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_TOWER, C_COILS, C_STORM, C_DETAIL = begin("TempestCoilMine", ["Base", "Tower", "Coils", "Storm", "Details"], seed=12)
BLACK = M("Black", (12, 12, 18), rough=0.45)
TRIM = M("Volt Trim (Metal)", (90, 170, 255), rough=0.3, metal=0.5, glow=(70, 150, 255), glow_strength=1.0, rbx="Neon")
SLATE = M("Storm Marble (Marble)", (26, 26, 40), rough=0.25, marble=((22, 22, 34), (190, 140, 255)))
COPPER = M("Copper (Metal)", (205, 115, 62), rough=0.3, metal=1.0)
CERAMIC = M("Ceramic", (232, 236, 246), rough=0.25, rbx="SmoothPlastic")
INSUL = M("Blue Glaze", (60, 90, 190), rough=0.2)
STEEL = M("Steel (Metal)", (110, 116, 128), rough=0.35, metal=0.9, plate=11.0)
VOLT = M("Lightning", (210, 230, 255), rough=0.3, glow=(150, 200, 255), glow_strength=10, light=(14, 2.0))
ARC = M("Violet Arc", (220, 170, 255), rough=0.3, glow=(180, 110, 255), glow_strength=8, rbx="Neon", light=(8, 1.0))
CLOUD = M("Storm Cloud", (78, 82, 104), rough=0.9, noise=((58, 62, 82), (110, 114, 136), 2.5, 0.3))
JAR = M("Jar Glass", (170, 210, 255), rough=0.05, glow=(120, 170, 255), glow_strength=1.2, rbx="Glass", alpha=0.3)
HAZ = M("Hazard Yellow", (250, 200, 30), rough=0.5)
RUBBER = M("Cable Rubber", (24, 24, 28), rough=0.8)
ORE = M("Charged Ore", (200, 225, 255), rough=0.15, glow=(140, 190, 255), glow_strength=2.2, rbx="Neon")

top = base_plinth(10.5, 10.5, BLACK, TRIM, SLATE, C_BASE, c=1.2)
for k in range(6):                                          # hazard stripes on the front edge
    x = -3.3 + k * 1.3
    hexa(f"Hazard Stripe {k + 1}", [V(x, -5.27, 0.3), V(x + 0.6, -5.27, 0.3), V(x + 0.6, -5.2, 0.3), V(x, -5.2, 0.3),
                                     V(x + 0.6, -5.27, 1.5), V(x + 1.2, -5.27, 1.5), V(x + 1.2, -5.2, 1.5), V(x + 0.6, -5.2, 1.5)], HAZ, C_BASE)

# ---- main tower: steel base, copper column, insulator stack, coil winding, toroid
T = V(0, 0.9, top)
lathe("Tower Foot", T, [(2.5, 0), (2.5, 0.5), (1.9, 0.8), (1.6, 1.4), (1.3, 1.5)], STEEL, C_TOWER, n=24, smooth=False)
cyl("Coil Former", T + V(0, 0, 1.5), T + V(0, 0, 8.6), 0.95, 0.85, CERAMIC, C_TOWER, n=24)
for k in range(26):                                         # copper winding
    z = 1.8 + k * 0.26
    torus(f"Winding {k + 1}", T + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 0.98 - 0.004 * k, 0.07, COPPER, C_TOWER, n_major=20, n_minor=4)
for k, z in enumerate((1.6, 8.7)):
    torus(f"Former Band {k + 1}", T + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 1.05, 0.14, STEEL, C_TOWER, n_major=24, n_minor=6)
for k in range(4):                                          # insulator skirts
    z = 9.0 + k * 0.62
    lathe(f"Insulator {k + 1}", T + V(0, 0, z), [(0.45, 0), (1.25 - 0.08 * k, 0.12), (1.15 - 0.08 * k, 0.28), (0.45, 0.42)], INSUL if k % 2 else CERAMIC, C_TOWER, n=20)
cyl("Top Stem", T + V(0, 0, 11.4), T + V(0, 0, 12.4), 0.35, 0.35, COPPER, C_TOWER, n=12)
torus("Toroid", T + V(0, 0, 12.8), V(0, 0, 1), V(0, 1, 0), 2.1, 0.7, STEEL, C_TOWER, n_major=40, n_minor=14)
sphere("Top Orb", T + V(0, 0, 13.6), 0.85, VOLT, C_TOWER)

# ---- three side coils
SIDE = []
for k, ang in enumerate((210, 330, 90)):
    a = math.radians(ang);P = V(3.7 * math.cos(a), 0.9 + 3.6 * math.sin(a), top)
    SIDE.append(P)
    lathe(f"Side Foot {k + 1}", P, [(0.9, 0), (0.9, 0.35), (0.6, 0.5)], STEEL, C_COILS, n=16, smooth=False)
    cyl(f"Side Former {k + 1}", P + V(0, 0, 0.5), P + V(0, 0, 3.6), 0.42, 0.38, CERAMIC, C_COILS, n=16)
    for j in range(10):
        torus(f"Side Winding {k + 1}-{j + 1}", P + V(0, 0, 0.75 + j * 0.27), V(0, 0, 1), V(0, 1, 0), 0.45, 0.06, COPPER, C_COILS, n_major=14, n_minor=4)
    torus(f"Side Toroid {k + 1}", P + V(0, 0, 3.9), V(0, 0, 1), V(0, 1, 0), 0.75, 0.25, STEEL, C_COILS, n_major=20, n_minor=8)
    sphere(f"Side Orb {k + 1}", P + V(0, 0, 4.25), 0.35, VOLT, C_COILS)

def bolt(name, a, b, mat, jag=0.45, seg=7, w=0.13, seed=0):
    r = random.Random(seed)
    pts = [a]
    d = b - a
    u, v = perp_basis(d)
    for i in range(1, seg):
        t = i / seg
        pts.append(a + d * t + u * r.uniform(-jag, jag) + v * r.uniform(-jag, jag))
    pts.append(b)
    for i in range(seg):
        beam(f"{name} {i + 1}", pts[i], pts[i + 1], w, w, u, mat, C_STORM)

for k, P in enumerate(SIDE):                                # arcs from the toroid to each side coil
    a = (P - T);a.z = 0;a.normalize()
    bolt(f"Arc {k + 1}", T + V(0, 0, 12.8) + a * 2.6, P + V(0, 0, 4.4), ARC if k % 2 else VOLT, jag=0.5, seg=8, seed=k)

# ---- storm cloud with a lightning strike into the top orb
CC = T + V(0, 0, 18.2)
rnd = random.Random(4)
for k in range(11):
    a = 2 * math.pi * k / 11;r = 2.6 if k % 2 else 1.6
    sc = rnd.uniform(1.4, 2.1)
    rock(f"Cloud Puff {k + 1}", CC + V(r * math.cos(a), r * 0.8 * math.sin(a), rnd.uniform(-0.3, 0.6)), (sc, sc * 0.9, sc * 0.7), CLOUD, C_STORM)
rock("Cloud Core", CC + V(0, 0, 0.6), (2.6, 2.2, 1.6), CLOUD, C_STORM)
bolt("Strike", CC - V(0, 0, 1.2), T + V(0, 0, 14.2), VOLT, jag=0.6, seg=6, w=0.18, seed=9)
for k in range(5):                                          # rain streaks
    a = 2 * math.pi * k / 5 + 0.4
    p = CC + V(2.4 * math.cos(a), 2.0 * math.sin(a), -1.3)
    beam(f"Rain {k + 1}", p, p + V(0.15, 0, -1.4), 0.05, 0.05, V(1, 0, 0), JAR, C_STORM)

# ---- capacitor (Leyden jars) and the ore chute at the front
J = V(0, -2.6, top)
for k, dx in enumerate((-1.4, 0, 1.4)):
    c = J + V(dx, 0, 0)
    lathe(f"Leyden Jar {k + 1}", c, [(0.55, 0), (0.6, 0.2), (0.6, 1.9), (0.42, 2.2), (0.25, 2.35)], JAR, C_DETAIL, n=16)
    cyl(f"Jar Foil {k + 1}", c + V(0, 0, 0.1), c + V(0, 0, 1.0), 0.62, 0.62, COPPER, C_DETAIL, n=16)
    cyl(f"Jar Rod {k + 1}", c + V(0, 0, 2.3), c + V(0, 0, 3.2), 0.06, 0.06, COPPER, C_DETAIL, n=6)
    dot(f"Jar Ball {k + 1}", c + V(0, 0, 3.3), 0.16, VOLT, C_DETAIL)
    bolt(f"Jar Spark {k + 1}", c + V(0, 0, 0.6), c + V(0, 0, 1.9), ARC, jag=0.18, seg=4, w=0.06, seed=20 + k)
abox("Chute Box", -1.2, 1.2, -4.4, -3.4, top, top + 1.6, STEEL, C_DETAIL)
abox("Chute Mouth Glow", -0.8, 0.8, -4.45, -4.38, top + 0.4, top + 1.3, VOLT, C_DETAIL)
hexa("Chute Lip", [V(-0.9, -4.4, top + 0.4), V(0.9, -4.4, top + 0.4), V(0.9, -5.2, top + 0.05), V(-0.9, -5.2, top + 0.05),
                   V(-0.9, -4.4, top + 0.55), V(0.9, -4.4, top + 0.55), V(0.9, -5.2, top + 0.2), V(-0.9, -5.2, top + 0.2)], STEEL, C_DETAIL)
ore_cube(V(0, -5.6, top + 0.9), ORE, C_DETAIL)
# control panel with lever and gauges (right side)
abox("Panel Body", -4.6, -3.4, -1.2, 1.4, top, top + 2.8, STEEL, C_DETAIL)
abox("Panel Face", -4.66, -4.6, -1.0, 1.2, top + 0.6, top + 2.6, BLACK, C_DETAIL)
for k, (y, z) in enumerate(((-0.45, 2.0), (0.6, 2.0))):
    cyl(f"Gauge {k + 1}", V(-4.62, y, top + z), V(-4.75, y, top + z), 0.38, 0.38, CERAMIC, C_DETAIL, n=16, hint=V(0, 0, 1))
    beam(f"Gauge Needle {k + 1}", V(-4.77, y, top + z), V(-4.77, y + 0.2, top + z + 0.25), 0.04, 0.04, V(-1, 0, 0), BLACK, C_DETAIL)
cyl("Lever Pivot", V(-4.66, 0.1, top + 1.0), V(-4.85, 0.1, top + 1.0), 0.18, 0.18, COPPER, C_DETAIL, n=10, hint=V(0, 0, 1))
cyl("Lever Arm", V(-4.8, 0.1, top + 1.0), V(-4.85, -0.5, top + 1.9), 0.07, 0.07, STEEL, C_DETAIL, n=6)
dot("Lever Knob", V(-4.86, -0.55, top + 1.95), 0.17, HAZ, C_DETAIL)
dot("Panel Light", V(-4.67, 0.1, top + 0.75), 0.12, VOLT, C_DETAIL)
# cables snaking across the base from the panel to the coils
for k, P in enumerate(SIDE):
    a0 = V(-3.4, 0.2, top + 0.15);mid = (a0 + P) / 2 + V(0.4 * k, -0.6, 0)
    path_tube(f"Cable {k + 1}", [a0, (a0 + mid) / 2 + V(0, 0, 0.05), mid, (mid + P) / 2, P + V(0, 0, 0.2)], [0.12] * 5, RUBBER, C_DETAIL, n=6)

finish_mine(bg=(0.012, 0.012, 0.03), tint=(0.7, 0.75, 1.0))
