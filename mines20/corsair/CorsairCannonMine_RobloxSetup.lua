-- CorsairCannonMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import CorsairCannonMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	CannonIron = {"Metal", 40, 40, 44, 0},
	CannonSmoke = {"SmoothPlastic", 200, 200, 204, 0.2},
	DeckPlanks = {"WoodPlanks", 164, 122, 78, 0},
	DoubloonOre = {"Neon", 255, 196, 60, 0},
	FlagBlack = {"Fabric", 16, 16, 18, 0},
	Gold = {"Metal", 240, 188, 66, 0},
	IsletRock = {"Slate", 96, 92, 88, 0},
	IsletSand = {"Sand", 226, 200, 140, 0},
	LanternGlow = {"Neon", 255, 210, 130, 0},
	MuzzleFlash = {"Neon", 255, 150, 40, 0},
	PalmLeaf = {"SmoothPlastic", 64, 150, 64, 0},
	PalmTrunk = {"Wood", 130, 96, 60, 0},
	Rope = {"Fabric", 150, 120, 80, 0},
	Ruby = {"Glass", 220, 20, 50, 0.1},
	SailRed = {"Fabric", 176, 34, 30, 0},
	Sailcloth = {"Fabric", 236, 224, 196, 0},
	SeaFoam = {"SmoothPlastic", 236, 246, 250, 0},
	SeaWater = {"Glass", 30, 112, 150, 0},
	ShipTimber = {"WoodPlanks", 86, 52, 32, 0},
	SkullWhite = {"SmoothPlastic", 240, 236, 224, 0}
}
local LIGHTS = {
	LanternGlow = {255, 170, 70, 12, 1.4},
	MuzzleFlash = {255, 110, 20, 10, 1.5}
}
local ORE_PART = "DoubloonOre"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("CorsairCannonMine_Roblox", true) or workspace:FindFirstChild("CorsairCannonMine", true) end
assert(model, "Select the imported CorsairCannonMine model first.")
local styled, lit, drop = 0, 0, nil
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") then
		local key = p.Name:gsub("%.%d+$", "")
		local l = LOOK[key]
		pcall(function()
			p.Anchored = true
			for _, sa in ipairs(p:GetChildren()) do if sa:IsA("SurfaceAppearance") then sa:Destroy() end end
			if l then
				p.Material = Enum.Material[l[1]]
				p.Color = Color3.fromRGB(l[2], l[3], l[4])
				p.Transparency = l[5]
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
		if key == ORE_PART then drop = p end
	end
end
if drop then
	drop.Transparency = 1; drop.CanCollide = false; drop.CanQuery = false; drop.Name = "Drop"
	local oreLook = LOOK[ORE_PART]
	model:SetAttribute("OreValue", model:GetAttribute("OreValue") or 25)
	model:SetAttribute("DropInterval", model:GetAttribute("DropInterval") or 2)
	model:SetAttribute("OreSize", model:GetAttribute("OreSize") or 1)
	model:SetAttribute("OreColor", Color3.fromRGB(oreLook[2], oreLook[3], oreLook[4]))
	model:SetAttribute("OreMaterial", oreLook[1])
	local old = model:FindFirstChild("Dropper"); if old then old:Destroy() end
	local s = Instance.new("Script")
	s.Name = "Dropper"
	s.Source = [[
local Debris = game:GetService("Debris")
local mine = script.Parent
local drop = mine:FindFirstChild("Drop", true)
while true do
	task.wait(mine:GetAttribute("DropInterval") or 2)
	if drop and mine:GetAttribute("Enabled") ~= false then
		local size = mine:GetAttribute("OreSize") or 1
		local ore = Instance.new("Part")
		ore.Name = "Ore"
		ore.Size = Vector3.new(size, size, size)
		ore.Material = Enum.Material[mine:GetAttribute("OreMaterial") or "Neon"]
		ore.Color = mine:GetAttribute("OreColor") or Color3.new(1, 1, 1)
		ore.CFrame = drop.CFrame * CFrame.Angles(math.random() * 6.28, math.random() * 6.28, 0)
		ore:SetAttribute("Value", mine:GetAttribute("OreValue") or 25)
		ore.Parent = workspace
		Debris:AddItem(ore, 30)
	end
end
]]
	s.Parent = model
end
print(("[CorsairCannonMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
