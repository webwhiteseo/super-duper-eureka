"""Fire & Ice Twin Serpents Mine - FUSION of the Frost Wyrm and the Crimson Drake.
A frost wyrm and a fire drake spiral up a twisted obsidian pillar from a yin-yang base of ice and magma; their heads meet
in front of it, frost breath and flame colliding in a violet equinox orb that drops the ore. Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_PILLAR, C_FROST, C_FIRE, C_TERRAIN = begin("TwinSerpentsMine", ["Base", "Pillar", "Frost Wyrm", "Fire Drake", "Terrain"], seed=18)
BASE = M("Twin Stone (Slate)", (40, 34, 46), rough=0.85, rbx="Slate", noise=((28, 24, 34), (58, 50, 66), 4.0, 0.4))
TRIM = M("Equinox Trim (Metal)", (180, 120, 255), rough=0.3, metal=0.5, glow=(150, 90, 255), glow_strength=1.2, rbx="Neon")
ICEF = M("Frozen Floor (Marble)", (150, 196, 228), rough=0.25, marble=((120, 170, 210), (236, 248, 255)))
MAGMA = M("Magma Crust", (44, 30, 28), rough=0.85, rbx="Basalt", noise=((28, 20, 20), (70, 46, 40), 5.0, 0.5))
LAVA = M("Lava Glow", (255, 110, 20), rough=0.4, glow=(255, 80, 10), glow_strength=4.0, rbx="Neon", light=(12, 1.5))
OBSID = M("Obsidian Pillar", (34, 26, 44), rough=0.2, metal=0.3, rbx="Basalt")
RUNEB = M("Frost Rune", (120, 220, 255), rough=0.3, glow=(80, 200, 255), glow_strength=4.0, rbx="Neon", light=(6, 0.8))
RUNER = M("Fire Rune", (255, 100, 40), rough=0.3, glow=(255, 70, 20), glow_strength=4.0, rbx="Neon", light=(6, 0.8))
FSCALE = M("Frost Scales", (64, 116, 178), rough=0.35, metal=0.3, noise=((44, 90, 150), (96, 150, 206), 14.0, 0.25))
FBELLY = M("Frost Belly", (210, 230, 244), rough=0.5)
FHORN = M("Ice Horn", (230, 240, 250), rough=0.3)
ICE = M("Ice Crystal", (150, 225, 255), rough=0.05, glow=(110, 200, 255), glow_strength=1.0, rbx="Glass", alpha=0.15, light=(8, 0.6))
SNOW = M("Snow", (240, 246, 255), rough=0.8, rbx="Snow")
FROST = M("Frost Breath", (170, 240, 255), rough=0.3, glow=(120, 220, 255), glow_strength=3.0, rbx="Neon")
RSCALE = M("Drake Scales", (168, 32, 28), rough=0.35, metal=0.3, noise=((126, 20, 18), (204, 56, 44), 14.0, 0.25))
RBELLY = M("Drake Belly", (236, 164, 80), rough=0.5)
RHORN = M("Charred Horn", (40, 30, 30), rough=0.4)
FLAME = M("Flame Breath", (255, 150, 40), rough=0.3, glow=(255, 110, 20), glow_strength=3.0, rbx="Neon")
EYEB = M("Frost Eye", (180, 250, 255), rough=0.2, glow=(140, 240, 255), glow_strength=6.0, rbx="Neon")
EYER = M("Ember Eye", (255, 220, 80), rough=0.2, glow=(255, 180, 40), glow_strength=6.0, rbx="Neon")
TOOTH = M("Fang", (245, 240, 228), rough=0.4)
ORB = M("Equinox Orb", (200, 140, 255), rough=0.1, glow=(170, 100, 255), glow_strength=5.0, rbx="Neon", light=(16, 2.0))
ORE = M("Equinox Ore", (210, 160, 255), rough=0.15, glow=(170, 110, 255), glow_strength=2.2, rbx="Neon")

top = base_plinth(12.5, 12.5, BASE, TRIM, ICEF, C_BASE, c=1.2)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(18)

# ---- twisted obsidian pillar with frost and fire runes
PC = V(0, 0.6, top)
lathe("Pillar Foot", PC, [(1.55, 0), (1.55, 0.4), (1.3, 0.55), (1.2, 0.8)], OBSID, C_PILLAR, n=8, smooth=False)
for k in range(8):
    z = 0.8 + k * 0.7
    a = k * 0.18
    obox(f"Pillar Block {k + 1}", PC + V(0, 0, z + 0.35), (1.7, 1.7, 0.68), V(math.cos(a), math.sin(a), 0), V(-math.sin(a), math.cos(a), 0), Z_AX, OBSID, C_PILLAR)
    for j in range(4):
        b = a + j * math.pi / 2
        n_ = V(math.cos(b), math.sin(b), 0);t_ = V(-math.sin(b), math.cos(b), 0)
        mat = RUNEB if n_.x < -0.1 or (abs(n_.x) <= 0.1 and n_.y < 0) else RUNER
        if (k + j) % 2 == 0:
            obox(f"Pillar Rune {k + 1}-{j + 1}", PC + V(0, 0, z + 0.35) + n_ * 0.86, (0.06, 0.3, 0.3), n_, (t_ + Z_AX).normalized(), (Z_AX - t_).normalized(), mat, C_PILLAR)
            for dz in (-0.25, 0.25):
                obox(f"Pillar Rune Tick {k + 1}-{j + 1}{dz}", PC + V(0, 0, z + 0.35 + dz) + n_ * 0.86, (0.06, 0.07, 0.1), n_, t_, Z_AX, mat, C_PILLAR)
lathe("Pillar Capital", PC + V(0, 0, 6.4), [(1.0, 0), (1.4, 0.3), (1.45, 0.55), (0.9, 0.7)], OBSID, C_PILLAR, n=8, smooth=False)
for k in range(4):
    a = k * math.pi / 2 + math.pi / 4
    crystal(f"Capital Shard {k + 1}", PC + V(0.7 * math.cos(a), 0.7 * math.sin(a), 7.0), V(0.3 * math.cos(a), 0.3 * math.sin(a), 1), 1.2, 0.2,
            ICE if math.cos(a) < 0 else LAVA, C_PILLAR)

# ---- the serpents: helices around the pillar
R = 2.35;Z0 = top + 0.45;Z1 = top + 6.0
def helix(theta_end, turns_deg, z0, z1):
    pts = []
    N = 44
    for i in range(N + 1):
        t = i / N
        th = math.radians(theta_end - turns_deg * (1 - t))
        rr = R + 0.35 * (1 - t) ** 2
        pts.append(V(PC.x + rr * math.cos(th), PC.y + rr * math.sin(th), z0 + (z1 - z0) * t))
    return pts

ORBP = V(0, PC.y - R - 1.9, Z1 + 1.15)

def serpent(tag, theta_end, sign, coll, SC, BE, HO, EY, BR):
    pts = helix(theta_end, 400, Z0, Z1)
    end = pts[-1]
    head = V(sign * 2.7, ORBP.y + 0.35, ORBP.z + 0.3)
    neck = [end + (head - end) * 0.35 + V(0, -0.2, 0.75), end + (head - end) * 0.7 + V(0, -0.1, 0.65)]
    path = pts + neck + [head]
    N = len(path)
    radii = [0.08 + 0.48 * min(1.0, i / (N * 0.45)) - (0.08 if i > N - 4 else 0.0) for i in range(N)]
    path_tube(f"{tag} Body", path, radii, SC, coll, n=14)
    for i in range(3, N - 2, 2):                          # belly bands + dorsal spines
        d = (path[i + 1] - path[i - 1]).normalized()
        out = V(path[i].x - PC.x, path[i].y - PC.y, 0).normalized()
        u = (out - d * out.dot(d)).normalized()
        torus(f"{tag} Belly Band {i}", path[i], d, u, radii[i] * 0.93, radii[i] * 0.16, BE, coll, n_major=12, n_minor=4)
        spine_dir = (V(0, 0, 1) * 0.6 + out * 0.8).normalized()
        if i < N - 3:
            crystal(f"{tag} Spine {i}", path[i] + spine_dir * radii[i] * 0.75, spine_dir, 0.25 + radii[i] * 0.9, 0.1 + radii[i] * 0.12, HO, coll, sides=4)
    cone(f"{tag} Tail Tip", path[0], path[0] + (path[0] - path[1]).normalized() * 0.6, 0.1, HO, coll, n=6)
    # head facing the orb
    f = (ORBP - head);f.z = 0;f = f.normalized()
    side = V(-f.y, f.x, 0)
    H = head
    ellip(f"{tag} Skull", H, 0.62, 0.72, 0.5, SC, coll, n=16, m=6, ax=side, ay=f, az=Z_AX)
    ellip(f"{tag} Snout", H + f * 0.75 + V(0, 0, -0.05), 0.4, 0.55, 0.3, SC, coll, n=14, m=5, ax=side, ay=f, az=Z_AX)
    jaw_d = (f * 0.85 + V(0, 0, -0.5)).normalized()
    ellip(f"{tag} Jaw", H + f * 0.45 + V(0, 0, -0.42), 0.36, 0.6, 0.16, BE, coll, n=12, m=4, ax=side, ay=jaw_d, az=jaw_d.cross(side) * -1)
    for k in range(4):                                    # fangs
        for s in (-1, 1):
            p = H + f * (0.65 + k * 0.17) + side * s * (0.3 - k * 0.04) + V(0, 0, -0.27)
            cone(f"{tag} Fang {k}{s}", p, p + V(0, 0, -0.2 + k * 0.03), 0.05, TOOTH, coll, n=4)
    for s in (-1, 1):
        dot(f"{tag} Eye {s}", H + f * 0.35 + side * s * 0.47 + V(0, 0, 0.2), 0.13, EY, coll)
        ellip(f"{tag} Brow {s}", H + f * 0.3 + side * s * 0.42 + V(0, 0, 0.36), 0.12, 0.3, 0.08, HO, coll, n=8, m=3, ax=side, ay=f, az=Z_AX)
        hb = H + f * -0.1 + side * s * 0.35 + V(0, 0, 0.35)
        path_tube(f"{tag} Horn {s}", [hb, hb + f * -0.55 + side * s * 0.25 + V(0, 0, 0.35), hb + f * -1.1 + side * s * 0.3 + V(0, 0, 0.95)], [0.12, 0.08, 0.01], HO, coll, n=8)
        for k in range(3):                                # cheek frills
            p = H + f * (-0.1 - 0.15 * k) + side * s * 0.55 + V(0, 0, -0.05 - 0.12 * k)
            cone(f"{tag} Frill {s}{k}", p, p + side * s * 0.45 + f * -0.35, 0.08, HO, coll, n=4)
        dot(f"{tag} Nostril {s}", H + f * 1.25 + side * s * 0.14 + V(0, 0, 0.12), 0.05, HO, coll)
    # breath stream toward the orb
    m0 = H + f * 1.05 + V(0, 0, -0.2)
    for k in range(5):
        t = (k + 1) / 6
        c = m0 + (ORBP - m0) * t
        r = 0.18 + 0.2 * math.sin(math.pi * t)
        rock_f(f"{tag} Breath {k + 1}", c + V(0, rnd.uniform(-0.1, 0.1), rnd.uniform(-0.1, 0.1)), (r * 1.3, r, r), BR, coll, rough=0.25, subd=1)
    # fins (ice blades for the wyrm, membrane fins for the drake)
    i = int(N * 0.7)
    out = V(path[i].x - PC.x, path[i].y - PC.y, 0).normalized()
    for k, dz in enumerate((0.0, 0.35)):
        b = path[i + k * 2]
        blade(f"{tag} Fin {k + 1}", [b + V(0, 0, 0.35), b + out * 1.4 + V(0, 0, 1.3 - dz), b + out * 1.6 + V(0, 0, 0.55 - dz), b + out * 0.9 + V(0, 0, 0.15)],
              0.05, HO if tag == "Frost Wyrm" else SC, coll)

serpent("Frost Wyrm", -138, -1, C_FROST, FSCALE, FBELLY, FHORN, EYEB, FROST)
serpent("Fire Drake", -42 + 360, 1, C_FIRE, RSCALE, RBELLY, RHORN, EYER, FLAME)

# ---- equinox orb + ore drop
dot("Equinox Orb", ORBP, 0.5, ORB, C_PILLAR)
for k in range(2):
    torus(f"Orb Halo {k + 1}", ORBP, V(math.cos(k * 1.4), 0.3, math.sin(k * 1.4)), Z_AX, 0.85, 0.04, TRIM, C_PILLAR, n_major=24, n_minor=4)
ore_cube(ORBP + V(0, -0.1, -1.55), ORE, C_PILLAR, size=0.8)

# ---- frost half (left): crystal clusters, snow drifts, frozen pool
for k, (x, y, sz) in enumerate(((-4.3, 3.6, 0.55), (-4.4, -1.6, 0.45), (-1.4, 4.4, 0.4))):
    crystal_cluster(f"Ice Cluster {k + 1}", V(x, y, top + 0.2), 5, sz, ICE, SNOW, C_TERRAIN, seed=k)
for k, (x, y, sx, sy) in enumerate(((-3.2, 1.6, 1.4, 1.0), (-4.6, -4.3, 0.9, 0.8), (-0.9, -4.6, 1.0, 0.6))):
    ellip(f"Snow Drift {k + 1}", V(x, y, top), sx, sy, 0.35, SNOW, C_TERRAIN, n=14, m=3, half=True)
for k in range(5):
    a = rnd.uniform(0, 6.28)
    crystal(f"Ice Spike {k + 1}", V(-2.0 - rnd.uniform(0, 3), rnd.uniform(-3.5, 3.5), top), V(math.cos(a) * 0.3, math.sin(a) * 0.3, 1), rnd.uniform(0.6, 1.1), 0.13, ICE, C_TERRAIN)
# ---- fire half (right): magma rocks, lava pool, flame tongues
ellip("Lava Pool", V(3.9, -1.2, top + 0.08), 1.3, 1.0, 0.06, LAVA, C_TERRAIN, n=16, m=2, half=True)
for k in range(7):
    a = 2 * math.pi * k / 7
    rock_f(f"Pool Rock {k + 1}", V(3.9 + 1.45 * math.cos(a), -1.2 + 1.15 * math.sin(a), top + 0.15), (0.35, 0.3, 0.28), MAGMA, C_TERRAIN, rough=0.3)
for k, (x, y, sz) in enumerate(((4.3, 3.8, 0.55), (1.6, 4.5, 0.4), (4.6, -4.2, 0.45))):
    rock_f(f"Magma Boulder {k + 1}", V(x, y, top + sz * 0.6), (sz * 1.4, sz * 1.2, sz), MAGMA, C_TERRAIN, rough=0.3)
    for j in range(3):
        a = rnd.uniform(0, 6.28)
        crystal(f"Fire Crystal {k + 1}-{j + 1}", V(x + math.cos(a) * sz * 0.5, y + math.sin(a) * sz * 0.5, top + sz), V(math.cos(a) * 0.4, math.sin(a) * 0.4, 1),
                sz * rnd.uniform(1.6, 2.4), sz * 0.3, LAVA, C_TERRAIN)
for k in range(4):
    p = V(3.9 + rnd.uniform(-0.7, 0.7), -1.2 + rnd.uniform(-0.5, 0.5), top + 0.1)
    cone(f"Flame Tongue {k + 1}", p, p + V(0, 0, rnd.uniform(0.5, 0.9)), 0.16, FLAME, C_TERRAIN, n=5)
# ---- braziers at the front corners: frost (left) and fire (right)
for s, glow in ((-1, RUNEB), (1, RUNER)):
    B = V(s * 4.5, -4.7 + 0.2, top)
    lathe(f"Brazier {s}", B, [(0.45, 0), (0.25, 0.3), (0.2, 1.4), (0.55, 1.6), (0.6, 1.9), (0.45, 1.9)], OBSID, C_TERRAIN, n=8, smooth=False)
    if s < 0:
        crystal_cluster("Brazier Ice", B + V(0, 0, 1.85), 4, 0.22, ICE, SNOW, C_TERRAIN, seed=9)
    else:
        for k in range(3):
            cone(f"Brazier Flame {k}", B + V(0.15 * math.cos(k * 2.1), 0.15 * math.sin(k * 2.1), 1.85), B + V(0, 0, 2.6 + 0.15 * k), 0.22, FLAME, C_TERRAIN, n=6)
    dot(f"Brazier Glow {s}", B + V(0, 0, 1.95), 0.28, glow, C_TERRAIN)

finish_mine(bg=(0.016, 0.012, 0.03), tint=(0.95, 0.85, 1.0))
