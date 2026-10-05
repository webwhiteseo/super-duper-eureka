"""Clockwork Owl Mine - a brass mechanical owl with glowing lens eyes, open chest gears and plated wings
perches on a clock tower; ore pops out of the cuckoo door. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_TOWER, C_OWL, C_WINGS, C_DETAIL = begin("ClockworkOwlMine", ["Base", "Clock Tower", "Owl", "Wings", "Details"], seed=44)
WALNUT = M("Walnut (Wood)", (74, 46, 30), rough=0.6, rbx="WoodPlanks", noise=((56, 34, 22), (96, 62, 40), 5.0, 0.15))
TRIM = M("Amber Trim (Metal)", (255, 176, 60), rough=0.3, metal=0.6, glow=(255, 150, 40), glow_strength=1.0, rbx="Neon")
CREAM = M("Clock Marble (Marble)", (232, 222, 196), rough=0.3, marble=((224, 212, 184), (210, 160, 70)))
BRASS = M("Brass (Metal)", (212, 160, 72), rough=0.28, metal=1.0)
COPPER = M("Copper (Metal)", (198, 112, 64), rough=0.3, metal=1.0, plate=12.0)
IRON = M("Dark Iron (Metal)", (46, 44, 48), rough=0.4, metal=0.9)
FACE = M("Clock Face", (244, 238, 222), rough=0.5)
INK = M("Ink Black", (18, 16, 16), rough=0.5)
AMBER = M("Amber Lens", (255, 190, 80), rough=0.1, glow=(255, 160, 40), glow_strength=7.0, rbx="Neon", light=(10, 1.6))
CORE = M("Mainspring Core", (255, 220, 140), rough=0.3, glow=(255, 180, 60), glow_strength=10, rbx="Neon", light=(12, 1.8))
GLASS = M("Glass", (200, 230, 255), rough=0.05, glow=(160, 200, 255), glow_strength=0.4, rbx="Glass", alpha=0.5)
ORE = M("Gear Ore", (255, 210, 120), rough=0.2, glow=(255, 180, 70), glow_strength=2.0, rbx="Neon")

top = base_plinth(10.5, 10.5, WALNUT, TRIM, CREAM, C_BASE, c=1.0)

def gear(name, C, axis, up, r, teeth, th, mat, coll, hub=None):
    tube(name, C, axis, up, r, r * 0.45, th, mat, coll, n=max(24, teeth * 2))
    a_ = axis.normalized();u = up.normalized();v = a_.cross(u).normalized()
    for k in range(teeth):
        ang = 2 * math.pi * k / teeth
        rr = math.cos(ang) * v + math.sin(ang) * u;tt = -math.sin(ang) * v + math.cos(ang) * u
        obox(f"{name} Tooth {k + 1}", C + rr * (r + 0.12), (0.22 * r / 1.0 + 0.12, 0.28, th), tt, rr, a_, mat, coll) if False else \
            obox(f"{name} Tooth {k + 1}", C + rr * (r + 0.12), (th, 0.26, 0.3), a_, rr, tt, mat, coll)
    for k in range(4):
        ang = math.pi / 4 + k * math.pi / 2
        rr = math.cos(ang) * v + math.sin(ang) * u
        beam(f"{name} Spoke {k + 1}", C + rr * r * 0.2, C + rr * r * 0.5, 0.12, th * 0.8, a_, mat, coll)
    if hub:
        cyl(f"{name} Hub", C - a_ * th * 0.7, C + a_ * th * 0.7, r * 0.2, r * 0.2, hub, coll, n=12, hint=u)

# ---- clock tower with face, pendulum window and cuckoo door
T = V(0, 1.0, top)
lathe("Tower", T, [(2.6, 0), (2.6, 0.6), (2.2, 0.9), (2.1, 6.4), (2.4, 6.7), (2.4, 7.1), (1.9, 7.3)], WALNUT, C_TOWER, n=8, smooth=False)
for k, z in enumerate((0.75, 6.85)):
    torus(f"Tower Band {k + 1}", T + V(0, 0, z), V(0, 0, 1), V(0, 1, 0), 2.35 if k else 2.45, 0.12, BRASS, C_TOWER, n_major=8, n_minor=4)
F = T + V(0, -2.12, 4.6)                                    # clock face
cyl("Clock Bezel", F, F + V(0, -0.25, 0), 1.45, 1.45, BRASS, C_TOWER, n=32, hint=V(0, 0, 1))
cyl("Clock Face", F + V(0, -0.25, 0), F + V(0, -0.3, 0), 1.25, 1.25, FACE, C_TOWER, n=32, hint=V(0, 0, 1))
for k in range(12):
    a = 2 * math.pi * k / 12
    p = F + V(1.05 * math.cos(a), -0.32, 1.05 * math.sin(a))
    abox(f"Hour Mark {k + 1}", p.x - 0.05, p.x + 0.05, p.y - 0.03, p.y, p.z - (0.16 if k % 3 == 0 else 0.09), p.z + (0.16 if k % 3 == 0 else 0.09), INK, C_TOWER)
beam("Hour Hand", F + V(0, -0.36, 0), F + V(0.45, -0.36, 0.45), 0.08, 0.04, V(0, -1, 0), INK, C_TOWER)
beam("Minute Hand", F + V(0, -0.38, 0), F + V(-0.15, -0.38, 0.95), 0.06, 0.04, V(0, -1, 0), INK, C_TOWER)
dot("Clock Pin", F + V(0, -0.4, 0), 0.08, BRASS, C_TOWER)
D = T + V(0, -2.05, 2.1)                                    # cuckoo door (open) and ore chute
abox("Cuckoo Hole", D.x - 0.7, D.x + 0.7, D.y - 0.05, D.y + 0.3, D.z - 0.8, D.z + 0.8, INK, C_TOWER)
hexa("Door Roof", [V(D.x - 1.0, D.y - 0.6, D.z + 0.85), V(D.x + 1.0, D.y - 0.6, D.z + 0.85), V(D.x + 1.0, D.y + 0.2, D.z + 0.85), V(D.x - 1.0, D.y + 0.2, D.z + 0.85),
                   V(D.x - 0.05, D.y - 0.6, D.z + 1.5), V(D.x + 0.05, D.y - 0.6, D.z + 1.5), V(D.x + 0.05, D.y + 0.2, D.z + 1.5), V(D.x - 0.05, D.y + 0.2, D.z + 1.5)], COPPER, C_TOWER)
for side in (1, -1):
    obox(f"Cuckoo Door {side}", D + V(side * 1.05, -0.45, 0), (0.08, 0.7, 1.55), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), WALNUT, C_TOWER)
hexa("Ore Chute", [V(D.x - 0.6, D.y - 0.1, D.z - 0.75), V(D.x + 0.6, D.y - 0.1, D.z - 0.75), V(D.x + 0.6, D.y - 1.6, D.z - 1.3), V(D.x - 0.6, D.y - 1.6, D.z - 1.3),
                   V(D.x - 0.6, D.y - 0.1, D.z - 0.6), V(D.x + 0.6, D.y - 0.1, D.z - 0.6), V(D.x + 0.6, D.y - 1.6, D.z - 1.15), V(D.x - 0.6, D.y - 1.6, D.z - 1.15)], BRASS, C_TOWER)
ore_cube(V(D.x, D.y - 2.3, D.z - 1.0), ORE, C_TOWER)
# perch on top of the tower
P0 = T + V(0, 0, 7.3)
cyl("Perch Post", P0, P0 + V(0, 0, 0.6), 0.5, 0.4, BRASS, C_TOWER, n=12)
cyl("Perch Bar", P0 + V(-1.6, 0, 0.75), P0 + V(1.6, 0, 0.75), 0.24, 0.24, IRON, C_TOWER, n=10, hint=V(0, 0, 1))

# ---- the owl
O = P0 + V(0, 0, 3.1)
lathe("Owl Body", O + V(0, 0, -2.2), [(0.6, 0), (1.5, 0.4), (1.95, 1.4), (2.0, 2.4), (1.7, 3.3), (1.2, 3.8)], COPPER, C_OWL, n=20)
for k in range(5):                                          # brass feather-plate rows on the belly
    z = -1.6 + k * 0.62
    for j in range(5):
        a = math.radians(-90 + (j - 2) * 22 + (11 if k % 2 else 0))
        r = 1.85 + 0.15 * math.sin(k)
        c = O + V(r * math.cos(a), r * math.sin(a) + 0.05, z)
        blade(f"Belly Plate {k + 1}-{j + 1}", [c + V(-0.28 * math.sin(a), 0.28 * math.cos(a), 0.25), c + V(0.28 * math.sin(a), -0.28 * math.cos(a), 0.25), c + V(0, 0, -0.35) + V(math.cos(a), math.sin(a), 0) * 0.12], 0.06, BRASS, C_OWL)
# open chest window with spinning gears and a glowing mainspring
CW = O + V(0, -1.75, 0.6)
torus("Chest Window Rim", CW, V(0, -1, 0), V(0, 0, 1), 0.85, 0.1, BRASS, C_OWL, n_major=24, n_minor=6)
dot("Mainspring Core", CW + V(0, 0.35, 0), 0.5, CORE, C_OWL)
gear("Chest Gear A", CW + V(0.35, -0.05, 0.2), V(0, -1, 0), V(0, 0, 1), 0.38, 10, 0.12, BRASS, C_OWL, hub=IRON)
gear("Chest Gear B", CW + V(-0.32, -0.1, -0.25), V(0, -1, 0), V(0, 0, 1), 0.3, 8, 0.12, IRON, C_OWL)
cyl("Chest Glass", CW + V(0, -0.15, 0), CW + V(0, -0.18, 0), 0.8, 0.8, GLASS, C_OWL, n=20, hint=V(0, 0, 1))
H = O + V(0, -0.15, 2.4)
lathe("Owl Head", H + V(0, 0, -0.9), [(1.25, 0), (1.75, 0.5), (1.85, 1.2), (1.55, 1.85), (0.9, 2.15), (0.0, 2.25)], COPPER, C_OWL, n=20)
for side, lab in ((1, "L"), (-1, "R")):
    E = H + V(side * 0.78, -1.78, 0.42)
    torus(f"Eye Rim {lab}", E, V(side * 0.25, -1, 0).normalized(), V(0, 0, 1), 0.74, 0.15, BRASS, C_OWL, n_major=24, n_minor=6)
    torus(f"Eye Inner Rim {lab}", E + V(0, -0.05, 0), V(side * 0.25, -1, 0).normalized(), V(0, 0, 1), 0.4, 0.06, IRON, C_OWL, n_major=20, n_minor=4)
    cyl(f"Eye Lens {lab}", E + V(0, 0.3, 0), E + V(0, -0.06, 0), 0.66, 0.66, AMBER, C_OWL, n=20, hint=V(0, 0, 1))
    dot(f"Pupil {lab}", E + V(0, -0.1, 0), 0.18, INK, C_OWL)
    cone(f"Ear Tuft {lab}", H + V(side * 1.1, -0.2, 1.4), H + V(side * 1.75, 0.1, 2.9), 0.42, BRASS, C_OWL, n=6)
    gear(f"Ear Gear {lab}", H + V(side * 1.8, 0.1, 0.6), V(side, 0, 0), V(0, 0, 1), 0.42, 9, 0.14, BRASS, C_OWL, hub=IRON)
cone("Beak", H + V(0, -1.75, -0.2), H + V(0, -2.3, -0.85), 0.34, IRON, C_OWL, n=6)
for side in (1, -1):                                        # talons on the perch
    for j in range(3):
        a = math.radians(-90 + (j - 1) * 30)
        base = P0 + V(side * 0.8 + 0.3 * math.cos(a) * 0.5, 0, 1.05)
        path_tube(f"Talon {side}-{j + 1}", [base, base + V(0.2 * math.cos(a), 0.45 * math.sin(a), -0.05), base + V(0.25 * math.cos(a), 0.5 * math.sin(a), -0.45)], [0.12, 0.1, 0.03], IRON, C_OWL, n=6)
# wind-up key on the back
K = O + V(0, 1.9, 0.6)
cyl("Key Shaft", K, K + V(0, 1.4, 0), 0.16, 0.16, BRASS, C_DETAIL, n=10, hint=V(0, 0, 1))
for side in (1, -1):
    torus(f"Key Bow {side}", K + V(side * 0.6, 1.55, 0), V(0, 1, 0), V(0, 0, 1), 0.5, 0.14, BRASS, C_DETAIL, n_major=18, n_minor=6)

# ---- spread mechanical wings: brass bones with copper/brass feather plates
for side, lab in ((1, "L"), (-1, "R")):
    sh = O + V(side * 1.7, 0.3, 1.0)
    elbow = sh + V(side * 2.4, 0.9, 1.0)
    tip = elbow + V(side * 2.6, 1.0, -0.8)
    cyl(f"Wing Bone {lab} 1", sh, elbow, 0.2, 0.16, BRASS, C_WINGS, n=8)
    cyl(f"Wing Bone {lab} 2", elbow, tip, 0.16, 0.08, BRASS, C_WINGS, n=8)
    gear(f"Wing Gear {lab}", sh, V(side, 0.2, 0).normalized(), V(0, 0, 1), 0.45, 10, 0.16, IRON, C_WINGS, hub=BRASS)
    gear(f"Elbow Gear {lab}", elbow, V(side, 0.3, 0.2).normalized(), V(0, 0, 1), 0.32, 8, 0.14, BRASS, C_WINGS)
    for k in range(9):
        t = k / 8
        root = sh + (elbow - sh) * min(1, t * 2) + (tip - elbow) * max(0, t * 2 - 1)
        L = 1.6 + 1.6 * math.sin(math.pi * t) + 0.6 * t
        d = V(side * 0.35 * t, 0.25, -1).normalized()
        w = 0.32
        u = V(side, 0.4, 0).normalized()
        blade(f"Feather {lab} {k + 1}", [root - u * w, root + u * w, root + d * L + u * w * 0.4, root + d * (L + 0.35), root + d * L - u * w * 0.4], 0.06, COPPER if k % 2 else BRASS, C_WINGS)

# ---- details: big gear on the base, oil can, small gears
gear("Floor Gear", V(3.6, -3.3, top + 0.12), V(0, 0, 1), V(0, 1, 0), 1.05, 14, 0.2, BRASS, C_DETAIL, hub=IRON)
gear("Floor Gear Small", V(4.1, -1.6, top + 0.12), V(0, 0, 1), V(0, 1, 0), 0.55, 9, 0.2, COPPER, C_DETAIL, hub=IRON)
OC = V(-3.7, -3.4, top)
lathe("Oil Can", OC, [(0.6, 0), (0.62, 0.7), (0.3, 1.0), (0.12, 1.2)], COPPER, C_DETAIL, n=14)
cyl("Oil Spout", OC + V(0, 0, 1.15), OC + V(0.6, -0.5, 1.9), 0.06, 0.04, BRASS, C_DETAIL, n=6)
torus("Oil Handle", OC + V(-0.55, 0, 0.6), V(0, 1, 0), V(0, 0, 1), 0.35, 0.06, BRASS, C_DETAIL, n_major=12, n_minor=4)
for k, (x, y) in enumerate(((-4.2, 3.8), (3.9, 3.9))):
    post_lantern(f"Lamp {k + 1}", V(x, y, top), 2.4, IRON, AMBER, BRASS, C_DETAIL, r=0.35)

finish_mine(bg=(0.02, 0.014, 0.01), tint=(1.0, 0.85, 0.7))
