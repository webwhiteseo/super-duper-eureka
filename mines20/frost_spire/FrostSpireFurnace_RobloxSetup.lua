-- FrostSpireFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import FrostSpireFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 150, 230, 255, 0.6},
	Conveyor = {"DiamondPlate", 60, 84, 116, 0},
	DeepIce = {"Glacier", 30, 60, 110, 0},
	FrostNeon = {"Neon", 160, 240, 255, 0},
	FrostSteel = {"Metal", 120, 140, 168, 0},
	FrostWell = {"Neon", 140, 230, 255, 0},
	IceCrystal = {"Glass", 170, 230, 255, 0.2},
	PackedIce = {"Ice", 170, 214, 240, 0},
	Snow = {"Snow", 242, 248, 255, 0},
	SpireCore = {"Neon", 230, 250, 255, 0}
}
local LIGHTS = {
	FrostNeon = {100, 220, 255, 8, 1},
	FrostWell = {80, 210, 255, 16, 2},
	IceCrystal = {110, 200, 255, 10, 1},
	SpireCore = {170, 235, 255, 20, 2.4}
}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("FrostSpireFurnace_Roblox", true) or workspace:FindFirstChild("FrostSpireFurnace", true) end
assert(model, "Select the imported FrostSpireFurnace model first.")
local styled, lit, burn, conv = 0, 0, nil, {}
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
print(("[FrostSpireFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)
