"""Ore Haven Enchanting Altar - an original take on a floating-book enchanting table, themed for Ore Haven:
dark obsidian block, castle-red cloth with gold trim, glowing ore crystals in the corners, an open glowing book
floating above and an orbiting ring of rune tiles. Book, runes and crystals use their own materials, so they
import as separate parts you can animate. Writes EnchantingAltar_RobloxSetup.lua (colours + glow lights)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BASE, C_BOOK, C_FX = begin("EnchantingAltar", ["Base", "Book", "Effects"], seed=77)
OBS = M("Obsidian", (34, 26, 46), rough=0.35, metal=0.2, rbx="Slate", noise=((22, 16, 32), (56, 42, 74), 6.0, 0.3))
OBS2 = M("Obsidian Trim", (58, 44, 78), rough=0.3, rbx="Slate")
CLOTH = M("Altar Cloth (Fabric)", (176, 40, 44), rough=0.85, rbx="Fabric")
GOLD = M("Gold Trim (Metal)", (236, 186, 70), rough=0.25, metal=1.0, rbx="Metal")
DIA = M("Ore Crystal", (90, 230, 255), rough=0.1, glow=(40, 210, 255), glow_strength=2.5, rbx="Neon", light=(8, 1.0))
AME = M("Amethyst Crystal", (190, 110, 255), rough=0.1, glow=(160, 80, 255), glow_strength=2.5, rbx="Neon", light=(8, 1.0))
COVER = M("Book Cover", (120, 30, 36), rough=0.6, rbx="Fabric")
PAGES = M("Book Pages", (250, 238, 205), rough=0.8, glow=(255, 236, 190), glow_strength=0.8, rbx="SmoothPlastic", light=(12, 1.2))
INK = M("Book Runes", (160, 110, 255), rough=0.2, glow=(150, 90, 255), glow_strength=4.0, rbx="Neon")
RUNE = M("Rune Ring", (170, 120, 255), rough=0.2, glow=(150, 90, 255), glow_strength=4.0, rbx="Neon", light=(10, 1.4))
BEAM = M("Magic Beam", (190, 140, 255), rough=0.2, glow=(170, 110, 255), glow_strength=2.0, rbx="Neon", alpha=0.6)
BEAM.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.25
HALO = M("Glow Ring", (190, 140, 255), rough=0.2, glow=(170, 110, 255), glow_strength=3.0, rbx="Neon", light=(14, 1.6))
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
S, H = 3.0, 3.2                                         # half width (6 x 6 studs), block height

# ---- obsidian block with bevelled edges + darker plinth
hexa("Plinth", [V(-S - 0.5, -S - 0.5, 0), V(S + 0.5, -S - 0.5, 0), V(S + 0.5, S + 0.5, 0), V(-S - 0.5, S + 0.5, 0),
                V(-S - 0.2, -S - 0.2, 0.5), V(S + 0.2, -S - 0.2, 0.5), V(S + 0.2, S + 0.2, 0.5), V(-S - 0.2, S + 0.2, 0.5)], OBS2, C_BASE)
hexa("Block", [V(-S, -S, 0.5), V(S, -S, 0.5), V(S, S, 0.5), V(-S, S, 0.5),
               V(-S + 0.25, -S + 0.25, H), V(S - 0.25, -S + 0.25, H), V(S - 0.25, S - 0.25, H), V(-S + 0.25, S - 0.25, H)], OBS, C_BASE)
for sx in (-1, 1):                                        # gold corner caps + glowing ore crystals growing from each corner
    for sy in (-1, 1):
        C = V(sx * (S - 0.15), sy * (S - 0.15), 0)
        abox(f"Corner Gold {sx}{sy}", C.x - 0.45, C.x + 0.45, C.y - 0.45, C.y + 0.45, H - 0.2, H + 0.25, GOLD, C_BASE)
        abox(f"Corner Foot {sx}{sy}", C.x - 0.5, C.x + 0.5, C.y - 0.5, C.y + 0.5, 0.5, 1.0, GOLD, C_BASE)
        mat = DIA if sx == sy else AME
        d = V(sx * 0.5, sy * 0.5, 1).normalized()
        crystal(f"Corner Crystal {sx}{sy}", V(sx * (S + 0.05), sy * (S + 0.05), 1.0), V(sx, sy, 0.8).normalized(), 1.3, 0.28, mat, C_FX)
        crystal(f"Corner Crystal Small {sx}{sy}", V(sx * (S + 0.05), sy * (S - 0.8), 0.7), V(sx, 0.2 * sy, 0.6).normalized(), 0.8, 0.18, mat, C_FX)
GLYPHS = [[((-0.35, 0.4), (0.35, 0.4)), ((0, 0.4), (0, -0.4)), ((-0.3, -0.1), (0.3, -0.4))],            # glowing rune glyphs
          [((-0.3, -0.4), (0, 0.4)), ((0, 0.4), (0.3, -0.4)), ((-0.18, 0.0), (0.18, 0.0))],
          [((0, 0.45), (0.35, 0)), ((0.35, 0), (0, -0.45)), ((0, -0.45), (-0.35, 0)), ((-0.35, 0), (0, 0.45))],
          [((-0.3, 0.4), (-0.3, -0.4)), ((-0.3, 0.0), (0.3, 0.4)), ((-0.3, 0.0), (0.3, -0.4))]]
for k in range(4):
    a = k * math.pi / 2
    n_ = V(math.cos(a), math.sin(a), 0); t_ = V(-n_.y, n_.x, 0)
    for j, s in enumerate((-1, 1)):
        C = n_ * (S - 0.1 + 0.02) + t_ * s * 1.3 + V(0, 0, 1.55)
        for q, ((x0, z0), (x1, z1)) in enumerate(GLYPHS[(k * 2 + j) % 4]):
            beam(f"Face Rune {k}{j}{q}", C + t_ * x0 + V(0, 0, z0), C + t_ * x1 + V(0, 0, z1), 0.13, 0.06, n_, INK, C_FX)
# ---- castle-red cloth draped over the top with gold border and hanging tabs
abox("Cloth Top", -S + 0.05, S - 0.05, -S + 0.05, S - 0.05, H, H + 0.12, CLOTH, C_BASE)
for k in range(4):
    a = k * math.pi / 2
    n_ = V(math.cos(a), math.sin(a), 0); t_ = V(-n_.y, n_.x, 0)
    obox(f"Cloth Drape {k}", n_ * (S - 0.17) + V(0, 0, H - 0.5), (2.6, 0.08, 1.2), t_, n_, Z_AX, CLOTH, C_BASE)
    blade(f"Cloth Tip {k}", [n_ * (S - 0.12) + t_ * -1.3 + V(0, 0, H - 1.1), n_ * (S - 0.12) + t_ * 1.3 + V(0, 0, H - 1.1), n_ * (S - 0.12) + V(0, 0, H - 1.8)], 0.08, CLOTH, C_BASE)
    obox(f"Cloth Gold Hem {k}", n_ * (S - 0.11) + V(0, 0, H - 1.12), (2.6, 0.06, 0.12), t_, n_, Z_AX, GOLD, C_BASE)
    dot(f"Cloth Gem {k}", n_ * (S - 0.08) + V(0, 0, H - 1.55), 0.16, AME if k % 2 else DIA, C_BASE)
# small gold book stand on top + purple glow ring
lathe("Stand Base", V(0, 0, H + 0.12), [(1.0, 0), (1.0, 0.15), (0.35, 0.3), (0.25, 0.9), (0.5, 1.05), (0.01, 1.05)], GOLD, C_BASE, n=12, smooth=False)
torus("Glow Ring", V(0, 0, H + 0.2), Z_AX, Y_AX, 2.2, 0.07, HALO, C_FX, n_major=40, n_minor=6)

lathe("Magic Beam", V(0, 0, H + 1.17), [(0.35, 0), (1.3, 1.0), (0.01, 1.01)], BEAM, C_FX, n=16)
# ---- open floating book, tilted toward the front (-Y)
BC = V(0, 0, H + 2.4)
tilt = math.radians(28)
up = V(0, -math.sin(tilt), math.cos(tilt))               # book normal
fwd = V(0, math.cos(tilt), math.sin(tilt))               # top edge of the pages
def book_pt(u, v, h=0.0):
    """u: -1..1 across the spread (x), v: -1..1 along the page height; pages dip toward the spine."""
    lift = 0.32 * abs(u) ** 0.6
    return BC + X_AX * (u * 1.6) + fwd * (v * 1.1) + up * (lift + h)
def sheet(name, h0, h1, mat, u0, u1, coll, nu=6):
    bm = bmesh.new(); rows = []
    for i in range(nu + 1):
        u = u0 + (u1 - u0) * i / nu
        rows.append([bm.verts.new(book_pt(u, v, h)) for v in (-1, 1) for h in (h0, h1)])
    for i in range(nu):
        a, b = rows[i], rows[i + 1]
        bm.faces.new((a[0], b[0], b[2], a[2])); bm.faces.new((a[1], a[3], b[3], b[1]))      # bottom / top
        bm.faces.new((a[0], a[1], b[1], b[0])); bm.faces.new((a[2], b[2], b[3], a[3]))      # page edges
    for r in (rows[0], rows[-1]):
        bm.faces.new((r[0], r[2], r[3], r[1]))
    return finish(name, bm, mat, coll, merge=0)
for s, (u0, u1) in ((-1, (-1.06, -0.02)), (1, (0.02, 1.06))):
    sheet(f"Book Cover {s}", -0.1, -0.02, COVER, u0 * 1.0, u1 * 1.0, C_BOOK)
    sheet(f"Book Pages {s}", -0.02, 0.2, PAGES, u0 * 0.94, u1 * 0.94, C_BOOK)
    # a couple of pages flipping up
    for j, ang in enumerate((0.35, 0.7)):
        p0 = book_pt(0.0, -0.95, 0.2); p1 = book_pt(0.0, 0.95, 0.2)
        out = (X_AX * s * math.cos(ang) + up * math.sin(ang)) * 1.45
        blade(f"Flip Page {s}{j}", [p0, p0 + out, p1 + out, p1], 0.03, PAGES, C_BOOK)
cyl("Book Spine", book_pt(0, -1.05, -0.06), book_pt(0, 1.05, -0.06), 0.16, 0.16, COVER, C_BOOK, n=8)
for s in (-1, 1):                                       # gold corner clasps
    for v in (-1, 1):
        obox(f"Book Clasp {s}{v}", book_pt(s * 1.0, v * 1.0, -0.06), (0.25, 0.25, 0.1), X_AX, fwd, up, GOLD, C_BOOK)
for s in (-1, 1):                                       # glowing rune lines written on the pages
    for r in range(5):
        v = 0.7 - r * 0.32
        for c in range(3):
            u = s * (0.25 + c * 0.24)
            w = 0.2 if (r + c) % 2 else 0.13
            obox(f"Page Rune {s}{r}{c}", book_pt(u, v, 0.215 if abs(u) > 0.3 else 0.205), (w, 0.1, 0.03), X_AX, fwd, up, INK, C_BOOK)
# ---- orbiting rune tiles + floating sparkle crystals
for k in range(10):
    a = k * 2 * math.pi / 10
    P = V(2.7 * math.cos(a), 2.7 * math.sin(a), H + 2.2 + 0.35 * math.sin(3 * a))
    rad = V(math.cos(a), math.sin(a), 0)
    blade(f"Rune Tile {k}", [P + V(0, 0, 0.32) , P + rad.cross(Z_AX) * 0.24 , P - V(0, 0, 0.32), P - rad.cross(Z_AX) * 0.24], 0.05, RUNE, C_FX)
for k, (x, y, z) in enumerate(((-1.8, -1.2, 6.9), (1.9, 0.9, 7.3), (0.4, 1.8, 7.8), (-1.2, 1.5, 6.4))):
    crystal(f"Float Shard {k}", V(x, y, z), V(0.2, 0.1, 1).normalized(), 0.55, 0.13, DIA if k % 2 else AME, C_FX)

finish_mine(bg=(0.02, 0.016, 0.035), tint=(0.85, 0.8, 1.0), mood_light=(0, -3, 8))
write_look_lua(NAME if "NAME" in globals() else "EnchantingAltar",
               "Book Cover/Pages/Runes, Rune Ring and Glow Ring import as their own parts - spin the Rune Ring or bob the book with a TweenService script.")
