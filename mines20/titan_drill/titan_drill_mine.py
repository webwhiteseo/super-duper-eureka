"""Titan Drill Mine - a heavy tracked mining rig. Its lattice derrick drives a giant auger into a glowing ore crater,
a conveyor hauls the ore up to a hopper and the chute drops it. Hazard paint, beacons, exhaust stacks, ladders.
Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_RIG, C_DRILL, C_CRAWLER, C_QUARRY = begin("TitanDrillMine", ["Base", "Derrick", "Drill", "Crawler", "Quarry"], seed=19)
PLATE = M("Tread Plate (Metal)", (66, 68, 72), rough=0.5, metal=0.7, rbx="DiamondPlate", plate=9.0)
HAZ = M("Hazard Yellow", (246, 184, 20), rough=0.4, rbx="SmoothPlastic")
GRAVEL = M("Quarry Gravel", (120, 110, 100), rough=0.95, rbx="Pebble", noise=((90, 82, 74), (156, 146, 134), 8.0, 0.5))
YEL = M("Rig Yellow", (240, 176, 20), rough=0.35, metal=0.2)
BLK = M("Hazard Black", (24, 24, 26), rough=0.5)
STEEL = M("Rig Steel (Metal)", (130, 134, 140), rough=0.35, metal=0.9, rbx="Metal")
RUBBER = M("Track Rubber", (34, 34, 36), rough=0.8, rbx="Rubber" if False else "SmoothPlastic")
ROCK = M("Quarry Rock", (108, 92, 80), rough=0.9, rbx="Slate", noise=((80, 66, 56), (140, 122, 106), 3.0, 0.5))
PIT = M("Pit Dark", (18, 16, 16), rough=0.9)
GLASS = M("Cab Glass", (150, 210, 240), rough=0.1, glow=(120, 190, 230), glow_strength=1.6, rbx="Glass", alpha=0.2)
BEACON = M("Beacon", (255, 130, 20), rough=0.3, glow=(255, 100, 0), glow_strength=5.0, rbx="Neon", light=(12, 1.6))
SMOKE = M("Exhaust Smoke", (110, 110, 116), rough=0.9, rbx="SmoothPlastic", alpha=0.25)
GEMG = M("Titan Crystal", (60, 255, 190), rough=0.1, glow=(30, 230, 160), glow_strength=2.0, rbx="Neon", light=(10, 1.2))
COPPER = M("Copper Pipe (Metal)", (190, 110, 60), rough=0.3, metal=1.0, rbx="Metal")
ORE = M("Titan Ore", (90, 255, 200), rough=0.15, glow=(40, 230, 170), glow_strength=2.0, rbx="Neon")

top = base_plinth(13.5, 13.5, PLATE, HAZ, GRAVEL, C_BASE, c=1.2)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(19)

# ---- ore crater
CC = V(-1.4, -1.4, top)
lathe("Crater Pit", CC, [(2.0, 0.02), (1.5, -0.01), (0.9, 0.0), (0.01, 0.01)], PIT, C_QUARRY, n=20)
for k in range(14):
    a = 2 * math.pi * k / 14 + rnd.uniform(-0.1, 0.1)
    r = 2.2 + rnd.uniform(-0.15, 0.2)
    s_ = rnd.uniform(0.45, 0.7)
    rock_f(f"Crater Rim {k + 1}", CC + V(r * math.cos(a), r * math.sin(a), 0.2), (s_, s_ * 0.9, s_ * 0.7), ROCK, C_QUARRY, rough=0.3)
    if k % 3 == 0:
        crystal(f"Rim Crystal {k + 1}", CC + V((r - 0.2) * math.cos(a), (r - 0.2) * math.sin(a), 0.4),
                V(-math.cos(a) * 0.4, -math.sin(a) * 0.4, 1), rnd.uniform(0.8, 1.3), 0.17, GEMG, C_QUARRY)
for k in range(8):                                          # debris
    a = rnd.uniform(0, 6.28);r = rnd.uniform(2.9, 3.6)
    rock_f(f"Debris {k + 1}", CC + V(r * math.cos(a), r * math.sin(a), 0.05), (0.25, 0.22, 0.18), ROCK, C_QUARRY, rough=0.35)

# ---- giant auger drill
shaft_top = top + 7.0
cyl("Drill Shaft", CC + V(0, 0, -0.3), V(CC.x, CC.y, shaft_top), 0.26, 0.26, STEEL, C_DRILL, n=12)
bm = bmesh.new()
N = 120;turns = 4.0;z0, z1 = top + 0.25, top + 4.6
inner, outer = [], []
for i in range(N + 1):
    t = i / N;a = 2 * math.pi * turns * t;z = z0 + (z1 - z0) * t
    taper = min(1.0, 0.35 + t * 3)
    inner.append(bm.verts.new(CC + V(0.26 * math.cos(a), 0.26 * math.sin(a), z - top + top - CC.z + 0) if False else V(CC.x + 0.26 * math.cos(a), CC.y + 0.26 * math.sin(a), z)))
    outer.append(bm.verts.new(V(CC.x + 0.95 * taper * math.cos(a), CC.y + 0.95 * taper * math.sin(a), z - 0.05)))
for i in range(N):
    bm.faces.new((inner[i], outer[i], outer[i + 1], inner[i + 1])).smooth = True
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.09)
finish("Auger Flight", bm, STEEL, C_DRILL, merge=0)
cone("Drill Tip", V(CC.x, CC.y, top + 0.3), V(CC.x, CC.y, top - 0.6), 0.45, BLK, C_DRILL, n=12)
for k in range(3):
    a = k * 2.1
    cone(f"Cutter Tooth {k + 1}", V(CC.x + 0.4 * math.cos(a), CC.y + 0.4 * math.sin(a), top + 0.3),
         V(CC.x + 0.75 * math.cos(a), CC.y + 0.75 * math.sin(a), top - 0.05), 0.1, GEMG, C_DRILL, n=4)
for k, z in enumerate((top + 4.8, top + 6.2)):
    torus(f"Shaft Collar {k + 1}", V(CC.x, CC.y, z), Z_AX, X_AX, 0.33, 0.08, YEL, C_DRILL, n_major=12, n_minor=4)

# ---- lattice derrick over the crater
H = 10.0
legs = []
for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
    b = V(CC.x + sx * 1.9, CC.y + sy * 1.9, top);t = V(CC.x + sx * 0.55, CC.y + sy * 0.55, top + H)
    legs.append((b, t))
    beam(f"Derrick Leg {sx}{sy}", b, t, 0.2, 0.2, X_AX if sx * sy > 0 else Y_AX, YEL, C_RIG)
    abox(f"Leg Footing {sx}{sy}", b.x - 0.35, b.x + 0.35, b.y - 0.35, b.y + 0.35, top, top + 0.3, BLK, C_RIG)
def leg_at(k, f):
    b, t = legs[k];return b + (t - b) * f
lv = [0.12, 0.3, 0.48, 0.66, 0.84, 1.0]
for li, f in enumerate(lv):
    for k in range(4):
        p0, p1 = leg_at(k, f), leg_at((k + 1) % 4, f)
        beam(f"Derrick Girt {li}{k}", p0, p1, 0.12, 0.12, Z_AX, YEL, C_RIG)
        if li < len(lv) - 1:
            q0, q1 = leg_at(k, lv[li + 1]), leg_at((k + 1) % 4, lv[li + 1])
            beam(f"Derrick Brace {li}{k}", p0, q1, 0.07, 0.07, Z_AX, STEEL, C_RIG)
CB = V(CC.x, CC.y, top + H)
abox("Crown Block", CB.x - 0.75, CB.x + 0.75, CB.y - 0.75, CB.y + 0.75, CB.z, CB.z + 0.45, BLK, C_RIG)
for k in range(3):
    cyl(f"Crown Sheave {k + 1}", V(CB.x - 0.3, CB.y - 0.3 + k * 0.3, CB.z + 0.65), V(CB.x + 0.3, CB.y - 0.3 + k * 0.3, CB.z + 0.65), 0.28, 0.28, STEEL, C_RIG, n=14, hint=Z_AX)
for s, mat in ((-1, BEACON), (1, BEACON)):
    dot(f"Crown Beacon {s}", CB + V(s * 0.6, s * 0.6, 0.65), 0.17, mat, C_RIG)
# top drive (motor housing on the shaft)
TD = V(CC.x, CC.y, shaft_top)
abox("Top Drive", TD.x - 0.8, TD.x + 0.8, TD.y - 0.65, TD.y + 0.65, TD.z, TD.z + 1.4, YEL, C_DRILL)
for k in range(4):
    abox(f"Top Drive Stripe {k}", TD.x - 0.82, TD.x + 0.82, TD.y - 0.67, TD.y + 0.67, TD.z + 0.12 + k * 0.32, TD.z + 0.22 + k * 0.32, BLK, C_DRILL) if k in (0, 3) else None
for k in range(5):
    abox(f"Motor Fin {k}", TD.x - 0.6 + k * 0.3 - 0.04, TD.x - 0.6 + k * 0.3 + 0.04, TD.y - 0.75, TD.y - 0.65, TD.z + 0.3, TD.z + 1.15, STEEL, C_DRILL)
for k in range(3):
    cyl(f"Drill Cable {k + 1}", V(CB.x - 0.25 + k * 0.25, CB.y, CB.z), V(TD.x - 0.25 + k * 0.25, TD.y, TD.z + 1.4), 0.03, 0.03, BLK, C_RIG, n=4)
path_tube("Hydraulic Hose", [TD + V(0.8, 0.3, 0.9), TD + V(1.6, 0.6, 0.4), TD + V(2.5, 1.4, -1.0), V(1.5, 1.8, top + 3.6)], [0.09] * 4, COPPER, C_RIG, n=8)

# ---- tracked crawler (back right)
CR = V(2.6, 2.9, top)
def track(name, y):
    ring = []
    for k in range(10):
        a = math.pi / 2 + math.pi * k / 9
        ring.append(V(CR.x - 1.9 + 0.65 * math.cos(a), y, CR.z + 0.7 + 0.65 * math.sin(a)))
    for k in range(10):
        a = -math.pi / 2 + math.pi * k / 9
        ring.append(V(CR.x + 1.9 + 0.65 * math.cos(a), y, CR.z + 0.7 + 0.65 * math.sin(a)))
    ring2 = [p + V(0, 0.9, 0) for p in ring]
    finish(f"{name} Belt", loft([ring, ring2], smooth_sides=False), RUBBER, C_CRAWLER, merge=0)
    per = ring + [ring[0]]
    for k in range(len(ring)):                               # grousers
        p0, p1 = per[k], per[k + 1]
        mid = (p0 + p1) / 2;tng = (p1 - p0).normalized()
        nrm = V(-tng.z, 0, tng.x) * -1 if False else (mid - V(mid.x if abs(mid.x - CR.x) < 1.9 else (CR.x - 1.9 if mid.x < CR.x else CR.x + 1.9), y, CR.z + 0.7)).normalized()
        obox(f"{name} Grouser {k}", mid + nrm * 0.06 + V(0, 0.45, 0), (0.14, 0.95, 0.12), tng, Y_AX, nrm, BLK, C_CRAWLER)
    for k, x in enumerate((-1.9, -0.95, 0.0, 0.95, 1.9)):
        r = 0.5 if k in (0, 4) else 0.32
        z = CR.z + 0.7 if k in (0, 4) else CR.z + 0.4
        cyl(f"{name} Wheel {k}", V(CR.x + x, y - 0.05, z), V(CR.x + x, y + 0.95, z), r, r, STEEL, C_CRAWLER, n=12, hint=Z_AX)
        dot(f"{name} Hub {k}", V(CR.x + x, y - 0.06, z), r * 0.4, YEL, C_CRAWLER)
for k, y in enumerate((CR.y - 1.9, CR.y + 1.0)):
    track(f"Track {k + 1}", y)
BZ = CR.z + 1.45
abox("Undercarriage", CR.x - 1.6, CR.x + 1.6, CR.y - 1.0, CR.y + 1.0, CR.z + 0.5, BZ, BLK, C_CRAWLER)
abox("Crawler Deck", CR.x - 2.7, CR.x + 2.7, CR.y - 2.1, CR.y + 2.1, BZ, BZ + 0.35, YEL, C_CRAWLER)
for k in range(14):                                         # hazard stripes on the deck edge
    x = CR.x - 2.6 + k * 0.38
    hexa(f"Deck Stripe {k}", [V(x, CR.y - 2.12, BZ + 0.05), V(x + 0.18, CR.y - 2.12, BZ + 0.05), V(x + 0.18, CR.y - 2.08, BZ + 0.05), V(x, CR.y - 2.08, BZ + 0.05),
                              V(x + 0.12, CR.y - 2.12, BZ + 0.3), V(x + 0.3, CR.y - 2.12, BZ + 0.3), V(x + 0.3, CR.y - 2.08, BZ + 0.3), V(x + 0.12, CR.y - 2.08, BZ + 0.3)], BLK, C_CRAWLER)
D = BZ + 0.35
# engine housing with grilles + exhaust stacks
abox("Engine House", CR.x - 0.2, CR.x + 2.6, CR.y - 1.4, CR.y + 1.9, D, D + 2.0, YEL, C_CRAWLER)
hexa("Engine Roof", [V(CR.x - 0.2, CR.y - 1.4, D + 2.0), V(CR.x + 2.6, CR.y - 1.4, D + 2.0), V(CR.x + 2.6, CR.y + 1.9, D + 2.0), V(CR.x - 0.2, CR.y + 1.9, D + 2.0),
                     V(CR.x, CR.y - 1.2, D + 2.35), V(CR.x + 2.4, CR.y - 1.2, D + 2.35), V(CR.x + 2.4, CR.y + 1.7, D + 2.35), V(CR.x, CR.y + 1.7, D + 2.35)], YEL, C_CRAWLER)
for k in range(6):
    abox(f"Grille Slat {k}", CR.x + 0.3 + k * 0.33, CR.x + 0.48 + k * 0.33, CR.y - 1.46, CR.y - 1.38, D + 0.4, D + 1.5, BLK, C_CRAWLER)
for k, x in enumerate((CR.x + 1.2, CR.x + 2.0)):
    cyl(f"Exhaust Stack {k + 1}", V(x, CR.y + 1.3, D + 2.3), V(x, CR.y + 1.3, D + 4.0), 0.18, 0.18, STEEL, C_CRAWLER, n=10)
    cyl(f"Exhaust Cap {k + 1}", V(x, CR.y + 1.3, D + 4.0), V(x + 0.1, CR.y + 1.3, D + 4.25), 0.22, 0.2, BLK, C_CRAWLER, n=10)
    for j in range(3):
        r = 0.3 + 0.18 * j
        rock_f(f"Exhaust Smoke {k}{j}", V(x - 0.3 * j, CR.y + 1.3 + 0.2 * j, D + 4.6 + 0.55 * j + 0.2 * k), (r, r, r * 0.8), SMOKE, C_CRAWLER, rough=0.2, subd=2)
for k in range(3):                                          # fuel tanks
    cyl(f"Fuel Tank {k + 1}", V(CR.x - 2.5, CR.y - 1.6 + k * 0.85, D + 0.4), V(CR.x - 0.4, CR.y - 1.6 + k * 0.85, D + 0.4), 0.38, 0.38, COPPER if k == 1 else STEEL, C_CRAWLER, n=14, hint=Z_AX) if k == 9 else None
cyl("Fuel Tank", V(CR.x - 2.5, CR.y + 1.55, D + 0.42), V(CR.x - 0.4, CR.y + 1.55, D + 0.42), 0.4, 0.4, STEEL, C_CRAWLER, n=14, hint=Z_AX)
for x in (CR.x - 2.2, CR.x - 0.7):
    torus(f"Tank Strap {x}", V(x, CR.y + 1.55, D + 0.42), X_AX, Z_AX, 0.41, 0.04, BLK, C_CRAWLER, n_major=14, n_minor=4)
# operator cab
CB0 = V(CR.x - 2.5, CR.y - 1.9, D)
abox("Cab Body", CB0.x, CB0.x + 2.0, CB0.y, CB0.y + 2.2, D, D + 2.6, YEL, C_CRAWLER)
abox("Cab Window Front", CB0.x + 0.2, CB0.x + 1.8, CB0.y - 0.04, CB0.y + 0.02, D + 1.2, D + 2.35, GLASS, C_CRAWLER)
abox("Cab Window Side", CB0.x - 0.04, CB0.x + 0.02, CB0.y + 0.2, CB0.y + 2.0, D + 1.2, D + 2.35, GLASS, C_CRAWLER)
abox("Cab Roof", CB0.x - 0.15, CB0.x + 2.15, CB0.y - 0.15, CB0.y + 2.35, D + 2.6, D + 2.8, BLK, C_CRAWLER)
for k, (dx, dy) in enumerate(((0.3, 0.3), (1.7, 0.3))):
    cyl(f"Cab Beacon Base {k}", V(CB0.x + dx, CB0.y + dy, D + 2.8), V(CB0.x + dx, CB0.y + dy, D + 2.9), 0.16, 0.16, BLK, C_CRAWLER, n=10)
    lathe(f"Cab Beacon {k}", V(CB0.x + dx, CB0.y + dy, D + 2.9), [(0.14, 0), (0.14, 0.25), (0.08, 0.32)], BEACON, C_CRAWLER, n=10)
abox("Cab Light Bar", CB0.x + 0.6, CB0.x + 1.4, CB0.y - 0.1, CB0.y + 0.05, D + 2.62, D + 2.75, GLASS, C_CRAWLER)
# railings + ladder
for k in range(4):
    z = D + 0.3 + k * 0.0
for s in (-1, 1):
    p0 = V(CR.x + 2.65, CR.y + s * 2.0, D)
    cyl(f"Rail Post {s}", p0, p0 + V(0, 0, 1.0), 0.04, 0.04, YEL, C_CRAWLER, n=6)
cyl("Rail Top", V(CR.x + 2.65, CR.y - 2.0, D + 1.0), V(CR.x + 2.65, CR.y + 2.0, D + 1.0), 0.05, 0.05, YEL, C_CRAWLER, n=6, hint=Z_AX)
for k in range(5):
    cyl(f"Ladder Rung {k}", V(CR.x + 2.8, CR.y - 0.4, top + 0.3 + k * 0.33), V(CR.x + 2.8, CR.y + 0.2, top + 0.3 + k * 0.33), 0.03, 0.03, STEEL, C_CRAWLER, n=6, hint=Z_AX)
for y in (CR.y - 0.4, CR.y + 0.2):
    cyl(f"Ladder Side {y}", V(CR.x + 2.8, y, top + 0.1), V(CR.x + 2.8, y, D + 0.1), 0.04, 0.04, STEEL, C_CRAWLER, n=6)
# boom arm from crawler to derrick
for dz in (0.0, 0.9):
    beam(f"Boom Chord {dz}", V(CR.x - 2.5, CR.y - 0.2, D + 1.0 + dz), leg_at(2, 0.48) + V(0, 0, dz - 0.3), 0.18, 0.18, Z_AX, YEL, C_RIG)
for k in range(5):
    f0 = k / 5;f1 = (k + 1) / 5
    a0 = V(CR.x - 2.5, CR.y - 0.2, D + 1.0);a1 = leg_at(2, 0.48) + V(0, 0, -0.3)
    beam(f"Boom Lacing {k}", a0 + (a1 - a0) * f0, a0 + (a1 - a0) * f1 + V(0, 0, 0.9), 0.08, 0.08, Z_AX, STEEL, C_RIG)

# ---- conveyor from the crater up to a hopper at the front right; the chute drops the ore
C0 = V(CC.x + 2.0, CC.y - 0.6, top + 0.5);C1 = V(4.3, -3.2, top + 4.2)
d = (C1 - C0);L = d.length;dn = d.normalized();sd = V(-dn.y, dn.x, 0).normalized()
up = dn.cross(sd).normalized() * -1 if dn.cross(sd).z < 0 else dn.cross(sd).normalized()
beam("Conveyor Belt", C0, C1, 0.9, 0.08, Z_AX, RUBBER, C_QUARRY)
for s in (-1, 1):
    beam(f"Conveyor Rail {s}", C0 + sd * s * 0.52 + up * 0.1, C1 + sd * s * 0.52 + up * 0.1, 0.1, 0.3, Z_AX, YEL, C_QUARRY)
for k in range(9):
    p = C0 + d * (k + 0.5) / 9 - up * 0.12
    cyl(f"Conveyor Roller {k}", p - sd * 0.5, p + sd * 0.5, 0.08, 0.08, STEEL, C_QUARRY, n=8, hint=Z_AX)
for k, f in enumerate((0.35, 0.7, 0.98)):
    p = C0 + d * f
    for s in (-1, 1):
        beam(f"Conveyor Leg {k}{s}", p + sd * s * 0.5 - up * 0.1, V(p.x, p.y, top) + sd * s * 0.6, 0.12, 0.12, dn, STEEL, C_QUARRY)
for k in range(5):
    p = C0 + d * (0.12 + 0.17 * k) + up * 0.18
    rock_f(f"Belt Ore {k + 1}", p, (0.22, 0.2, 0.16), GEMG if k % 2 else ROCK, C_QUARRY, rough=0.3)
HP = V(4.3, -3.7, top + 2.6)
lathe("Hopper", HP, [(0.35, 0), (1.3, 1.3), (1.35, 1.6)], YEL, C_QUARRY, n=4, smooth=False)
for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
    beam(f"Hopper Leg {sx}{sy}", HP + V(sx * 0.75, sy * 0.75, 0.8), V(HP.x + sx * 1.0, HP.y + sy * 1.0, top), 0.14, 0.14, X_AX, STEEL, C_QUARRY)
for k in range(5):
    rock_f(f"Hopper Ore {k + 1}", HP + V(rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6), 1.45), (0.3, 0.3, 0.22), GEMG, C_QUARRY, rough=0.3)
CH0 = HP + V(0, 0, 0.1);CH1 = V(HP.x, -6.2, top + 1.25)
beam("Chute", CH0, CH1, 0.75, 0.08, X_AX, STEEL, C_QUARRY)
for s in (-1, 1):
    beam(f"Chute Wall {s}", CH0 + V(s * 0.38, 0, 0.18), CH1 + V(s * 0.38, 0, 0.18), 0.06, 0.36, X_AX, YEL, C_QUARRY)
ore_cube(CH1 + V(0, -0.5, 0.15), ORE, C_QUARRY, size=0.8)
# warning signs + cones
for k, (x, y) in enumerate(((-5.2, -4.8), (-4.8, 1.9), (1.0, -5.0))):
    lathe(f"Traffic Cone {k + 1}", V(x, y, top), [(0.35, 0), (0.35, 0.08), (0.28, 0.1), (0.05, 0.8)], BEACON if False else HAZ, C_QUARRY, n=10, smooth=False)
    torus(f"Cone Band {k + 1}", V(x, y, top + 0.42), Z_AX, X_AX, 0.17, 0.035, BLK, C_QUARRY, n_major=10, n_minor=4)
abox("Sign Post", -5.25, -5.15, 4.3, 4.4, top, top + 2.0, STEEL, C_QUARRY)
hexa("Warning Sign", [V(-5.2, 4.25, top + 1.4), V(-5.2, 4.25, top + 1.4), V(-5.2, 4.25, top + 1.4), V(-5.2, 4.25, top + 1.4),
                      V(-5.85, 4.25, top + 1.4), V(-4.55, 4.25, top + 1.4), V(-4.55, 4.2, top + 1.4), V(-5.85, 4.2, top + 1.4)], HAZ, C_QUARRY) if False else None
blade("Warning Sign", [V(-5.9, 4.24, top + 1.35), V(-4.5, 4.24, top + 1.35), V(-5.2, 4.24, top + 2.55)], 0.06, HAZ, C_QUARRY)
abox("Warning Mark", -5.25, -5.15, 4.18, 4.2, top + 1.6, top + 2.15, BLK, C_QUARRY)
dot("Warning Dot", V(-5.2, 4.19, top + 1.48), 0.06, BLK, C_QUARRY)
for k in range(3):                                          # spare drill pipes
    cyl(f"Pipe Rack {k + 1}", V(-5.4, -0.8 + k * 0.4, top + 0.25 + (0.35 if k == 1 else 0)), V(-2.9 - 0.0, -0.8 + k * 0.4, top + 0.25 + (0.35 if k == 1 else 0)), 0.18, 0.18, STEEL, C_QUARRY, n=10, hint=Z_AX)

finish_mine(bg=(0.02, 0.02, 0.025), tint=(1.0, 0.95, 0.88))
