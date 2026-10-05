"""Ore Express Mine - a green and brass steam tank engine on a short length of track beside a little station platform.
Steam billows from the chimney, the firebox glows in the cab and ore tumbles down a chute from the coal bunker.
Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_TRACK, C_LOCO, C_WHEELS, C_STATION = begin("OreExpressMine", ["Base", "Track", "Locomotive", "Wheels", "Station"], seed=15)
SOOT = M("Soot Iron (Metal)", (34, 34, 38), rough=0.5, metal=0.7, rbx="DiamondPlate", plate=10.0)
BRASS = M("Brass (Metal)", (226, 172, 70), rough=0.25, metal=1.0, rbx="Metal")
BALLAST = M("Ballast", (112, 104, 96), rough=0.95, rbx="Pebble", noise=((82, 76, 70), (150, 142, 132), 9.0, 0.5))
STEEL = M("Rail Steel", (150, 150, 158), rough=0.3, metal=0.9, rbx="Metal")
SLEEPER = M("Sleeper Wood (Wood)", (82, 58, 40), rough=0.8, rbx="Wood")
GREEN = M("Engine Green", (22, 92, 54), rough=0.3, metal=0.2)
BLACK = M("Black Paint", (18, 18, 20), rough=0.45)
RED = M("Buffer Red", (184, 34, 28), rough=0.4)
WARM = M("Lamp Glow", (255, 222, 150), rough=0.4, glow=(255, 190, 100), glow_strength=6.0, rbx="Neon", light=(12, 1.4))
FIRE = M("Firebox Fire", (255, 120, 30), rough=0.4, glow=(255, 100, 20), glow_strength=7.0, rbx="Neon", light=(10, 1.6))
STEAM = M("Steam", (236, 238, 242), rough=0.8, rbx="SmoothPlastic", alpha=0.15)
COAL = M("Coal", (36, 34, 36), rough=0.6, metal=0.2, rbx="Slate")
PLANK = M("Platform Planks (Wood)", (150, 112, 74), rough=0.8, rbx="WoodPlanks", noise=((120, 88, 58), (170, 130, 88), 3.0, 0.3))
BRICK = M("Platform Brick", (150, 70, 52), rough=0.9, rbx="Brick", noise=((120, 54, 40), (178, 92, 70), 6.0, 0.4))
CREAM = M("Station Cream", (234, 222, 190), rough=0.6)
ORE = M("Express Ore", (255, 196, 90), rough=0.2, glow=(255, 150, 40), glow_strength=2.4, rbx="Neon")

top = base_plinth(15.0, 10.0, SOOT, BRASS, BALLAST, C_BASE, c=1.0)
Y0 = -0.6                                                    # track centre line
Y_AX, Z_AX, X_AX = V(0, 1, 0), V(0, 0, 1), V(1, 0, 0)

# ---- track: sleepers, rails, buffer stops
for k in range(15):
    x = -6.3 + k * 0.9
    abox(f"Sleeper {k + 1}", x - 0.28, x + 0.28, Y0 - 1.35, Y0 + 1.35, top, top + 0.18, SLEEPER, C_TRACK)
for s in (-1, 1):
    profile_x(f"Rail {s}", [(Y0 + s * 0.85 - 0.14, top + 0.18), (Y0 + s * 0.85 + 0.14, top + 0.18), (Y0 + s * 0.85 + 0.05, top + 0.28),
                             (Y0 + s * 0.85 + 0.05, top + 0.38), (Y0 + s * 0.85 + 0.1, top + 0.46), (Y0 + s * 0.85 - 0.1, top + 0.46),
                             (Y0 + s * 0.85 - 0.05, top + 0.38), (Y0 + s * 0.85 - 0.05, top + 0.28)], -6.6, 6.6, STEEL, C_TRACK)
for sx in (-1, 1):
    x = sx * 6.55
    abox(f"Stop Beam {sx}", x - 0.2, x + 0.2, Y0 - 1.2, Y0 + 1.2, top + 0.9, top + 1.4, RED, C_TRACK)
    for s in (-1, 1):
        beam(f"Stop Strut {sx}{s}", V(x, Y0 + s * 0.85, top + 0.46), V(x, Y0 + s * 0.85, top + 1.2), 0.18, 0.18, X_AX, SOOT, C_TRACK)
        beam(f"Stop Brace {sx}{s}", V(x - sx * 0.8, Y0 + s * 0.85, top + 0.46), V(x, Y0 + s * 0.85, top + 1.15), 0.16, 0.16, Y_AX, SOOT, C_TRACK)
    dot(f"Stop Lamp {sx}", V(x, Y0, top + 1.6), 0.18, RED, C_TRACK)

# ---- wheels
WZ = top + 0.46                                             # rail head height

def wheel(name, x, r, s, spokes, crank=None):
    C = V(x, Y0 + s * 0.85, WZ + r)
    tube(f"{name} Tyre", C, Y_AX, Z_AX, r, r * 0.84, 0.22, BLACK, C_WHEELS, n=28)
    tube(f"{name} Flange", C + V(0, -s * 0.13, 0), Y_AX, Z_AX, r + 0.08, r * 0.9, 0.05, STEEL, C_WHEELS, n=28)
    tube(f"{name} Rim", C + V(0, s * 0.02, 0), Y_AX, Z_AX, r * 0.86, r * 0.76, 0.2, RED, C_WHEELS, n=28)
    cyl(f"{name} Hub", C + V(0, -s * 0.12, 0), C + V(0, s * 0.16, 0), r * 0.2, r * 0.17, RED, C_WHEELS, n=12, hint=Z_AX)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        d = V(math.cos(a), 0, math.sin(a))
        beam(f"{name} Spoke {k + 1}", C + d * r * 0.16, C + d * r * 0.78, 0.1, 0.12, Z_AX if abs(d.z) < 0.9 else X_AX, RED, C_WHEELS)
    if crank is not None:                                   # counterweight + crank pin
        a = crank;d = V(math.cos(a), 0, math.sin(a))
        blade(f"{name} Counterweight", [C - d * r * 0.2 + V(-d.z, 0, d.x) * r * 0.45, C - d * r * 0.72, C - d * r * 0.2 - V(-d.z, 0, d.x) * r * 0.45], 0.16, RED, C_WHEELS)
        P = C + d * r * 0.5 + V(0, s * 0.2, 0)
        cyl(f"{name} Crank Pin", C + d * r * 0.5, P + V(0, s * 0.1, 0), 0.08, 0.08, STEEL, C_WHEELS, n=8, hint=Z_AX)
        return P
    return None

DRIVERS = (-2.0, 0.15, 2.3);RD = 0.95
CRANK = math.radians(-35)
pins = {}
for s in (-1, 1):
    for k, x in enumerate(DRIVERS):
        pins[(s, k)] = wheel(f"Driver {k + 1} {'L' if s < 0 else 'R'}", x, RD, s, 12, crank=CRANK)
    wheel(f"Pony {'L' if s < 0 else 'R'}", 3.95, 0.5, s, 8)
    wheel(f"Trailing {'L' if s < 0 else 'R'}", -4.0, 0.55, s, 8)
    for k, x in enumerate(DRIVERS + (3.95, -4.0)):
        r = RD if k < 3 else (0.5 if k == 3 else 0.55)
        cyl(f"Axle {k + 1} {s}", V(x, Y0 + s * 0.6, WZ + r), V(x, Y0 + s * 0.74, WZ + r), 0.12, 0.12, STEEL, C_WHEELS, n=8, hint=Z_AX)
    # coupling rod + main rod + crosshead + slide bars
    p0, p2 = pins[(s, 0)], pins[(s, 2)]
    beam(f"Coupling Rod {s}", p0 + V(-0.15, s * 0.04, 0), p2 + V(0.15, s * 0.04, 0), 0.08, 0.16, Z_AX, STEEL, C_WHEELS)
    XH = V(3.0, Y0 + s * 1.15, WZ + 1.0)
    beam(f"Main Rod {s}", pins[(s, 1)] + V(0, s * 0.14, 0), XH, 0.08, 0.18, Z_AX, STEEL, C_WHEELS)
    obox(f"Crosshead {s}", XH, (0.4, 0.2, 0.3), X_AX, Y_AX, Z_AX, BRASS, C_WHEELS)
    for dz in (-0.2, 0.2):
        beam(f"Slide Bar {s}{dz}", XH + V(-0.6, 0, dz), XH + V(1.0, 0, dz), 0.1, 0.06, Z_AX, STEEL, C_WHEELS)

# ---- running plate, valance and frames
abox("Frame", -5.0, 4.9, Y0 - 0.55, Y0 + 0.55, WZ + 0.6, WZ + 1.6, BLACK, C_LOCO)
for s in (-1, 1):
    abox(f"Running Plate {s}", -5.0, 4.9, Y0 + s * 0.55 - (0.95 if s < 0 else 0), Y0 + s * 0.55 + (0.95 if s > 0 else 0), WZ + 2.0, WZ + 2.1, BLACK, C_LOCO)
    abox(f"Valance {s}", -5.0, 4.9, Y0 + s * 1.5 - 0.05, Y0 + s * 1.5 + 0.05, WZ + 1.75, WZ + 2.05, RED, C_LOCO)
    for k, x in enumerate(DRIVERS):                         # splashers
        tube(f"Splasher {s}{k}", V(x, Y0 + s * 1.1, WZ + RD), Y_AX, Z_AX, RD + 0.14, RD + 0.04, 0.5, GREEN, C_LOCO, n=28)
abox("Buffer Beam Front", 4.9, 5.1, Y0 - 1.55, Y0 + 1.55, WZ + 1.0, WZ + 1.9, RED, C_LOCO)
abox("Buffer Beam Rear", -6.45, -6.25, Y0 - 1.55, Y0 + 1.55, WZ + 1.0, WZ + 1.9, RED, C_LOCO)
for x, d in ((5.1, 1), (-6.45, -1)):
    for s in (-1, 1):
        cyl(f"Buffer Stock {x}{s}", V(x, Y0 + s * 1.05, WZ + 1.45), V(x + d * 0.35, Y0 + s * 1.05, WZ + 1.45), 0.13, 0.13, BLACK, C_LOCO, n=10)
        cyl(f"Buffer Head {x}{s}", V(x + d * 0.35, Y0 + s * 1.05, WZ + 1.45), V(x + d * 0.42, Y0 + s * 1.05, WZ + 1.45), 0.26, 0.26, STEEL, C_LOCO, n=14)
    torus(f"Coupling Hook {x}", V(x + d * 0.3, Y0, WZ + 1.3), Y_AX, Z_AX, 0.14, 0.04, STEEL, C_LOCO, n_major=10, n_minor=4)
# cowcatcher (pilot)
for k in range(7):
    y = Y0 - 1.2 + k * 0.4
    beam(f"Pilot Slat {k + 1}", V(5.1, y, WZ + 1.0), V(5.75 - abs(y - Y0) * 0.35, y * 0.7 + Y0 * 0.3, WZ + 0.08), 0.1, 0.12, Y_AX, RED, C_LOCO)

# ---- cylinders
for s in (-1, 1):
    CY = V(3.9, Y0 + s * 1.2, WZ + 1.15)
    cyl(f"Cylinder {s}", CY + V(-0.75, 0, 0), CY + V(0.75, 0, 0), 0.45, 0.45, GREEN, C_LOCO, n=20, hint=Z_AX)
    for dx in (-0.78, 0.78):
        cyl(f"Cylinder Cap {s}{dx}", CY + V(dx, 0, 0), CY + V(dx * 1.06, 0, 0), 0.5, 0.42, BRASS, C_LOCO, n=20, hint=Z_AX)
    obox(f"Steam Chest {s}", CY + V(0, s * 0.05, 0.6), (1.2, 0.5, 0.35), X_AX, Y_AX, Z_AX, GREEN, C_LOCO)

# ---- boiler, smokebox, chimney, domes
BZ = WZ + 3.05;BR = 1.0
cyl("Boiler", V(-2.6, Y0, BZ), V(3.7, Y0, BZ), BR, BR, GREEN, C_LOCO, n=32, hint=Y_AX)
for k, x in enumerate((-2.0, -0.4, 1.2, 2.8)):
    cyl(f"Boiler Band {k + 1}", V(x - 0.07, Y0, BZ), V(x + 0.07, Y0, BZ), BR + 0.04, BR + 0.04, BRASS, C_LOCO, n=32, hint=Y_AX)
abox("Firebox", -2.9, -1.4, Y0 - 0.95, Y0 + 0.95, WZ + 1.6, BZ + 0.5, GREEN, C_LOCO)
cyl("Smokebox", V(3.7, Y0, BZ), V(4.85, Y0, BZ), BR + 0.08, BR + 0.08, BLACK, C_LOCO, n=32, hint=Y_AX)
abox("Smokebox Saddle", 3.7, 4.85, Y0 - 0.7, Y0 + 0.7, WZ + 1.5, BZ - 0.4, BLACK, C_LOCO)
cyl("Smokebox Door", V(4.85, Y0, BZ), V(5.05, Y0, BZ), BR - 0.02, BR - 0.25, BLACK, C_LOCO, n=32, hint=Y_AX)
for dz in (0.35, -0.35):
    beam(f"Door Hinge {dz}", V(5.0, Y0 - 0.85, BZ + dz), V(5.0, Y0 + 0.4, BZ + dz), 0.08, 0.1, Z_AX, BRASS, C_LOCO)
cyl("Door Dart", V(5.05, Y0, BZ), V(5.25, Y0, BZ), 0.09, 0.07, BRASS, C_LOCO, n=8, hint=Z_AX)
abox("Number Plate", 4.98, 5.04, Y0 - 0.35, Y0 + 0.35, BZ - 0.75, BZ - 0.5, BRASS, C_LOCO)
lathe("Chimney", V(4.25, Y0, BZ + 0.8), [(0.42, 0), (0.36, 0.3), (0.34, 1.3), (0.48, 1.65), (0.5, 1.8), (0.36, 1.8)], BLACK, C_LOCO, n=20)
torus("Chimney Cap Ring", V(4.25, Y0, BZ + 2.6), Z_AX, Y_AX, 0.47, 0.06, BRASS, C_LOCO, n_major=20, n_minor=5)
lathe("Steam Dome", V(1.6, Y0, BZ + 0.8), [(0.55, 0), (0.5, 0.3), (0.48, 0.55), (0.36, 0.8), (0.15, 0.9), (0.01, 0.92)], BRASS, C_LOCO, n=20)
lathe("Sand Dome", V(-0.2, Y0, BZ + 0.85), [(0.45, 0), (0.4, 0.3), (0.28, 0.5), (0.01, 0.6)], GREEN, C_LOCO, n=16)
cyl("Safety Valve", V(-1.0, Y0, BZ + 0.9), V(-1.0, Y0, BZ + 1.4), 0.12, 0.1, BRASS, C_LOCO, n=10)
lathe("Whistle", V(-2.3, Y0, BZ + 0.85), [(0.06, 0), (0.06, 0.4), (0.13, 0.42), (0.13, 0.75), (0.09, 0.85), (0.01, 0.86)], BRASS, C_LOCO, n=10)
for s in (-1, 1):                                           # handrails
    hr = [V(x, Y0 + s * (BR + 0.18), BZ + 0.35) for x in (-2.4, 0.5, 3.6)]
    path_tube(f"Handrail {s}", hr, [0.04] * 3, BRASS, C_LOCO, n=6)
    for x in (-2.0, 0.5, 3.2):
        cyl(f"Handrail Stanchion {s}{x}", V(x, Y0 + s * BR * 0.92, BZ + 0.3), V(x, Y0 + s * (BR + 0.18), BZ + 0.35), 0.03, 0.03, BRASS, C_LOCO, n=6)
# headlamps on the buffer beam
for y in (-0.9, 0.9):
    abox(f"Lamp Body {y}", 4.85, 5.25, Y0 + y - 0.22, Y0 + y + 0.22, WZ + 1.95, WZ + 2.45, BLACK, C_LOCO)
    cyl(f"Lamp Lens {y}", V(5.25, Y0 + y, WZ + 2.2), V(5.3, Y0 + y, WZ + 2.2), 0.16, 0.16, WARM, C_LOCO, n=14, hint=Z_AX)

# ---- cab with glowing firebox door
CX0, CX1 = -5.0, -2.6
abox("Cab Front", CX1 - 0.15, CX1, Y0 - 1.45, Y0 + 1.45, WZ + 2.1, WZ + 5.0, GREEN, C_LOCO)
abox("Cab Back", CX0, CX0 + 0.15, Y0 - 1.45, Y0 + 1.45, WZ + 2.1, WZ + 5.0, GREEN, C_LOCO)
for s in (-1, 1):
    yo = Y0 + s * 1.45
    abox(f"Cab Side Low {s}", CX0, CX1, yo - 0.08, yo + 0.08, WZ + 2.1, WZ + 3.6, GREEN, C_LOCO)
    abox(f"Cab Side Post F {s}", CX1 - 0.4, CX1, yo - 0.08, yo + 0.08, WZ + 3.6, WZ + 5.0, GREEN, C_LOCO)
    abox(f"Cab Side Post B {s}", CX0, CX0 + 0.4, yo - 0.08, yo + 0.08, WZ + 3.6, WZ + 5.0, GREEN, C_LOCO)
    abox(f"Cab Lining {s}", CX0 + 0.15, CX1 - 0.15, yo - 0.1, yo + 0.1, WZ + 3.3, WZ + 3.4, BRASS, C_LOCO)
    for dy in (-0.75, 0.75):
        cyl(f"Spectacle {s}{dy}", V(CX1 - 0.18, Y0 + dy, WZ + 4.2), V(CX1 + 0.02, Y0 + dy, WZ + 4.2), 0.3, 0.3, WARM, C_LOCO, n=14, hint=Z_AX)
rows = []
for k in range(13):
    y = -1.8 + 0.3 * k
    z = WZ + 5.0 + 0.35 * (1 - (y / 1.8) ** 2)
    rows.append([V(CX0 - 0.3, Y0 + y, z), V(CX1 + 0.3, Y0 + y, z), V(CX1 + 0.3, Y0 + y, z + 0.12), V(CX0 - 0.3, Y0 + y, z + 0.12)])
finish("Cab Roof", loft(rows, smooth_sides=False), BLACK, C_LOCO, merge=0)
abox("Cab Floor", CX0, CX1, Y0 - 1.4, Y0 + 1.4, WZ + 2.0, WZ + 2.15, PLANK, C_LOCO)
abox("Backhead", CX1 - 0.3, CX1 - 0.15, Y0 - 0.9, Y0 + 0.9, WZ + 2.15, WZ + 4.0, SOOT, C_LOCO)
abox("Firehole Glow", CX1 - 0.34, CX1 - 0.29, Y0 - 0.35, Y0 + 0.35, WZ + 2.6, WZ + 3.1, FIRE, C_LOCO)
for k, (dy, dz) in enumerate(((-0.45, 3.6), (0.45, 3.6), (0, 3.85))):
    cyl(f"Gauge {k + 1}", V(CX1 - 0.32, Y0 + dy, WZ + dz), V(CX1 - 0.4, Y0 + dy, WZ + dz), 0.14, 0.14, BRASS, C_LOCO, n=12, hint=Z_AX)

# ---- coal bunker + ore chute
abox("Bunker", -6.25, CX0, Y0 - 1.45, Y0 + 1.45, WZ + 2.0, WZ + 4.2, GREEN, C_LOCO)
abox("Bunker Lip", -6.3, CX0, Y0 - 1.5, Y0 + 1.5, WZ + 4.2, WZ + 4.35, BRASS, C_LOCO)
rnd = random.Random(15)
for k in range(9):
    rock_f(f"Coal {k + 1}", V(rnd.uniform(-6.0, -5.25), Y0 + rnd.uniform(-1.1, 1.1), WZ + 4.3 + rnd.uniform(0, 0.25)), (0.4, 0.4, 0.3), COAL, C_LOCO, rough=0.3, subd=1)
for k in range(5):
    rock_f(f"Ore Lump {k + 1}", V(rnd.uniform(-6.0, -5.25), Y0 + rnd.uniform(-1.0, 1.0), WZ + 4.5 + rnd.uniform(0, 0.2)), (0.26, 0.26, 0.22), ORE, C_LOCO, rough=0.3, subd=1)
CH0 = V(-5.6, Y0 - 1.5, WZ + 3.6);CH1 = V(-5.6, -4.85, top + 1.3)
d = (CH1 - CH0)
for k, off in enumerate((-0.45, 0.45)):
    beam(f"Chute Side {k + 1}", CH0 + V(off, 0, 0.2), CH1 + V(off, 0, 0.2), 0.08, 0.45, X_AX, BRASS, C_LOCO)
beam("Chute Floor", CH0, CH1, 0.9, 0.08, X_AX, SOOT, C_LOCO)
beam("Chute Prop", CH1 + V(0, 0.4, -0.05), V(-5.6, -4.45, top), 0.14, 0.14, X_AX, SOOT, C_LOCO)
ore_cube(CH1 + V(0, -0.45, 0.25), ORE, C_LOCO, size=0.85)

# ---- steam: chimney plume + cylinder wisps
for k, (dx, dz, r) in enumerate(((0.0, 3.0, 0.55), (-0.5, 3.6, 0.75), (-1.3, 4.1, 0.9), (-2.3, 4.4, 0.8), (-3.1, 4.55, 0.6))):
    rock_f(f"Steam Puff {k + 1}", V(4.25 + dx, Y0 + rnd.uniform(-0.2, 0.2), BZ + dz), (r * 1.3, r, r * 0.9), STEAM, C_LOCO, rough=0.18, subd=2)
for s in (-1, 1):
    rock_f(f"Cylinder Wisp {s}", V(4.9, Y0 + s * 1.45, WZ + 0.5), (0.45, 0.35, 0.3), STEAM, C_LOCO, rough=0.2, subd=1)

# ---- station platform at the back
PY0, PY1 = Y0 + 1.75, 4.3
slab("Platform", [(4.5, PY0), (4.5, PY1), (-4.5, PY1), (-4.5, PY0)], top, [(4.5, PY0), (4.5, PY1), (-4.5, PY1), (-4.5, PY0)], top + 1.2, BRICK, C_STATION)
abox("Platform Deck", -4.6, 4.6, PY0 - 0.12, PY1, top + 1.2, top + 1.35, PLANK, C_STATION)
abox("Platform Edge", -4.6, 4.6, PY0 - 0.14, PY0 + 0.15, top + 1.35, top + 1.4, CREAM, C_STATION)
for k in range(3):
    abox(f"Platform Step {k + 1}", 4.5, 5.2 - 0.0, PY0 + 0.2, PY1 - 0.2, top, top + 0.4 * (k + 1), BRICK, C_STATION) if False else \
        abox(f"Platform Step {k + 1}", 4.5 + 0.35 * k, 4.85 + 0.35 * k, PY0 + 0.3, PY1 - 0.3, top, top + 1.2 - 0.4 * (k + 1) + 0.4, BRICK, C_STATION)
PT = top + 1.35
# canopy on cast-iron posts
for x in (-3.2, 0.0, 3.2):
    cyl(f"Canopy Post {x}", V(x, PY1 - 0.5, PT), V(x, PY1 - 0.5, PT + 3.6), 0.1, 0.1, GREEN, C_STATION, n=8)
    beam(f"Canopy Bracket {x}", V(x, PY1 - 0.5, PT + 2.9), V(x, PY0 + 0.4, PT + 3.55), 0.08, 0.12, X_AX, GREEN, C_STATION)
hexa("Canopy Roof", [V(-4.0, PY0 + 0.1, PT + 3.55), V(4.0, PY0 + 0.1, PT + 3.55), V(4.0, PY1 - 0.1, PT + 3.95), V(-4.0, PY1 - 0.1, PT + 3.95),
                     V(-4.0, PY0 + 0.1, PT + 3.7), V(4.0, PY0 + 0.1, PT + 3.7), V(4.0, PY1 - 0.1, PT + 4.1), V(-4.0, PY1 - 0.1, PT + 4.1)], CREAM, C_STATION)
for k in range(16):                                         # valance boards
    x = -3.9 + k * 0.52
    hexa(f"Canopy Valance {k + 1}", [V(x - 0.24, PY0 + 0.08, PT + 3.2), V(x + 0.24, PY0 + 0.08, PT + 3.2), V(x + 0.24, PY0 + 0.12, PT + 3.2), V(x - 0.24, PY0 + 0.12, PT + 3.2),
                                     V(x - 0.24, PY0 + 0.08, PT + 3.6), V(x + 0.24, PY0 + 0.08, PT + 3.6), V(x + 0.24, PY0 + 0.12, PT + 3.6), V(x - 0.24, PY0 + 0.12, PT + 3.6)], GREEN, C_STATION)
    cone(f"Valance Point {k + 1}", V(x, PY0 + 0.1, PT + 3.2), V(x, PY0 + 0.1, PT + 2.95), 0.18, GREEN, C_STATION, n=4)
# hanging clock + sign + lamps + bench + luggage
cyl("Clock Rod", V(0, PY0 + 1.0, PT + 3.55), V(0, PY0 + 1.0, PT + 3.0), 0.04, 0.04, STEEL, C_STATION, n=6)
cyl("Station Clock", V(0, PY0 + 0.88, PT + 2.6), V(0, PY0 + 1.12, PT + 2.6), 0.42, 0.42, BLACK, C_STATION, n=20, hint=Z_AX)
for s in (-1, 1):
    cyl(f"Clock Face {s}", V(0, PY0 + 1.0 + s * 0.12, PT + 2.6), V(0, PY0 + 1.0 + s * 0.14, PT + 2.6), 0.34, 0.34, CREAM, C_STATION, n=20, hint=Z_AX)
    beam(f"Clock Hand H {s}", V(0, PY0 + 1.0 + s * 0.15, PT + 2.6), V(0.15, PY0 + 1.0 + s * 0.15, PT + 2.78), 0.03, 0.04, Y_AX, BLACK, C_STATION)
    beam(f"Clock Hand M {s}", V(0, PY0 + 1.0 + s * 0.15, PT + 2.6), V(-0.05, PY0 + 1.0 + s * 0.15, PT + 2.88), 0.03, 0.03, Y_AX, BLACK, C_STATION)
abox("Name Board", -2.3, -0.8, PY1 - 0.25, PY1 - 0.15, PT + 1.6, PT + 2.2, CREAM, C_STATION)
abox("Name Board Frame", -2.4, -0.7, PY1 - 0.2, PY1 - 0.1, PT + 1.5, PT + 2.3, GREEN, C_STATION)
abox("Name Board Stripe", -2.2, -0.9, PY1 - 0.28, PY1 - 0.24, PT + 1.85, PT + 1.95, RED, C_STATION)
for x in (-3.7, 3.7):
    post_lantern(f"Platform Lamp {x}", V(x, PY0 + 0.6, PT), 2.0, GREEN, WARM, BLACK, C_STATION, r=0.28)
abox("Bench Seat", 0.8, 2.6, PY1 - 0.9, PY1 - 0.45, PT + 0.6, PT + 0.7, PLANK, C_STATION)
abox("Bench Back", 0.8, 2.6, PY1 - 0.5, PY1 - 0.4, PT + 0.7, PT + 1.3, PLANK, C_STATION)
for x in (0.95, 2.45):
    abox(f"Bench Leg {x}", x - 0.06, x + 0.06, PY1 - 0.9, PY1 - 0.45, PT, PT + 0.6, SOOT, C_STATION)
for k, (x, y, sz, mat) in enumerate(((-1.8, PY0 + 1.0, (0.9, 0.6, 0.6), PLANK), (-1.7, PY0 + 1.0, (0.7, 0.5, 0.45), RED), (3.0, PY0 + 0.9, (0.6, 0.6, 0.5), SLEEPER))):
    z = PT + (0.3 if k != 1 else 0.82)
    obox(f"Luggage {k + 1}", V(x, y, z), sz, X_AX, Y_AX, Z_AX, mat, C_STATION)
    abox(f"Luggage Strap {k + 1}", x - 0.05, x + 0.05, y - sz[1] / 2 - 0.02, y + sz[1] / 2 + 0.02, z - sz[2] / 2, z + sz[2] / 2 + 0.02, BRASS, C_STATION)

# ---- semaphore signal at the back-right
SG = V(6.35, 3.3, top)
cyl("Signal Post", SG, SG + V(0, 0, 5.5), 0.13, 0.1, CREAM, C_STATION, n=8)
dot("Signal Finial", SG + V(0, 0, 5.6), 0.16, RED, C_STATION)
hexa("Signal Arm", [SG + V(-0.12, -0.05, 4.7), SG + V(-0.12, -0.05, 4.7), SG + V(-0.12, 0.05, 4.7), SG + V(-0.12, 0.05, 4.7),
                    SG + V(-1.6, -0.05, 5.15), SG + V(-0.12, -0.05, 5.0), SG + V(-0.12, 0.05, 5.0), SG + V(-1.6, 0.05, 5.15)], RED, C_STATION)
abox("Signal Arm Stripe", SG.x - 1.3, SG.x - 1.1, SG.y - 0.07, SG.y - 0.05, top + 4.8, top + 5.08, CREAM, C_STATION)
cyl("Signal Lamp", SG + V(0.14, 0, 4.85), SG + V(0.24, 0, 4.85), 0.14, 0.14, WARM, C_STATION, n=10, hint=Z_AX)
for k in range(5):
    cyl(f"Signal Ladder Rung {k + 1}", SG + V(-0.25, 0.15, 0.8 + k * 0.8), SG + V(0.25, 0.15, 0.8 + k * 0.8), 0.03, 0.03, SOOT, C_STATION, n=6, hint=Z_AX)

finish_mine(bg=(0.02, 0.02, 0.03), tint=(1.0, 0.92, 0.8))
