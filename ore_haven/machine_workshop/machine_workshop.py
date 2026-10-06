"""MACHINE WORKSHOP - Ore Haven. A chunky stylised low-poly industrial building for the hilltop, with an indoor
machine showcase, Machine Archive console, fusion station, star/evolution station and three rear collection alcoves.

    python3 machine_workshop.py -- --out . [--render] [--samples 48]

Writes:
  MachineWorkshop.blend
  MachineWorkshop_Building_Roblox.fbx    building + all interior props (place on top of the foundation)
  MachineWorkshop_Foundation_Roblox.fbx  stone foundation + entrance landing, steps and ramp (place on the hill)
  MachineWorkshop_RobloxSetup.lua         optional: colours/materials/transparency/lights for every part
Units: 1 Blender unit = 1 stud. Built at 50% of the 72 x 56 brief (36 x 28 studs, ~11 studs inside height; --scale 1 for full size).
Front faces -Y (down the hill). Floor level is Z = 1 (top of the foundation).
Key gameplay parts are exported as separate, named MeshParts (see SEPARATE below); everything else is merged
per material to keep the part count low.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "mines20"))
from mine_kit import *

C_FOUND, C_SHELL, C_ROOF, C_SHOW, C_ARCH, C_FUSE, C_EVO, C_REAR, C_PROPS = begin(
    "MachineWorkshop", ["Foundation", "Shell", "Roof", "Showcase", "Archive", "Fusion", "Evolution", "Rear Displays", "Props"], seed=7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)

# ------------------------------------------------------------------ palette
CONC = M("Warm Concrete", (196, 190, 180), rough=0.85, rbx="Concrete", noise=((178, 172, 162), (212, 206, 196), 3.0, 0.15))
STONE = M("Foundation Stone", (168, 160, 148), rough=0.9, rbx="Slate", noise=((140, 132, 120), (190, 182, 170), 2.5, 0.35))
FLOOR = M("Concrete Floor", (182, 178, 170), rough=0.8, rbx="Concrete", noise=((166, 162, 154), (196, 192, 184), 6.0, 0.1))
STEEL = M("Charcoal Steel (Metal)", (52, 54, 60), rough=0.45, metal=0.75, rbx="Metal")
STEEL2 = M("Light Steel (DiamondPlate)", (120, 124, 132), rough=0.4, metal=0.8, rbx="DiamondPlate", plate=8.0)
BLUE = M("Blue Wall Panel", (84, 112, 146), rough=0.6, rbx="SmoothPlastic")
BLUE2 = M("Dark Blue Panel", (62, 84, 114), rough=0.6, rbx="SmoothPlastic")
COPPER = M("Copper (Metal)", (196, 116, 62), rough=0.35, metal=0.9, rbx="Metal")
ORANGE = M("Industrial Orange", (232, 124, 40), rough=0.5)
GLASS = M("Window Glass", (190, 220, 240), rough=0.05, rbx="Glass", alpha=0.6)
HAZ = M("Hazard Yellow", (236, 190, 40), rough=0.5)
HAZB = M("Hazard Black", (30, 30, 34), rough=0.5)
CYAN = M("Archive Cyan", (60, 220, 240), rough=0.3, glow=(30, 210, 240), glow_strength=3.0, rbx="Neon", light=(10, 1.0))
FUSE = M("Fusion Orange", (255, 140, 40), rough=0.3, glow=(255, 110, 20), glow_strength=3.5, rbx="Neon", light=(12, 1.4))
PURP = M("Evolution Purple", (170, 90, 240), rough=0.3, glow=(150, 70, 240), glow_strength=3.0, rbx="Neon", light=(10, 1.0))
GOLD = M("Gold Detail (Metal)", (236, 186, 70), rough=0.25, metal=1.0, rbx="Metal")
SCREEN = M("Blank Screen", (24, 30, 40), rough=0.2, rbx="SmoothPlastic")
PLAQUE = M("Blank Plaque", (210, 206, 196), rough=0.5, rbx="SmoothPlastic")
PROJ = M("Projection Surface", (40, 60, 76), rough=0.15, metal=0.3, rbx="SmoothPlastic")
LAMP = M("Soft Lamp", (255, 244, 214), rough=0.4, glow=(255, 236, 200), glow_strength=3.0, rbx="Neon", light=(24, 1.2))
HOLO = M("Display Placeholder", (90, 220, 255), rough=0.1, rbx="ForceField", alpha=1.0)
WOOD = M("Crate Wood (Wood)", (150, 110, 70), rough=0.8, rbx="WoodPlanks")

SEPARATE = set()                                    # objects exported individually under their own names
def sep(ob):
    SEPARATE.add(ob.name)
    return ob

def bevbox(name, x0, x1, y0, y1, z0, z1, mat, coll, b=0.25):
    """Chunky box with bevelled edges."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = V((x0 + x1) / 2 + v.co.x * (x1 - x0), (y0 + y1) / 2 + v.co.y * (y1 - y0), (z0 + z1) / 2 + v.co.z * (z1 - z0))
    bb = min(b, (x1 - x0) * 0.45, (y1 - y0) * 0.45, (z1 - z0) * 0.45)
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bb, segments=1, affect='EDGES')
    return finish(name, bm, mat, coll, merge=0)

def hazard_strip(name, x0, x1, y0, y1, z, coll, along_x=True, w=0.8):
    """Short run of yellow/black hazard stripes on the floor."""
    L = (x1 - x0) if along_x else (y1 - y0)
    n = max(2, int(L / 1.0))
    for k in range(n):
        a = (x0 if along_x else y0) + k * L / n
        b = a + L / n
        mat = HAZ if k % 2 == 0 else HAZB
        if along_x:
            abox(f"{name} {k}", a, b, y0, y1, z, z + 0.04, mat, coll)
        else:
            abox(f"{name} {k}", x0, x1, a, b, z, z + 0.04, mat, coll)

FZ = 2.0                                             # floor level
W, D = 36.0, 28.0                                    # half footprint (72 x 56)
T = 2.0                                              # wall thickness
CEIL = FZ + 22.0                                     # 22 studs clear height

# ------------------------------------------------------------------ FOUNDATION + LANDING (separate FBX)
slab("Foundation Slab", chamfer_rect(78.0, 62.0, 2.0), -2.0, chamfer_rect(78.0, 62.0, 2.0), FZ - 0.5, STONE, C_FOUND)
slab("Foundation Cap", chamfer_rect(77.0, 61.0, 1.8), FZ - 0.5, chamfer_rect(76.2, 60.2, 1.6), FZ - 0.12, CONC, C_FOUND)
for k in range(10):                                   # stone course lines
    x = -36 + k * 8.0
    abox(f"Foundation Block Line {k}", x - 0.15, x + 0.15, -31.05, -30.9, -1.5, FZ - 0.6, STEEL, C_FOUND)
LAND_Y0, LAND_Y1 = -40.0, -31.0                       # landing in front of the entrance
bevbox("Entrance Landing", -14.0, 14.0, LAND_Y0, LAND_Y1 + 0.5, -2.0, FZ, STONE, C_FOUND, b=0.4)
abox("Landing Top", -13.6, 13.6, LAND_Y0 + 0.4, LAND_Y1, FZ - 0.05, FZ + 0.02, CONC, C_FOUND)
for k in range(4):                                    # short steps down the hill from the landing
    z = FZ - 0.5 * (k + 1)
    bevbox(f"Front Step {k}", -9.0, 9.0, LAND_Y0 - 1.4 * (k + 1), LAND_Y0 - 1.4 * k, -2.0, z, STONE, C_FOUND, b=0.15)
# practical ramp route along the left side of the landing
hexa("Access Ramp", [V(-24.0, LAND_Y0 - 5.6, -2.0), V(-14.0, LAND_Y0 - 5.6, -2.0), V(-14.0, LAND_Y0 + 3.0, -2.0), V(-24.0, LAND_Y0 + 3.0, -2.0),
                     V(-24.0, LAND_Y0 - 5.6, -0.0), V(-14.0, LAND_Y0 - 5.6, -0.0), V(-14.0, LAND_Y0 + 3.0, FZ), V(-24.0, LAND_Y0 + 3.0, FZ)], STONE, C_FOUND)
hexa("Ramp Surface", [V(-23.6, LAND_Y0 - 5.6, -0.0), V(-14.4, LAND_Y0 - 5.6, -0.0), V(-14.4, LAND_Y0 + 3.0, FZ), V(-23.6, LAND_Y0 + 3.0, FZ),
                      V(-23.6, LAND_Y0 - 5.6, 0.04), V(-14.4, LAND_Y0 - 5.6, 0.04), V(-14.4, LAND_Y0 + 3.0, FZ + 0.04), V(-23.6, LAND_Y0 + 3.0, FZ + 0.04)], CONC, C_FOUND)
for s in (-1, 1):                                     # chunky landing bollards with low lights
    for x in (s * 12.6,):
        bevbox(f"Landing Bollard {s}", x - 0.7, x + 0.7, LAND_Y0 + 0.3, LAND_Y0 + 1.7, FZ, FZ + 2.4, STEEL, C_FOUND, b=0.2)
        abox(f"Bollard Light {s}", x - 0.5, x + 0.5, LAND_Y0 + 0.25, LAND_Y0 + 0.3, FZ + 1.6, FZ + 2.0, LAMP, C_FOUND)
hexa("Ramp Rail", [V(-24.0, LAND_Y0 - 5.6, 0.0), V(-23.6, LAND_Y0 - 5.6, 0.0), V(-23.6, LAND_Y0 + 3.0, FZ), V(-24.0, LAND_Y0 + 3.0, FZ),
                   V(-24.0, LAND_Y0 - 5.6, 1.2), V(-23.6, LAND_Y0 - 5.6, 1.2), V(-23.6, LAND_Y0 + 3.0, FZ + 1.2), V(-24.0, LAND_Y0 + 3.0, FZ + 1.2)], STEEL, C_FOUND)

# ------------------------------------------------------------------ SHELL
abox("Interior Floor", -W + T, W - T, -D + T, D - T, FZ - 0.1, FZ, FLOOR, C_SHELL)
# front wall with entrance (14 x 15) and two large windows
EW, EH = 7.0, FZ + 15.0
WX0, WX1, WZ0, WZ1 = 12.0, 26.0, FZ + 4.0, FZ + 16.0
fy0, fy1 = -D, -D + T
abox("Front Wall Low L", -W, -EW, fy0, fy1, FZ, WZ0, CONC, C_SHELL)
abox("Front Wall Low R", EW, W, fy0, fy1, FZ, WZ0, CONC, C_SHELL)
for s in (-1, 1):
    abox(f"Front Wall Pier Out {s}", min(s * WX1, s * W), max(s * WX1, s * W), fy0, fy1, WZ0, CEIL, BLUE, C_SHELL)
    abox(f"Front Wall Pier In {s}", min(s * EW, s * WX0), max(s * EW, s * WX0), fy0, fy1, WZ0, CEIL, BLUE, C_SHELL)
    abox(f"Front Wall Over Window {s}", min(s * WX0, s * WX1), max(s * WX0, s * WX1), fy0, fy1, WZ1, CEIL, BLUE, C_SHELL)
abox("Front Wall Over Door", -EW, EW, fy0, fy1, EH, CEIL, BLUE, C_SHELL)
# windows: charcoal frames, glass, mullions
for s in (-1, 1):
    a, b = min(s * WX0, s * WX1), max(s * WX0, s * WX1)
    abox(f"Window Glass {s}", a, b, fy0 + 0.9, fy0 + 1.1, WZ0, WZ1, GLASS, C_SHELL)
    for (x0, x1, z0, z1) in ((a - 0.6, a + 0.4, WZ0 - 0.6, WZ1 + 0.6), (b - 0.4, b + 0.6, WZ0 - 0.6, WZ1 + 0.6),
                             (a - 0.6, b + 0.6, WZ1, WZ1 + 0.8), (a - 0.6, b + 0.6, WZ0 - 0.8, WZ0)):
        bevbox(f"Window Frame {s} {x0:.0f}{z0:.0f}", x0, x1, fy0 - 0.5, fy1 + 0.2, z0, z1, STEEL, C_SHELL, b=0.15)
    for k in range(1, 3):
        x = a + k * (b - a) / 3
        bevbox(f"Window Mullion {s}{k}", x - 0.3, x + 0.3, fy0 - 0.3, fy0 + 1.0, WZ0, WZ1, STEEL, C_SHELL, b=0.08)
    bevbox(f"Window Transom {s}", a, b, fy0 - 0.3, fy0 + 1.0, WZ0 + 7.8, WZ0 + 8.4, STEEL, C_SHELL, b=0.08)
    bevbox(f"Window Sill {s}", a - 0.8, b + 0.8, fy0 - 1.2, fy0 + 0.2, WZ0 - 1.2, WZ0 - 0.6, CONC, C_SHELL, b=0.15)
# recessed doorway: thick charcoal portal frame projecting forward
bevbox("Entrance Frame L", -EW - 2.2, -EW, fy0 - 2.2, fy1 + 0.3, FZ, EH + 0.2, STEEL, C_SHELL, b=0.35)
bevbox("Entrance Frame R", EW, EW + 2.2, fy0 - 2.2, fy1 + 0.3, FZ, EH + 0.2, STEEL, C_SHELL, b=0.35)
bevbox("Entrance Lintel", -EW - 2.2, EW + 2.2, fy0 - 2.2, fy1 + 0.3, EH, EH + 2.2, STEEL, C_SHELL, b=0.35)
abox("Entrance Threshold", -EW, EW, fy0 - 2.2, fy1, FZ - 0.05, FZ + 0.05, STEEL2, C_SHELL)
for s in (-1, 1):
    abox(f"Door Frame Copper Trim {s}", s * (EW + 1.1) - 0.15, s * (EW + 1.1) + 0.15, fy0 - 2.25, fy0 - 2.15, FZ + 1.0, EH - 1.0, COPPER, C_SHELL)
# sign panel above the entrance (clean surface for Roblox text)
bevbox("Sign Frame", -12.0, 12.0, fy0 - 1.4, fy0 + 0.2, EH + 2.4, EH + 6.6, STEEL, C_SHELL, b=0.3)
sep(abox("Sign Surface", -11.2, 11.2, fy0 - 1.5, fy0 - 1.38, EH + 2.9, EH + 6.1, BLUE2, C_SHELL))
for s in (-1, 1):
    dot(f"Sign Bolt {s}a", V(s * 11.6, fy0 - 1.45, EH + 3.0), 0.18, COPPER, C_SHELL)
    dot(f"Sign Bolt {s}b", V(s * 11.6, fy0 - 1.45, EH + 6.0), 0.18, COPPER, C_SHELL)
# side walls (concrete base band, blue panels, charcoal pilasters)
for s in (-1, 1):
    x0, x1 = sorted((s * W, s * (W - T)))
    abox(f"Side Wall Base {s}", x0, x1, -D, D, FZ, FZ + 6.0, CONC, C_SHELL)
    abox(f"Side Wall Panels {s}", x0, x1, -D, D, FZ + 6.0, CEIL, BLUE, C_SHELL)
    for k in range(5):
        y = -D + 4 + k * 12.0
        bevbox(f"Side Pilaster {s}{k}", min(s * (W + 0.8), s * (W - 0.2)), max(s * (W + 0.8), s * (W - 0.2)), y - 1.0, y + 1.0, FZ, CEIL + 0.6, STEEL, C_SHELL, b=0.2)
    for k in range(4):                                # panel seams
        y = -D + 10 + k * 12.0
        abox(f"Side Panel Seam {s}{k}", min(s * (W + 0.05), s * W), max(s * (W + 0.05), s * W), y - 0.12, y + 0.12, FZ + 6.0, CEIL, BLUE2, C_SHELL)
# rear wall with three alcove openings
ry0, ry1 = D - T, D
AL = (-18.0, 0.0, 18.0); AW, AH = 4.5, FZ + 11.0
xs = [-W] + [v for x in AL for v in (x - AW, x + AW)] + [W]
for k in range(0, len(xs), 2):
    abox(f"Rear Wall Section {k}", xs[k], xs[k + 1], ry0, ry1, FZ, CEIL, BLUE, C_SHELL)
for x in AL:
    abox(f"Rear Wall Over Alcove {x:.0f}", x - AW, x + AW, ry0, ry1, AH, CEIL, BLUE, C_SHELL)
for k in range(0, len(xs), 2):
    abox(f"Rear Wall Base Band {k}", xs[k], xs[k + 1], ry1 - 0.1, ry1 + 0.05, FZ, FZ + 6.0, CONC, C_SHELL)
# heavy corner supports + top beam ring
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * W, sy * D
        bevbox(f"Corner Support {sx}{sy}", x - 2.2, x + 2.2, y - 2.2, y + 2.2, -0.5, CEIL + 2.0, STEEL, C_SHELL, b=0.5)
        bevbox(f"Corner Footing {sx}{sy}", x - 2.8, x + 2.8, y - 2.8, y + 2.8, -0.5, FZ + 1.2, STONE, C_SHELL, b=0.4)
bevbox("Ring Beam Front", -W, W, -D - 0.6, -D + T, CEIL, CEIL + 1.6, STEEL, C_SHELL, b=0.3)
bevbox("Ring Beam Rear", -W, W, D - T, D + 0.6, CEIL, CEIL + 1.6, STEEL, C_SHELL, b=0.3)
for s in (-1, 1):
    bevbox(f"Ring Beam Side {s}", min(s * (W + 0.6), s * (W - T)), max(s * (W + 0.6), s * (W - T)), -D, D, CEIL, CEIL + 1.6, STEEL, C_SHELL, b=0.3)

# ------------------------------------------------------------------ ROOF: raised central section with skylight, asymmetric sides
RZ = CEIL + 1.6
CX0, CX1, CY0, CY1 = -14.0, 14.0, -22.0, 22.0       # raised central section
TOPZ = FZ + 30.0                                     # highest roof ~30 above floor
abox("Roof Left", -W, CX0, -D, D, RZ - 1.6, RZ, CONC, C_ROOF)
bevbox("Roof Left Parapet", -W - 0.4, CX0, -D - 0.4, -D + 0.8, RZ, RZ + 1.4, STEEL, C_ROOF, b=0.2)
# lower right roof section (slopes down to the side - asymmetric silhouette)
hexa("Roof Right", [V(CX1, -D, RZ - 1.6), V(W, -D, RZ - 1.6), V(W, D, RZ - 1.6), V(CX1, D, RZ - 1.6),
                    V(CX1, -D, RZ), V(W + 0.6, -D, RZ - 1.6), V(W + 0.6, D, RZ - 1.6), V(CX1, D, RZ)], STEEL2, C_ROOF)
abox("Roof Centre Low Front", CX0, CX1, -D, CY0, RZ - 1.6, RZ, CONC, C_ROOF)
abox("Roof Centre Low Rear", CX0, CX1, CY1, D, RZ - 1.6, RZ, CONC, C_ROOF)
for s in (-1, 1):                                    # clerestory walls of the raised section
    abox(f"Clerestory Side {s}", min(s * CX1, s * (CX1 - 1.2)), max(s * CX1, s * (CX1 - 1.2)), CY0, CY1, RZ - 1.6, TOPZ - 1.2, BLUE2, C_ROOF)
abox("Clerestory Front", CX0, CX1, CY0, CY0 + 1.2, RZ - 1.6, TOPZ - 1.2, BLUE2, C_ROOF)
abox("Clerestory Rear", CX0, CX1, CY1 - 1.2, CY1, RZ - 1.6, TOPZ - 1.2, BLUE2, C_ROOF)
for k in range(4):                                   # clerestory windows on the front face
    x = -10.5 + k * 7.0
    abox(f"Clerestory Window {k}", x - 2.6, x + 2.6, CY0 - 0.05, CY0 + 0.1, RZ + 0.5, TOPZ - 2.0, GLASS, C_ROOF)
bevbox("Raised Roof Slab Front", CX0 - 1.0, CX1 + 1.0, CY0 - 1.0, -10.0, TOPZ - 1.2, TOPZ, STEEL, C_ROOF, b=0.3)
bevbox("Raised Roof Slab Rear", CX0 - 1.0, CX1 + 1.0, 10.0, CY1 + 1.0, TOPZ - 1.2, TOPZ, STEEL, C_ROOF, b=0.3)
for s in (-1, 1):
    bevbox(f"Raised Roof Slab Side {s}", min(s * (CX1 + 1.0), s * 7.0), max(s * (CX1 + 1.0), s * 7.0), -10.0, 10.0, TOPZ - 1.2, TOPZ, STEEL, C_ROOF, b=0.3)
abox("Skylight Glass", -7.0, 7.0, -10.0, 10.0, TOPZ - 0.9, TOPZ - 0.6, GLASS, C_ROOF)
for k in range(1, 4):
    y = -10 + k * 5.0
    bevbox(f"Skylight Rib {k}", -7.0, 7.0, y - 0.25, y + 0.25, TOPZ - 1.0, TOPZ - 0.3, STEEL, C_ROOF, b=0.08)
# roof vent + exterior pipes
bevbox("Roof Vent Box", -30.0, -24.0, 6.0, 12.0, RZ, RZ + 2.6, STEEL2, C_ROOF, b=0.3)
for k in range(5):
    abox(f"Vent Louvre {k}", -29.6, -24.4, 5.9, 6.0, RZ + 0.5 + k * 0.4, RZ + 0.75 + k * 0.4, STEEL, C_ROOF)
bevbox("Roof Vent Cap", -30.6, -23.4, 5.4, 12.6, RZ + 2.6, RZ + 3.1, STEEL, C_ROOF, b=0.2)
for k, y in enumerate((-14.0, -10.0)):
    path_tube(f"Exterior Pipe {k}", [V(W + 1.2, y, FZ + 1.0), V(W + 1.2, y, RZ - 2.0), V(W - 2.0, y, RZ + 1.2), V(26.0, y, RZ + 1.2)],
              [0.7 - 0.15 * k] * 4, COPPER, C_ROOF, n=12)
    for z in (FZ + 6.0, FZ + 14.0):
        torus(f"Pipe Clamp {k}{z:.0f}", V(W + 1.2, y, z), Z_AX, Y_AX, 0.78 - 0.15 * k, 0.12, STEEL, C_ROOF, n_major=12, n_minor=4)
path_tube("Exterior Pipe Tall", [V(-W - 1.0, 14.0, FZ + 1.0), V(-W - 1.0, 14.0, RZ + 4.0)], [0.9, 0.9], COPPER, C_ROOF, n=12)
lathe("Exhaust Cap", V(-W - 1.0, 14.0, RZ + 4.0), [(1.2, 0), (1.2, 0.4), (0.9, 0.9)], STEEL, C_ROOF, n=12, smooth=False)
# interior ceiling beams + soft industrial lights (part of the shell, under the roof)
for k in range(5):
    y = -20 + k * 10.0
    bevbox(f"Ceiling Beam {k}", -W + T, W - T, y - 0.6, y + 0.6, CEIL - 1.4, CEIL, STEEL, C_SHELL, b=0.15)
for (x, y) in ((-22, -15), (22, -15), (-22, 5), (22, 5), (-22, 20), (22, 20), (0, -20), (0, 20)):
    cyl(f"Lamp Cord {x}{y}", V(x, y, CEIL - 1.4), V(x, y, CEIL - 3.2), 0.06, 0.06, STEEL, C_SHELL, n=4)
    lathe(f"Lamp Shade {x}{y}", V(x, y, CEIL - 4.4), [(0.4, 1.2), (1.6, 0.0), (1.7, -0.1)], STEEL, C_SHELL, n=12, smooth=False)
    cyl(f"Lamp Glow {x}{y}", V(x, y, CEIL - 4.45), V(x, y, CEIL - 4.35), 1.3, 1.3, LAMP, C_SHELL, n=12)

# ------------------------------------------------------------------ FLOOR STRIPS + HAZARD MARKINGS
for s in (-1, 1):                                    # broad inset strips: entrance -> showcase -> stations
    abox(f"Guide Strip Entrance {s}", s * 3.2 - 0.6, s * 3.2 + 0.6, -D + T, -9.0, FZ, FZ + 0.03, STEEL2, C_SHELL)
abox("Guide Strip To Fusion", -25.0, -10.0, -0.6, 0.6, FZ, FZ + 0.03, STEEL2, C_SHELL)
abox("Guide Strip To Evolution", 10.0, 25.0, -0.6, 0.6, FZ, FZ + 0.03, STEEL2, C_SHELL)
abox("Guide Strip To Rear", -0.6, 0.6, 9.0, D - T, FZ, FZ + 0.03, STEEL2, C_SHELL)
abox("Guide Accent Fusion", -22.0, -12.0, -0.15, 0.15, FZ + 0.03, FZ + 0.05, FUSE, C_SHELL)
abox("Guide Accent Evolution", 12.0, 22.0, -0.15, 0.15, FZ + 0.03, FZ + 0.05, PURP, C_SHELL)
abox("Guide Accent Archive", 2.95, 3.45, -D + T, -11.0, FZ + 0.03, FZ + 0.05, CYAN, C_SHELL)
hazard_strip("Hazard Fusion", -24.4, -23.6, -9.5, 9.5, FZ, C_FUSE, along_x=False)
hazard_strip("Hazard Evolution", 23.6, 24.4, -9.5, 9.5, FZ, C_EVO, along_x=False)

# ------------------------------------------------------------------ CENTRAL MACHINE SHOWCASE (octagon, ~14 across, 2 high)
SC = V(0.0, 0.0, FZ)
R8 = 7.0 / math.cos(math.pi / 8)                     # 14 studs across flats
lathe("Showcase Base", SC, [(R8, 0), (R8, 0.9), (R8 - 0.3, 1.1), (0.01, 1.1)], STEEL, C_SHOW, n=8, smooth=False)
for k in range(8):                                   # base rotated so flats face the room axes
    pass
lathe("Showcase Platform", SC + V(0, 0, 1.1), [(R8 - 0.6, 0), (R8 - 0.6, 0.55), (R8 - 0.95, 0.9), (5.2, 0.9), (5.2, 0.7), (0.01, 0.7)], STEEL2, C_SHOW, n=8, smooth=False)
sep(lathe("Projection Surface", SC + V(0, 0, 1.65), [(4.6, 0), (4.6, 0.12), (0.01, 0.12)], PROJ, C_SHOW, n=32))
sep(torus("Showcase Light Ring", SC + V(0, 0, 1.86), Z_AX, Y_AX, 4.9, 0.16, CYAN, C_SHOW, n_major=48, n_minor=6))
for k in range(8):                                   # bolts + panel divisions
    a = math.pi / 8 + k * math.pi / 4
    d = V(math.cos(a), math.sin(a), 0)
    dot(f"Showcase Bolt {k}", SC + d * (R8 - 1.2) + V(0, 0, 2.0), 0.16, STEEL, C_SHOW)
    beam(f"Showcase Panel Line {k}", SC + d * 5.4 + V(0, 0, 2.01), SC + d * (R8 - 0.9) + V(0, 0, 2.01), 0.08, 0.02, Z_AX, STEEL, C_SHOW)
for k in range(4):                                   # four chunky projector units
    a = math.pi / 4 + k * math.pi / 2
    d = V(math.cos(a), math.sin(a), 0)
    P = SC + d * 5.7 + V(0, 0, 2.0)
    pr = obox(f"Projector {k + 1}", P + V(0, 0, 0.55), (1.6, 1.3, 1.1), d, V(-d.y, d.x, 0), Z_AX, STEEL, C_SHOW)
    sep(pr)
    sep(cyl(f"Projector {k + 1} Lens", P + V(0, 0, 0.75) - d * 0.55, P + V(0, 0, 1.2) - d * 1.0, 0.38, 0.32, CYAN, C_SHOW, n=12))
PLACEHOLDER = sep(obox("Display Placeholder", SC + V(0, 0, 9.0), (6.0, 6.0, 6.0), X_AX, Y_AX, Z_AX, HOLO, C_SHOW))
IP = SC + V(0, -R8 - 0.9, 0)                          # small angled information panel at the front
bevbox("Info Panel Post", IP.x - 0.4, IP.x + 0.4, IP.y - 0.3, IP.y + 0.3, FZ, FZ + 2.6, STEEL, C_SHOW, b=0.1)
sep(obox("Info Panel Screen", IP + V(0, -0.2, 2.9), (3.0, 0.15, 1.6), X_AX, V(0, 1, 0.6).normalized(), V(0, -0.6, 1).normalized(), SCREEN, C_SHOW))
obox("Info Panel Frame", IP + V(0, -0.1, 2.85), (3.4, 0.25, 2.0), X_AX, V(0, 1, 0.6).normalized(), V(0, -0.6, 1).normalized(), STEEL, C_SHOW)

# ------------------------------------------------------------------ ARCHIVE CONSOLE (front-right of the showcase)
AC = V(11.5, -12.0, FZ)
face = V(-0.45, -1, 0).normalized()                   # turned to greet players coming in
side = V(-face.y, face.x, 0)
obox("Archive Pedestal", AC + V(0, 0, 1.3), (5.0, 2.4, 2.6), side, face * -1, Z_AX, STEEL, C_ARCH)
obox("Archive Pedestal Foot", AC + V(0, 0, 0.25), (5.6, 3.0, 0.5), side, face * -1, Z_AX, STEEL2, C_ARCH)
obox("Archive Desk", AC + V(0, 0, 2.75) + face * 0.5, (5.0, 1.6, 0.3), side, face * -1, Z_AX, STEEL2, C_ARCH)
sep(obox("Archive Control Panel", AC + V(0, 0, 2.95) + face * 0.6, (3.2, 1.0, 0.14), side, face * -1, Z_AX, SCREEN, C_ARCH))
for k in range(4):
    dot(f"Archive Button {k}", AC + V(0, 0, 3.05) + face * 0.75 + side * (-1.2 + k * 0.8), 0.14, CYAN if k % 2 else COPPER, C_ARCH)
up = (Z_AX * 0.85 - face * 0.5).normalized()
SCC = AC + V(0, 0, 5.2) - face * 0.4
obox("Archive Screen Frame", SCC, (5.0, 0.6, 3.3), side, (face * -1 * 0.85 + Z_AX * 0.5).normalized(), up, STEEL, C_ARCH)
sep(obox("Archive Screen", SCC + face * 0.32, (4.3, 0.06, 2.6), side, (face * -1 * 0.85 + Z_AX * 0.5).normalized(), up, SCREEN, C_ARCH))
for s in (-1, 1):
    obox(f"Archive Accent {s}", SCC + face * 0.33 + side * s * 2.35, (0.14, 0.08, 2.9), side, (face * -1 * 0.85 + Z_AX * 0.5).normalized(), up, CYAN, C_ARCH)
obox("Archive Accent Top", SCC + face * 0.33 + up * 1.55, (4.6, 0.08, 0.14), side, (face * -1 * 0.85 + Z_AX * 0.5).normalized(), up, CYAN, C_ARCH)
obox("Archive Screen Back", SCC - face * 0.5 - up * 0.3, (3.0, 0.8, 1.8), side, face * -1, Z_AX, STEEL, C_ARCH)

# ------------------------------------------------------------------ FUSION STATION (left wall: 16 wide, 9 deep, 14 tall; faces +X)
FX0, FX1 = -W + T, -W + T + 9.0                      # depth along X
bevbox("Fusion Base Plinth", FX0, FX1, -8.0, 8.0, FZ, FZ + 1.0, STEEL, C_FUSE, b=0.3)
for y in (-8.0, 8.0):                                # overhead frame posts + header
    bevbox(f"Fusion Frame Post {y:.0f}", FX0, FX0 + 1.6, y - 0.8 if y > 0 else y, y if y > 0 else y + 0.8, FZ + 1.0, FZ + 14.0, STEEL, C_FUSE, b=0.25)
bevbox("Fusion Overhead Frame", FX0, FX0 + 6.0, -8.0, 8.0, FZ + 12.4, FZ + 14.0, STEEL, C_FUSE, b=0.3)
bevbox("Fusion Overhead Front Beam", FX0 + 5.0, FX0 + 6.6, -8.0, 8.0, FZ + 11.6, FZ + 13.2, STEEL2, C_FUSE, b=0.25)
for k in range(8):
    abox(f"Fusion Beam Hazard {k}", FX0 + 6.6, FX0 + 6.64, -7.5 + k * 1.9, -6.6 + k * 1.9, FZ + 11.8, FZ + 13.0, HAZ if k % 2 else HAZB, C_FUSE)
CH = V(FX0 + 3.4, 1.5, FZ + 1.0)                      # large central chamber
lathe("Fusion Chamber Base", CH, [(2.9, 0), (2.9, 1.0), (2.5, 1.3)], STEEL2, C_FUSE, n=12, smooth=False)
lathe("Fusion Chamber Glass", CH + V(0, 0, 1.3), [(2.3, 0), (2.3, 5.2)], GLASS, C_FUSE, n=16)
for k in range(4):
    a = k * math.pi / 2 + math.pi / 4
    cyl(f"Fusion Chamber Rib {k}", CH + V(2.35 * math.cos(a), 2.35 * math.sin(a), 1.3), CH + V(2.35 * math.cos(a), 2.35 * math.sin(a), 6.5), 0.22, 0.22, STEEL, C_FUSE, n=6)
lathe("Fusion Chamber Cap", CH + V(0, 0, 6.5), [(2.7, 0), (2.7, 0.6), (1.6, 1.4), (1.0, 1.6)], STEEL, C_FUSE, n=12, smooth=False)
sep(lathe("Fusion Energy Core", CH + V(0, 0, 2.6), [(0.01, 0), (1.0, 0.6), (1.2, 1.6), (1.0, 2.6), (0.01, 3.2)], FUSE, C_FUSE, n=12))
for k, (y0, label) in enumerate(((-6.2, 1), (-3.4, 2), (-0.6, 3))):
    # three separated ingredient trays at the front (empty for gameplay displays)
    TR = V(FX1 - 1.4, y0 - 1.5, FZ + 1.0)
    bevbox(f"Tray Stand {label}", TR.x - 1.1, TR.x + 1.1, y0 - 2.5, y0 - 0.5, FZ + 1.0, FZ + 2.6, STEEL, C_FUSE, b=0.15)
    sep(bevbox(f"Ingredient Tray {label}", TR.x - 1.2, TR.x + 1.2, y0 - 2.6, y0 - 0.4, FZ + 2.6, FZ + 3.0, STEEL2, C_FUSE, b=0.12))
    abox(f"Tray Accent {label}", TR.x + 1.18, TR.x + 1.24, y0 - 2.4, y0 - 0.6, FZ + 2.65, FZ + 2.85, FUSE, C_FUSE)
    path_tube(f"Tray Pipe {label}", [V(TR.x - 1.1, y0 - 1.5, FZ + 2.0), V(TR.x - 2.4, y0 - 1.5 + (1.5 - (y0 - 1.5)) * 0.3, FZ + 3.0), CH + V(1.6, (y0 - 1.5 - CH.y) * 0.4, 3.4)],
              [0.32, 0.32, 0.32], COPPER, C_FUSE, n=10)
for k, s in enumerate((-1, 1)):                      # two thick mechanical arms angled towards the chamber
    sh = V(FX0 + 4.2, CH.y + s * 6.0, FZ + 12.2)
    el = V(FX0 + 5.4, CH.y + s * 4.2, FZ + 10.0)
    hd = V(CH.x + 1.0, CH.y + s * 2.4, FZ + 8.4)
    arm = bmesh.new()
    for a_, b_, r in ((sh, el, 0.55), (el, hd, 0.45)):
        u, v = perp_basis((b_ - a_))
        loft([ring_pts(a_, u, v, r, 10), ring_pts(b_, u, v, r * 0.9, 10)], bm=arm)
    sep(finish(f"Fusion Arm {'L' if s < 0 else 'R'}", arm, STEEL2, C_FUSE, merge=0))
    dot(f"Fusion Arm Joint {k}a", sh, 0.8, STEEL, C_FUSE)
    dot(f"Fusion Arm Joint {k}b", el, 0.65, COPPER, C_FUSE)
    cone(f"Fusion Arm Emitter {k}", hd, hd + (CH + V(0, 0, 4.0) - hd).normalized() * 1.2, 0.45, FUSE, C_FUSE, n=8)
sep(bevbox("Fusion Output Platform", FX1 - 3.4, FX1 + 0.2, 4.0, 7.6, FZ + 1.0, FZ + 2.2, STEEL2, C_FUSE, b=0.2))
abox("Output Platform Ring", FX1 - 3.0, FX1 - 0.2, 4.4, 7.2, FZ + 2.2, FZ + 2.26, FUSE, C_FUSE)
path_tube("Output Pipe", [CH + V(1.0, 2.2, 1.6), V(FX1 - 2.0, 5.8, FZ + 3.0), V(FX1 - 1.6, 5.8, FZ + 2.4)], [0.4] * 3, COPPER, C_FUSE, n=10)
TM = V(FX1 + 0.6, -8.6, FZ)                           # accessible control terminal on the front corner
bevbox("Fusion Terminal Body", TM.x - 0.9, TM.x + 0.9, TM.y - 0.6, TM.y + 0.9, FZ, FZ + 3.6, STEEL, C_FUSE, b=0.15)
sep(obox("Fusion Terminal Screen", TM + V(0.95, 0.15, 3.0), (0.08, 1.6, 1.1), V(1, 0, 0.4).normalized(), Y_AX, V(-0.4, 0, 1).normalized(), SCREEN, C_FUSE))
abox("Fusion Terminal Light", TM.x + 0.9, TM.x + 0.96, TM.y - 0.4, TM.y + 0.7, FZ + 2.0, FZ + 2.2, FUSE, C_FUSE)
bevbox("Fusion Back Panel", FX0 - 0.2, FX0 + 0.4, -8.0, 8.0, FZ + 1.0, FZ + 12.4, BLUE2, C_FUSE, b=0.1)

# ------------------------------------------------------------------ STAR / EVOLUTION STATION (right wall; faces -X)
EX1, EX0 = W - T, W - T - 9.0
bevbox("Evolution Base Plinth", EX0, EX1, -8.0, 8.0, FZ, FZ + 0.8, STEEL, C_EVO, b=0.3)
bevbox("Evolution Back Panel", EX1 - 0.4, EX1 + 0.2, -8.0, 8.0, FZ + 0.8, FZ + 14.0, BLUE2, C_EVO, b=0.1)
PC = V(EX0 + 4.6, 0.0, FZ + 0.8)
lathe("Evolution Pedestal Base", PC, [(2.6, 0), (2.6, 0.8), (2.2, 1.1), (2.0, 1.1)], STEEL, C_EVO, n=8, smooth=False)
sep(lathe("Evolution Centre Pedestal", PC + V(0, 0, 1.1), [(2.0, 0), (1.6, 1.2), (1.9, 1.5), (0.01, 1.5)], STEEL2, C_EVO, n=8, smooth=False))
torus("Pedestal Purple Ring", PC + V(0, 0, 2.62), Z_AX, Y_AX, 1.7, 0.1, PURP, C_EVO, n_major=24, n_minor=4)
for s in (-1, 1):                                    # thick arch over the pedestal
    bevbox(f"Evolution Arch Post {s}", PC.x - 0.8, PC.x + 1.2, s * 3.0 - 0.9, s * 3.0 + 0.9, FZ + 0.8, FZ + 11.0, STEEL, C_EVO, b=0.25)
    abox(f"Arch Post Accent {s}", PC.x - 0.84, PC.x - 0.8, s * 3.0 - 0.3, s * 3.0 + 0.3, FZ + 2.0, FZ + 10.0, PURP, C_EVO)
bevbox("Evolution Arch Top", PC.x - 0.8, PC.x + 1.2, -3.9, 3.9, FZ + 11.0, FZ + 13.0, STEEL, C_EVO, b=0.3)
STAR = []
for k in range(10):
    a = math.pi / 2 + k * math.pi / 5
    r = 1.2 if k % 2 == 0 else 0.5
    STAR.append(V(PC.x - 0.9, r * math.cos(a), FZ + 12.0 + r * math.sin(a)))
sep(blade("Evolution Star Emblem", STAR, 0.25, GOLD, C_EVO))
for s in (-1, 1):                                    # two symmetrical preview plinths
    PP = V(EX0 + 3.6, s * 6.0, FZ + 0.8)
    bevbox(f"Preview Plinth Base {s}", PP.x - 1.5, PP.x + 1.5, PP.y - 1.5, PP.y + 1.5, FZ + 0.8, FZ + 2.0, STEEL, C_EVO, b=0.2)
    sep(bevbox(f"Evolution Preview Plinth {'L' if s < 0 else 'R'}", PP.x - 1.2, PP.x + 1.2, PP.y - 1.2, PP.y + 1.2, FZ + 2.0, FZ + 2.5, STEEL2, C_EVO, b=0.12))
    abox(f"Preview Plinth Accent {s}", PP.x - 1.54, PP.x - 1.5, PP.y - 1.0, PP.y + 1.0, FZ + 1.2, FZ + 1.5, PURP, C_EVO)
    small = [V(PP.x - 1.55, PP.y + 0.35 * math.cos(math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.42),
               FZ + 1.75 + 0.35 * math.sin(math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.42)) for k in range(10)]
    blade(f"Gold Star Detail {s}", small, 0.06, GOLD, C_EVO)
    # branching light channel from the centre pedestal to each preview plinth
    pts = [PC + V(-1.6, 0, 0.82), PC + V(-2.4, s * 1.4, 0.82), V(PP.x - 0.6, PP.y - s * 1.6, FZ + 0.82)]
    for j in range(2):
        beam(f"Light Channel {s}{j}", pts[j], pts[j + 1], 0.35, 0.05, Z_AX, PURP, C_EVO)
CS = V(EX0 - 0.6, -8.0, FZ)                            # control screen facing the player (front corner)
bevbox("Evolution Screen Stand", CS.x - 0.5, CS.x + 0.5, CS.y - 0.5, CS.y + 0.5, FZ, FZ + 3.2, STEEL, C_EVO, b=0.12)
obox("Evolution Screen Frame", CS + V(-0.1, 0, 3.9), (0.4, 3.0, 2.0), V(-1, 0, 0.3).normalized() * -1, Y_AX, V(0.3, 0, 1).normalized(), STEEL, C_EVO)
sep(obox("Evolution Control Screen", CS + V(-0.32, 0, 3.95), (0.06, 2.6, 1.6), V(-1, 0, 0.3).normalized() * -1, Y_AX, V(0.3, 0, 1).normalized(), SCREEN, C_EVO))
abox("Evolution Screen Accent", CS.x - 0.36, CS.x - 0.3, CS.y - 1.4, CS.y + 1.4, FZ + 4.95, FZ + 5.05, PURP, C_EVO)

# ------------------------------------------------------------------ REAR COLLECTION ALCOVES (cyan / orange / purple)
for k, (x, acc) in enumerate(zip(AL, (CYAN, FUSE, PURP))):
    a0, a1 = x - AW, x + AW
    abox(f"Alcove Back {k}", a0 - 1.0, a1 + 1.0, D + 4.0, D + 5.0, FZ, AH + 1.0, CONC, C_REAR)
    for s in (-1, 1):
        abox(f"Alcove Side {k}{s}", min(x + s * AW, x + s * (AW + 1.0)), max(x + s * AW, x + s * (AW + 1.0)), D, D + 4.0, FZ, AH + 1.0, CONC, C_REAR)
    abox(f"Alcove Roof {k}", a0 - 1.0, a1 + 1.0, D, D + 5.0, AH, AH + 1.0, CONC, C_REAR)
    abox(f"Alcove Floor {k}", a0, a1, D - T, D + 4.0, FZ - 0.1, FZ, FLOOR, C_REAR)
    abox(f"Alcove Wall Panel {k}", a0 + 0.2, a1 - 0.2, D + 3.9, D + 4.0, FZ + 0.5, AH - 0.5, BLUE2, C_REAR)
    for s in (-1, 1):                                # simple metal frame
        bevbox(f"Alcove Frame Post {k}{s}", x + s * AW - 0.6, x + s * AW + 0.6, D - T - 0.4, D - T + 0.4, FZ, AH, STEEL, C_REAR, b=0.12)
    bevbox(f"Alcove Frame Header {k}", a0 - 0.6, a1 + 0.6, D - T - 0.4, D - T + 0.4, AH - 0.8, AH + 0.4, STEEL, C_REAR, b=0.12)
    abox(f"Alcove Accent Strip {k}", a0 + 0.4, a1 - 0.4, D - T - 0.45, D - T - 0.4, AH - 0.6, AH - 0.3, acc, C_REAR)
    bevbox(f"Alcove Plinth Base {k}", x - 2.2, x + 2.2, D + 0.4, D + 3.6, FZ, FZ + 2.6, STEEL, C_REAR, b=0.2)
    sep(bevbox(f"Collection Display {k + 1}", x - 1.8, x + 1.8, D + 0.7, D + 3.3, FZ + 2.6, FZ + 3.0, STEEL2, C_REAR, b=0.1))
    sep(obox(f"Collection Plaque {k + 1}", V(x, D + 0.35, FZ + 1.5), (2.6, 0.08, 1.0), X_AX, Y_AX, Z_AX, PLAQUE, C_REAR))
    abox(f"Plinth Accent {k}", x - 2.24, x + 2.24, D + 0.36, D + 0.4, FZ + 2.3, FZ + 2.45, acc, C_REAR)
    cyl(f"Alcove Spot Light {k}", V(x, D + 2.0, AH - 0.05), V(x, D + 2.0, AH - 0.25), 1.0, 1.0, LAMP, C_REAR, n=12)

# ------------------------------------------------------------------ WALL DETAILS + CORNER PROPS (kept out of walking routes)
for s in (-1, 1):                                    # large wall vents
    for y in (-18.0, 16.0):
        bevbox(f"Wall Vent {s}{y:.0f}", min(s * (W - T), s * (W - T - 0.3)), max(s * (W - T), s * (W - T - 0.3)), y - 2.0, y + 2.0, FZ + 15.0, FZ + 18.0, STEEL, C_PROPS, b=0.1)
        for j in range(4):
            abox(f"Wall Vent Slat {s}{y:.0f}{j}", min(s * (W - T - 0.32), s * (W - T - 0.36)), max(s * (W - T - 0.32), s * (W - T - 0.36)), y - 1.7, y + 1.7, FZ + 15.4 + j * 0.65, FZ + 15.7 + j * 0.65, STEEL2, C_PROPS)
path_tube("Interior Pipe Left", [V(-W + T + 0.6, -D + T + 1.0, FZ + 19.0), V(-W + T + 0.6, D - T - 1.0, FZ + 19.0)], [0.5, 0.5], COPPER, C_PROPS, n=10)
path_tube("Interior Pipe Right", [V(W - T - 0.6, -D + T + 1.0, FZ + 19.5), V(W - T - 0.6, D - T - 1.0, FZ + 19.5)], [0.5, 0.5], COPPER, C_PROPS, n=10)
path_tube("Interior Pipe Rear", [V(-W + T + 1.0, D - T - 0.6, FZ + 20.0), V(W - T - 1.0, D - T - 0.6, FZ + 20.0)], [0.45, 0.45], COPPER, C_PROPS, n=10)
TC = V(29.0, 21.5, FZ)                                 # tool cabinet + crates (rear right corner)
bevbox("Tool Cabinet", TC.x - 2.0, TC.x + 2.0, TC.y + 1.6, TC.y + 3.2, FZ, FZ + 5.0, ORANGE, C_PROPS, b=0.15)
for j in range(3):
    abox(f"Tool Drawer {j}", TC.x - 1.8, TC.x + 1.8, TC.y + 1.56, TC.y + 1.6, FZ + 0.6 + j * 1.3, FZ + 1.6 + j * 1.3, STEEL, C_PROPS)
for k, (dx, dy, sz) in enumerate(((-4.6, 1.8, 2.2), (-2.4, 2.0, 1.8), (-4.0, 1.9, 1.4))):
    z0 = FZ if k < 2 else FZ + 2.2
    bevbox(f"Crate {k}", TC.x + dx - sz / 2, TC.x + dx + sz / 2, TC.y + dy - sz / 2, TC.y + dy + sz / 2, z0, z0 + sz, WOOD, C_PROPS, b=0.12)

# ------------------------------------------------------------------ SCALE (50% of the original 72 x 56 brief)
SCALE = float(arg("--scale", 0.5))
for ob in MINE_OBJECTS:
    ob.data.transform(Matrix.Scale(SCALE, 4))

# ------------------------------------------------------------------ EXPORT
name = "MachineWorkshop"
OUT_DIR = OUT
os.makedirs(OUT_DIR, exist_ok=True)
scene = bpy.context.scene
root_empty = bpy.data.objects.new(name, None)
STATE["root"].objects.link(root_empty)
for ob in MINE_OBJECTS:
    me = ob.data
    c = sum((v.co for v in me.vertices), Vector()) / max(len(me.vertices), 1)
    me.transform(Matrix.Translation(-c))
    ob.location = c
    ob.parent = root_empty
tris = sum(len(p.vertices) - 2 for ob in MINE_OBJECTS for p in ob.data.polygons)
print(f"[workshop] objects={len(MINE_OBJECTS)} triangles={tris} separate={len(SEPARATE)}")

def export(fbx_name, obs):
    exp = bpy.data.collections.new("_export")
    scene.collection.children.link(exp)
    groups, singles = {}, []
    for ob in obs:
        if ob.name in SEPARATE:
            singles.append(ob)
        else:
            groups.setdefault(ob.data.materials[0].name, []).append(ob)
    made = []
    for ob in singles:
        dd = ob.copy();dd.data = ob.data.copy();dd.parent = None;dd.matrix_world = ob.matrix_world.copy()
        exp.objects.link(dd);dd.name = ob.name.replace(" ", "");made.append(dd)
    for mname, grp in groups.items():
        dups = []
        for ob in grp:
            dd = ob.copy();dd.data = ob.data.copy();dd.parent = None;dd.matrix_world = ob.matrix_world.copy()
            exp.objects.link(dd);dups.append(dd)
        with bpy.context.temp_override(active_object=dups[0], selected_editable_objects=dups, selected_objects=dups):
            bpy.ops.object.join()
        dups[0].name = export_name(mname);made.append(dups[0])
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for j in made:
        j.select_set(True)
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT_DIR, fbx_name), use_selection=True, object_types={'MESH'}, use_triangles=True,
                             mesh_smooth_type='FACE', apply_unit_scale=True)
    parts = [(j.name, j.data.materials[0].name) for j in made]
    for j in made:
        bpy.data.objects.remove(j, do_unlink=True)
    bpy.data.collections.remove(exp)
    print(f"[workshop] exported {fbx_name}: {len(parts)} parts")
    return parts

found_obs = [o for o in MINE_OBJECTS if o.users_collection[0] == C_FOUND]
bld_obs = [o for o in MINE_OBJECTS if o.users_collection[0] != C_FOUND]
parts = export(f"{name}_Building_Roblox.fbx", bld_obs) + export(f"{name}_Foundation_Roblox.fbx", found_obs)

# optional colour/material/transparency setup for every exported part
rows = []
for pname, mname in sorted(set(parts)):
    rb = RBX[export_name(mname)]
    rows.append('\t["%s"] = {"%s", %d, %d, %d, %g%s},' % (pname, rb[0], *rb[1], rb[2], (", {%d, %d, %d, %g, %g}" % rb[3]) if rb[3] else ""))
lua = """-- MachineWorkshop: colours, Roblox materials, transparency and soft lights for both imported models.
-- Import MachineWorkshop_Foundation_Roblox.fbx and MachineWorkshop_Building_Roblox.fbx (Scale Unit = Stud,
-- untick "Import as single mesh"), select both models, paste this file into the Command Bar.
local LOOK = {
%s
}
for _, model in ipairs(game:GetService("Selection"):Get()) do
	for _, p in ipairs(model:GetDescendants()) do
		if p:IsA("BasePart") then
			local l = LOOK[(p.Name:gsub("%%.%%d+$", ""))]
			p.Anchored = true
			if l then
				p.Material = Enum.Material[l[1]]; p.Color = Color3.fromRGB(l[2], l[3], l[4]); p.Transparency = l[5]
				if p:IsA("MeshPart") then p.TextureID = "" end
				if l[6] then
					local light = p:FindFirstChild("SoftLight") or Instance.new("PointLight")
					light.Name = "SoftLight"; light.Color = Color3.fromRGB(l[6][1], l[6][2], l[6][3]); light.Range = l[6][4]; light.Brightness = l[6][5]; light.Shadows = true
					light.Parent = p
				end
			end
			if p.Name == "DisplayPlaceholder" then p.CanCollide = false end
		end
	end
end
print("[MachineWorkshop] styled")
""" % "\n".join(rows)
open(os.path.join(OUT_DIR, f"{name}_RobloxSetup.lua"), "w").write(lua)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, f"{name}.blend"))

# ------------------------------------------------------------------ RENDERS
if RENDER:
    PLACEHOLDER.hide_render = True
    for o in MINE_OBJECTS:
        if o.name.startswith('Burn'):
            o.hide_render = True
    scene.render.engine = 'CYCLES'; scene.cycles.samples = SAMPLES; scene.cycles.use_denoising = True
    scene.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.new("Sky"); scene.world = world; world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.45, 0.6, 0.85, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
    stage = STATE["stage"]
    gme = bpy.data.meshes.new("Hill"); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=160); bm.to_mesh(gme); bm.free()
    g = bpy.data.objects.new("Hill", gme); g.location.z = -1.9 * SCALE; stage.objects.link(g); gme.materials.append(new_mat("Grass", lin((96, 150, 80)), rough=0.95))
    def light(n, kind, loc, energy, col=(1, 1, 1), rot=None, size=1.0):
        ld = bpy.data.lights.new(n, kind); ld.energy = energy; ld.color = col
        if kind == 'SUN': ld.angle = math.radians(8)
        else: ld.shadow_soft_size = size
        ob = bpy.data.objects.new(n, ld); ob.location = loc
        if rot: ob.rotation_euler = rot
        stage.objects.link(ob)
    light("Sun", 'SUN', V(0, 0, 80), 3.5, (1.0, 0.96, 0.9), rot=Euler((math.radians(50), 0, math.radians(-35))))
    for (x, y) in ((-20, -12), (20, -12), (-20, 10), (20, 10), (0, 0)):
        light(f"Room Fill {x}{y}", 'POINT', V(x, y, CEIL - 5) * SCALE, 4500 * SCALE * SCALE, (1.0, 0.95, 0.88), size=4 * SCALE)
    cams = {
        "exterior_hero": (V(62, -96, 44), V(0, -6, 10), 32, (1600, 1100)),
        "exterior_front": (V(0, -112, 18), V(0, 0, 12), 32, (1600, 1100)),
        "exterior_back": (V(-70, 80, 50), V(0, 0, 10), 32, (1600, 1100)),
        "interior_entrance": (V(0, -25, FZ + 7.0), V(0, 6, FZ + 5.0), 18, (1600, 1100)),
        "interior_overview": (V(-28, -24, FZ + 19), V(4, 6, FZ + 2), 16, (1600, 1100)),
        "interior_fusion": (V(-6, -16, FZ + 9), V(-28, 0, FZ + 6), 24, (1400, 1100)),
        "interior_evolution": (V(6, -16, FZ + 9), V(29, 0, FZ + 6), 24, (1400, 1100)),
        "interior_rear": (V(0, 4, FZ + 8), V(0, 30, FZ + 4), 22, (1600, 1000)),
        "cutaway_top": (V(0, -46, 120), V(0, 0, 0), 38, (1500, 1300)),
    }
    roof = [o for o in MINE_OBJECTS if o.users_collection[0] == C_ROOF]
    ceiling = [o for o in MINE_OBJECTS if o.name.startswith(("Ceiling Beam", "Lamp ", "Ring Beam"))]
    rdir = os.path.join(OUT_DIR, "renders"); os.makedirs(rdir, exist_ok=True)
    cams = {k: (l * SCALE, t * SCALE, ln, r) for k, (l, t, ln, r) in cams.items()}
    for n, (loc, tgt, lens, res) in cams.items():
        if VIEWS != "hero,front,left,back" and n not in VIEWS.split(","):
            continue
        cd = bpy.data.cameras.new(n); cd.lens = lens; cd.clip_end = 1000
        co = bpy.data.objects.new(n, cd); co.location = loc; co.rotation_euler = (tgt - loc).to_track_quat('-Z', 'Y').to_euler(); stage.objects.link(co)
        cut = n == "cutaway_top"
        for o in roof + (ceiling if cut else []):
            o.hide_render = cut
        scene.camera = co
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.filepath = os.path.join(rdir, f"{n}.png")
        bpy.ops.render.render(write_still=True)
        print("[workshop] rendered", n)
    for o in roof + ceiling:
        o.hide_render = False
