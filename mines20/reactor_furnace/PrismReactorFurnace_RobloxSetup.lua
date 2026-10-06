-- PrismReactorFurnace: colours, Roblox materials, glow lights and a working SELL script.
-- 1. Import PrismReactorFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (any Part named "Ore" with a "Value" attribute - what the mine droppers make) that touches the glowing
-- intake pool is destroyed and its Value x Multiplier is added to the owner's leaderstats Cash.
-- Owner = model attribute OwnerUserId (set it per plot), otherwise the first player in the server.
local LOOK = {
	AmberNeon = {"Neon", 255, 180, 40, 0},
	Black = {"SmoothPlastic", 14, 14, 18, 0},
	BurnZone = {"ForceField", 120, 240, 255, 0.6},
	DarkPlate = {"DiamondPlate", 58, 60, 66, 0},
	PoolGlass = {"Glass", 170, 240, 255, 0.5},
	PrismPool = {"Neon", 90, 240, 255, 0},
	ReactorCore = {"Neon", 220, 255, 255, 0},
	SteelPlate = {"DiamondPlate", 96, 100, 108, 0},
	TealNeon = {"Neon", 60, 255, 220, 0}
}
local LIGHTS = {
	AmberNeon = {255, 150, 20, 8, 1},
	PrismPool = {40, 220, 255, 16, 2},
	ReactorCore = {140, 240, 255, 20, 2.5},
	TealNeon = {20, 255, 200, 8, 1}
}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("PrismReactorFurnace_Roblox", true) or workspace:FindFirstChild("PrismReactorFurnace", true) end
assert(model, "Select the imported PrismReactorFurnace model first.")
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
print(("[PrismReactorFurnace] %d parts coloured, %d lights, sell script %s"):format(styled, lit, burn and "added" or "NOT found"))
-- No leaderstats yet? Add a Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)
