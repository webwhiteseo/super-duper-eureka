-- NightmareLamentFurnace: colours, Roblox materials, glow lights and a working SELL script.
-- 1. Import NightmareLamentFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (any Part named "Ore" with a "Value" attribute - what the mine droppers make) that touches the glowing
-- vortex mouth is destroyed and its Value x Multiplier is added to the owner's leaderstats Cash.
-- Owner = model attribute OwnerUserId (set it per plot), otherwise the first player in the server.
local LOOK = {
	BurnZone = {"ForceField", 255, 160, 240, 0.35},
	CandleFlame = {"Neon", 170, 230, 255, 0},
	CandleWax = {"SmoothPlastic", 220, 210, 236, 0},
	DreamCloud = {"SmoothPlastic", 240, 196, 236, 0},
	DreamCrystal = {"Glass", 190, 140, 255, 0.15},
	DreamObsidian = {"Basalt", 40, 26, 60, 0},
	DreamTears = {"Neon", 130, 230, 255, 0},
	DreamVortex = {"Neon", 220, 120, 255, 0},
	MaskCrack = {"SmoothPlastic", 40, 20, 50, 0},
	MoonSilver = {"Metal", 200, 196, 220, 0},
	PinkTrim = {"Neon", 255, 120, 210, 0},
	PorcelainMask = {"SmoothPlastic", 236, 228, 244, 0},
	Starlight = {"Neon", 255, 240, 200, 0},
	VoidBlack = {"SmoothPlastic", 8, 4, 14, 0}
}
local LIGHTS = {
	CandleFlame = {120, 200, 255, 8, 1.2},
	DreamCrystal = {150, 90, 255, 8, 0.7},
	DreamTears = {90, 210, 255, 10, 1.2},
	DreamVortex = {190, 80, 255, 16, 2}
}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("NightmareLamentFurnace_Roblox", true) or workspace:FindFirstChild("NightmareLamentFurnace", true) end
assert(model, "Select the imported NightmareLamentFurnace model first.")
local styled, lit, burn = 0, 0, nil
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
	end
end
if burn then
	burn.Name = "Burn"; burn.CanCollide = false; burn.CanTouch = true; burn.CanQuery = false
	model:SetAttribute("Multiplier", model:GetAttribute("Multiplier") or 2)
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
print(("[NightmareLamentFurnace] %d parts coloured, %d lights, sell script %s"):format(styled, lit, burn and "added" or "NOT found"))
-- No leaderstats yet? Add a Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)
