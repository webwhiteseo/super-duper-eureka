"""Haunted Crypt Furnace - a mossy stone crypt in a graveyard; ore rolls straight through its open door (no ramp) into
ghostly green fire. Gravestones, iron fence, a dead tree, jack-o'-lanterns and wisps. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_CRYPT, C_YARD = begin("HauntedCryptFurnace", ["Graveyard", "Crypt", "Yard"], seed=151)
SOIL = M("Grave Soil", (62, 54, 46), rough=0.95, rbx="Ground", noise=((44, 38, 32), (84, 74, 62), 5.0, 0.4))
GRASS = M("Dead Grass", (90, 100, 60), rough=0.9, rbx="Grass")
STONE = M("Crypt Stone", (110, 112, 116), rough=0.9, rbx="Slate", noise=((84, 86, 90), (136, 138, 142), 3.5, 0.5))
DARKST = M("Dark Stone", (64, 66, 72), rough=0.85, rbx="Slate")
MOSS = M("Moss", (70, 110, 50), rough=0.9, rbx="Grass")
GHOST = M("Ghost Fire", (110, 255, 160), rough=0.3, glow=(60, 255, 120), glow_strength=4.5, rbx="Neon", light=(16, 2.0))
WISP = M("Wisp", (200, 255, 220), rough=0.3, glow=(150, 255, 190), glow_strength=5.0, rbx="Neon", light=(6, 0.8))
IRON = M("Wrought Iron (Metal)", (36, 34, 38), rough=0.5, metal=0.8, rbx="Metal")
WOOD = M("Dead Wood (Wood)", (64, 50, 40), rough=0.9, rbx="Wood")
PUMP = M("Pumpkin", (240, 120, 20), rough=0.5)
PGLOW = M("Pumpkin Glow", (255, 200, 60), rough=0.3, glow=(255, 160, 20), glow_strength=5.0, rbx="Neon", light=(6, 0.8))
BURN = M("Burn Zone", (110, 255, 160), rough=0.2, glow=(60, 255, 120), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(151)
ellip("Graveyard Mound", V(0, 0.8, 0), 7.4, 7.0, 0.3, SOIL, C_BASE, n=28, m=3, half=True)
for k in range(10):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(3.5, 6.5)
    ellip(f"Grass Patch {k}", V(r * math.cos(a), 0.8 + r * math.sin(a), 0.2), rnd.uniform(0.6, 1.1), rnd.uniform(0.5, 0.9), 0.1, GRASS, C_BASE, n=10, m=2, half=True)
# crypt with an open door at ground level
abox("Crypt Back", -3.4, 3.4, 0.4, 4.4, 0.0, 4.6, STONE, C_CRYPT)
for s in (-1, 1):
    abox(f"Crypt Wall {s}", min(s * 2.4, s * 3.4), max(s * 2.4, s * 3.4), -1.8, 0.4, 0.0, 4.6, STONE, C_CRYPT)
    abox(f"Pillar {s}", min(s * 2.3, s * 3.0), max(s * 2.3, s * 3.0), -2.4, -1.8, 0.0, 4.4, DARKST, C_CRYPT)
    abox(f"Pillar Cap {s}", min(s * 2.2, s * 3.1), max(s * 2.2, s * 3.1), -2.5, -1.7, 4.4, 4.7, STONE, C_CRYPT)
abox("Door Lintel", -2.4, 2.4, -1.9, 0.4, 3.0, 4.6, STONE, C_CRYPT)
abox("Crypt Floor", -2.4, 2.4, -1.8, 0.4, 0.0, 0.05, DARKST, C_CRYPT)
abox("Ghost Fire Wall", -2.4, 2.4, 0.3, 0.45, 0.05, 3.0, GHOST, C_CRYPT)
burn_zone(BURN, -2.2, 2.2, -2.6, 0.2, 0.05, 2.8, C_CRYPT)
for k in range(4):
    cone(f"Ghost Flame {k}", V(-1.6 + k * 1.05, 0.0, 0.05), V(-1.6 + k * 1.05, -0.1, 1.2 + 0.4 * (k % 2)), 0.4, GHOST, C_CRYPT, n=6)
hexa("Crypt Roof", [V(-3.8, -2.6, 4.6), V(3.8, -2.6, 4.6), V(3.8, 4.8, 4.6), V(-3.8, 4.8, 4.6),
                    V(-0.3, -2.6, 6.6), V(0.3, -2.6, 6.6), V(0.3, 4.8, 6.6), V(-0.3, 4.8, 6.6)], DARKST, C_CRYPT)
abox("Cross Post", -0.15, 0.15, -2.2, -1.9, 6.4, 8.4, STONE, C_CRYPT)
abox("Cross Bar", -0.7, 0.7, -2.2, -1.9, 7.5, 7.8, STONE, C_CRYPT)
abox("Name Plate", -1.4, 1.4, -1.95, -1.9, 3.3, 3.9, DARKST, C_CRYPT)
dot("Skull Emblem", V(0, -2.0, 4.2), 0.3, STONE, C_CRYPT)
for k in range(6):
    ellip(f"Roof Moss {k}", V(rnd.uniform(-3, 3), rnd.uniform(-2, 4), 5.4), 0.7, 0.6, 0.15, MOSS, C_CRYPT, n=8, m=2, half=True)
# gravestones
for k, (x, y, rot) in enumerate(((-5.0, 1.0, 0.2), (-4.6, 3.8, -0.1), (4.8, 1.4, -0.2), (4.4, 4.2, 0.15), (-5.4, -2.0, 0.3))):
    d = V(math.sin(rot), -math.cos(rot), 0);s_ = V(math.cos(rot), math.sin(rot), 0)
    G = V(x, y, 0.2)
    obox(f"Gravestone {k}", G + V(0, 0, 0.7), (1.0, 0.3, 1.5), s_, d, Z_AX, STONE, C_YARD)
    cyl(f"Grave Top {k}", G + V(0, 0, 1.45) - d * 0.15, G + V(0, 0, 1.45) + d * 0.15, 0.5, 0.5, STONE, C_YARD, n=14, hint=Z_AX)
    obox(f"Grave Mound {k}", G + V(0, 0, 0.05) - d * 1.0, (0.9, 1.6, 0.3), s_, d, Z_AX, SOIL, C_YARD)
# iron fence along the back
for k in range(15):
    x = -6.0 + k * 0.85
    cyl(f"Fence Bar {k}", V(x, 6.0, 0.1), V(x, 6.0, 2.0), 0.05, 0.05, IRON, C_YARD, n=5)
    cone(f"Fence Spike {k}", V(x, 6.0, 2.0), V(x, 6.0, 2.35), 0.1, IRON, C_YARD, n=4)
for z in (0.6, 1.7):
    cyl(f"Fence Rail {z}", V(-6.0, 6.0, z), V(5.9, 6.0, z), 0.05, 0.05, IRON, C_YARD, n=5, hint=Z_AX)
# dead tree + pumpkins + wisps
T = V(5.2, -2.6, 0.2)
path_tube("Dead Tree", [T, T + V(0.2, 0, 2.0), T + V(-0.2, 0.1, 3.8), T + V(0.3, 0, 5.0)], [0.4, 0.3, 0.2, 0.08], WOOD, C_YARD, n=8)
for k, (d, h) in enumerate(((V(-1, -0.2, 0.5), 2.6), (V(1, 0.3, 0.6), 3.4), (V(-0.6, 0.6, 0.8), 4.2))):
    b = T + V(0, 0, h)
    path_tube(f"Branch {k}", [b, b + d * 0.8, b + d * 1.6 + V(0, 0, 0.3)], [0.15, 0.09, 0.03], WOOD, C_YARD, n=6)
for k, (x, y) in enumerate(((-3.4, -3.6), (3.4, -3.8), (-1.0, -5.2))):
    P = V(x, y, 0.5)
    ellip(f"Pumpkin {k}", P, 0.6, 0.55, 0.45, PUMP, C_YARD, n=12, m=4)
    for s in (-1, 1):
        cone(f"Pumpkin Eye {k}{s}", P + V(s * 0.2, -0.5, 0.12), P + V(s * 0.2, -0.56, 0.3), 0.1, PGLOW, C_YARD, n=3)
    abox(f"Pumpkin Mouth {k}", P.x - 0.25, P.x + 0.25, P.y - 0.58, P.y - 0.52, P.z - 0.15, P.z - 0.05, PGLOW, C_YARD)
    cyl(f"Pumpkin Stem {k}", P + V(0, 0, 0.4), P + V(0.05, 0, 0.65), 0.07, 0.05, WOOD, C_YARD, n=5)
for k in range(6):
    dot(f"Wisp {k}", V(rnd.uniform(-5, 5), rnd.uniform(-4, 5), rnd.uniform(2.5, 6.5)), 0.18, WISP, C_YARD)
finish_mine(bg=(0.012, 0.02, 0.02), tint=(0.75, 0.95, 0.85))
write_furnace_lua("HauntedCryptFurnace")
