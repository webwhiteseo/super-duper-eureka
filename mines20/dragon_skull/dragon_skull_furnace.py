"""Dragon Skull Forge - a colossal horned dragon skull half-buried in scorched ground; ore rolls straight into its
fiery open jaws at ground level (no ramp). Ribs, claws, embers, glowing eye sockets. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_SKULL, C_DETAIL = begin("DragonSkullFurnace", ["Ground", "Skull", "Details"], seed=131)
ASH = M("Scorched Earth", (60, 46, 40), rough=0.95, rbx="Ground", noise=((40, 30, 26), (86, 66, 56), 4.0, 0.4))
BONE = M("Dragon Bone", (222, 210, 182), rough=0.7, rbx="Limestone", noise=((196, 182, 150), (238, 230, 208), 3.0, 0.3))
HORN = M("Black Horn", (36, 30, 30), rough=0.4)
FIRE = M("Skull Fire", (255, 120, 30), rough=0.3, glow=(255, 90, 10), glow_strength=4.5, rbx="Neon", light=(16, 2.2))
EYE = M("Eye Fire", (255, 60, 20), rough=0.3, glow=(255, 40, 0), glow_strength=6.0, rbx="Neon", light=(8, 1.2))
DARK = M("Socket Dark", (14, 8, 6), rough=0.7)
ROCK = M("Ash Rock", (50, 44, 42), rough=0.9, rbx="Basalt")
BURN = M("Burn Zone", (255, 130, 40), rough=0.2, glow=(255, 100, 20), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(131)
ellip("Scorched Ground", V(0, 1.0, 0), 7.4, 7.0, 0.35, ASH, C_BASE, n=28, m=3, half=True)
for k in range(8):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(5.0, 6.6)
    if math.sin(a) < -0.6 and abs(math.cos(a)) < 0.5: continue
    rock_f(f"Ash Rock {k}", V(r * math.cos(a), 1.0 + r * math.sin(a), 0.2), (0.7, 0.6, 0.5), ROCK, C_BASE, rough=0.3)
# cranium + snout + jaws
ellip("Cranium", V(0, 2.4, 3.0), 3.6, 3.4, 3.1, BONE, C_SKULL, n=22, m=8)
ellip("Snout", V(0, -0.6, 2.4), 2.9, 2.6, 1.3, BONE, C_SKULL, n=20, m=6)
ellip("Mouth Dark", V(0, -1.8, 0.95), 2.6, 2.0, 1.0, DARK, C_SKULL, n=20, m=5)
ellip("Throat Fire", V(0, -2.7, 0.9), 2.0, 0.7, 0.8, FIRE, C_SKULL, n=18, m=5)
ellip("Lower Jaw", V(0, -2.3, 0.0), 3.0, 2.4, 0.2, BONE, C_SKULL, n=22, m=3, half=True)
for k in range(9):
    a = math.radians(205 + k * 16.25)
    p = V(2.55 * math.cos(a), -1.0 + 2.2 * math.sin(a), 0)
    cone(f"Fang {k}", V(p.x, p.y, 1.7), V(p.x * 0.95, p.y, 1.7 - (1.1 if k in (1, 7) else 0.6)), 0.2 if k in (1, 7) else 0.14, BONE, C_SKULL, n=5)
    if 1 < k < 7 and k % 2 == 0:
        cone(f"Lower Fang {k}", V(p.x, p.y - 0.2, 0.15), V(p.x, p.y - 0.2, 0.75), 0.14, BONE, C_SKULL, n=5)
burn_zone(BURN, -2.3, 2.3, -3.8, -1.3, 0.05, 1.9, C_SKULL)
for s in (-1, 1):
    E = V(s * 1.9, -0.2, 4.0)
    ellip(f"Eye Socket {s}", E, 0.9, 0.5, 0.75, DARK, C_SKULL, n=14, m=4)
    dot(f"Eye Fire {s}", E + V(0, -0.35, 0), 0.38, EYE, C_SKULL)
    dot(f"Nostril {s}", V(s * 0.6, -2.6, 3.0), 0.25, DARK, C_SKULL)
    pts = [V(s * 2.6, 2.4, 5.0), V(s * 4.0, 3.6, 6.4), V(s * 4.6, 5.6, 7.4), V(s * 4.2, 7.4, 7.6), V(s * 3.4, 8.2, 7.0)]
    path_tube(f"Great Horn {s}", pts, [0.75, 0.6, 0.45, 0.28, 0.05], HORN, C_SKULL, n=10)
    for j in range(3):
        cone(f"Brow Spike {s}{j}", V(s * (1.2 + 0.6 * j), 0.8 + 0.6 * j, 5.2 - 0.2 * j), V(s * (1.6 + 0.8 * j), 1.6 + 0.6 * j, 6.4 - 0.3 * j), 0.22, HORN, C_SKULL, n=5)
    cyl(f"Cheek Bone {s}", V(s * 2.6, -0.6, 2.2), V(s * 3.5, 1.8, 2.6), 0.4, 0.3, BONE, C_SKULL, n=8)
# ribs + spine behind, claws in front
for k in range(5):
    y = 5.2 + k * 0.9
    for s in (-1, 1):
        path_tube(f"Rib {k}{s}", [V(0, y, 1.4), V(s * 2.0, y + 0.1, 2.4 - 0.15 * k), V(s * 3.0, y + 0.2, 0.2)], [0.2, 0.18, 0.12], BONE, C_DETAIL, n=7)
path_tube("Spine", [V(0, 4.8, 1.6), V(0, 7.0, 1.3), V(0, 9.0, 0.4)], [0.35, 0.3, 0.2], BONE, C_DETAIL, n=8)
for s in (-1, 1):
    H = V(s * 4.6, -2.2, 0.2)
    for j in range(3):
        a = math.radians(-120 + j * 30) if s < 0 else math.radians(-60 - j * 30)
        path_tube(f"Claw {s}{j}", [H, H + V(0.9 * math.cos(a), 0.9 * math.sin(a), 0.6), H + V(1.4 * math.cos(a), 1.4 * math.sin(a), 0.0)], [0.25, 0.18, 0.04], HORN, C_DETAIL, n=6)
for k in range(12):
    dot(f"Ember {k}", V(rnd.uniform(-4, 4), rnd.uniform(-4, 3), rnd.uniform(1, 7)), 0.08, EYE, C_DETAIL)
finish_mine(bg=(0.03, 0.012, 0.008), tint=(1.0, 0.82, 0.7))
write_furnace_lua("DragonSkullFurnace")
