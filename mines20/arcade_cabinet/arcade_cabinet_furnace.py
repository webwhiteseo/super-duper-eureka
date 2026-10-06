"""Arcade Cabinet Furnace - a giant retro arcade machine on a checkerboard floor; ore rolls straight into the glowing
prize slot at the bottom front (no ramp). Screen with pixel invaders, joystick, buttons, coin slots, neon marquee.
mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_CAB, C_DETAIL = begin("ArcadeCabinetFurnace", ["Floor", "Cabinet", "Details"], seed=161)
TILE_W = M("Floor White", (232, 232, 236), rough=0.3)
TILE_B = M("Floor Black", (24, 24, 30), rough=0.3)
CAB = M("Cabinet Purple", (90, 40, 170), rough=0.35)
CAB2 = M("Cabinet Black", (20, 18, 26), rough=0.4)
SCREEN = M("Screen", (20, 30, 60), rough=0.1, glow=(30, 60, 140), glow_strength=1.2, rbx="Neon")
PIX = M("Pixel Green", (80, 255, 120), rough=0.3, glow=(40, 255, 90), glow_strength=5.0, rbx="Neon")
PINK = M("Neon Pink", (255, 60, 200), rough=0.3, glow=(255, 30, 190), glow_strength=5.0, rbx="Neon", light=(10, 1.4))
CYAN = M("Neon Cyan", (40, 230, 255), rough=0.3, glow=(0, 220, 255), glow_strength=5.0, rbx="Neon", light=(10, 1.4))
SLOT = M("Prize Slot Glow", (255, 220, 80), rough=0.3, glow=(255, 190, 40), glow_strength=4.0, rbx="Neon", light=(14, 1.8))
RED = M("Button Red", (240, 40, 50), rough=0.3)
YEL = M("Button Yellow", (255, 220, 40), rough=0.3)
CHROME = M("Chrome (Metal)", (190, 194, 204), rough=0.15, metal=1.0, rbx="Metal")
BURN = M("Burn Zone", (255, 220, 80), rough=0.2, glow=(255, 190, 40), glow_strength=1.0, rbx="ForceField", alpha=0.7)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
for i in range(8):
    for j in range(8):
        x0, y0 = -6.0 + i * 1.5, -5.6 + j * 1.5
        abox(f"Tile {i}{j}", x0, x0 + 1.5, y0, y0 + 1.5, 0, 0.12, TILE_W if (i + j) % 2 else TILE_B, C_BASE)
abox("Floor Glow", -6.05, 6.05, -5.68, -5.6, 0.0, 0.14, CYAN, C_BASE)
# cabinet body (prize slot at the bottom front)
for s in (-1, 1):
    hexa(f"Side Panel {s}", [V(s * 2.9, -2.6, 0.12), V(s * 3.3, -2.6, 0.12), V(s * 3.3, 3.0, 0.12), V(s * 2.9, 3.0, 0.12),
                             V(s * 2.9, -1.0, 10.0), V(s * 3.3, -1.0, 10.0), V(s * 3.3, 3.0, 10.0), V(s * 2.9, 3.0, 10.0)], CAB, C_CAB)
    abox(f"Side Stripe {s}", min(s * 3.3, s * 3.34), max(s * 3.3, s * 3.34), -1.8, 2.6, 2.6, 2.8, PINK, C_CAB)
    abox(f"Side Stripe2 {s}", min(s * 3.3, s * 3.34), max(s * 3.3, s * 3.34), -1.2, 2.6, 3.0, 3.2, CYAN, C_CAB)
abox("Cabinet Back", -2.9, 2.9, 2.6, 3.0, 0.12, 10.0, CAB2, C_CAB)
abox("Slot Roof", -2.9, 2.9, -2.6, 2.6, 2.4, 2.8, CAB2, C_CAB)
abox("Slot Glow Back", -2.9, 2.9, 2.4, 2.6, 0.12, 2.4, SLOT, C_CAB)
abox("Slot Frame", -2.95, 2.95, -2.7, -2.5, 2.3, 2.5, CHROME, C_CAB)
burn_zone(BURN, -2.6, 2.6, -2.8, 2.2, 0.15, 2.2, C_CAB)
hexa("Control Deck", [V(-2.9, -2.6, 2.8), V(2.9, -2.6, 2.8), V(2.9, -0.6, 2.8), V(-2.9, -0.6, 2.8),
                      V(-2.9, -2.8, 3.6), V(2.9, -2.8, 3.6), V(2.9, -0.6, 4.2), V(-2.9, -0.6, 4.2)], CAB2, C_CAB)
hexa("Screen Bezel", [V(-2.9, -0.6, 4.2), V(2.9, -0.6, 4.2), V(2.9, 0.4, 4.2), V(-2.9, 0.4, 4.2),
                      V(-2.9, -1.0, 8.2), V(2.9, -1.0, 8.2), V(2.9, 0.0, 8.2), V(-2.9, 0.0, 8.2)], CAB2, C_CAB)
nrm = V(0, -4.0, 0.4).normalized()
SCC = V(0, -0.85, 6.2)
obox("Screen", SCC, (4.8, 3.4, 0.06), X_AX, (V(0, -0.4, 4.0)).normalized(), nrm, SCREEN, C_CAB)
up_s = V(0, -0.4, 4.0).normalized()
INV = ["0011100", "0111110", "1101011", "1111111", "0101010", "1000001"]
for r, row in enumerate(INV):
    for c, ch in enumerate(row):
        if ch == "1":
            obox(f"Pixel {r}{c}", SCC + nrm * 0.05 + X_AX * (-0.9 + c * 0.3) + up_s * (1.0 - r * 0.3), (0.26, 0.26, 0.03), X_AX, up_s, nrm, PIX, C_CAB)
for k in range(6):
    obox(f"Score Pixel {k}", SCC + nrm * 0.05 + X_AX * (-2.0 + k * 0.35) + up_s * (-1.3), (0.2, 0.2, 0.03), X_AX, up_s, nrm, PINK, C_CAB)
abox("Marquee", -2.9, 2.9, -1.2, 0.2, 8.2, 10.0, PINK, C_CAB)
abox("Marquee Frame", -3.0, 3.0, -1.3, -1.15, 8.1, 10.1, CHROME, C_CAB)
for k in range(5):
    abox(f"Marquee Letter {k}", -2.2 + k * 1.0, -1.7 + k * 1.0, -1.32, -1.28, 8.6, 9.6, CYAN, C_CAB)
abox("Top Cap", -3.3, 3.3, -1.3, 3.0, 10.0, 10.3, CAB2, C_CAB)
# controls
J = V(-1.3, -1.7, 3.95)
cyl("Joystick Base", J, J + V(0, 0, 0.12), 0.35, 0.35, CHROME, C_DETAIL, n=12)
cyl("Joystick", J, J + V(0.1, -0.1, 0.8), 0.06, 0.06, CHROME, C_DETAIL, n=6)
dot("Joystick Ball", J + V(0.1, -0.1, 0.9), 0.22, RED, C_DETAIL)
for k, (dx, dy, mat) in enumerate(((0.6, 0.1, RED), (1.2, 0.0, YEL), (1.8, -0.1, CYAN), (0.9, 0.6, PINK), (1.5, 0.5, RED))):
    p = V(dx, -1.7 + dy * 0.6, 3.9 + 0.17 * dy)
    cyl(f"Button {k}", p, p + V(0, 0, 0.18), 0.2, 0.2, mat, C_DETAIL, n=12)
for s in (-1, 1):
    abox(f"Coin Door {s}", s * 0.9 - 0.5, s * 0.9 + 0.5, -2.65, -2.6, 2.85, 3.3, CHROME, C_DETAIL) if False else None
# neon posts + giant coins
for s in (-1, 1):
    cyl(f"Neon Post {s}", V(s * 5.2, -3.8, 0.12), V(s * 5.2, -3.8, 4.6), 0.18, 0.18, PINK if s < 0 else CYAN, C_DETAIL, n=10)
    dot(f"Neon Post Top {s}", V(s * 5.2, -3.8, 4.8), 0.32, CYAN if s < 0 else PINK, C_DETAIL)
for k, (x, y, rot) in enumerate(((-4.8, 2.0, 0.3), (5.0, 1.6, -0.2), (4.4, 4.2, 0.6))):
    cyl(f"Giant Coin {k}", V(x, y, 0.8), V(x + 0.3 * math.sin(rot), y + 0.3 * math.cos(rot), 0.8), 0.7, 0.7, YEL, C_DETAIL, n=20, hint=Z_AX)
finish_mine(bg=(0.02, 0.01, 0.04), tint=(0.95, 0.85, 1.0))
write_furnace_lua("ArcadeCabinetFurnace")
