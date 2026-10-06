"""Gold Vault Furnace - a bank vault with its huge round door swung open; ore rolls straight into the glowing vault
(no ramp) past piles of gold bars and coins. Marble floor, velvet rope posts, money bags. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_VAULT, C_DOOR, C_LOOT = begin("GoldVaultFurnace", ["Marble Floor", "Vault", "Door", "Loot"], seed=181)
MARB = M("Marble Floor (Marble)", (232, 228, 220), rough=0.25, marble=((222, 218, 210), (150, 140, 130)))
MARB2 = M("Black Marble (Marble)", (30, 30, 36), rough=0.25, marble=((24, 24, 30), (200, 180, 120)))
STEEL = M("Vault Steel (Metal)", (150, 156, 166), rough=0.25, metal=0.95, rbx="Metal")
DARKS = M("Dark Steel (Metal)", (70, 74, 82), rough=0.3, metal=0.9, rbx="DiamondPlate")
GOLD = M("Gold (Metal)", (245, 196, 70), rough=0.2, metal=1.0, rbx="Metal")
GLOW = M("Vault Glow", (255, 220, 120), rough=0.3, glow=(255, 190, 60), glow_strength=4.0, rbx="Neon", light=(16, 2.2))
VELVET = M("Velvet (Fabric)", (170, 20, 40), rough=0.8, rbx="Fabric")
BAG = M("Money Bag (Fabric)", (190, 160, 110), rough=0.8, rbx="Fabric")
GREEN = M("Cash Green", (90, 170, 90), rough=0.6)
BURN = M("Burn Zone", (255, 220, 120), rough=0.2, glow=(255, 190, 60), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(181)
for i in range(6):
    for j in range(6):
        x0, y0 = -6.0 + i * 2.0, -5.6 + j * 2.0
        abox(f"Floor Tile {i}{j}", x0 + 0.02, x0 + 1.98, y0 + 0.02, y0 + 1.98, 0, 0.2, MARB if (i + j) % 2 else MARB2, C_BASE)
abox("Floor Border", -6.1, 6.1, -5.7, -5.6, 0, 0.22, GOLD, C_BASE)
# vault block with a round opening down to the floor
VC = V(0, -2.2, 2.4);VR = 2.6
abox("Vault Block Back", -4.6, 4.6, -1.6, 4.4, 0.0, 6.6, DARKS, C_VAULT)
tube("Vault Frame", VC, Y_AX, Z_AX, VR + 0.7, VR, 1.2, STEEL, C_VAULT, n=40)
for s in (-1, 1):
    abox(f"Vault Wall {s}", min(s * (VR + 0.4), s * 4.6), max(s * (VR + 0.4), s * 4.6), -2.8, -1.6, 0.0, 6.6, DARKS, C_VAULT)
abox("Vault Top", -4.6, 4.6, -2.8, -1.6, 5.2, 6.6, DARKS, C_VAULT)
abox("Vault Interior Glow", -2.4, 2.4, -1.65, -1.5, 0.0, 4.6, GLOW, C_VAULT)
abox("Vault Floor", -2.4, 2.4, -2.9, -1.5, 0.0, 0.2, STEEL, C_VAULT)
burn_zone(BURN, -2.3, 2.3, -3.4, -1.7, 0.2, 2.6, C_VAULT)
for k in range(12):
    a = 2 * math.pi * k / 12
    dot(f"Frame Bolt {k}", VC + V((VR + 0.35) * math.cos(a), -0.62, (VR + 0.35) * math.sin(a)), 0.16, GOLD, C_VAULT)
abox("Vault Sign", -1.8, 1.8, -2.86, -2.8, 5.5, 6.3, GOLD, C_VAULT)
# huge round door swung open to the left
hinge = V(-(VR + 0.7), -2.8, 2.4)
dn = V(-0.35, -1, 0).normalized()
DC = hinge + dn * (VR + 0.6) + V(0, 0, 0)
ax = V(1, -0.35, 0).normalized()
cyl("Vault Door", DC - ax * 0.5, DC + ax * 0.5, VR + 0.55, VR + 0.55, STEEL, C_DOOR, n=40, hint=Z_AX)
tube("Door Rim", DC - ax * 0.55, ax, Z_AX, VR + 0.6, VR + 0.2, 0.2, GOLD, C_DOOR, n=40)
F = DC - ax * 0.6
torus("Door Wheel", F - ax * 0.3, ax, Z_AX, 1.0, 0.12, GOLD, C_DOOR, n_major=24, n_minor=6)
cyl("Wheel Hub", F, F - ax * 0.4, 0.35, 0.35, GOLD, C_DOOR, n=12, hint=Z_AX)
u, v = perp_basis(ax)
for k in range(6):
    a = k * math.pi / 3
    d = math.cos(a) * u + math.sin(a) * v
    cyl(f"Wheel Spoke {k}", F - ax * 0.3, F - ax * 0.3 + d * 1.0, 0.07, 0.07, GOLD, C_DOOR, n=6)
    cyl(f"Locking Bolt {k}", DC + ax * 0.55 + d * (VR + 0.2), DC + ax * 0.55 + d * (VR + 0.2) + ax * 0.5, 0.18, 0.18, STEEL, C_DOOR, n=8)
cyl("Hinge", hinge + V(0, 0, -2.0), hinge + V(0, 0, 2.2), 0.3, 0.3, DARKS, C_DOOR, n=10)
# loot: gold bars, coin piles, money bags
def bar(name, C, rot):
    r = Euler((0, 0, rot)).to_matrix()
    hexa(name, [C + r @ V(-0.5, -0.25, 0), C + r @ V(0.5, -0.25, 0), C + r @ V(0.5, 0.25, 0), C + r @ V(-0.5, 0.25, 0),
                C + r @ V(-0.4, -0.17, 0.25), C + r @ V(0.4, -0.17, 0.25), C + r @ V(0.4, 0.17, 0.25), C + r @ V(-0.4, 0.17, 0.25)], GOLD, C_LOOT)
for s in (-1, 1):
    B = V(s * 4.4, -4.0, 0.2)
    for lv in range(3):
        for k in range(3 - lv):
            bar(f"Gold Bar {s}{lv}{k}", B + V(-0.55 * (2 - lv) / 2 + k * 0.55, 0, lv * 0.25), 1.5708)
for k, (x, y) in enumerate(((3.8, 2.0), (-4.2, 1.6), (5.0, -0.6))):
    for j in range(12):
        p = V(x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.6, 0.6), 0.2)
        cyl(f"Coin {k}{j}", p + V(0, 0, 0.05 * (j % 4)), p + V(0, 0, 0.05 * (j % 4) + 0.06), 0.24, 0.24, GOLD, C_LOOT, n=12)
for k, (x, y) in enumerate(((-5.2, -0.6), (5.2, 3.8), (-3.6, 4.6))):
    P = V(x, y, 0.2)
    ellip(f"Money Bag {k}", P + V(0, 0, 0.6), 0.65, 0.6, 0.65, BAG, C_LOOT, n=12, m=5)
    cyl(f"Bag Neck {k}", P + V(0, 0, 1.15), P + V(0, 0, 1.5), 0.2, 0.32, BAG, C_LOOT, n=10)
    torus(f"Bag Tie {k}", P + V(0, 0, 1.25), Z_AX, Y_AX, 0.22, 0.05, GOLD, C_LOOT, n_major=10, n_minor=4)
    abox(f"Cash Sign {k}", P.x - 0.2, P.x + 0.2, P.y - 0.63, P.y - 0.6, P.z + 0.4, P.z + 0.8, GREEN, C_LOOT)
for s in (-1, 1):                                           # velvet rope posts in front
    for k in range(2):
        P = V(s * (3.0 + k * 1.6), -5.0, 0.2)
        cyl(f"Rope Post {s}{k}", P, P + V(0, 0, 1.4), 0.1, 0.1, GOLD, C_LOOT, n=8)
        dot(f"Post Top {s}{k}", P + V(0, 0, 1.5), 0.15, GOLD, C_LOOT)
        cyl(f"Post Foot {s}{k}", P, P + V(0, 0, 0.08), 0.35, 0.35, GOLD, C_LOOT, n=12)
    path_tube(f"Velvet Rope {s}", [V(s * 3.0, -5.0, 1.3), V(s * 3.8, -5.0, 0.95), V(s * 4.6, -5.0, 1.3)], [0.07] * 3, VELVET, C_LOOT, n=6)
finish_mine(bg=(0.03, 0.026, 0.016), tint=(1.0, 0.95, 0.85))
write_furnace_lua("GoldVaultFurnace")
