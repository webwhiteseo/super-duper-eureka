"""Prism Reactor Furnace - an original Miner's-Haven-style furnace built from the shared traits of classic furnaces:
a low stepped diamond-plate platform, a wide front entry lip, a sunken glowing intake pool where the ore is sold,
chunky angled armour blocks with neon panels, antenna pylons with glowing tips, and a big reactor ring centrepiece
on an arch behind. Built with mine_kit; writes a sell-script setup Lua."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_ARMOUR, C_POOL, C_REACTOR, C_DETAIL = begin("PrismReactorFurnace", ["Platform", "Armour", "Pool", "Reactor", "Details"], seed=41)
PLATE = M("Dark Plate (DiamondPlate)", (58, 60, 66), rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
PLATE2 = M("Steel Plate (DiamondPlate)", (96, 100, 108), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
BLACK = M("Black", (14, 14, 18), rough=0.5)
POOL = M("Prism Pool", (90, 240, 255), rough=0.05, glow=(40, 220, 255), glow_strength=3.0, rbx="Neon", light=(16, 2.0))
GLASS = M("Pool Glass", (170, 240, 255), rough=0.05, glow=(120, 220, 255), glow_strength=0.5, rbx="Glass", alpha=0.5)
TEAL = M("Teal Neon", (60, 255, 220), rough=0.3, glow=(20, 255, 200), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
AMBER = M("Amber Neon", (255, 180, 40), rough=0.3, glow=(255, 150, 20), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
CORE = M("Reactor Core", (220, 255, 255), rough=0.3, glow=(140, 240, 255), glow_strength=8.0, rbx="Neon", light=(20, 2.5))
BURN = M("Burn Zone", (120, 240, 255), rough=0.2, glow=(80, 220, 255), glow_strength=1.0, rbx="ForceField", alpha=0.6)
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)

# ---- stepped platform
slab("Platform Low", chamfer_rect(14.0, 13.0, 1.2), 0.0, chamfer_rect(13.6, 12.6, 1.1), 0.6, PLATE, C_BASE)
slab("Platform Mid", chamfer_rect(11.0, 10.0, 1.0), 0.6, chamfer_rect(10.6, 9.6, 0.9), 1.1, PLATE2, C_BASE)
for k, x in enumerate((-6.5, 6.5)):
    abox(f"Platform Glow {k}", x - 0.05, x + 0.05, -4.0, 4.0, 0.25, 0.4, TEAL, C_BASE)
abox("Front Glow", -5.5, 5.5, -6.32, -6.25, 0.25, 0.4, TEAL, C_BASE)
# conveyor ramp: from the ground up to the pool lip, then flat straight into the pool (no steps)
CONV = M("Conveyor", (30, 32, 38), rough=0.6, rbx="DiamondPlate", plate=12.0)
RZ = 1.3
hexa("Conveyor Slope", [V(-2.5, -8.8, 0), V(2.5, -8.8, 0), V(2.5, -5.0, 0), V(-2.5, -5.0, 0),
                        V(-2.5, -8.8, 0.02), V(2.5, -8.8, 0.02), V(2.5, -5.0, RZ), V(-2.5, -5.0, RZ)], CONV, C_BASE)
abox("Conveyor Flat", -2.5, 2.5, -5.0, -2.95, 0.0, RZ, CONV, C_BASE)
slope = math.atan2(RZ, 3.8)
up = V(0, -math.sin(slope), math.cos(slope));fw = V(0, math.cos(slope), math.sin(slope))
for k in range(4):                                          # glowing chevrons pointing into the furnace
    y = -8.2 + k * 1.3
    z = (y + 8.8) / 3.8 * RZ if y < -5.0 else RZ
    c = V(0, y, z) + (up if y < -5.0 else Z_AX) * 0.02
    f = fw if y < -5.0 else Y_AX
    for sgn in (1, -1):
        obox(f"Chevron {k}{sgn}", c + V(sgn * 0.45, 0, 0) - f * 0.0, (1.1, 0.16, 0.03), (V(sgn * 1, 0, 0) * 0.7 - f * 0.7).normalized(), (V(-sgn * 0.7, 0, 0) + f * 0.7).normalized().cross(up if y < -5.0 else Z_AX).cross(up if y < -5.0 else Z_AX) * -1 if False else (f.cross(up if y < -5.0 else Z_AX)).normalized() * 0 + (up if y < -5.0 else Z_AX).cross((V(sgn, 0, 0) * 0.7 - f * 0.7).normalized()).normalized(), up if y < -5.0 else Z_AX, TEAL, C_BASE)
for sgn in (1, -1):                                         # side rails keep ore on the ramp
    hexa(f"Ramp Rail {sgn}", [V(sgn * 2.5, -8.8, 0), V(sgn * 2.8, -8.8, 0), V(sgn * 2.8, -5.0, RZ), V(sgn * 2.5, -5.0, RZ),
                               V(sgn * 2.5, -8.8, 0.45), V(sgn * 2.8, -8.8, 0.45), V(sgn * 2.8, -5.0, RZ + 0.45), V(sgn * 2.5, -5.0, RZ + 0.45)], PLATE2, C_BASE)
    abox(f"Flat Rail {sgn}", min(sgn * 2.5, sgn * 2.8), max(sgn * 2.5, sgn * 2.8), -5.0, -3.0, 0.0, RZ + 0.45, PLATE2, C_BASE)
    abox(f"Rail Glow {sgn}", min(sgn * 2.62, sgn * 2.68), max(sgn * 2.62, sgn * 2.68), -5.0, -3.0, RZ + 0.45, RZ + 0.5, AMBER, C_BASE)

# ---- sunken glowing intake pool (where ore is sold)
PZ = 1.1
for s in (-1, 1):
    abox(f"Pool Wall X{s}", s * 3.0 - 0.4, s * 3.0 + 0.4, -3.0, 2.6, PZ, PZ + 0.9, PLATE, C_POOL)
abox("Pool Wall Back", -3.4, 3.4, 2.2, 2.9, PZ, PZ + 1.3, PLATE, C_POOL)
abox("Pool Liquid", -2.6, 2.6, -2.95, 2.2, PZ - 0.2, PZ + 0.05, POOL, C_POOL)
abox("Pool Back Glass", -2.6, 2.6, 2.05, 2.2, PZ + 0.1, PZ + 1.2, GLASS, C_POOL)
for s in (-1, 1):
    abox(f"Pool Rim Glow {s}", s * 2.62 - 0.04, s * 2.62 + 0.04, -3.0, 2.2, PZ + 0.85, PZ + 0.95, TEAL, C_POOL)
bz = abox("Burn Zone", -2.5, 2.5, -2.9, 2.1, PZ + 0.15, PZ + 1.0, BURN, C_POOL)
bz.hide_render = True

# ---- chunky armour blocks either side, angled, with neon panels
for s in (-1, 1):
    hexa(f"Side Armour {s}", [V(s * 3.4, -3.6, 1.1), V(s * 6.0, -3.6, 1.1), V(s * 6.0, 3.4, 1.1), V(s * 3.4, 3.4, 1.1),
                              V(s * 3.6, -3.0, 2.6), V(s * 5.3, -3.0, 2.2), V(s * 5.3, 2.8, 2.2), V(s * 3.6, 2.8, 2.6)], PLATE, C_ARMOUR)
    for k, y in enumerate((-4.6, )):
        hexa(f"Front Bumper {s}", [V(s * 3.0, -6.2, 0.6), V(s * 5.6, -6.2, 0.6), V(s * 5.6, -3.6, 1.1), V(s * 3.0, -3.6, 1.1),
                                   V(s * 3.2, -6.0, 2.1), V(s * 5.4, -6.0, 2.1), V(s * 5.4, -3.8, 2.6), V(s * 3.2, -3.8, 2.6)], PLATE2, C_ARMOUR)
    abox(f"Bumper Panel {s}", s * 4.3 - 0.55, s * 4.3 + 0.55, -6.25, -6.1, 1.0, 1.8, TEAL, C_ARMOUR)
    abox(f"Bumper Frame {s}", s * 4.3 - 0.7, s * 4.3 + 0.7, -6.2, -6.05, 0.85, 1.95, BLACK, C_ARMOUR)
    for k in range(3):
        abox(f"Side Vent {s}{k}", s * 6.02 - 0.03, s * 6.02 + 0.03, -2.2 + k * 1.6, -1.3 + k * 1.6, 1.4, 1.9, AMBER, C_ARMOUR)
    abox(f"Top Strip {s}", s * 4.45 - 0.1, s * 4.45 + 0.1, -2.8, 2.6, 2.42, 2.5, AMBER, C_ARMOUR)

# ---- antenna pylons with glowing tips
for k, (x, y, h) in enumerate(((-4.6, 3.6, 5.5), (4.6, 3.6, 5.5), (-5.6, -1.0, 4.2), (5.6, -1.0, 4.2))):
    abox(f"Pylon Foot {k}", x - 0.45, x + 0.45, y - 0.45, y + 0.45, 1.1, 2.6, PLATE2, C_DETAIL)
    cyl(f"Pylon Mast {k}", V(x, y, 2.6), V(x, y, 2.6 + h), 0.16, 0.12, BLACK, C_DETAIL, n=8)
    for j in range(2):
        abox(f"Pylon Fin {k}{j}", x - 0.25, x + 0.25, y - 0.05, y + 0.05, 3.4 + j * 1.2, 3.8 + j * 1.2, PLATE2, C_DETAIL)
    abox(f"Pylon Tip {k}", x - 0.22, x + 0.22, y - 0.22, y + 0.22, 2.6 + h, 3.0 + h, TEAL, C_DETAIL)

# ---- reactor ring on an arch behind the pool
for s in (-1, 1):
    hexa(f"Arch Leg {s}", [V(s * 2.2, 3.0, 1.1), V(s * 3.6, 3.0, 1.1), V(s * 3.6, 4.6, 1.1), V(s * 2.2, 4.6, 1.1),
                           V(s * 1.2, 3.4, 6.5), V(s * 2.2, 3.4, 6.5), V(s * 2.2, 4.4, 6.5), V(s * 1.2, 4.4, 6.5)], PLATE, C_REACTOR)
    abox(f"Arch Light {s}", s * 2.9 - 0.3, s * 2.9 + 0.3, 2.95, 3.0, 2.0, 3.4, AMBER, C_REACTOR)
RC = V(0, 3.9, 8.6)
tube("Reactor Ring", RC, Y_AX, Z_AX, 3.0, 2.3, 1.0, PLATE, C_REACTOR, n=40)
tube("Reactor Inner", RC, Y_AX, Z_AX, 1.7, 1.2, 0.8, PLATE2, C_REACTOR, n=32)
cyl("Reactor Back", RC + V(0, 0.4, 0), RC + V(0, 0.55, 0), 2.35, 2.35, BLACK, C_REACTOR, n=32, hint=Z_AX)
cyl("Reactor Core", RC + V(0, 0.3, 0), RC + V(0, -0.2, 0), 1.2, 1.2, CORE, C_REACTOR, n=24, hint=Z_AX)
for k in range(8):                                         # glowing segments in the ring + outer spikes
    a = 2 * math.pi * k / 8 + math.pi / 8
    d = V(math.cos(a), 0, math.sin(a));t = V(-math.sin(a), 0, math.cos(a))
    obox(f"Ring Light {k}", RC + d * 2.65 + V(0, -0.52, 0), (0.5, 0.06, 0.45), t, Y_AX, d, TEAL if k % 2 else AMBER, C_REACTOR)
    beam(f"Ring Spoke {k}", RC + d * 1.65, RC + d * 2.35, 0.3, 0.6, Y_AX, PLATE2, C_REACTOR)
    if k % 2 == 0:
        beam(f"Ring Spike {k}", RC + d * 3.0, RC + d * 4.2, 0.35, 0.5, Y_AX, BLACK, C_REACTOR)
        obox(f"Spike Tip {k}", RC + d * 4.3, (0.5, 0.55, 0.4), t, Y_AX, d, AMBER, C_REACTOR)
for k in range(7):                                          # core dot cluster
    a = 2 * math.pi * k / 6
    p = RC + V(0, -0.25, 0) + (V(0.55 * math.cos(a), 0, 0.55 * math.sin(a)) if k < 6 else V(0, 0, 0))
    cyl(f"Core Dot {k}", p, p + V(0, -0.08, 0), 0.2, 0.2, TEAL, C_REACTOR, n=12, hint=Z_AX)
for s in (-1, 1):                                           # energy beams from ring down to pool corners
    cyl(f"Feed Beam {s}", RC + V(s * 1.2, -0.3, -1.6), V(s * 2.0, 1.8, PZ + 1.0), 0.07, 0.07, TEAL, C_REACTOR, n=6)

finish_mine(bg=(0.02, 0.022, 0.03), tint=(0.85, 0.92, 1.0))

used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
items = sorted((k, v) for k, v in RBX.items() if k in used)
look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nightmare_furnace", "NightmareLamentFurnace_RobloxSetup.lua")).read()
head, rest = src.split("local LOOK = {", 1)
rest = rest.split("local model = ", 1)[1]
lua = head.replace("NightmareLamentFurnace", "PrismReactorFurnace").replace("vortex mouth", "intake pool") + \
      "local LOOK = {\n" + look + "\n}\nlocal LIGHTS = {\n" + lights + "\n}\nlocal model = " + rest.replace("NightmareLamentFurnace", "PrismReactorFurnace")
lua = lua.replace("print((\"[PrismReactorFurnace]", '''-- conveyor ramp: push ore up the ramp and into the pool
local speed = model:GetAttribute("ConveyorSpeed") or 8
model:SetAttribute("ConveyorSpeed", speed)
local nConv = 0
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") and p.Name:gsub("%.%d+$", "") == "Conveyor" and burn then
		local dir = burn.Position - p.Position
		p.AssemblyLinearVelocity = dir.Unit * speed
		p.Anchored = true
		nConv += 1
	end
end
print(("[PrismReactorFurnace] conveyor ramp parts: %d (speed attribute ConveyorSpeed)"):format(nConv))
print(("[PrismReactorFurnace]''', 1)
open(os.path.join(OUT, "PrismReactorFurnace_RobloxSetup.lua"), "w").write(lua)
print("[mine] wrote furnace setup lua")
