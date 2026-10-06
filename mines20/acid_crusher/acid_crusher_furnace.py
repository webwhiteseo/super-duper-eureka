"""Acid Crusher Furnace - an original Miner's-Haven-style furnace built from the shared traits of classic furnaces:
a low stepped diamond-plate platform, a wide front entry lip, a sunken glowing intake pool where the ore is sold,
chunky angled armour blocks with neon panels, antenna pylons with glowing tips, and a giant hydraulic crusher hammer over a bubbling acid pit,
with acid tanks, pipes and hazard stripes. Built with mine_kit; writes a sell-script setup Lua."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_BASE, C_ARMOUR, C_POOL, C_REACTOR, C_DETAIL = begin("AcidCrusherFurnace", ["Platform", "Armour", "Pool", "Crusher", "Details"], seed=41)
PLATE = M("Dark Plate (DiamondPlate)", (58, 60, 66), rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
PLATE2 = M("Steel Plate (DiamondPlate)", (96, 100, 108), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
BLACK = M("Black", (14, 14, 18), rough=0.5)
POOL = M("Acid Pool", (120, 255, 60), rough=0.05, glow=(80, 255, 20), glow_strength=3.0, rbx="Neon", light=(16, 2.0))
GLASS = M("Pool Glass", (190, 255, 170), rough=0.05, glow=(130, 255, 90), glow_strength=0.5, rbx="Glass", alpha=0.5)
TEAL = M("Acid Neon", (140, 255, 40), rough=0.3, glow=(100, 255, 10), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
AMBER = M("Hazard Neon", (255, 200, 20), rough=0.3, glow=(255, 170, 0), glow_strength=5.0, rbx="Neon", light=(8, 1.0))
CORE = M("Acid Core", (200, 255, 150), rough=0.3, glow=(120, 255, 60), glow_strength=8.0, rbx="Neon", light=(20, 2.5))
BURN = M("Burn Zone", (140, 255, 80), rough=0.2, glow=(100, 255, 40), glow_strength=1.0, rbx="ForceField", alpha=0.6)
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

# ---- hydraulic crusher: a gantry over the pit with a huge hammer, pistons, acid tanks and pipes
HAZ = M("Hazard Yellow", (240, 196, 20), rough=0.45, rbx="SmoothPlastic")
PIPE = M("Pipe Steel (Metal)", (140, 146, 150), rough=0.3, metal=0.9, rbx="Metal")
TANKG = M("Tank Glass", (170, 255, 140), rough=0.05, glow=(110, 255, 60), glow_strength=0.6, rbx="Glass", alpha=0.4)
for s_ in (-1, 1):
    hexa(f"Gantry Leg {s_}", [V(s_ * 3.4, -1.6, 1.1), V(s_ * 4.6, -1.6, 1.1), V(s_ * 4.6, 2.6, 1.1), V(s_ * 3.4, 2.6, 1.1),
                              V(s_ * 3.4, -0.6, 8.4), V(s_ * 4.2, -0.6, 8.4), V(s_ * 4.2, 1.6, 8.4), V(s_ * 3.4, 1.6, 8.4)], PLATE, C_REACTOR)
    for k in range(5):                                      # hazard stripes on the legs
        z = 2.2 + k * 1.15
        hexa(f"Leg Stripe {s_}{k}", [V(s_ * 3.38, -1.52 + 0.12 * k, z), V(s_ * 3.38, -1.52 + 0.12 * k, z), V(s_ * 3.38, -1.52 + 0.12 * k, z + 0.3), V(s_ * 3.38, -1.52 + 0.12 * k, z + 0.3),
                                     V(s_ * 3.38, -1.0 + 0.12 * k, z + 0.3), V(s_ * 3.38, -1.0 + 0.12 * k, z + 0.3), V(s_ * 3.38, -1.0 + 0.12 * k, z + 0.6), V(s_ * 3.38, -1.0 + 0.12 * k, z + 0.6)], HAZ, C_REACTOR) if False else \
            obox(f"Leg Stripe {s_}{k}", V(s_ * 3.37, -0.3, z), (0.04, 1.6, 0.35), X_AX, (Y_AX + Z_AX * 0.6).normalized(), (Z_AX - Y_AX * 0.6).normalized(), HAZ, C_REACTOR)
    abox(f"Leg Light {s_}", s_ * 4.62 - 0.03, s_ * 4.62 + 0.03, 0.0, 1.2, 3.0, 6.0, TEAL, C_REACTOR)
abox("Gantry Beam", -4.4, 4.4, -0.8, 1.8, 8.4, 9.9, PLATE2, C_REACTOR)
for k in range(9):
    x = -4.0 + k * 1.0
    obox(f"Beam Stripe {k}", V(x, -0.82, 9.15), (0.4, 0.04, 1.5), (X_AX + Z_AX * 0.8).normalized(), Y_AX, (Z_AX - X_AX * 0.8).normalized(), HAZ, C_REACTOR)
abox("Beam Light", -3.8, 3.8, -0.84, -0.8, 8.5, 8.62, AMBER, C_REACTOR)
# motor housing + pistons
abox("Motor Housing", -1.6, 1.6, -0.4, 1.4, 9.9, 11.2, PLATE, C_REACTOR)
for k in range(4):
    abox(f"Motor Fin {k}", -1.3 + k * 0.85 - 0.08, -1.3 + k * 0.85 + 0.08, -0.5, 1.5, 10.1, 11.0, PLATE2, C_REACTOR)
cyl("Motor Core", V(0, -0.45, 10.55), V(0, -0.6, 10.55), 0.45, 0.45, CORE, C_REACTOR, n=16, hint=Z_AX)
HZ = PZ + 3.4                                                # hammer bottom height (raised, ore passes under)
for s_ in (-1, 1):
    cyl(f"Piston Sleeve {s_}", V(s_ * 1.6, 0.5, 8.4), V(s_ * 1.6, 0.5, 6.4), 0.42, 0.42, PIPE, C_REACTOR, n=14)
    cyl(f"Piston Rod {s_}", V(s_ * 1.6, 0.5, 6.4), V(s_ * 1.6, 0.5, HZ + 1.4), 0.22, 0.22, PIPE, C_REACTOR, n=12)
    torus(f"Piston Seal {s_}", V(s_ * 1.6, 0.5, 6.4), Z_AX, Y_AX, 0.43, 0.07, HAZ, C_REACTOR, n_major=14, n_minor=4)
cyl("Main Ram", V(0, 0.5, 8.4), V(0, 0.5, HZ + 1.4), 0.6, 0.6, PIPE, C_REACTOR, n=18)
abox("Hammer Head", -2.4, 2.4, -1.4, 2.0, HZ, HZ + 1.4, PLATE2, C_REACTOR)
abox("Hammer Face", -2.3, 2.3, -1.3, 1.9, HZ - 0.25, HZ, BLACK, C_REACTOR)
for k in range(5):                                          # crushing teeth
    x = -1.9 + k * 0.95
    cone(f"Hammer Tooth {k}", V(x, 0.3, HZ - 0.25), V(x, 0.3, HZ - 0.85), 0.32, PLATE, C_REACTOR, n=4)
for k in range(8):
    x = -2.3 + k * 0.62
    obox(f"Hammer Stripe {k}", V(x, -1.42, HZ + 0.7), (0.3, 0.04, 1.3), (X_AX + Z_AX * 0.9).normalized(), Y_AX, (Z_AX - X_AX * 0.9).normalized(), HAZ, C_REACTOR)
abox("Hammer Light", -2.0, 2.0, -1.44, -1.4, HZ + 1.1, HZ + 1.25, TEAL, C_REACTOR)
# acid tanks behind with pipes into the pit
for s_ in (-1, 1):
    T = V(s_ * 2.0, 4.6, 1.1)
    cyl(f"Acid Tank {s_}", T, T + V(0, 0, 3.6), 1.05, 1.05, TANKG, C_DETAIL, n=18)
    cyl(f"Acid Fill {s_}", T + V(0, 0, 0.05), T + V(0, 0, 2.6), 0.85, 0.85, POOL, C_DETAIL, n=16)
    for z in (0.0, 3.6):
        cyl(f"Tank Cap {s_}{z}", T + V(0, 0, z - 0.15), T + V(0, 0, z + 0.25), 1.15, 1.15, PLATE, C_DETAIL, n=18)
    for k in range(3):
        dot(f"Tank Bubble {s_}{k}", T + V(0.3 * (k - 1), -0.2, 1.0 + 0.6 * k), 0.12, CORE, C_DETAIL)
    path_tube(f"Acid Pipe {s_}", [T + V(0, -0.9, 3.2), T + V(0, -1.8, 3.4), T + V(-s_ * 0.6, -2.6, 2.6), V(s_ * 1.4, 1.9, PZ + 1.0)], [0.18] * 4, PIPE, C_DETAIL, n=8)
    dot(f"Acid Drip {s_}", V(s_ * 1.4, 1.75, PZ + 0.6), 0.14, POOL, C_DETAIL)
for k in range(3):                                          # bubbles in the pit
    dot(f"Pit Bubble {k}", V(-1.2 + 1.2 * k, -0.6 + 0.7 * (k % 2), PZ + 0.1), 0.2, CORE, C_POOL)

finish_mine(bg=(0.016, 0.024, 0.014), tint=(0.88, 1.0, 0.85))

used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
items = sorted((k, v) for k, v in RBX.items() if k in used)
look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nightmare_furnace", "NightmareLamentFurnace_RobloxSetup.lua")).read()
head, rest = src.split("local LOOK = {", 1)
rest = rest.split("local model = ", 1)[1]
lua = head.replace("NightmareLamentFurnace", "AcidCrusherFurnace").replace("vortex mouth", "intake pool") + \
      "local LOOK = {\n" + look + "\n}\nlocal LIGHTS = {\n" + lights + "\n}\nlocal model = " + rest.replace("NightmareLamentFurnace", "AcidCrusherFurnace")
lua = lua.replace("print((\"[AcidCrusherFurnace]", '''-- conveyor ramp: push ore up the ramp and into the pool
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
print(("[AcidCrusherFurnace] conveyor ramp parts: %d (speed attribute ConveyorSpeed)"):format(nConv))
print(("[AcidCrusherFurnace]''', 1)
open(os.path.join(OUT, "AcidCrusherFurnace_RobloxSetup.lua"), "w").write(lua)
print("[mine] wrote furnace setup lua")
