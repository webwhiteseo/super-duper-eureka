"""Clockwork Grinder Furnace - a brass steam machine on a riveted wooden deck: a conveyor ramp carries ore up between
two giant toothed grinding rollers into a glowing furnace pit. Big meshing side gears, drive belts, steam chimneys,
gauges and copper pipes. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

C_BASE, C_GRIND, C_FRAME, C_DETAIL = begin("ClockworkGrinderFurnace", ["Deck", "Grinders", "Frame", "Details"], seed=111)
WOOD = M("Deck Planks (Wood)", (130, 90, 56), rough=0.8, rbx="WoodPlanks", noise=((104, 70, 42), (156, 112, 72), 3.0, 0.3))
WOOD2 = M("Dark Planks (Wood)", (94, 62, 38), rough=0.8, rbx="WoodPlanks")
BRASS = M("Brass (Metal)", (214, 166, 74), rough=0.25, metal=1.0, rbx="Metal")
COPPER = M("Copper (Metal)", (196, 112, 62), rough=0.3, metal=1.0, rbx="Metal")
IRON = M("Dark Iron (Metal)", (52, 50, 54), rough=0.4, metal=0.9, rbx="Metal")
FIRE = M("Furnace Fire", (255, 140, 40), rough=0.3, glow=(255, 100, 10), glow_strength=4.0, rbx="Neon", light=(16, 2.0))
AMBER = M("Amber Glow", (255, 190, 80), rough=0.3, glow=(255, 160, 40), glow_strength=4.0, rbx="Neon", light=(8, 1.0))
GAUGE = M("Gauge Face", (240, 232, 210), rough=0.5)
STEAM = M("Steam", (230, 230, 234), rough=0.9, rbx="SmoothPlastic", alpha=0.3)
BELT = M("Leather Belt", (70, 40, 26), rough=0.7, rbx="Fabric")
CONVM = M("Conveyor", (60, 50, 44), rough=0.6, rbx="DiamondPlate", plate=12.0)
BURN = M("Burn Zone", (255, 150, 60), rough=0.2, glow=(255, 110, 20), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)

def gear(name, C, axis, up, r, teeth, th, mat, coll, hub=None):
    tube(name, C, axis, up, r, r * 0.45, th, mat, coll, n=max(24, teeth * 2))
    a_ = axis.normalized();u = up.normalized();v = a_.cross(u).normalized()
    for k in range(teeth):
        ang = 2 * math.pi * k / teeth
        rr = math.cos(ang) * v + math.sin(ang) * u;tt = -math.sin(ang) * v + math.cos(ang) * u
        obox(f"{name} Tooth {k + 1}", C + rr * (r + 0.14), (th, 0.3, 0.32), a_, rr, tt, mat, coll)
    for k in range(4):
        ang = math.pi / 4 + k * math.pi / 2
        rr = math.cos(ang) * v + math.sin(ang) * u
        beam(f"{name} Spoke {k}", C + rr * r * 0.2, C + rr * r * 0.5, 0.16, th * 0.8, a_, mat, coll)
    if hub:
        cyl(f"{name} Hub", C - a_ * th * 0.8, C + a_ * th * 0.8, r * 0.18, r * 0.18, hub, coll, n=12, hint=u)

# ---- wooden plank deck with brass corners and rivets
for k in range(12):
    y0 = -5.6 + k * 0.95
    abox(f"Plank {k}", -6.2, 6.2, y0, y0 + 0.9, 0, 0.5 + 0.03 * (k % 2), WOOD if k % 2 else WOOD2, C_BASE)
for sx in (-1, 1):
    for sy in (-1, 1):
        abox(f"Corner Plate {sx}{sy}", sx * 6.25 - 0.7, sx * 6.25 + 0.7, sy * 5.65 - 0.7, sy * 5.65 + 0.7, 0.0, 0.6, BRASS, C_BASE)
    for k in range(6):
        dot(f"Rivet {sx}{k}", V(sx * 6.0, -4.5 + k * 1.8, 0.55), 0.09, BRASS, C_BASE)

# ---- ramp + furnace pit + grinding rollers
conveyor_ramp(CONVM, AMBER, BRASS, AMBER, y_front=-9.0, y_lip=-5.2, y_end=-2.9, coll=C_BASE)
abox("Pit Box", -3.0, 3.0, -2.9, 2.6, 0.0, 1.3, IRON, C_GRIND)
abox("Pit Fire", -2.6, 2.6, -2.8, 2.2, 1.1, 1.25, FIRE, C_GRIND)
burn_zone(BURN, -2.5, 2.5, -2.8, 2.2, 1.25, 2.0, C_GRIND)
for k, y in enumerate((-1.1, 1.1)):
    RC = V(0, y, 2.6)
    cyl(f"Roller {k}", RC - X_AX * 2.4, RC + X_AX * 2.4, 0.75, 0.75, IRON, C_GRIND, n=20, hint=Z_AX)
    for j in range(10):
        a = 2 * math.pi * j / 10 + k * 0.3
        d = V(0, math.cos(a), math.sin(a))
        for xx in (-1.6, 0.0, 1.6):
            obox(f"Roller Tooth {k}-{j}-{xx}", RC + V(xx, 0, 0) + d * 0.85, (0.7, 0.22, 0.3), X_AX, d, d.cross(X_AX), BRASS, C_GRIND)
# frame + side gears
for s in (-1, 1):
    abox(f"Frame Side {s}", s * 3.0 - 0.3 if s > 0 else s * 3.0 - 0.3, s * 3.0 + 0.3, -2.4, 2.4, 1.3, 4.0, BRASS if False else WOOD2, C_FRAME) if False else \
        abox(f"Frame Side {s}", min(s * 2.7, s * 3.3), max(s * 2.7, s * 3.3), -2.4, 2.4, 0.5, 4.0, WOOD2, C_FRAME)
    for k, y in enumerate((-1.1, 1.1)):
        gear(f"Side Gear {s}{k}", V(s * 3.6, y, 2.6), X_AX, Z_AX, 0.95, 12, 0.3, BRASS if k else COPPER, C_FRAME, hub=IRON)
    gear(f"Big Gear {s}", V(s * 4.2, 1.6, 5.0), X_AX, Z_AX, 1.9, 18, 0.35, BRASS, C_FRAME, hub=IRON)
    path_tube(f"Drive Belt {s}", [V(s * 4.25, 1.6, 6.9), V(s * 4.25, 3.8, 6.0), V(s * 4.25, 4.0, 2.6), V(s * 4.25, 1.6, 3.1)], [0.1] * 4, BELT, C_FRAME, n=5)
abox("Top Beam", -4.0, 4.0, -0.4, 0.4, 4.0, 4.6, WOOD2, C_FRAME)
for k in range(5):
    dot(f"Beam Bolt {k}", V(-3.2 + k * 1.6, -0.45, 4.3), 0.12, BRASS, C_FRAME)
# ---- boiler + chimneys + gauges + pipes at the back
BO = V(0, 4.0, 0.5)
cyl("Boiler", BO + V(-3.2, 0, 1.6), BO + V(3.2, 0, 1.6), 1.6, 1.6, COPPER, C_DETAIL, n=24, hint=Z_AX)
for x in (-2.4, -0.8, 0.8, 2.4):
    torus(f"Boiler Band {x}", BO + V(x, 0, 1.6), X_AX, Z_AX, 1.62, 0.08, BRASS, C_DETAIL, n_major=24, n_minor=4)
abox("Firebox Door", -0.6, 0.6, BO.y - 1.65, BO.y - 1.4, 0.7, 1.7, IRON, C_DETAIL) if False else None
for k, x in enumerate((-2.0, 2.0)):
    cyl(f"Chimney {k}", BO + V(x, 0, 2.9), BO + V(x, 0, 7.4), 0.42, 0.36, IRON, C_DETAIL, n=12)
    cyl(f"Chimney Crown {k}", BO + V(x, 0, 7.4), BO + V(x, 0, 7.8), 0.48, 0.6, BRASS, C_DETAIL, n=12)
    for j, (dz, r) in enumerate(((8.5, 0.55), (9.3, 0.75), (10.2, 0.9))):
        rock_f(f"Chimney Steam {k}{j}", BO + V(x + 0.2 * j, 0.2 * j, dz), (r, r, r * 0.8), STEAM, C_DETAIL, rough=0.15, subd=2)
for k, x in enumerate((-1.0, 1.0)):
    G = BO + V(x, -1.62, 2.4)
    cyl(f"Gauge {k}", G, G + V(0, -0.22, 0), 0.42, 0.42, BRASS, C_DETAIL, n=18, hint=Z_AX)
    cyl(f"Gauge Face {k}", G + V(0, -0.22, 0), G + V(0, -0.25, 0), 0.34, 0.34, GAUGE, C_DETAIL, n=18, hint=Z_AX)
    beam(f"Gauge Needle {k}", G + V(0, -0.27, 0), G + V(0.2, -0.27, 0.18), 0.04, 0.03, Y_AX, IRON, C_DETAIL)
for s in (-1, 1):
    path_tube(f"Steam Pipe {s}", [BO + V(s * 3.0, -0.6, 2.6), BO + V(s * 3.4, -2.0, 3.2), V(s * 3.6, 0.0, 4.4), V(s * 3.6, 0.8, 5.0)], [0.16] * 4, COPPER, C_DETAIL, n=8)
    post_lantern(f"Lamp {s}", V(s * 5.3, -4.4, 0.5), 2.2, IRON, AMBER, BRASS, C_DETAIL, r=0.3)

finish_mine(bg=(0.03, 0.02, 0.012), tint=(1.0, 0.88, 0.7))
write_furnace_lua("ClockworkGrinderFurnace")
