"""Nine more original furnaces. Run with --f <1-9>. Front-intake ones take ore straight in at ground level;
ramp ones have a conveyor ramp. Each writes .blend, _Roblox.fbx and _RobloxSetup.lua (colours, lights, sell script,
conveyor push). mine_kit + furnace_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *

F = int(arg("--f", 1))
NAMES = {1: "TreasureChestFurnace", 2: "WitchCauldronFurnace", 3: "RecyclerFurnace", 4: "SnowGlobeFurnace", 5: "FairyRingFurnace",
         6: "MeteorCraterFurnace", 7: "HourglassFurnace", 8: "LighthouseFurnace", 9: "JackpotFurnace"}
NAME = NAMES[F]
C1, C2, C3, C4 = begin(NAME, ["Base", "Body", "Glow", "Details"], seed=600 + F)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
rnd = random.Random(600 + F)
def clear(m, w=1.0):
    """See-through glass in the Blender renders (Roblox uses Glass + transparency)."""
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            for key in ("Transmission Weight", "Transmission"):
                if key in n.inputs:
                    n.inputs[key].default_value = w
            n.inputs["Roughness"].default_value = 0.02
    return m
def burn(glow):
    return M("Burn Zone", glow, rough=0.2, glow=glow, glow_strength=1.0, rbx="ForceField", alpha=0.7)
FRONT = (-2.3, 2.3, -3.6, -1.2, 0.05, 2.2)                  # front intake sell box

if F == 1:   # Treasure Chest: giant open chest on a sandy islet, glowing gold inside, coins spilling out the front
    SAND = M("Sand", (222, 196, 140), rough=0.95, rbx="Sand"); WOOD = M("Chest Wood (Wood)", (120, 74, 40), rough=0.8, rbx="WoodPlanks", noise=((96, 56, 28), (146, 94, 54), 4.0, 0.3))
    GOLD = M("Gold (Metal)", (245, 196, 70), rough=0.2, metal=1.0, rbx="Metal"); GLOW = M("Treasure Glow", (255, 220, 100), rough=0.3, glow=(255, 190, 40), glow_strength=4.0, rbx="Neon", light=(16, 2.2))
    GEM = M("Ruby", (230, 30, 60), rough=0.1, glow=(200, 10, 40), glow_strength=1.0, rbx="Glass", alpha=0.1); PALM = M("Palm Leaf", (60, 150, 60), rough=0.6)
    ellip("Islet", V(0, 0.8, 0), 7.2, 6.8, 0.4, SAND, C1, n=28, m=3, half=True)
    abox("Chest Back", -3.6, 3.6, 0.2, 3.4, 0.0, 3.6, WOOD, C2)
    for s in (-1, 1):
        abox(f"Chest Side {s}", min(s * 2.6, s * 3.6), max(s * 2.6, s * 3.6), -3.0, 0.2, 0.0, 3.6, WOOD, C2)
        for x in (s * 3.0,):
            abox(f"Corner Band {s}", x - 0.62, x + 0.62, -3.05, -2.8, 0.0, 3.6, GOLD, C2)
    abox("Chest Lintel", -2.6, 2.6, -3.0, 0.2, 2.4, 3.6, WOOD, C2)
    abox("Treasure Glow Back", -2.6, 2.6, 0.05, 0.2, 0.0, 2.4, GLOW, C3)
    for k in range(4):
        abox(f"Gold Band {k}", -3.65, 3.65, -3.05 + k * 2.1, -2.75 + k * 2.1, 3.5, 3.7, GOLD, C2) if k < 3 else None
    hexa("Chest Lid", [V(-3.7, 3.3, 3.6), V(3.7, 3.3, 3.6), V(3.7, 3.6, 3.6), V(-3.7, 3.6, 3.6),
                       V(-3.7, 5.2, 8.2), V(3.7, 5.2, 8.2), V(3.7, 5.5, 8.2), V(-3.7, 5.5, 8.2)], WOOD, C2)
    for k in range(3):
        a = -1.8 + k * 1.8
        abox(f"Lid Band {k}", a - 0.25, a + 0.25, 3.2, 3.7, 3.6, 3.8, GOLD, C2)
    obox("Lock Plate", V(0, -3.08, 3.0), (1.0, 0.1, 1.0), X_AX, Y_AX, Z_AX, GOLD, C2)
    for k in range(18):
        p = V(rnd.uniform(-2.2, 2.2), rnd.uniform(-1.5, 0.0), 0.1 + rnd.uniform(0, 0.5))
        cyl(f"Coin {k}", p, p + V(0, 0, 0.06), 0.22, 0.22, GOLD, C4, n=10)
    for k in range(10):
        p = V(rnd.uniform(-3, 3), rnd.uniform(-5.2, -3.4), 0.12)
        cyl(f"Spilled Coin {k}", p, p + V(0, 0, 0.05), 0.22, 0.22, GOLD, C4, n=10)
    for k in range(4):
        crystal(f"Treasure Gem {k}", V(-1.6 + k * 1.1, -0.6, 0.6), V(0.2 * (k - 1.5), -0.3, 1), 0.6, 0.18, GEM, C4)
    T = V(5.0, 3.8, 0.3)
    path_tube("Palm Trunk", [T, T + V(-0.4, 0.2, 2.5), T + V(-1.2, 0.0, 4.6)], [0.25, 0.2, 0.15], WOOD, C4, n=8)
    for k in range(6):
        a = k * math.pi / 3;d = V(math.cos(a), math.sin(a), 0);c = T + V(-1.2, 0.0, 4.6)
        blade(f"Palm Frond {k}", [c, c + d * 1.0 + V(-d.y, d.x, 0) * 0.35 + V(0, 0, 0.2), c + d * 2.0 + V(0, 0, -0.7), c + d * 1.0 - V(-d.y, d.x, 0) * 0.35 + V(0, 0, 0.2)], 0.04, PALM, C4)
    burn_zone(burn((255, 220, 100)), *FRONT, C3)
elif F == 2: # Witch Cauldron: huge bubbling cauldron over purple fire, ramp up to its rim, broomstick, potion shelf
    STONE = M("Hearth Stone", (90, 86, 96), rough=0.9, rbx="Slate", noise=((66, 62, 72), (116, 112, 122), 3.0, 0.4))
    IRON = M("Cauldron Iron (Metal)", (40, 38, 44), rough=0.4, metal=0.9, rbx="Metal"); BREW = M("Witch Brew", (120, 255, 90), rough=0.1, glow=(80, 255, 40), glow_strength=4.0, rbx="Neon", light=(16, 2.0))
    FIRE = M("Witch Fire", (190, 80, 255), rough=0.3, glow=(160, 40, 255), glow_strength=5.0, rbx="Neon", light=(10, 1.4)); WOOD = M("Broom Wood (Wood)", (110, 74, 44), rough=0.8, rbx="Wood")
    STRAW = M("Straw", (210, 180, 90), rough=0.8); BOT = [M("Potion Pink", (255, 80, 180), rough=0.1, rbx="Glass", alpha=0.2), M("Potion Blue", (80, 160, 255), rough=0.1, rbx="Glass", alpha=0.2)]
    CONVM = M("Conveyor", (60, 52, 66), rough=0.6, rbx="DiamondPlate", plate=12.0)
    lathe("Hearth", V(0, 0.4, 0), [(6.8, 0), (6.8, 0.4), (6.4, 0.6), (0.01, 0.6)], STONE, C1, n=16, smooth=False)
    conveyor_ramp(CONVM, FIRE, STONE, FIRE, y_front=-10.0, y_lip=-4.2, y_end=-2.2, rz=2.6, coll=C1)
    lathe("Cauldron", V(0, 0.6, 0.6), [(1.6, 0), (2.9, 0.6), (3.3, 1.4), (3.2, 2.0), (3.0, 2.3), (3.3, 2.6), (2.85, 2.6), (2.7, 2.2)], IRON, C2, n=28)
    lathe("Brew", V(0, 0.6, 2.85), [(2.7, 0), (2.7, 0.15)], BREW, C3, n=28)
    for k in range(6):
        dot(f"Bubble {k}", V(rnd.uniform(-1.8, 1.8), 0.6 + rnd.uniform(-1.6, 1.6), 3.1 + rnd.uniform(0, 0.3)), rnd.uniform(0.15, 0.3), BREW, C3)
    for k in range(4):
        dot(f"Steam {k}", V(rnd.uniform(-1, 1), 0.6 + rnd.uniform(-1, 1), 4.0 + k * 0.8), 0.35 + 0.1 * k, BREW, C3)
    for k in range(6):
        a = 2 * math.pi * k / 6
        cone(f"Witch Flame {k}", V(2.6 * math.cos(a), 0.6 + 2.6 * math.sin(a), 0.6), V(2.9 * math.cos(a), 0.6 + 2.9 * math.sin(a), 1.8), 0.45, FIRE, C3, n=6)
        cyl(f"Fire Log {k}", V(1.6 * math.cos(a), 0.6 + 1.6 * math.sin(a), 0.65), V(3.4 * math.cos(a), 0.6 + 3.4 * math.sin(a), 0.65), 0.2, 0.2, WOOD, C4, n=6)
    for s in (-1, 1):
        cyl(f"Cauldron Leg {s}", V(s * 2.0, 1.8, 0.6), V(s * 2.2, 2.2, 1.4), 0.25, 0.2, IRON, C2, n=6)
    B = V(4.8, 3.0, 0.6)
    cyl("Broom Handle", B, B + V(-0.4, 0.3, 4.6), 0.1, 0.08, WOOD, C4, n=6)
    cyl("Broom Bristles", B + V(0, 0, -0.0), B + V(0.1, -0.1, 1.4), 0.55, 0.15, STRAW, C4, n=10)
    abox("Potion Shelf", -6.0, -4.2, 2.2, 3.0, 0.6, 3.6, WOOD, C4)
    for k in range(3):
        for j in range(2):
            lathe(f"Potion {k}{j}", V(-5.6 + j * 0.9, 2.6, 1.0 + k * 1.0), [(0.25, 0), (0.3, 0.3), (0.1, 0.55), (0.1, 0.7)], BOT[(k + j) % 2], C4, n=10)
    burn_zone(burn((120, 255, 90)), -2.4, 2.4, -1.8, 3.0, 2.85, 3.8, C3)
elif F == 3: # Recycler: big recycling machine, green arrow emblem, rotating crusher drum in a front hatch at ground level
    BODY = M("Recycler Green", (60, 150, 80), rough=0.4, metal=0.3); P = M("Steel Plate (DiamondPlate)", (120, 126, 134), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
    DARK = M("Hatch Dark", (24, 26, 30), rough=0.5); GLOW = M("Recycle Glow", (120, 255, 140), rough=0.2, glow=(70, 255, 100), glow_strength=4.5, rbx="Neon", light=(14, 1.8))
    HAZ = M("Hazard Yellow", (240, 196, 20), rough=0.45); WHITE = M("Emblem White", (240, 244, 240), rough=0.4)
    abox("Concrete Pad", -6.0, 6.0, -5.4, 5.0, 0.0, 0.2, P, C1)
    abox("Machine Back", -4.2, 4.2, -0.6, 3.8, 0.2, 7.0, BODY, C2)
    for s in (-1, 1):
        abox(f"Machine Side {s}", min(s * 2.6, s * 4.2), max(s * 2.6, s * 4.2), -3.4, -0.6, 0.2, 7.0, BODY, C2)
    abox("Hatch Top", -2.6, 2.6, -3.4, -0.6, 2.6, 7.0, BODY, C2)
    abox("Hatch Frame", -2.9, 2.9, -3.55, -3.4, 0.2, 2.9, HAZ, C2)
    abox("Hatch Inside", -2.6, 2.6, -0.75, -0.6, 0.2, 2.6, DARK, C2)
    for k in range(2):
        cyl(f"Crusher Drum {k}", V(-2.5, -1.8 + k * 0.6, 2.2 - k * 0.2), V(2.5, -1.8 + k * 0.6, 2.2 - k * 0.2), 0.32, 0.32, P, C2, n=12, hint=Z_AX)
    abox("Hatch Glow", -2.6, 2.6, -1.0, -0.8, 0.2, 1.0, GLOW, C3)
    for k in range(3):                                      # recycle arrows emblem
        a = math.radians(90 + 120 * k)
        c = V(0, -3.42, 4.8) + V(math.cos(a), 0, math.sin(a)) * 1.0
        t = V(-math.sin(a), 0, math.cos(a))
        beam(f"Emblem Arm {k}", c - t * 0.6, c + t * 0.4, 0.32, 0.06, Y_AX, GLOW, C3)
        blade(f"Emblem Arrow {k}", [c + t * 0.4 + V(math.cos(a), 0, math.sin(a)) * 0.35 + V(0, -0.03, 0), c + t * 0.95 + V(0, -0.03, 0), c + t * 0.4 - V(math.cos(a), 0, math.sin(a)) * 0.35 + V(0, -0.03, 0)], 0.06, GLOW, C3)
    abox("Emblem Panel", -1.9, 1.9, -3.44, -3.38, 3.4, 6.2, WHITE, C2)
    for s in (-1, 1):
        cyl(f"Exhaust {s}", V(s * 3.0, 2.0, 7.0), V(s * 3.0, 2.0, 9.0), 0.4, 0.4, P, C4, n=10)
        dot(f"Exhaust Light {s}", V(s * 3.0, 2.0, 9.2), 0.3, GLOW, C3)
        for k in range(4):
            abox(f"Side Stripe {s}{k}", min(s * 4.2, s * 4.24), max(s * 4.2, s * 4.24), -3.0 + k * 1.6, -2.4 + k * 1.6, 1.0, 1.4, HAZ, C2)
    for k, (x, y, mat) in enumerate(((-5.0, -3.0, BODY), (5.0, -3.4, P), (5.2, 2.6, BODY))):
        lathe(f"Bin {k}", V(x, y, 0.2), [(0.7, 0), (0.85, 1.6), (0.9, 1.7)], mat, C4, n=10, smooth=False)
        dot(f"Bin Light {k}", V(x, y - 0.85, 1.3), 0.12, GLOW, C3)
    burn_zone(burn((120, 255, 140)), *FRONT, C3)
elif F == 4: # Snow Globe: giant glass globe with a tiny snowy village on a wooden base; ore enters the drawer slot at the front
    WOOD = M("Globe Base (Wood)", (110, 64, 36), rough=0.5, rbx="Wood"); GOLD = M("Gold Trim (Metal)", (240, 190, 70), rough=0.2, metal=1.0, rbx="Metal")
    GLASS = clear(M("Globe Glass", (230, 245, 255), rough=0.02, rbx="Glass", alpha=0.7)); SNOW = M("Snow", (245, 250, 255), rough=0.8, rbx="Snow")
    GLOW = M("Drawer Glow", (160, 220, 255), rough=0.3, glow=(110, 200, 255), glow_strength=4.0, rbx="Neon", light=(14, 1.8))
    RED = M("House Red", (200, 50, 50), rough=0.5); TREE = M("Pine", (40, 110, 60), rough=0.6); WARM = M("Window Warm", (255, 210, 120), rough=0.3, glow=(255, 180, 60), glow_strength=4.0, rbx="Neon")
    lathe("Globe Base", V(0, 0.6, 0), [(4.6, 0), (4.6, 0.4), (4.2, 0.6), (3.6, 2.4), (3.8, 2.6), (3.2, 2.7)], WOOD, C1, n=28)
    torus("Base Trim", V(0, 0.6, 2.55), Z_AX, Y_AX, 3.75, 0.08, GOLD, C1, n_major=36, n_minor=4)
    abox("Drawer Recess", -2.4, 2.4, -3.9, -1.0, 0.0, 2.2, WOOD, C2) if False else None
    abox("Drawer Glow", -2.3, 2.3, -1.1, -0.9, 0.05, 2.1, GLOW, C3)
    abox("Drawer Frame", -2.6, 2.6, -4.6, -3.6, 2.2, 2.6, GOLD, C2)
    for s in (-1, 1):
        abox(f"Drawer Post {s}", min(s * 2.4, s * 2.8), max(s * 2.4, s * 2.8), -4.6, -1.0, 0.0, 2.6, GOLD, C2)
    G0 = V(0, 0.6, 6.0)
    ellip("Globe Glass", G0, 3.4, 3.4, 3.4, GLASS, C2, n=28, m=10)
    ellip("Snow Ground", G0 + V(0, 0, -2.4), 2.4, 2.4, 0.5, SNOW, C4, n=20, m=3, half=True)
    for k, (dx, dy, h) in enumerate(((-0.9, 0.2, 1.0), (0.8, -0.3, 0.8))):
        H = G0 + V(dx, dy, -2.0)
        abox(f"House {k}", H.x - 0.45, H.x + 0.45, H.y - 0.4, H.y + 0.4, H.z, H.z + h * 0.8, RED, C4)
        hexa(f"House Roof {k}", [V(H.x - 0.55, H.y - 0.5, H.z + h * 0.8), V(H.x + 0.55, H.y - 0.5, H.z + h * 0.8), V(H.x + 0.55, H.y + 0.5, H.z + h * 0.8), V(H.x - 0.55, H.y + 0.5, H.z + h * 0.8),
                                 V(H.x - 0.05, H.y - 0.5, H.z + h * 1.3), V(H.x + 0.05, H.y - 0.5, H.z + h * 1.3), V(H.x + 0.05, H.y + 0.5, H.z + h * 1.3), V(H.x - 0.05, H.y + 0.5, H.z + h * 1.3)], SNOW, C4)
        abox(f"House Window {k}", H.x - 0.15, H.x + 0.15, H.y - 0.42, H.y - 0.4, H.z + 0.3, H.z + 0.55, WARM, C4)
    for k, (dx, dy) in enumerate(((0.2, 1.2), (-1.6, -0.9), (1.5, 0.9))):
        cone(f"Pine {k}", G0 + V(dx, dy, -2.2), G0 + V(dx, dy, -0.6), 0.45, TREE, C4, n=8)
    for k in range(18):
        a = rnd.uniform(0, 6.28);r = rnd.uniform(0.3, 2.8);z = rnd.uniform(-1.5, 2.6)
        if r * r + z * z > 9: continue
        dot(f"Snowflake {k}", G0 + V(r * math.cos(a), r * math.sin(a), z), 0.07, SNOW, C4)
    burn_zone(burn((160, 220, 255)), -2.3, 2.3, -4.5, -1.2, 0.05, 2.1, C3)
elif F == 5: # Fairy Ring: a circle of giant glowing mushrooms around a shimmering pool; ore rolls in between the front caps
    MOSS = M("Moss", (70, 130, 60), rough=0.9, rbx="Grass"); STEM = M("Mushroom Stem", (236, 226, 210), rough=0.6)
    CAPS = [M("Cap Pink", (255, 120, 190), rough=0.4, glow=(255, 80, 170), glow_strength=0.6), M("Cap Blue", (90, 170, 255), rough=0.4, glow=(60, 140, 255), glow_strength=0.6),
            M("Cap Purple", (170, 100, 255), rough=0.4, glow=(140, 70, 255), glow_strength=0.6)]
    DOTS = M("Cap Dots", (255, 250, 240), rough=0.5); POOL = M("Fairy Pool", (200, 160, 255), rough=0.05, glow=(170, 120, 255), glow_strength=3.5, rbx="Neon", light=(16, 2.0))
    SPARK = M("Fairy Light", (255, 250, 200), rough=0.3, glow=(255, 240, 160), glow_strength=6.0, rbx="Neon", light=(6, 0.8)); WING = M("Fairy Wing", (200, 240, 255), rough=0.1, rbx="Glass", alpha=0.4)
    ellip("Moss Mound", V(0, 0.4, 0), 7.0, 6.8, 0.3, MOSS, C1, n=28, m=3, half=True)
    lathe("Fairy Pool", V(0, 0.4, 0.05), [(3.0, 0), (3.0, 0.3)], POOL, C3, n=28)
    for k in range(10):
        a = math.radians(-60 + k * 30)
        if -110 < math.degrees(a) % 360 - 270 < -70 + 40 and 250 < math.degrees(a) % 360 < 290: continue
        if 255 < math.degrees(a) % 360 < 285: continue
        p = V(4.0 * math.cos(a), 0.4 + 4.0 * math.sin(a), 0.2)
        h = 1.6 + 1.6 * (0.5 + 0.5 * math.sin(a))
        cyl(f"Stem {k}", p, p + V(0, 0, h), 0.4, 0.3, STEM, C2, n=10)
        ellip(f"Cap {k}", p + V(0, 0, h), 1.3, 1.3, 0.75, CAPS[k % 3], C2, n=16, m=4, half=True)
        for j in range(3):
            b = j * 2.1 + k
            dot(f"Cap Dot {k}{j}", p + V(0.8 * math.cos(b), 0.8 * math.sin(b), h + 0.5), 0.14, DOTS, C2)
    for k in range(8):
        P0 = V(rnd.uniform(-3.5, 3.5), rnd.uniform(-2.5, 4.0), rnd.uniform(2.5, 5.5))
        dot(f"Fairy {k}", P0, 0.15, SPARK, C3)
        if k % 2 == 0:
            for s in (-1, 1):
                blade(f"Fairy Wing {k}{s}", [P0, P0 + V(s * 0.4, 0.05, 0.3), P0 + V(s * 0.35, 0.05, -0.1)], 0.02, WING, C3)
    for k in range(12):
        a = rnd.uniform(0, 6.28);r = rnd.uniform(5.2, 6.4)
        if math.sin(a) < -0.5: continue
        cyl(f"Tiny Shroom {k}", V(r * math.cos(a), 0.4 + r * math.sin(a), 0.1), V(r * math.cos(a), 0.4 + r * math.sin(a), 0.6), 0.08, 0.06, STEM, C4, n=6)
        ellip(f"Tiny Cap {k}", V(r * math.cos(a), 0.4 + r * math.sin(a), 0.6), 0.3, 0.3, 0.18, CAPS[k % 3], C4, n=8, m=2, half=True)
    burn_zone(burn((200, 160, 255)), -2.6, 2.6, -2.4, 3.0, 0.1, 1.6, C3)
elif F == 6: # Meteor Crater: a glowing meteor sits in a smoking crater; ore rolls down the crater lip at the front into the molten core
    ROCK = M("Crater Rock", (84, 72, 64), rough=0.9, rbx="Slate", noise=((60, 50, 44), (110, 96, 86), 3.0, 0.5))
    METEOR = M("Meteor Crust", (40, 32, 34), rough=0.7, rbx="Basalt"); CORE = M("Meteor Core", (255, 120, 40), rough=0.3, glow=(255, 80, 10), glow_strength=4.5, rbx="Neon", light=(18, 2.4))
    ICE = M("Space Crystal", (130, 220, 255), rough=0.05, glow=(80, 190, 255), glow_strength=1.2, rbx="Glass", alpha=0.15, light=(8, 0.8)); SMOKE = M("Smoke", (90, 86, 86), rough=0.9, alpha=0.25)
    for k in range(16):
        a = 2 * math.pi * k / 16
        if 250 < math.degrees(a) < 290: continue
        rock_f(f"Crater Rim {k}", V(4.6 * math.cos(a), 0.6 + 4.6 * math.sin(a), 0.6), (1.5, 1.2, 0.9 + 0.3 * (k % 3)), ROCK, C1, rough=0.3)
    lathe("Crater Floor", V(0, 0.6, 0), [(4.4, 0.2), (3.0, 0.05), (0.01, 0.0)], ROCK, C1, n=20, smooth=False)
    lathe("Molten Pool", V(0, 0.6, 0.06), [(2.8, 0), (2.8, 0.12)], CORE, C3, n=20)
    rock_f("Meteor", V(0.4, 1.8, 2.4), (1.8, 1.6, 1.5), METEOR, C2, rough=0.25, subd=2)
    for k in range(6):
        a = rnd.uniform(0, 6.28)
        path_tube(f"Meteor Crack {k}", [V(0.4, 1.8, 2.4) + V(math.cos(a), math.sin(a), rnd.uniform(-0.5, 0.5)).normalized() * r for r in (1.3, 1.65)], [0.12, 0.06], CORE, C3, n=5)
    for k, (dz, r) in enumerate(((4.2, 0.8), (5.4, 1.1), (6.8, 1.3))):
        rock_f(f"Smoke {k}", V(0.4 - 0.4 * k, 1.8 + 0.3 * k, dz), (r, r, r * 0.8), SMOKE, C4, rough=0.2, subd=2)
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.4
        if 230 < math.degrees(a) % 360 < 310: continue
        crystal(f"Space Crystal {k}", V(5.6 * math.cos(a), 0.6 + 5.6 * math.sin(a), 0.6), V(math.cos(a) * 0.4, math.sin(a) * 0.4, 1), 1.8, 0.4, ICE, C4, sides=6)
    for k in range(8):
        dot(f"Ember {k}", V(rnd.uniform(-3, 3), rnd.uniform(-1, 3.5), rnd.uniform(1, 5)), 0.08, CORE, C3)
    burn_zone(burn((255, 120, 40)), -2.6, 2.6, -2.2, 3.2, 0.1, 1.6, C3)
elif F == 7: # Hourglass: a giant ornate hourglass on a pedestal; glowing sand falls; ore enters the pedestal slot at the front
    WOOD = M("Dark Wood (Wood)", (70, 42, 26), rough=0.5, rbx="Wood"); GOLD = M("Gold (Metal)", (240, 190, 70), rough=0.2, metal=1.0, rbx="Metal")
    GLASS = clear(M("Hourglass Glass", (230, 245, 255), rough=0.02, rbx="Glass", alpha=0.7)); SAND = M("Time Sand", (255, 210, 120), rough=0.4, glow=(255, 180, 60), glow_strength=2.5, rbx="Neon", light=(14, 1.8))
    GLOW = M("Slot Glow", (255, 200, 90), rough=0.3, glow=(255, 170, 40), glow_strength=4.0, rbx="Neon", light=(12, 1.6)); STONE = M("Pedestal Marble (Marble)", (230, 226, 216), rough=0.3, marble=((220, 216, 206), (190, 160, 100)))
    abox("Pedestal", -4.2, 4.2, -3.6, 4.0, 0.0, 2.6, STONE, C1)
    abox("Pedestal Top", -4.5, 4.5, -3.9, 4.3, 2.6, 3.0, GOLD, C1)
    abox("Slot Back", -2.5, 2.5, -1.2, -1.0, 0.0, 2.2, GLOW, C3)
    abox("Slot Cut Top", -2.5, 2.5, -3.62, -1.0, 2.2, 2.6, STONE, C1) if False else None
    for s in (-1, 1):
        abox(f"Slot Pillar {s}", min(s * 2.5, s * 2.9), max(s * 2.5, s * 2.9), -3.7, -3.5, 0.0, 2.6, GOLD, C1)
    H0 = V(0, 0.4, 3.0)
    for z in (0.0, 7.6):
        lathe(f"Frame Disc {z}", H0 + V(0, 0, z), [(3.0, 0), (3.0, 0.5), (0.01, 0.5)], WOOD, C2, n=24)
        torus(f"Frame Trim {z}", H0 + V(0, 0, z + 0.25), Z_AX, Y_AX, 3.0, 0.1, GOLD, C2, n_major=24, n_minor=4)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        cyl(f"Frame Post {k}", H0 + V(2.5 * math.cos(a), 2.5 * math.sin(a), 0.5), H0 + V(2.5 * math.cos(a), 2.5 * math.sin(a), 7.6), 0.25, 0.25, WOOD, C2, n=10)
        for z in (2.0, 5.6):
            torus(f"Post Ring {k}{z}", H0 + V(2.5 * math.cos(a), 2.5 * math.sin(a), z), Z_AX, Y_AX, 0.3, 0.06, GOLD, C2, n_major=10, n_minor=4)
    lathe("Hourglass", H0 + V(0, 0, 0.5), [(2.0, 0), (2.0, 0.6), (1.6, 2.2), (0.3, 3.55), (0.3, 3.65), (1.6, 5.0), (2.0, 6.5), (2.0, 7.1)], GLASS, C2, n=24)
    lathe("Bottom Sand", H0 + V(0, 0, 0.55), [(1.9, 0), (1.85, 0.6), (1.2, 1.5), (0.01, 1.9)], SAND, C3, n=20)
    lathe("Top Sand", H0 + V(0, 0, 4.4), [(0.6, 0), (1.3, 0.7), (1.6, 1.5), (0.01, 1.6)], SAND, C3, n=20)
    cyl("Sand Stream", H0 + V(0, 0, 4.4), H0 + V(0, 0, 2.4), 0.06, 0.06, SAND, C3, n=6)
    burn_zone(burn((255, 200, 90)), -2.4, 2.4, -3.8, -1.2, 0.05, 2.1, C3)
elif F == 8: # Lighthouse: a striped lighthouse on a rocky outcrop; ore rolls through the glowing front door at ground level
    ROCK = M("Shore Rock", (100, 96, 92), rough=0.9, rbx="Slate", noise=((76, 72, 68), (126, 122, 116), 3.0, 0.5)); WHITE = M("Tower White", (240, 240, 236), rough=0.5)
    RED = M("Tower Red", (200, 40, 40), rough=0.5); BLACK = M("Lantern Iron (Metal)", (36, 36, 40), rough=0.4, metal=0.8, rbx="Metal")
    BEAM = M("Lighthouse Beam", (255, 250, 200), rough=0.3, glow=(255, 240, 160), glow_strength=5.0, rbx="Neon", light=(22, 2.6)); DOOR = M("Door Glow", (255, 210, 120), rough=0.3, glow=(255, 180, 60), glow_strength=4.0, rbx="Neon", light=(12, 1.6))
    SEA = M("Shallows", (60, 150, 180), rough=0.05, rbx="Glass", alpha=0.2)
    ellip("Shallows", V(0, 0.6, 0), 7.4, 7.0, 0.15, SEA, C1, n=28, m=2, half=True)
    for k in range(12):
        a = 2 * math.pi * k / 12
        if 250 < math.degrees(a) < 290: continue
        rock_f(f"Outcrop {k}", V(4.4 * math.cos(a), 1.2 + 4.0 * math.sin(a), 0.4), (1.4, 1.2, 0.8), ROCK, C1, rough=0.3)
    T = V(0, 1.4, 0)
    for k in range(5):
        z0 = k * 2.0;r0 = 3.0 - 0.3 * k;r1 = 3.0 - 0.3 * (k + 1)
        lathe(f"Tower Band {k}", T + V(0, 0, z0), [(r0, 0), (r1, 2.0)], RED if k % 2 else WHITE, C2, n=24, smooth=False)
    lathe("Gallery", T + V(0, 0, 10.0), [(2.0, 0), (2.6, 0.2), (2.6, 0.4), (1.6, 0.4)], BLACK, C2, n=24, smooth=False)
    for k in range(16):
        a = 2 * math.pi * k / 16
        cyl(f"Rail Post {k}", T + V(2.5 * math.cos(a), 2.5 * math.sin(a), 10.4), T + V(2.5 * math.cos(a), 2.5 * math.sin(a), 11.2), 0.04, 0.04, BLACK, C2, n=4)
    torus("Gallery Rail", T + V(0, 0, 11.2), Z_AX, Y_AX, 2.5, 0.05, BLACK, C2, n_major=24, n_minor=4)
    cyl("Lantern Glass", T + V(0, 0, 10.4), T + V(0, 0, 12.2), 1.3, 1.3, BEAM, C3, n=16)
    lathe("Lantern Roof", T + V(0, 0, 12.2), [(1.7, 0), (1.0, 0.8), (0.2, 1.4), (0.01, 1.8)], RED, C2, n=16)
    for s in (-1, 1):
        cyl(f"Light Beam {s}", T + V(0, 0, 11.3), T + V(s * 5.0, -2.5, 11.0), 0.2, 0.55, BEAM, C3, n=10)
    abox("Door Arch", -2.4, 2.4, -2.0, -1.0, 0.0, 2.6, WHITE, C2) if False else None
    abox("Door Glow", -2.2, 2.2, -0.5, -0.3, 0.0, 2.4, DOOR, C3)
    abox("Door Lintel", -2.6, 2.6, -2.6, -0.4, 2.4, 3.0, BLACK, C2)
    for s in (-1, 1):
        abox(f"Door Post {s}", min(s * 2.3, s * 2.7), max(s * 2.3, s * 2.7), -2.6, -0.4, 0.0, 2.4, BLACK, C2)
    burn_zone(burn((255, 210, 120)), -2.1, 2.1, -3.4, -0.6, 0.05, 2.2, C3)
else:        # Jackpot: a giant slot machine with spinning-reel screen, lever and lights; ore drops into the payout tray at the front
    RED = M("Cabinet Red", (200, 30, 40), rough=0.35, metal=0.3); GOLD = M("Gold (Metal)", (245, 196, 70), rough=0.2, metal=1.0, rbx="Metal")
    REEL = M("Reel White", (250, 248, 240), rough=0.4); DARK = M("Tray Dark", (30, 24, 26), rough=0.5)
    BULB = M("Marquee Bulbs", (255, 240, 160), rough=0.3, glow=(255, 220, 100), glow_strength=5.0, rbx="Neon", light=(8, 1.0)); GLOW = M("Payout Glow", (255, 220, 100), rough=0.3, glow=(255, 190, 40), glow_strength=4.0, rbx="Neon", light=(14, 1.8))
    SYM = [M("Symbol Cherry", (230, 30, 50), rough=0.4, glow=(230, 20, 40), glow_strength=1.0), M("Symbol Seven", (255, 200, 30), rough=0.4, glow=(255, 180, 20), glow_strength=1.0), M("Symbol Bell", (60, 160, 255), rough=0.4, glow=(40, 140, 255), glow_strength=1.0)]
    CARPET = M("Casino Carpet", (110, 20, 40), rough=0.9, rbx="Fabric", noise=((80, 10, 28), (150, 40, 60), 6.0, 0.2))
    abox("Carpet", -6.0, 6.0, -5.4, 5.0, 0.0, 0.1, CARPET, C1)
    abox("Cabinet Lower", -3.6, 3.6, -0.6, 3.4, 0.1, 3.0, RED, C2)
    for s in (-1, 1):
        abox(f"Cabinet Side {s}", min(s * 2.6, s * 3.6), max(s * 2.6, s * 3.6), -3.2, -0.6, 0.1, 3.0, RED, C2)
    abox("Tray Lip", -2.6, 2.6, -3.3, -3.1, 0.1, 0.5, GOLD, C2)
    abox("Tray Roof", -3.6, 3.6, -3.2, -0.6, 2.4, 3.0, GOLD, C2)
    abox("Payout Glow", -2.6, 2.6, -0.75, -0.6, 0.1, 2.4, GLOW, C3)
    abox("Cabinet Upper", -3.4, 3.4, -1.0, 3.0, 3.0, 8.0, RED, C2)
    abox("Reel Window", -2.8, 2.8, -1.06, -1.0, 4.4, 6.6, GOLD, C2)
    for k in range(3):
        x = -1.8 + k * 1.8
        abox(f"Reel {k}", x - 0.75, x + 0.75, -1.12, -1.06, 4.6, 6.4, REEL, C2)
        dot(f"Reel Symbol {k}", V(x, -1.18, 5.5), 0.45, SYM[k % 3] if k != 1 else SYM[1], C3)
    abox("Marquee", -3.6, 3.6, -1.2, 3.2, 8.0, 9.6, GOLD, C2)
    abox("Marquee Panel", -3.0, 3.0, -1.26, -1.2, 8.3, 9.3, SYM[0], C3)
    for k in range(10):
        dot(f"Bulb {k}", V(-3.4 + k * 0.755, -1.25, 9.7), 0.18, BULB, C3)
    for k in range(5):
        dot(f"Side Bulb L{k}", V(-3.45, -1.05, 3.4 + k * 0.9), 0.15, BULB, C3)
        dot(f"Side Bulb R{k}", V(3.45, -1.05, 3.4 + k * 0.9), 0.15, BULB, C3)
    cyl("Lever Base", V(3.6, 1.0, 5.2), V(4.2, 1.0, 5.2), 0.4, 0.4, GOLD, C4, n=12, hint=Z_AX)
    cyl("Lever Arm", V(4.0, 1.0, 5.2), V(4.2, 0.8, 8.4), 0.12, 0.12, GOLD, C4, n=8)
    dot("Lever Knob", V(4.2, 0.8, 8.6), 0.45, SYM[0], C4)
    for k in range(14):
        p = V(rnd.uniform(-2.2, 2.2), rnd.uniform(-3.0, -1.0), 0.15 + rnd.uniform(0, 0.4))
        cyl(f"Jackpot Coin {k}", p, p + V(0, 0, 0.06), 0.22, 0.22, GOLD, C4, n=10)
    burn_zone(burn((255, 220, 100)), *FRONT, C3)

finish_mine(bg=(0.02, 0.02, 0.028), tint=(0.95, 0.95, 1.0))
write_furnace_lua(NAME)
