"""Prism Upgrader - an original Miner's-Haven-style upgrader: a conveyor belt section runs through a chunky
diamond-plate gate; three glowing laser rings across the belt upgrade every ore that passes (once per ore).
Writes PrismUpgrader_RobloxSetup.lua: colours, lights, moving belt and the upgrade script. mine_kit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from furnace_kit import *
C_BELT, C_GATE, C_FX = begin("PrismUpgrader", ["Belt", "Gate", "Effects"], seed=501)
P = M("Dark Plate (DiamondPlate)", (70, 74, 84), rough=0.4, metal=0.7, rbx="DiamondPlate", plate=7.0)
P2 = M("Steel Plate (DiamondPlate)", (130, 136, 148), rough=0.35, metal=0.8, rbx="DiamondPlate", plate=9.0)
BELT = M("Conveyor", (34, 36, 42), rough=0.6, rbx="SmoothPlastic")
ARROW = M("Belt Arrows", (120, 255, 140), rough=0.3, glow=(80, 255, 110), glow_strength=4.0, rbx="Neon")
LASER = M("Upgrade Laser", (110, 255, 140), rough=0.2, glow=(60, 255, 100), glow_strength=5.0, rbx="Neon", light=(14, 2.0))
CORE = M("Prism Core", (190, 255, 210), rough=0.05, glow=(120, 255, 160), glow_strength=1.5, rbx="Glass", alpha=0.25, light=(10, 1.2))
LAMP = M("Gate Lamp", (255, 220, 90), rough=0.3, glow=(255, 190, 40), glow_strength=5.0, rbx="Neon", light=(6, 0.8))
ZONE = M("Upgrade Zone", (110, 255, 140), rough=0.2, glow=(60, 255, 100), glow_strength=1.0, rbx="ForceField", alpha=1.0)
ENDM = M("Belt End", (40, 40, 40), rough=0.5, alpha=1.0)
Z_AX, Y_AX, X_AX = V(0, 0, 1), V(0, 1, 0), V(1, 0, 0)
BZ = 1.0                                                     # belt top height (matches a standard conveyor)
L = 6.0                                                      # belt half length (along Y, ore moves -Y -> +Y)
abox("Belt Frame", -2.0, 2.0, -L, L, 0.0, BZ - 0.1, P, C_BELT)
abox("Conveyor", -1.7, 1.7, -L, L, BZ - 0.1, BZ, BELT, C_BELT)
for s in (-1, 1):
    abox(f"Belt Rail {s}", min(s * 1.7, s * 2.0), max(s * 1.7, s * 2.0), -L, L, BZ - 0.1, BZ + 0.5, P2, C_BELT)
    for k in range(6):
        cyl(f"Roller Cap {s}{k}", V(s * 2.0, -L + 0.8 + k * 2.1, BZ - 0.45), V(s * 2.1, -L + 0.8 + k * 2.1, BZ - 0.45), 0.3, 0.3, P2, C_BELT, n=10, hint=Z_AX)
for k in range(8):                                           # glowing chevrons on the belt
    y = -L + 0.7 + k * 1.5
    for sgn in (1, -1):
        ax = (V(sgn, 0, 0) * 0.7 - V(0, 1, 0) * 0.7).normalized()
        obox(f"Belt Arrow {k}{sgn}", V(sgn * 0.4, y, BZ + 0.01), (0.9, 0.14, 0.02), ax, Z_AX.cross(ax), Z_AX, ARROW, C_BELT)
abox("Belt End", -1.6, 1.6, L - 0.1, L, BZ, BZ + 0.1, ENDM, C_BELT)
# chunky gate over the belt
for s in (-1, 1):
    hexa(f"Gate Pillar {s}", [V(s * 2.0, -1.8, 0), V(s * 3.6, -1.8, 0), V(s * 3.6, 1.8, 0), V(s * 2.0, 1.8, 0),
                              V(s * 2.0, -1.4, 5.4), V(s * 3.2, -1.4, 5.4), V(s * 3.2, 1.4, 5.4), V(s * 2.0, 1.4, 5.4)], P, C_GATE)
    for k in range(3):
        abox(f"Pillar Lamp {s}{k}", min(s * 3.25, s * 3.3), max(s * 3.25, s * 3.3) + 0.0, -0.4, 0.4, 1.2 + k * 1.3, 1.8 + k * 1.3, LAMP, C_GATE) if False else \
            abox(f"Pillar Lamp {s}{k}", s * 2.9 - 0.25, s * 2.9 + 0.25, -1.75 + 0.06 * k, -1.65 + 0.06 * k, 1.2 + k * 1.3, 1.8 + k * 1.3, LAMP, C_GATE)
    abox(f"Pillar Cap {s}", s * 2.6 - 1.0, s * 2.6 + 1.0, -1.6, 1.6, 5.4, 6.0, P2, C_GATE)
    cyl(f"Emitter {s}", V(s * 2.0, 0, BZ + 1.2), V(s * 1.7, 0, BZ + 1.2), 0.35, 0.3, P2, C_GATE, n=12, hint=Z_AX)
abox("Gate Beam", -3.2, 3.2, -1.4, 1.4, 6.0, 7.0, P, C_GATE)
for k in range(5):
    obox(f"Beam Stripe {k}", V(-2.4 + k * 1.2, -1.42, 6.5), (0.4, 0.04, 0.9), (X_AX + Z_AX).normalized(), Y_AX, (Z_AX - X_AX).normalized(), LAMP, C_GATE)
# prism core on top
crystal("Prism Up", V(0, 0, 7.6), Z_AX, 1.8, 0.8, CORE, C_FX, sides=6)
crystal("Prism Down", V(0, 0, 7.6), -Z_AX, 0.7, 0.8, CORE, C_FX, sides=6)
torus("Prism Ring", V(0, 0, 7.6), Z_AX, Y_AX, 1.2, 0.08, LASER, C_FX, n_major=24, n_minor=4)
cyl("Prism Beam", V(0, 0, 7.0), V(0, 0, BZ + 2.4), 0.12, 0.12, LASER, C_FX, n=8)
# three laser rings across the belt + horizontal laser bars
for k, y in enumerate((-1.0, 0.0, 1.0)):
    tube(f"Laser Ring {k}", V(0, y, BZ + 1.4), Y_AX, Z_AX, 1.75, 1.6, 0.08, LASER, C_FX, n=32)
for k, z in enumerate((BZ + 0.5, BZ + 1.2, BZ + 1.9)):
    cyl(f"Laser Bar {k}", V(-1.7, 0, z), V(1.7, 0, z), 0.05, 0.05, LASER, C_FX, n=6, hint=Z_AX)
burn_zone(ZONE, -1.6, 1.6, -1.2, 1.2, BZ, BZ + 2.4, C_FX).name = "Upgrade Zone"
finish_mine(bg=(0.016, 0.02, 0.026), tint=(0.85, 1.0, 0.9))

used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
items = sorted((k, v) for k, v in RBX.items() if k in used)
look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
lua = f'''-- PrismUpgrader: colours, materials, lights, a moving conveyor belt and the UPGRADE script.
-- 1. Import PrismUpgrader_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute) passing through the laser gate gets Value x Multiplier, once per ore.
-- Attributes on the model: Multiplier (default 1.5), ConveyorSpeed (default 8).
local LOOK = {{
{look}
}}
local LIGHTS = {{
{lights}
}}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("PrismUpgrader_Roblox", true) or workspace:FindFirstChild("PrismUpgrader", true) end
assert(model, "Select the imported PrismUpgrader model first.")
local zone, belt, beltEnd = nil, nil, nil
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") then
		local key = p.Name:gsub("%.%d+$", "")
		local l = LOOK[key]
		pcall(function()
			p.Anchored = true
			for _, sa in ipairs(p:GetChildren()) do if sa:IsA("SurfaceAppearance") then sa:Destroy() end end
			if l then
				p.Material = Enum.Material[l[1]]; p.Color = Color3.fromRGB(l[2], l[3], l[4]); p.Transparency = l[5]
				if p:IsA("MeshPart") then p.TextureID = "" end
			end
			local L = LIGHTS[key]
			if L then
				local light = p:FindFirstChild("MineLight") or Instance.new("PointLight")
				light.Name = "MineLight"; light.Color = Color3.fromRGB(L[1], L[2], L[3]); light.Range = L[4]; light.Brightness = L[5]; light.Parent = p
			end
		end)
		if key == "UpgradeZone" then zone = p elseif key == "Conveyor" then belt = p elseif key == "BeltEnd" then beltEnd = p end
	end
end
model:SetAttribute("Multiplier", model:GetAttribute("Multiplier") or 1.5)
model:SetAttribute("ConveyorSpeed", model:GetAttribute("ConveyorSpeed") or 8)
if belt and beltEnd then
	local dir = beltEnd.Position - belt.Position
	dir = Vector3.new(dir.X, 0, dir.Z).Unit
	belt.AssemblyLinearVelocity = dir * model:GetAttribute("ConveyorSpeed")
	beltEnd.CanCollide = false
end
if zone then
	zone.Name = "Upgrade"; zone.CanCollide = false; zone.CanTouch = true; zone.CanQuery = false
	local old = model:FindFirstChild("Upgrader"); if old then old:Destroy() end
	local s = Instance.new("Script")
	s.Name = "Upgrader"
	s.Source = [[
local up = script.Parent
local zone = up:FindFirstChild("Upgrade", true)
local tag = "Upgraded_" .. up.Name
zone.Touched:Connect(function(hit)
	if hit.Name ~= "Ore" or hit:GetAttribute(tag) then return end
	hit:SetAttribute(tag, true)
	hit:SetAttribute("Value", (hit:GetAttribute("Value") or 0) * (up:GetAttribute("Multiplier") or 1.5))
	local old = hit.Color
	hit.Color = Color3.fromRGB(120, 255, 150)
	task.delay(0.25, function() if hit.Parent then hit.Color = old end end)
end)
]]
	s.Parent = model
end
print("[PrismUpgrader] belt " .. (belt and "moving" or "NOT found") .. ", upgrade script " .. (zone and "added" or "NOT found"))
'''
open(os.path.join(OUT, "PrismUpgrader_RobloxSetup.lua"), "w").write(lua)
print("[mine] wrote upgrader lua")
