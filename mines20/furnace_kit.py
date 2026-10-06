"""furnace_kit - shared furnace parts on top of mine_kit: a conveyor ramp straight into the intake,
the invisible sell part ("Burn Zone") and the Roblox setup Lua (colours, lights, sell script, conveyor push)."""
from mine_kit import *


def conveyor_ramp(mat, chev, rail, glow, y_front=-8.8, y_lip=-5.0, y_end=-2.95, rz=1.3, w=2.5, coll=None):
    """Smooth ramp: ground at y_front up to height rz at y_lip, then flat to y_end. mat must be named 'Conveyor'."""
    hexa("Conveyor Slope", [V(-w, y_front, 0), V(w, y_front, 0), V(w, y_lip, 0), V(-w, y_lip, 0),
                            V(-w, y_front, 0.02), V(w, y_front, 0.02), V(w, y_lip, rz), V(-w, y_lip, rz)], mat, coll)
    abox("Conveyor Flat", -w, w, y_lip, y_end, 0.0, rz, mat, coll)
    L = y_lip - y_front
    sl = math.atan2(rz, L)
    up_s, fw_s = V(0, -math.sin(sl), math.cos(sl)), V(0, math.cos(sl), math.sin(sl))
    n_chev = max(2, int((y_end - y_front) / 1.3))
    for k in range(n_chev):
        y = y_front + 0.6 + k * 1.3
        on_slope = y < y_lip
        z = (y - y_front) / L * rz if on_slope else rz
        n, f = (up_s, fw_s) if on_slope else (V(0, 0, 1), V(0, 1, 0))
        c = V(0, y, z) + n * 0.02
        for sgn in (1, -1):
            ax = (V(sgn, 0, 0) * 0.7 - f * 0.7).normalized()
            obox(f"Chevron {k}{sgn}", c + V(sgn * 0.45, 0, 0), (1.1, 0.16, 0.03), ax, n.cross(ax).normalized(), n, chev, coll)
    for sgn in (1, -1):
        a, b = sorted((sgn * w, sgn * (w + 0.3)))
        hexa(f"Ramp Rail {sgn}", [V(a, y_front, 0), V(b, y_front, 0), V(b, y_lip, rz), V(a, y_lip, rz),
                                   V(a, y_front, 0.45), V(b, y_front, 0.45), V(b, y_lip, rz + 0.45), V(a, y_lip, rz + 0.45)], rail, coll)
        abox(f"Flat Rail {sgn}", a, b, y_lip, y_end, 0.0, rz + 0.45, rail, coll)
        abox(f"Rail Glow {sgn}", a + 0.1, b - 0.1, y_lip, y_end, rz + 0.45, rz + 0.5, glow, coll)


def burn_zone(mat, x0, x1, y0, y1, z0, z1, coll):
    """The sell part: anything named Ore touching it is sold (hidden in renders, see-through in Roblox)."""
    ob = abox("Burn Zone", x0, x1, y0, y1, z0, z1, mat, coll)
    ob.hide_render = True
    return ob


def write_furnace_lua(name):
    used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
    items = sorted((k, v) for k, v in RBX.items() if k in used)
    look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
    lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
    lua = f'''-- {name}: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import {name}_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {{
{look}
}}
local LIGHTS = {{
{lights}
}}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("{name}_Roblox", true) or workspace:FindFirstChild("{name}", true) end
assert(model, "Select the imported {name} model first.")
local styled, lit, burn, conv = 0, 0, nil, {{}}
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
				styled += 1
			end
			local L = LIGHTS[key]
			if L then
				local light = p:FindFirstChild("MineLight") or Instance.new("PointLight")
				light.Name = "MineLight"; light.Color = Color3.fromRGB(L[1], L[2], L[3]); light.Range = L[4]; light.Brightness = L[5]
				light.Parent = p
				lit += 1
			end
		end)
		if key == "BurnZone" then burn = p end
		if key == "Conveyor" then table.insert(conv, p) end
	end
end
if burn then
	burn.Name = "Burn"; burn.CanCollide = false; burn.CanTouch = true; burn.CanQuery = false
	model:SetAttribute("Multiplier", model:GetAttribute("Multiplier") or 2)
	model:SetAttribute("ConveyorSpeed", model:GetAttribute("ConveyorSpeed") or 8)
	for _, p in ipairs(conv) do
		p.AssemblyLinearVelocity = (burn.Position - p.Position).Unit * model:GetAttribute("ConveyorSpeed")
	end
	local old = model:FindFirstChild("Furnace"); if old then old:Destroy() end
	local s = Instance.new("Script")
	s.Name = "Furnace"
	s.Source = [[
local Players = game:GetService("Players")
local furnace = script.Parent
local burn = furnace:FindFirstChild("Burn", true)
local function owner()
	local id = furnace:GetAttribute("OwnerUserId")
	if id then return Players:GetPlayerByUserId(id) end
	return Players:GetPlayers()[1]
end
burn.Touched:Connect(function(hit)
	if hit.Name ~= "Ore" or hit:GetAttribute("Sold") then return end
	hit:SetAttribute("Sold", true)
	local value = (hit:GetAttribute("Value") or 0) * (furnace:GetAttribute("Multiplier") or 1)
	local plr = owner()
	local stats = plr and plr:FindFirstChild("leaderstats")
	local cash = stats and stats:FindFirstChild("Cash")
	if cash then cash.Value += value end
	hit:Destroy()
end)
]]
	s.Parent = model
end
print(("[{name}] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)
'''
    open(os.path.join(OUT, f"{name}_RobloxSetup.lua"), "w").write(lua)
    print("[mine] wrote furnace setup lua")


def write_look_lua(name, note=""):
    """Colours/materials/lights only (no gameplay script) - for decorative pieces like boost pads."""
    used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
    items = sorted((k, v) for k, v in RBX.items() if k in used)
    look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
    lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
    lua = f'''-- {name}: colours, Roblox materials and glow lights. {note}
-- 1. Import {name}_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {{
{look}
}}
local LIGHTS = {{
{lights}
}}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("{name}_Roblox", true) or workspace:FindFirstChild("{name}", true) end
assert(model, "Select the imported {name} model first.")
local styled, lit = 0, 0
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
				styled += 1
			end
			local L = LIGHTS[key]
			if L then
				local light = p:FindFirstChild("MineLight") or Instance.new("PointLight")
				light.Name = "MineLight"; light.Color = Color3.fromRGB(L[1], L[2], L[3]); light.Range = L[4]; light.Brightness = L[5]
				light.Parent = p
				lit += 1
			end
		end)
	end
end
print(("[{name}] %d parts coloured, %d lights"):format(styled, lit))
'''
    open(os.path.join(OUT, f"{name}_RobloxSetup.lua"), "w").write(lua)
    print("[mine] wrote look lua")
