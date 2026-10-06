"""Ten original Miner's-Haven-style droppers (dark diamond-plate blocks, neon panels, crystals, exhausts).
Run with --d <1-10>. Each writes <Name>.blend, <Name>_Roblox.fbx and <Name>_RobloxSetup.lua (colours, lights,
working dropper from the glowing ore cube). Built with mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

D = int(arg("--d", 1))
NAMES = {1: "CryoReactorDropper", 2: "BlastCraneDropper", 3: "FurnaceEngineDropper", 4: "EmberCrusherDropper", 5: "SapphireColossusDropper",
         6: "PlasmaPylonDropper", 7: "MagmaPumpDropper", 8: "StarforgeAnvilDropper", 9: "GeyserVentDropper", 10: "HiveExtractorDropper"}
NAME = NAMES[D]
C1, C2, C3, C4 = begin(NAME, ["Footing", "Body", "Glow", "Details"], seed=400 + D)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(400 + D)

def kit(plate, glow, accent):
    plate = tuple(min(255, int(c * 1.8)) for c in plate)
    P = M("Dark Plate (DiamondPlate)", plate, rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
    P2 = M("Steel Plate (DiamondPlate)", tuple(min(255, int(c * 1.6) + 10) for c in plate), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
    G = M("Core Glow", glow, rough=0.2, glow=glow, glow_strength=4.0, rbx="Neon", light=(14, 1.8))
    GL = M("Crystal", tuple(min(255, c + 40) for c in glow), rough=0.05, glow=glow, glow_strength=1.2, rbx="Glass", alpha=0.15, light=(8, 0.8))
    A = M("Accent Neon", accent, rough=0.3, glow=accent, glow_strength=5.0, rbx="Neon", light=(8, 1.0))
    O = M("Ore", tuple(min(255, c + 60) for c in glow), rough=0.15, glow=glow, glow_strength=2.2, rbx="Neon")
    return P, P2, G, GL, A, O

def footing(P, P2, A, w=7.0, l=7.0):
    slab("Footing Low", chamfer_rect(w, l, 0.8), 0.0, chamfer_rect(w - 0.2, l - 0.2, 0.75), 0.4, P2, C1)
    slab("Footing High", chamfer_rect(w - 1.4, l - 1.4, 0.6), 0.4, chamfer_rect(w - 1.6, l - 1.6, 0.55), 0.9, P, C1)
    abox("Footing Glow", -(w - 1.6) / 2, (w - 1.6) / 2, -(l - 1.4) / 2 - 0.02, -(l - 1.4) / 2, 0.5, 0.62, A, C1)
    return 0.9

def flame_jet(name, base, d, L, mat_out, mat_in):
    d = d.normalized();u, v = perp_basis(d)
    cyl(f"{name} Flame", base, base + d * L, 0.45, 0.0, mat_out, C3, n=10)
    cyl(f"{name} Core", base, base + d * L * 0.6, 0.25, 0.0, mat_in, C3, n=8)

def exhaust(name, P0, d, P, P2, fl, fl2):
    d = d.normalized()
    cyl(f"{name} Pipe", P0, P0 + d * 1.6, 0.4, 0.45, P, C4, n=10)
    tube(f"{name} Lip", P0 + d * 1.7, d, perp_basis(d)[0], 0.6, 0.4, 0.3, P2, C4, n=12)
    flame_jet(name, P0 + d * 1.85, d, 1.6, fl, fl2)

if D == 1:   # Cryo Reactor: capsule tower with glowing core window, three crystals on arms, side frost vents
    P, P2, G, GL, A, O = kit((30, 44, 52), (60, 240, 220), (120, 255, 230))
    top = footing(P, P2, A, 8, 8)
    abox("Machine Block", -3.0, 3.0, -2.6, 2.6, top, top + 2.2, P, C2)
    for s in (-1, 1):
        abox(f"Side Pod {s}", s * 3.0 - (0.0 if s > 0 else 1.2), s * 3.0 + (1.2 if s > 0 else 0.0), -1.6, 1.6, top, top + 1.6, P2, C2)
        cone(f"Frost Vent {s}", V(s * 3.6, 0, top + 1.6), V(s * 3.6, 0, top + 3.0), 0.45, GL, C3, n=6)
    T = V(0, 0.4, top + 2.2)
    lathe("Reactor Capsule", T, [(1.5, 0), (1.5, 0.4), (1.2, 0.6), (1.2, 4.6), (1.5, 4.8), (1.5, 5.2), (0.9, 5.6), (0.6, 6.0)], P, C2, n=16)
    abox("Core Window", -0.7, 0.7, T.y - 1.25, T.y - 1.1, T.z + 1.2, T.z + 4.0, G, C3)
    for k in range(4):
        abox(f"Window Bar {k}", -0.75, 0.75, T.y - 1.3, T.y - 1.18, T.z + 1.6 + k * 0.7, T.z + 1.7 + k * 0.7, P2, C2)
    for k, (a, h) in enumerate(((150, 1.6), (90, 2.2), (30, 1.6))):
        ar = math.radians(a)
        d = V(math.cos(ar), 0.0, math.sin(ar))
        J = T + V(0, 0, 5.6) + d * 1.0
        E = J + d * 1.6 + V(0, 0, 0.6)
        cyl(f"Arm {k}", J, E, 0.2, 0.18, P2, C2, n=8)
        dot(f"Arm Joint {k}", J, 0.35, P2, C2)
        crystal(f"Top Crystal {k}", E, (d + V(0, 0, 1.4)).normalized(), h, 0.55, GL, C3, sides=6)
        crystal(f"Top Crystal Base {k}", E, -(d + V(0, 0, 1.4)).normalized(), 0.6, 0.55, GL, C3, sides=6)
    ore_cube(V(0, -3.6, top + 1.4), O, C3, size=0.8)
    beam("Output Chute", V(0, -2.6, top + 1.9), V(0, -3.4, top + 1.6), 1.1, 0.12, X_AX, P2, C4)
elif D == 2: # Blast Crane: blocky crane with a hanging grab-claw, powder kegs and dynamite bundles
    P, P2, G, GL, A, O = kit((40, 36, 34), (255, 120, 40), (255, 200, 80))
    WOOD = M("Keg Wood (Wood)", (150, 104, 60), rough=0.8, rbx="WoodPlanks")
    RED = M("Dynamite Red", (200, 30, 30), rough=0.5)
    STONE = M("Quarry Stone", (110, 110, 112), rough=0.9, rbx="Slate", noise=((86, 86, 88), (136, 136, 138), 3.0, 0.4))
    top = footing(P, P2, A, 9, 8)
    abox("Crane Base", -2.6, 1.4, -1.4, 2.6, top, top + 2.0, STONE, C2)
    abox("Crane Cab", -2.2, 1.0, -1.0, 2.2, top + 2.0, top + 4.0, P, C2)
    abox("Cab Window", -1.6, 0.4, -1.05, -0.98, top + 2.8, top + 3.6, G, C3)
    beam("Boom", V(0.0, 0.6, top + 3.6), V(-4.6, -3.0, top + 7.6), 0.8, 0.8, Z_AX, P, C2)
    beam("Boom Back", V(0.0, 0.6, top + 3.6), V(1.6, 3.0, top + 5.0), 0.7, 0.7, Z_AX, P2, C2)
    abox("Counterweight", 1.0, 2.6, 2.4, 4.0, top + 4.0, top + 5.6, STONE, C2)
    TIP = V(-4.6, -3.0, top + 7.6)
    cyl("Cable", TIP, TIP + V(0, 0, -3.0), 0.06, 0.06, P2, C4, n=5)
    H = TIP + V(0, 0, -3.2)
    abox("Claw Head", H.x - 0.7, H.x + 0.7, H.y - 0.7, H.y + 0.7, H.z - 0.2, H.z + 0.5, P, C2)
    for k in range(3):
        a = 2 * math.pi * k / 3
        d = V(math.cos(a), math.sin(a), 0)
        path_tube(f"Claw Finger {k}", [H + d * 0.6, H + d * 1.2 + V(0, 0, -0.8), H + d * 0.7 + V(0, 0, -1.7)], [0.18, 0.14, 0.05], P2, C2, n=6)
    ore_cube(H + V(0, 0, -1.3), O, C3, size=0.8)
    for k, (x, y) in enumerate(((2.8, -2.2), (3.4, -0.6))):
        lathe(f"Powder Keg {k}", V(x, y, top), [(0.6, 0), (0.75, 0.6), (0.75, 0.9), (0.6, 1.5)], WOOD, C4, n=12)
        for z in (0.25, 1.25):
            torus(f"Keg Hoop {k}{z}", V(x, y, top + z), Z_AX, Y_AX, 0.68, 0.05, P, C4, n_major=12, n_minor=4)
        abox(f"Keg Label {k}", x - 0.35, x + 0.35, y - 0.78, y - 0.74, top + 0.6, top + 0.9, A, C4)
    for k in range(5):
        cyl(f"Dynamite {k}", V(-3.0 + k * 0.28, -3.0, top + 0.18), V(-3.0 + k * 0.28, -1.8, top + 0.18 + 0.08 * (k % 2)), 0.13, 0.13, RED, C4, n=8)
    torus("Dynamite Tape", V(-2.45, -2.4, top + 0.2), Y_AX, Z_AX, 0.7, 0.05, P2, C4, n_major=12, n_minor=4) if False else None
    path_tube("Fuse", [V(-2.4, -1.8, top + 0.25), V(-2.0, -1.2, top + 0.4), V(-1.6, -1.0, top + 0.2)], [0.03] * 3, P, C4, n=4)
    dot("Fuse Spark", V(-1.6, -1.0, top + 0.25), 0.15, A, C3)
elif D == 3: # Furnace Engine: block machine with screen + lamps, three flaming exhaust stacks, spark coil, glass chute
    P, P2, G, GL, A, O = kit((54, 44, 36), (255, 180, 50), (255, 80, 40))
    COP = M("Copper (Metal)", (200, 120, 70), rough=0.3, metal=1.0, rbx="Metal")
    SCR = M("Screen", (255, 220, 120), rough=0.2, glow=(255, 190, 60), glow_strength=2.0, rbx="Neon")
    top = footing(P, P2, A, 9, 8)
    abox("Engine Block", -2.2, 2.2, -1.8, 2.4, top, top + 5.6, P, C2)
    abox("Engine Shoulder", -2.6, 2.6, -2.0, 2.6, top + 5.2, top + 6.0, P2, C2)
    abox("Screen", -1.4, 0.6, -1.86, -1.8, top + 3.2, top + 4.8, SCR, C3)
    for k in range(4):
        abox(f"Screen Bar {k}", -1.2 + k * 0.4, -1.0 + k * 0.4, -1.9, -1.86, top + 3.4, top + 3.6 + 0.3 * k, P, C3)
    abox("Red Switch", -1.2, -0.4, -1.9, -1.8, top + 2.6, top + 2.9, A, C3)
    for k, (dx, dz) in enumerate(((1.2, 4.6), (1.2, 3.6), (1.2, 2.6))):
        cyl(f"Lamp {k}", V(dx, -1.8, top + dz), V(dx, -2.0, top + dz), 0.3, 0.3, G, C3, n=12, hint=Z_AX)
    abox("Side Lamp Box", 2.2, 3.4, -0.6, 1.4, top + 3.0, top + 4.6, P2, C2)
    abox("Side Lamp", 2.4, 3.2, -0.66, -0.6, top + 3.2, top + 4.4, G, C3)
    for k, (dx, ang) in enumerate(((-1.4, -25), (0.0, 0), (1.4, 25))):
        a = math.radians(ang)
        exhaust(f"Stack {k}", V(dx, 0.4, top + 6.0), V(math.sin(a), 0.1, math.cos(a)), P2, P, G, A)
    S = V(-3.2, -1.4, top)
    lathe("Spark Dome", S, [(1.4, 0), (1.5, 0.6), (1.2, 1.4), (0.5, 1.8), (0.2, 2.0)], P2, C2, n=16)
    torus("Dome Glow", S + V(0, 0, 0.8), Z_AX, Y_AX, 1.42, 0.08, G, C3, n_major=20, n_minor=4)
    for k in range(4):
        torus(f"Spark Coil {k}", S + V(0, 0, 2.2 + k * 0.3), Z_AX, Y_AX, 0.35 - 0.05 * k, 0.08, COP, C4, n_major=12, n_minor=4)
    cyl("Spark Rod", S + V(0, 0, 2.0), S + V(-0.4, -0.3, 3.8), 0.05, 0.03, P2, C4, n=5)
    dot("Spark", S + V(-0.4, -0.3, 3.9), 0.25, G, C3)
    abox("Glass Chute", 2.2, 3.6, -1.6, -0.6, top + 0.6, top + 2.4, GL, C3)
    ore_cube(V(2.9, -1.1, top + 1.3), O, C3, size=0.7)
elif D == 4: # Ember Crusher: low armoured machine, a jagged red crystal cluster bursting out, exhaust stacks
    P, P2, G, GL, A, O = kit((40, 38, 36), (255, 60, 50), (255, 230, 200))
    ROCK = M("Rubble", (70, 66, 60), rough=0.9, rbx="Slate")
    top = footing(P, P2, A, 9, 9)
    hexa("Crusher Body", [V(-3.4, -2.6, top), V(3.0, -2.6, top), V(3.0, 3.0, top), V(-3.4, 3.0, top),
                          V(-2.8, -1.8, top + 2.4), V(2.4, -1.8, top + 2.4), V(2.4, 2.4, top + 2.4), V(-2.8, 2.4, top + 2.4)], P, C2)
    abox("Crusher Jaw", -3.0, -1.0, -3.2, -1.4, top, top + 1.4, P2, C2)
    for k in range(9):
        a = rnd.uniform(-0.7, 0.9)
        crystal(f"Ember Crystal {k}", V(rnd.uniform(-0.6, 2.2), rnd.uniform(-1.2, 1.8), top + 2.2), V(math.sin(a), rnd.uniform(-0.5, 0.5), 1), rnd.uniform(1.6, 3.4), rnd.uniform(0.35, 0.6), GL, C3, sides=5)
    for k, x in enumerate((-2.2, -0.8)):
        cyl(f"Stack {k}", V(x, 1.6, top + 2.2), V(x, 1.6, top + 5.4 - k * 0.6), 0.22, 0.2, P2, C4, n=8)
        dot(f"Stack Light {k}", V(x, 1.6, top + 5.5 - k * 0.6), 0.3, A, C3)
        for j in range(2):
            torus(f"Stack Ring {k}{j}", V(x, 1.6, top + 3.0 + j * 1.0), Z_AX, Y_AX, 0.26, 0.05, A, C4, n_major=10, n_minor=4)
    for k, y in enumerate((-2.0, 0.0, 2.0)):
        cyl(f"Side Light {k}", V(3.0, y, top + 1.0), V(3.2, y, top + 1.0), 0.3, 0.3, A, C3, n=10, hint=Z_AX)
    for k in range(5):
        rock_f(f"Rubble {k}", V(rnd.uniform(-3.6, 3.6), rnd.uniform(-4.0, -3.0), top), (0.5, 0.4, 0.35), ROCK, C4, rough=0.3)
    ore_cube(V(-2.0, -3.9, top + 1.0), O, C3, size=1.1)
elif D == 5: # Sapphire Colossus: hunched block golem cradling a big blue gem over a pile of crystals
    P, P2, G, GL, A, O = kit((34, 40, 48), (70, 190, 255), (150, 230, 255))
    top = 0.6
    slab("Crystal Bed Base", chamfer_rect(8.5, 8.0, 1.2), 0.0, chamfer_rect(8.2, 7.7, 1.1), 0.6, P2, C1)
    for k in range(4):
        dot(f"Base Light {k}", V(-1.2 + k * 0.8, -3.9, 0.3), 0.18, A, C1)
    for k in range(14):
        a = rnd.uniform(0, 6.28);r = rnd.uniform(1.5, 3.6)
        crystal(f"Bed Crystal {k}", V(r * math.cos(a), r * math.sin(a), top), V(math.cos(a) * 0.4, math.sin(a) * 0.4, 1), rnd.uniform(0.6, 1.3), 0.3, GL, C3, sides=5)
    obox("Golem Torso", V(0, 0.6, top + 3.4), (4.4, 3.2, 3.6), X_AX, V(0, 1, 0.25).normalized(), V(0, -0.25, 1).normalized(), P, C2)
    obox("Golem Hump", V(0, 1.4, top + 5.6), (3.6, 2.6, 2.0), X_AX, V(0, 1, 0.4).normalized(), V(0, -0.4, 1).normalized(), P, C2)
    obox("Golem Head", V(0, -0.6, top + 6.0), (1.8, 1.8, 1.6), X_AX, V(0, 1, 0.15).normalized(), V(0, -0.15, 1).normalized(), P2, C2)
    abox("Golem Eye Slit", -0.6, 0.6, -1.55, -1.48, top + 6.0, top + 6.3, G, C3)
    for s in (-1, 1):
        obox(f"Shoulder {s}", V(s * 2.6, 0.6, top + 4.8), (1.6, 2.0, 1.6), X_AX, Y_AX, Z_AX, P2, C2)
        obox(f"Upper Arm {s}", V(s * 3.0, -0.2, top + 3.2), (1.2, 1.2, 2.6), X_AX, V(0, 1, 0.4).normalized(), V(0, -0.4, 1).normalized(), P, C2)
        obox(f"Fist {s}", V(s * 2.6, -1.6, top + 1.0), (1.6, 1.6, 1.4), X_AX, Y_AX, Z_AX, P, C2)
        for k in range(3):
            obox(f"Knuckle {s}{k}", V(s * 2.6 + (k - 1) * 0.45, -2.45, top + 1.2), (0.4, 0.2, 0.4), X_AX, Y_AX, Z_AX, P2, C2)
        obox(f"Leg {s}", V(s * 1.6, 1.4, top + 1.0), (1.4, 1.6, 2.0), X_AX, Y_AX, Z_AX, P, C2)
        crystal(f"Back Spike {s}", V(s * 1.0, 2.2, top + 6.4), V(s * 0.3, 0.5, 1), 1.6, 0.4, GL, C3, sides=5)
    crystal("Heart Gem Up", V(0, -1.2, top + 3.6), Z_AX, 1.0, 0.9, GL, C3, sides=8)
    crystal("Heart Gem Down", V(0, -1.2, top + 3.6), -Z_AX, 1.4, 0.9, GL, C3, sides=8)
    dot("Heart Glow", V(0, -1.2, top + 3.7), 0.4, G, C3)
    ore_cube(V(0, -3.2, top + 2.2), O, C3, size=0.8)
elif D == 6: # Plasma Pylon: tall spire with orbiting rings and a plasma orb, emitter feet
    P, P2, G, GL, A, O = kit((36, 30, 52), (190, 90, 255), (255, 140, 255))
    top = footing(P, P2, A, 8, 8)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        d = V(math.cos(a), math.sin(a), 0)
        hexa(f"Pylon Foot {k}", [d * 1.0 + V(0, 0, top) + V(-d.y, d.x, 0) * 0.6, d * 3.2 + V(0, 0, top) + V(-d.y, d.x, 0) * 0.6, d * 3.2 + V(0, 0, top) - V(-d.y, d.x, 0) * 0.6, d * 1.0 + V(0, 0, top) - V(-d.y, d.x, 0) * 0.6,
                                 d * 1.0 + V(0, 0, top + 3.0) + V(-d.y, d.x, 0) * 0.4, d * 3.2 + V(0, 0, top + 0.8) + V(-d.y, d.x, 0) * 0.4, d * 3.2 + V(0, 0, top + 0.8) - V(-d.y, d.x, 0) * 0.4, d * 1.0 + V(0, 0, top + 3.0) - V(-d.y, d.x, 0) * 0.4], P, C2)
        dot(f"Foot Emitter {k}", d * 3.0 + V(0, 0, top + 1.1), 0.3, A, C3)
    lathe("Spire", V(0, 0, top), [(1.3, 0), (1.1, 3.0), (0.7, 6.0), (0.9, 6.4), (0.5, 8.0), (0.1, 9.4)], P, C2, n=8, smooth=False)
    for k, z in enumerate((2.2, 4.4)):
        abox(f"Spire Window {k}", -0.35, 0.35, -1.3 + 0.12 * k, -1.1 + 0.12 * k, top + z, top + z + 1.2, G, C3)
    dot("Plasma Orb", V(0, 0, top + 10.2), 0.8, G, C3)
    for k in range(3):
        torus(f"Orbit Ring {k}", V(0, 0, top + 10.2), V(math.cos(k * 2.1), math.sin(k * 2.1), 1.4).normalized(), Y_AX, 1.4 + 0.2 * k, 0.07, A, C3, n_major=28, n_minor=4)
    for k in range(3):
        torus(f"Spire Ring {k}", V(0, 0, top + 2.0 + k * 2.0), Z_AX, Y_AX, 1.25 - 0.18 * k, 0.12, P2, C2, n_major=8, n_minor=4)
    beam("Ore Arm", V(0, -0.6, top + 5.0), V(0, -3.0, top + 4.0), 0.4, 0.4, X_AX, P2, C2)
    tube("Ore Ring", V(0, -3.0, top + 3.6), Z_AX, Y_AX, 0.8, 0.6, 0.3, A, C3, n=16)
    ore_cube(V(0, -3.0, top + 2.6), O, C3, size=0.8)
elif D == 7: # Magma Pump: a nodding pump-jack drawing lava from a crater, piped into a hopper
    P, P2, G, GL, A, O = kit((44, 36, 34), (255, 110, 30), (255, 200, 60))
    ROCK = M("Basalt", (54, 44, 42), rough=0.9, rbx="Basalt")
    top = footing(P, P2, A, 10, 8)
    lathe("Lava Crater", V(-2.8, 0.6, top), [(1.6, 0), (1.8, 0.5), (1.2, 0.6), (1.2, 0.5)], ROCK, C2, n=12, smooth=False)
    lathe("Lava", V(-2.8, 0.6, top + 0.45), [(1.2, 0), (1.2, 0.05)], G, C3, n=12)
    for s in (-1, 1):
        beam(f"A-Frame {s}", V(0.4, 0.6 + s * 1.2, top), V(0.4, 0.6, top + 4.6), 0.4, 0.4, X_AX, P, C2)
    WB = V(0.4, 0.6, top + 4.8)
    beam("Walking Beam", WB + V(-3.4, 0, 0.6), WB + V(3.0, 0, -0.5), 0.6, 0.7, Y_AX, P2, C2)
    dot("Beam Pivot", WB, 0.45, A, C3)
    HH = WB + V(-3.4, 0, 0.6)
    hexa("Horse Head", [HH + V(-0.2, -0.5, -1.6), HH + V(0.6, -0.5, -1.0), HH + V(0.6, 0.5, -1.0), HH + V(-0.2, 0.5, -1.6),
                        HH + V(-0.2, -0.5, 0.6), HH + V(0.6, -0.5, 0.6), HH + V(0.6, 0.5, 0.6), HH + V(-0.2, 0.5, 0.6)], P, C2)
    cyl("Polished Rod", HH + V(0.6, 0, -1.4), V(-2.8, 0.6, top + 0.5), 0.1, 0.1, P2, C4, n=6)
    cyl("Crank Wheel", V(3.4, 0.0, top + 1.6), V(3.4, 1.2, top + 1.6), 1.2, 1.2, P, C2, n=16, hint=Z_AX)
    abox("Counterweight", 2.6, 4.2, -0.1, 1.3, top + 0.2, top + 1.0, P2, C2)
    beam("Pitman Arm", V(3.6, 0.6, top + 2.4), WB + V(3.0, 0, -0.5), 0.3, 0.3, Y_AX, P2, C2)
    abox("Motor", 2.6, 4.4, 1.8, 3.4, top, top + 1.6, P, C2)
    abox("Motor Light", 2.8, 4.2, 1.74, 1.8, top + 0.6, top + 1.0, A, C3)
    path_tube("Lava Pipe", [V(-2.8, -0.8, top + 0.4), V(-2.8, -2.0, top + 1.6), V(-1.0, -2.6, top + 2.8), V(0.4, -2.6, top + 3.0)], [0.25] * 4, P2, C4, n=8)
    lathe("Hopper", V(0.8, -2.8, top + 1.4), [(0.3, 0), (1.0, 1.2), (1.1, 1.6)], P, C2, n=4, smooth=False)
    lathe("Hopper Lava", V(0.8, -2.8, top + 2.7), [(0.85, 0), (0.85, 0.1)], G, C3, n=4)
    ore_cube(V(0.8, -2.8, top + 0.6), O, C3, size=0.7)
elif D == 8: # Starforge Anvil: a giant anvil on a block stand, a mechanical hammer arm, star sparks, crystal ingots
    P, P2, G, GL, A, O = kit((40, 40, 50), (120, 200, 255), (255, 240, 180))
    top = footing(P, P2, A, 9, 8)
    abox("Anvil Stand", -1.4, 1.4, -1.2, 1.2, top, top + 2.2, P2, C2)
    hexa("Anvil Waist", [V(-1.2, -1.0, top + 2.2), V(1.2, -1.0, top + 2.2), V(1.2, 1.0, top + 2.2), V(-1.2, 1.0, top + 2.2),
                         V(-0.8, -0.6, top + 3.0), V(0.8, -0.6, top + 3.0), V(0.8, 0.6, top + 3.0), V(-0.8, 0.6, top + 3.0)], P, C2)
    abox("Anvil Top", -2.2, 1.8, -0.9, 0.9, top + 3.0, top + 3.9, P, C2)
    cone("Anvil Horn", V(-2.2, 0, top + 3.55), V(-4.0, 0, top + 3.75), 0.55, P, C2, n=8)
    abox("Hot Ingot", -0.6, 0.6, -0.4, 0.4, top + 3.9, top + 4.2, G, C3)
    abox("Hammer Column", 3.0, 4.0, 1.0, 2.0, top, top + 6.8, P, C2)
    beam("Hammer Arm", V(3.5, 1.5, top + 6.6), V(0.2, 0.0, top + 5.8), 0.6, 0.6, Z_AX, P2, C2)
    obox("Hammer Head", V(0.0, 0.0, top + 5.0), (1.8, 1.0, 1.4), X_AX, Y_AX, Z_AX, P, C2)
    abox("Hammer Glow", -0.9, 0.9, -0.52, -0.5, top + 4.5, top + 5.5, A, C3)
    for k in range(10):
        a = rnd.uniform(0, 6.28)
        crystal(f"Star Spark {k}", V(0, 0, top + 4.2) + V(math.cos(a), math.sin(a), rnd.uniform(0.2, 1.0)) * rnd.uniform(1.0, 2.2), Z_AX, 0.3, 0.1, A, C3, sides=4)
    for k in range(3):
        crystal(f"Ingot Crystal {k}", V(-3.2 + k * 0.7, 2.8, top), V(0.1 * k, 0.1, 1), 1.2 + 0.4 * k, 0.3, GL, C3, sides=6)
    abox("Quench Trough", -3.6, -1.6, -3.4, -2.2, top, top + 0.8, P2, C2)
    abox("Quench Water", -3.4, -1.8, -3.3, -2.3, top + 0.6, top + 0.75, G, C3)
    ore_cube(V(0.0, -2.4, top + 3.2), O, C3, size=0.7)
    beam("Ore Slide", V(0.0, -0.9, top + 3.4), V(0.0, -2.0, top + 3.0), 1.0, 0.1, X_AX, P2, C4)
elif D == 9: # Geyser Vent: rocky vent block, a steam column topped with crystals, pressure pipes and gauges
    P, P2, G, GL, A, O = kit((48, 52, 56), (110, 255, 200), (200, 255, 240))
    ROCK = M("Vent Rock", (80, 76, 72), rough=0.9, rbx="Slate", noise=((60, 56, 52), (104, 100, 94), 3.0, 0.5))
    STEAM = M("Steam", (236, 240, 244), rough=0.9, rbx="SmoothPlastic", alpha=0.3)
    top = footing(P, P2, A, 9, 9)
    for k in range(10):
        a = 2 * math.pi * k / 10
        rock_f(f"Vent Rock {k}", V(2.0 * math.cos(a), 0.6 + 2.0 * math.sin(a), top + 0.6), (1.0, 0.9, 1.0), ROCK, C2, rough=0.3)
    lathe("Vent Pool", V(0, 0.6, top + 0.8), [(1.5, 0), (1.5, 0.1)], G, C3, n=14)
    for k, (z, r) in enumerate(((2.4, 0.8), (3.8, 1.1), (5.4, 1.4), (7.0, 1.2))):
        rock_f(f"Steam Puff {k}", V(0.2 * math.sin(k), 0.6, top + z), (r, r, r * 0.9), STEAM, C3, rough=0.15, subd=2)
    for k in range(5):
        crystal(f"Geyser Crystal {k}", V(rnd.uniform(-2.6, 2.6), rnd.uniform(-0.8, 2.6), top + 0.8), V(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), 1), rnd.uniform(1.2, 2.4), 0.35, GL, C3, sides=6)
    for s in (-1, 1):
        abox(f"Pump Block {s}", s * 3.4 - 0.9, s * 3.4 + 0.9, -1.0, 1.6, top, top + 2.2, P, C2)
        path_tube(f"Pressure Pipe {s}", [V(s * 3.4, 0.3, top + 2.2), V(s * 3.4, 0.3, top + 3.2), V(s * 2.2, 0.6, top + 3.4), V(s * 1.6, 0.6, top + 1.4)], [0.22] * 4, P2, C4, n=8)
        cyl(f"Gauge {s}", V(s * 3.4, -1.0, top + 1.4), V(s * 3.4, -1.2, top + 1.4), 0.4, 0.4, P2, C4, n=14, hint=Z_AX)
        cyl(f"Gauge Face {s}", V(s * 3.4, -1.2, top + 1.4), V(s * 3.4, -1.25, top + 1.4), 0.32, 0.32, A, C3, n=14, hint=Z_AX)
    beam("Ore Spout", V(0, -1.2, top + 2.0), V(0, -3.0, top + 1.4), 0.9, 0.2, X_AX, P2, C4)
    ore_cube(V(0, -3.4, top + 1.0), O, C3, size=0.8)
else:        # Hive Extractor: honeycomb tower of hex cells, glowing honey, wax drips, bee drones
    P, P2, G, GL, A, O = kit((48, 40, 28), (255, 190, 40), (255, 240, 160))
    WAX = M("Honeycomb Wax", (230, 170, 50), rough=0.4)
    top = footing(P, P2, A, 8, 8)
    for row in range(5):
        for col in range(4 - row % 2):
            x = -1.95 + col * 1.3 + (0.65 if row % 2 else 0)
            z = top + 0.6 + row * 1.1
            lathe(f"Hex Cell {row}{col}", V(x, 0.4, z), [(0.72, 0), (0.72, 0.01)], P, C2, n=6, smooth=False) if False else None
            C = V(x, 0.4, z)
            ring = [C + V(0.7 * math.cos(math.pi / 6 + k * math.pi / 3), 0, 0.7 * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
            finish(f"Hex Cell {row}{col}", loft([[p + V(0, -0.8, 0) for p in ring], [p + V(0, 0.8, 0) for p in ring]], smooth_sides=False), WAX if (row + col) % 3 else P2, C2, merge=0)
            inner = [C + V(0.48 * math.cos(math.pi / 6 + k * math.pi / 3), -0.82, 0.48 * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
            finish(f"Honey {row}{col}", loft([inner, [p + V(0, -0.03, 0) for p in inner]], smooth_sides=False), G if (row + col) % 2 else A, C3, merge=0)
    for s in (-1, 1):
        abox(f"Frame {s}", s * 2.9 - 0.3, s * 2.9 + 0.3, -0.6, 1.4, top, top + 6.4, P, C2)
    abox("Frame Top", -3.2, 3.2, -0.6, 1.4, top + 6.4, top + 7.0, P, C2)
    for k in range(4):
        cone(f"Wax Drip {k}", V(-1.5 + k, -0.45, top + 6.4), V(-1.5 + k, -0.45, top + 5.7 - 0.2 * (k % 2)), 0.12, WAX, C4, n=6)
    for k, (x, z) in enumerate(((-3.6, 5.2), (3.8, 4.0), (2.6, 7.6))):
        B = V(x, -0.8, top + z)
        ellip(f"Bee Drone {k}", B, 0.45, 0.3, 0.3, A, C4, n=10, m=4)
        for j in range(3):
            torus(f"Bee Stripe {k}{j}", B + V(-0.2 + 0.2 * j, 0, 0), X_AX, Z_AX, 0.28, 0.04, P, C4, n_major=10, n_minor=4)
        for s in (-1, 1):
            blade(f"Bee Wing {k}{s}", [B + V(0, 0, 0.2), B + V(-0.3, s * 0.6, 0.6), B + V(0.3, s * 0.6, 0.6)], 0.02, GL, C4)
    beam("Honey Spout", V(0, -0.6, top + 1.2), V(0, -2.4, top + 0.8), 0.8, 0.15, X_AX, P2, C4)
    ore_cube(V(0, -2.9, top + 0.6), O, C3, size=0.7)

finish_mine(bg=(0.02, 0.02, 0.03), tint=(0.95, 0.95, 1.0))
