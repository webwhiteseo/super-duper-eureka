"""Five boost pads (speed / jump) in the classic dark diamond-plate style: a stepped base, pillars, a glowing energy
centrepiece and a glowing BoostPad square the player steps on. Run with --pad <n> (1-5). No gameplay code -
the part named "BoostPad" is the trigger to script later. mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

PAD = int(arg("--pad", 1))
NAMES = {1: "HexSpeedPad", 2: "SpringJumpPad", 3: "GaleBoostPad", 4: "ThunderBoostPad", 5: "RocketBoostPad"}
NAME = NAMES[PAD]
C_BASE, C_PILLARS, C_CORE, C_PAD = begin(NAME, ["Base", "Pillars", "Core", "Pad"], seed=300 + PAD)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)

def mats(plate_rgb, glow_rgb, accent_rgb):
    P = M("Dark Plate (DiamondPlate)", plate_rgb, rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
    P2 = M("Trim Plate (DiamondPlate)", tuple(min(255, int(c * 1.5)) for c in plate_rgb), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
    G = M("Energy Glow", glow_rgb, rough=0.2, glow=glow_rgb, glow_strength=3.0, rbx="Neon", light=(16, 2.0))
    GL = M("Energy Glass", tuple(min(255, c + 60) for c in glow_rgb), rough=0.05, glow=glow_rgb, glow_strength=1.2, rbx="Glass", alpha=0.35)
    A = M("Accent Neon", accent_rgb, rough=0.3, glow=accent_rgb, glow_strength=5.0, rbx="Neon", light=(8, 1.0))
    B = M("Boost Pad", tuple(min(255, c + 40) for c in glow_rgb), rough=0.1, glow=glow_rgb, glow_strength=4.0, rbx="Neon", light=(14, 1.8))
    return P, P2, G, GL, A, B

def chevrons(C, n, size, mat, coll, up=False):
    for k in range(n):
        y = C.y - size * 0.6 + k * size * 0.6
        for s in (-1, 1):
            ax = (V(s, 0, 0) * 0.7 - V(0, 1, 0) * 0.7).normalized()
            obox(f"Pad Arrow {k}{s}", V(C.x + s * size * 0.22, y, C.z + 0.02), (size * 0.5, size * 0.1, 0.03), ax, Z_AX.cross(ax), Z_AX, mat, coll)

def walk_ramp(mat, glow, top=1.2, w=2.4, y0=-10.0, y1=-5.4, y2=-3.2):
    """Gentle walk-up ramp at the front so players can walk straight onto the pad."""
    hexa("Walk Ramp", [V(-w, y0, 0), V(w, y0, 0), V(w, y1, 0), V(-w, y1, 0),
                       V(-w, y0, 0.02), V(w, y0, 0.02), V(w, y1, top), V(-w, y1, top)], mat, C_BASE)
    abox("Walk Ramp Top", -w, w, y1, y2, 0.0, top, mat, C_BASE)
    for sgn in (1, -1):
        a, b = sorted((sgn * w, sgn * (w + 0.15)))
        hexa(f"Ramp Edge Glow {sgn}", [V(a, y0, 0), V(b, y0, 0), V(b, y1, top), V(a, y1, top),
                                       V(a, y0, 0.1), V(b, y0, 0.1), V(b, y1, top + 0.1), V(a, y1, top + 0.1)], glow, C_BASE)
        abox(f"Ramp Top Glow {sgn}", a, b, y1, y2, 0.0, top + 0.1, glow, C_BASE)

if PAD == 1:      # Hex Speed Pad: hexagon steps, three slanted pylons, floating energy prism
    P, P2, G, GL, A, B = mats((30, 52, 56), (40, 230, 255), (120, 255, 240))
    for k, (r, z0, z1) in enumerate(((7.0, 0.0, 0.5), (5.6, 0.5, 0.9), (4.2, 0.9, 1.2))):
        lathe(f"Hex Step {k}", V(0, 0, z0), [(r, 0), (r, z1 - z0), (0.01, z1 - z0)], P if k != 1 else P2, C_BASE, n=6, smooth=False)
        torus(f"Step Glow {k}", V(0, 0, z1 + 0.01), Z_AX, Y_AX, r - 0.15, 0.04, A, C_BASE, n_major=6, n_minor=4)
    lathe("Boost Pad", V(0, 0, 1.2), [(3.2, 0), (3.2, 0.06), (0.01, 0.06)], B, C_PAD, n=6, smooth=False)
    chevrons(V(0, 0, 1.26), 3, 2.2, A, C_PAD)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        d = V(math.cos(a), math.sin(a), 0)
        b = d * 5.4 + V(0, 0, 0.5)
        abox(f"Pylon Foot {k}", b.x - 0.8, b.x + 0.8, b.y - 0.8, b.y + 0.8, 0.5, 1.6, P2, C_PILLARS)
        beam(f"Pylon {k}", b + V(0, 0, 1.6), d * 4.0 + V(0, 0, 7.2), 1.0, 1.0, Z_AX, P, C_PILLARS)
        abox(f"Pylon Light {k}", d.x * 4.0 - 0.25, d.x * 4.0 + 0.25, d.y * 4.0 - 0.25, d.y * 4.0 + 0.25, 7.6, 7.9, A, C_PILLARS)
        cyl(f"Pylon Beam {k}", d * 4.0 + V(0, 0, 7.0), V(0, 0, 6.0), 0.08, 0.08, A, C_CORE, n=6)
    crystal("Energy Prism Up", V(0, 0, 6.0), Z_AX, 1.8, 0.9, GL, C_CORE, sides=6)
    crystal("Energy Prism Down", V(0, 0, 6.0), -Z_AX, 1.8, 0.9, GL, C_CORE, sides=6)
    dot("Prism Core", V(0, 0, 6.0), 0.45, G, C_CORE)
    for k in range(2):
        torus(f"Prism Ring {k}", V(0, 0, 6.0), V(0.3 * (1 - 2 * k), 0.2, 1).normalized(), Y_AX, 1.5 + 0.3 * k, 0.06, A, C_CORE, n_major=24, n_minor=4)
elif PAD == 2:    # Spring Jump Pad: round steps, giant springs either side, floating jump ring
    P, P2, G, GL, A, B = mats((34, 54, 36), (80, 255, 110), (200, 255, 120))
    for k, (r, z0, z1) in enumerate(((6.6, 0.0, 0.5), (5.2, 0.5, 0.9), (3.8, 0.9, 1.2))):
        lathe(f"Round Step {k}", V(0, 0, z0), [(r, 0), (r, z1 - z0), (0.01, z1 - z0)], P if k != 1 else P2, C_BASE, n=24, smooth=False)
    lathe("Boost Pad", V(0, 0, 1.2), [(3.0, 0), (3.0, 0.06), (0.01, 0.06)], B, C_PAD, n=24)
    for k in range(3):                                          # up arrows (jump)
        y = -1.0 + k * 0.9
        for s in (-1, 1):
            ax = (V(s, 0, 0) * 0.7 + V(0, 1, 0) * 0.7).normalized()
            obox(f"Up Arrow {k}{s}", V(s * 0.45, y, 1.28), (1.1, 0.2, 0.03), ax, Z_AX.cross(ax), Z_AX, A, C_PAD)
    for s in (-1, 1):
        S = V(s * 5.0, 0.8, 0.5)
        abox(f"Spring Housing {s}", S.x - 1.0, S.x + 1.0, S.y - 1.0, S.y + 1.0, 0.5, 1.6, P2, C_PILLARS)
        pts = [S + V(0.75 * math.cos(t), 0.75 * math.sin(t), 1.2 + t * 0.32) for t in [i * 0.35 for i in range(60)]]
        path_tube(f"Spring Coil {s}", pts, [0.14] * len(pts), A, C_PILLARS, n=6)
        abox(f"Spring Cap {s}", S.x - 1.0, S.x + 1.0, S.y - 1.0, S.y + 1.0, 7.5, 8.0, P, C_PILLARS)
        abox(f"Cap Light {s}", S.x - 0.6, S.x + 0.6, S.y - 0.6, S.y + 0.6, 8.0, 8.1, G, C_PILLARS)
    beam("Top Bar", V(-5.0, 0.8, 8.3), V(5.0, 0.8, 8.3), 0.8, 0.6, Z_AX, P, C_CORE)
    tube("Jump Ring", V(0, 0.8, 5.4), Z_AX, Y_AX, 2.2, 1.8, 0.4, GL, C_CORE, n=32)
    torus("Jump Ring Glow", V(0, 0.8, 5.4), Z_AX, Y_AX, 2.0, 0.08, G, C_CORE, n_major=32, n_minor=4)
    cyl("Ring Hanger", V(0, 0.8, 8.0), V(0, 0.8, 5.6), 0.12, 0.12, P2, C_CORE, n=6)
elif PAD == 3:    # Gale Boost Pad: square steps, four turbine fans at the corners, swirl pad, arch
    P, P2, G, GL, A, B = mats((40, 46, 58), (180, 240, 255), (120, 200, 255))
    for k, (w, z0, z1) in enumerate(((13.0, 0.0, 0.5), (10.4, 0.5, 0.9), (7.8, 0.9, 1.2))):
        slab(f"Square Step {k}", chamfer_rect(w, w, 0.8), z0, chamfer_rect(w, w, 0.8), z1, P if k != 1 else P2, C_BASE)
    abox("Boost Pad", -3.0, 3.0, -3.0, 3.0, 1.2, 1.26, B, C_PAD)
    for k in range(4):
        pts = [V(r * math.cos(t + k * math.pi / 2), r * math.sin(t + k * math.pi / 2), 1.3) for r, t in [(0.2 + 0.6 * i, i * 1.0) for i in range(5)]]
        path_tube(f"Swirl {k}", pts, [0.08] * 5, A, C_PAD, n=5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            F = V(sx * 4.7, sy * 4.7, 1.2)
            abox(f"Fan Pillar {sx}{sy}", F.x - 0.7, F.x + 0.7, F.y - 0.7, F.y + 0.7, 1.2, 5.2, P, C_PILLARS)
            C = F + V(0, 0, 4.0)
            d = V(-sx, -sy, 0).normalized()
            tube(f"Fan Duct {sx}{sy}", C + d * 0.3 + V(0, 0, 1.3), d, Z_AX, 1.3, 1.1, 1.0, P2, C_PILLARS, n=20)
            for j in range(5):
                a = 2 * math.pi * j / 5
                u, v = perp_basis(d)
                r_ = math.cos(a) * u + math.sin(a) * v
                blade(f"Fan Blade {sx}{sy}{j}", [C + d * 0.3 + V(0, 0, 1.3), C + d * 0.3 + V(0, 0, 1.3) + r_ * 1.0 + (math.cos(a + 1.2) * u + math.sin(a + 1.2) * v) * 0.35, C + d * 0.3 + V(0, 0, 1.3) + r_ * 1.0], 0.05, GL, C_PILLARS)
            abox(f"Fan Mount {sx}{sy}", F.x - 0.35, F.x + 0.35, F.y - 0.35, F.y + 0.35, 5.2, 6.5, P2, C_PILLARS)
            dot(f"Fan Hub {sx}{sy}", C + d * 0.3 + V(0, 0, 1.3), 0.25, A, C_PILLARS)
    for s in (-1, 1):
        abox(f"Arch Leg {s}", s * 3.6 - 0.5, s * 3.6 + 0.5, -0.5, 0.5, 1.2, 7.0, P2, C_CORE)
    abox("Arch Top", -4.1, 4.1, -0.6, 0.6, 7.0, 8.0, P, C_CORE)
    abox("Arch Light", -3.1, 3.1, -0.62, -0.6, 7.2, 7.8, G, C_CORE)
    for k in range(3):
        torus(f"Wind Ring {k}", V(0, 0, 3.0 + k * 1.2), Z_AX, Y_AX, 2.0 - 0.3 * k, 0.05, GL, C_CORE, n_major=24, n_minor=4)
elif PAD == 4:    # Thunder Boost Pad: triangular steps, lightning-bolt pylons, crackling orb (speed + jump)
    P, P2, G, GL, A, B = mats((40, 38, 30), (255, 220, 60), (255, 250, 180))
    for k, (r, z0, z1) in enumerate(((7.4, 0.0, 0.5), (5.8, 0.5, 0.9), (4.3, 0.9, 1.2))):
        lathe(f"Tri Step {k}", V(0, 0, z0), [(r, 0), (r, z1 - z0), (0.01, z1 - z0)], P if k != 1 else P2, C_BASE, n=3, smooth=False)
    lathe("Boost Pad", V(0, 0, 1.2), [(3.0, 0), (3.0, 0.06), (0.01, 0.06)], B, C_PAD, n=3, smooth=False)
    BOLT = [(0.0, -0.5), (0.55, -0.12), (0.47, -0.42), (1.0, 0.0), (0.4, 0.2), (0.5, 0.48), (0.0, 0.5)]
    blade("Pad Bolt", [V(0.9 * b, -1.6 + 3.2 * a, 1.28) for a, b in BOLT], 0.04, A, C_PAD)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        d = V(math.cos(a), math.sin(a), 0)
        b = d * 4.4
        abox(f"Pylon Base {k}", b.x - 0.7, b.x + 0.7, b.y - 0.7, b.y + 0.7, 0.5, 1.8, P2, C_PILLARS)
        t = V(-d.y, d.x, 0)
        blade(f"Bolt Pylon {k}", [b + V(0, 0, 1.8) + t * 1.4 * bb + Z_AX * 6.0 * aa for aa, bb in BOLT], 0.5, P, C_PILLARS)
        dot(f"Pylon Spark {k}", b + V(0, 0, 8.0), 0.3, A, C_PILLARS)
        cyl(f"Arc {k}", b + V(0, 0, 7.6), V(0, 0, 5.8), 0.07, 0.07, A, C_CORE, n=5)
    dot("Thunder Orb", V(0, 0, 5.8), 0.9, G, C_CORE)
    for k in range(3):
        torus(f"Orb Ring {k}", V(0, 0, 5.8), V(math.cos(k * 2.1), math.sin(k * 2.1), 1.2).normalized(), Y_AX, 1.3, 0.05, GL, C_CORE, n_major=24, n_minor=4)
else:             # Rocket Boost Pad: octagon steps, twin thruster nozzles, flame arrows
    P, P2, G, GL, A, B = mats((50, 34, 30), (255, 130, 40), (255, 200, 80))
    for k, (r, z0, z1) in enumerate(((7.0, 0.0, 0.5), (5.6, 0.5, 0.9), (4.2, 0.9, 1.2))):
        lathe(f"Oct Step {k}", V(0, 0, z0), [(r, 0), (r, z1 - z0), (0.01, z1 - z0)], P if k != 1 else P2, C_BASE, n=8, smooth=False)
    lathe("Boost Pad", V(0, 0, 1.2), [(3.2, 0), (3.2, 0.06), (0.01, 0.06)], B, C_PAD, n=8, smooth=False)
    chevrons(V(0, 0, 1.26), 3, 2.2, A, C_PAD)
    for s in (-1, 1):
        T = V(s * 5.2, 1.0, 0.5)
        abox(f"Thruster Mount {s}", T.x - 1.1, T.x + 1.1, T.y - 1.1, T.y + 1.1, 0.5, 2.0, P2, C_PILLARS)
        cyl(f"Thruster Body {s}", T + V(0, 0, 2.0), T + V(0, 0, 6.6), 1.0, 0.9, P, C_PILLARS, n=16)
        lathe(f"Thruster Nozzle {s}", T + V(0, 0, 6.6), [(0.9, 0), (0.7, 0.4), (1.2, 1.4)], P2, C_PILLARS, n=16)
        lathe(f"Thruster Flame {s}", T + V(0, 0, 7.6), [(0.9, 0), (0.6, 0.8), (0.01, 2.2)], G, C_PILLARS, n=12)
        for j in range(3):
            torus(f"Thruster Band {s}{j}", T + V(0, 0, 2.8 + j * 1.3), Z_AX, Y_AX, 1.0, 0.07, A, C_PILLARS, n_major=16, n_minor=4)
    beam("Gantry Bar", V(-5.2, 1.0, 6.0), V(5.2, 1.0, 6.0), 0.6, 0.8, Z_AX, P, C_CORE)
    abox("Gantry Light", -3.6, 3.6, 0.68, 0.7, 5.75, 6.25, A, C_CORE)
    cyl("Booster Core", V(0, 1.0, 5.6), V(0, 1.0, 3.6), 0.6, 0.4, GL, C_CORE, n=12)
    dot("Booster Glow", V(0, 1.0, 3.4), 0.45, G, C_CORE)

# flatten the stepped base so the pad sits almost at ground level: players just walk on and stand in the middle
for ob in MINE_OBJECTS:
    for v in ob.data.vertices:
        z = v.co.z
        v.co.z = z / 4 if z <= 1.2 else z - 0.9
finish_mine(bg=(0.02, 0.024, 0.03), tint=(0.9, 0.95, 1.0))
write_look_lua(NAME, "The glowing part named BoostPad is the trigger for your speed/jump boost script.")
