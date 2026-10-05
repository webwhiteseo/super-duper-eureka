"""Sun Pyramid Mine - a stepped sandstone pyramid with a gold capstone beneath a floating sun disc;
golden ore rolls out of the temple door. Obelisks, sphinx, scarab and fire braziers.
Built with mine_kit (same pipeline as the other Ore Factory mines)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_PYR, C_SUN, C_STATUES, C_DETAIL = begin("SunPyramidMine", ["Base", "Pyramid", "Sun", "Statues", "Details"], seed=21)
DARK = M("Dark Stone", (44, 32, 22), rough=0.6)
GOLD = M("Gold (Metal)", (236, 186, 70), rough=0.25, metal=1.0, glow=(120, 80, 10), glow_strength=0.4)
TRIM = M("Gold Trim (Metal)", (240, 190, 70), rough=0.25, metal=1.0, glow=(255, 170, 40), glow_strength=1.0, rbx="Neon")
SANDM = M("Sand Marble (Marble)", (200, 170, 120), rough=0.4, marble=((190, 160, 112), (255, 230, 170)))
SAND = M("Sandstone", (214, 180, 124), rough=0.85, rbx="Sandstone", noise=((186, 150, 98), (232, 204, 150), 3.0, 0.35))
SAND2 = M("Pale Sandstone", (232, 206, 156), rough=0.85, rbx="Sandstone", noise=((210, 184, 134), (246, 226, 182), 3.0, 0.3))
LAPIS = M("Lapis", (30, 62, 170), rough=0.3, noise=((20, 44, 130), (60, 100, 210), 6.0, 0.15))
TURQ = M("Turquoise Glow", (80, 230, 210), rough=0.3, glow=(40, 220, 200), glow_strength=3.0, rbx="Neon", light=(7, 0.8))
SUN = M("Sun Core", (255, 236, 170), rough=0.3, glow=(255, 190, 70), glow_strength=14, rbx="Neon", light=(24, 2.6))
FLAME = M("Brazier Flame", (255, 170, 60), rough=0.4, glow=(255, 120, 30), glow_strength=12, rbx="Neon", light=(10, 1.6))
BLACK = M("Black", (16, 12, 10), rough=0.5)
ORE = M("Sunstone Ore", (255, 220, 120), rough=0.15, glow=(255, 190, 70), glow_strength=2.0, rbx="Neon")

top = base_plinth(11.0, 11.0, DARK, TRIM, SANDM, C_BASE, c=0.8)

# ---- stepped pyramid with a gold capstone
P = V(0, 1.0, top)
z = 0
for k, (w, h) in enumerate(((7.6, 1.5), (6.3, 1.4), (5.0, 1.35), (3.8, 1.3), (2.6, 1.2))):
    abox(f"Tier {k + 1}", P.x - w / 2, P.x + w / 2, P.y - w / 2, P.y + w / 2, top + z, top + z + h, SAND if k % 2 == 0 else SAND2, C_PYR)
    abox(f"Tier Lip {k + 1}", P.x - w / 2 - 0.12, P.x + w / 2 + 0.12, P.y - w / 2 - 0.12, P.y + w / 2 + 0.12, top + z + h - 0.18, top + z + h + 0.03, SAND2 if k % 2 == 0 else SAND, C_PYR)
    for j in range(int(w // 1.4)):                          # hieroglyph tiles on the front face
        x = P.x - w / 2 + 0.7 + j * 1.4
        if abs(x) < 1.2 and k < 2:
            continue
        abox(f"Glyph {k + 1}-{j + 1}", x - 0.28, x + 0.28, P.y - w / 2 - 0.06, P.y - w / 2, top + z + 0.35, top + z + h - 0.45, LAPIS if (j + k) % 2 else TURQ, C_PYR)
    z += h
cz = top + z
hexa("Capstone", [V(-1.3, P.y - 1.3, cz), V(1.3, P.y - 1.3, cz), V(1.3, P.y + 1.3, cz), V(-1.3, P.y + 1.3, cz),
                  V(-0.02, P.y - 0.02, cz + 2.2), V(0.02, P.y - 0.02, cz + 2.2), V(0.02, P.y + 0.02, cz + 2.2), V(-0.02, P.y + 0.02, cz + 2.2)], GOLD, C_PYR)
# temple door with gold frame, eye emblem above
fy = P.y - 3.8
abox("Door Dark", -0.95, 0.95, fy - 0.08, fy + 0.6, top, top + 2.6, BLACK, C_PYR)
abox("Door Frame L", -1.35, -0.95, fy - 0.2, fy + 0.2, top, top + 2.9, GOLD, C_PYR)
abox("Door Frame R", 0.95, 1.35, fy - 0.2, fy + 0.2, top, top + 2.9, GOLD, C_PYR)
abox("Door Lintel", -1.6, 1.6, fy - 0.25, fy + 0.2, top + 2.7, top + 3.2, GOLD, C_PYR)
E = V(0, P.y - 3.2 - 0.14, top + 4.3)                      # eye of the sun on tier 3
torus("Eye Outline", E, V(0, -1, 0), V(0, 0, 1), 0.62, 0.08, GOLD, C_PYR, n_major=24, n_minor=4)
dot("Eye Pupil", E + V(0, -0.05, 0), 0.3, TURQ, C_PYR)
beam("Eye Tail", E + V(0.55, -0.05, -0.15), E + V(1.15, -0.05, -0.7), 0.1, 0.1, V(0, -1, 0), GOLD, C_PYR)
beam("Eye Brow", E + V(-0.7, -0.05, 0.55), E + V(0.75, -0.05, 0.55), 0.1, 0.1, V(0, -1, 0), GOLD, C_PYR)
# golden ramp where the ore rolls out
hexa("Ore Ramp", [V(-0.9, fy - 0.1, top + 0.02), V(0.9, fy - 0.1, top + 0.02), V(0.9, fy - 2.4, top + 0.02), V(-0.9, fy - 2.4, top + 0.02),
                  V(-0.9, fy - 0.1, top + 0.35), V(0.9, fy - 0.1, top + 0.35), V(0.9, fy - 2.4, top + 0.08), V(-0.9, fy - 2.4, top + 0.08)], GOLD, C_PYR)
ore_cube(V(0, fy - 1.7, top + 0.75), ORE, C_PYR)

# ---- floating sun disc with rays
S = V(0, P.y, cz + 5.3)
sphere("Sun", S, 1.3, SUN, C_SUN)
torus("Sun Ring", S, V(0, -1, 0.1), V(0, 0, 1), 1.75, 0.16, GOLD, C_SUN, n_major=40, n_minor=6)
for k in range(12):
    a = 2 * math.pi * k / 12
    r_ = V(math.cos(a), 0, math.sin(a))
    l = 1.2 if k % 2 else 0.8
    blade(f"Sun Ray {k + 1}", [S + r_ * 1.9 + V(-math.sin(a), 0, math.cos(a)) * 0.22, S + r_ * (1.9 + l), S + r_ * 1.9 - V(-math.sin(a), 0, math.cos(a)) * 0.22], 0.12, GOLD, C_SUN)
for k in range(2):                                          # cobra wings either side of the sun
    side = 1 if k == 0 else -1
    pts = [S + V(side * 1.9, 0.05, -0.3), S + V(side * 3.2, 0.05, 0.4), S + V(side * 4.4, 0.05, 0.2), S + V(side * 3.6, 0.05, -0.5), S + V(side * 2.2, 0.05, -0.8)]
    blade(f"Sun Wing {k + 1}", pts, 0.12, LAPIS, C_SUN)
    for j in range(3):
        beam(f"Wing Feather {k + 1}-{j + 1}", S + V(side * (2.2 + j * 0.6), -0.05, -0.2), S + V(side * (2.6 + j * 0.7), -0.05, 0.35), 0.06, 0.06, V(0, -1, 0), GOLD, C_SUN)
cyl("Sun Beam", cz * V(0, 0, 1) + V(0, P.y, 2.2), S - V(0, 0, 1.3), 0.08, 0.08, SUN, C_SUN, n=6)

# ---- obelisks at the front corners
for side, lab in ((1, "L"), (-1, "R")):
    O = V(side * 4.2, -3.9, top)
    hexa(f"Obelisk {lab}", [O + V(-0.5, -0.5, 0), O + V(0.5, -0.5, 0), O + V(0.5, 0.5, 0), O + V(-0.5, 0.5, 0),
                            O + V(-0.32, -0.32, 6.2), O + V(0.32, -0.32, 6.2), O + V(0.32, 0.32, 6.2), O + V(-0.32, 0.32, 6.2)], SAND2, C_STATUES)
    hexa(f"Obelisk Tip {lab}", [O + V(-0.34, -0.34, 6.2), O + V(0.34, -0.34, 6.2), O + V(0.34, 0.34, 6.2), O + V(-0.34, 0.34, 6.2),
                                O + V(-0.01, -0.01, 7.0), O + V(0.01, -0.01, 7.0), O + V(0.01, 0.01, 7.0), O + V(-0.01, 0.01, 7.0)], GOLD, C_STATUES)
    abox(f"Obelisk Plinth {lab}", O.x - 0.75, O.x + 0.75, O.y - 0.75, O.y + 0.75, top, top + 0.4, DARK, C_STATUES)
    for j in range(4):
        abox(f"Obelisk Glyph {lab} {j + 1}", O.x - 0.16, O.x + 0.16, O.y - 0.49 + j * 0.0 - 0.03, O.y - 0.45, top + 1.0 + j * 1.2, top + 1.7 + j * 1.2, TURQ if j % 2 else LAPIS, C_STATUES)

# ---- sphinx on the right, scarab on the left
SX = V(-3.9, 0.9, top)
rock_f("Sphinx Body", SX + V(0, 0.6, 0.75), (0.85, 1.7, 0.75), SAND, C_STATUES, rough=0.08, subd=2)
for side in (1, -1):
    abox(f"Sphinx Paw {side}", SX.x + side * 0.35 - 0.22, SX.x + side * 0.35 + 0.22, SX.y - 1.6, SX.y - 0.4, top, top + 0.4, SAND, C_STATUES)
rock_f("Sphinx Chest", SX + V(0, -0.6, 1.2), (0.75, 0.6, 0.85), SAND, C_STATUES, rough=0.06, subd=2)
rock_f("Sphinx Head", SX + V(0, -0.75, 2.35), (0.48, 0.5, 0.55), SAND2, C_STATUES, rough=0.05, subd=2)
for k in range(5):                                          # striped nemes headdress
    abox(f"Nemes Stripe {k + 1}", SX.x - 0.75, SX.x + 0.75, SX.y - 0.55 + k * 0.12 - 0.05, SX.y - 0.55 + k * 0.12 + 0.05, top + 1.6, top + 2.9 - k * 0.08, GOLD if k % 2 else LAPIS, C_STATUES)
dot("Sphinx Eye L", SX + V(0.18, -1.22, 2.45), 0.07, TURQ, C_STATUES)
dot("Sphinx Eye R", SX + V(-0.18, -1.22, 2.45), 0.07, TURQ, C_STATUES)
SC = V(4.0, 1.4, top + 0.55)
rock_f("Scarab Shell", SC, (0.9, 1.2, 0.55), LAPIS, C_STATUES, rough=0.03, subd=2)
beam("Scarab Split", SC + V(0, -1.05, 0.5), SC + V(0, 1.05, 0.5), 0.06, 0.06, V(1, 0, 0), GOLD, C_STATUES)
rock_f("Scarab Head", SC + V(0, -1.3, -0.1), (0.5, 0.35, 0.3), GOLD, C_STATUES, rough=0.03, subd=1)
for side in (1, -1):
    for j in range(3):
        cyl(f"Scarab Leg {side}-{j + 1}", SC + V(side * 0.7, -0.6 + j * 0.6, -0.2), SC + V(side * 1.3, -0.8 + j * 0.8, -0.55), 0.07, 0.05, GOLD, C_STATUES, n=5)
dot("Scarab Gem", SC + V(0, -1.55, 0.05), 0.12, TURQ, C_STATUES)

# ---- fire braziers either side of the door
for side in (1, -1):
    Bz = V(side * 2.0, fy - 1.0, top)
    cyl(f"Brazier Stand {side}", Bz, Bz + V(0, 0, 1.5), 0.14, 0.14, GOLD, C_DETAIL, n=8)
    lathe(f"Brazier Bowl {side}", Bz + V(0, 0, 1.5), [(0.15, 0), (0.55, 0.25), (0.62, 0.5), (0.55, 0.52)], GOLD, C_DETAIL, n=12)
    lathe(f"Brazier Fire {side}", Bz + V(0, 0, 1.95), [(0.5, 0), (0.42, 0.3), (0.25, 0.65), (0.0, 1.0)], FLAME, C_DETAIL, n=10)
# canopic jars at the back
for k, x in enumerate((-2.2, -1.0, 1.0, 2.2)):
    J = V(x, 5.0, top)
    lathe(f"Canopic Jar {k + 1}", J, [(0.25, 0), (0.38, 0.25), (0.4, 0.75), (0.28, 0.95)], SAND2, C_DETAIL, n=12)
    rock_f(f"Canopic Lid {k + 1}", J + V(0, 0, 1.12), (0.26, 0.26, 0.24), GOLD if k % 2 else LAPIS, C_DETAIL, rough=0.03, subd=1)

finish_mine(bg=(0.03, 0.02, 0.008), tint=(1.0, 0.85, 0.65))
