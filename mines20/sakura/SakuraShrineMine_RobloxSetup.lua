-- SakuraShrineMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SakuraShrineMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Bamboo = {"SmoothPlastic", 150, 182, 82, 0},
	BlackLacquer = {"SmoothPlastic", 20, 18, 20, 0},
	Blossom = {"SmoothPlastic", 255, 150, 196, 0},
	BlossomOre = {"Neon", 255, 190, 220, 0},
	BlossomTrim = {"Neon", 255, 150, 190, 0},
	CherryBark = {"Wood", 74, 46, 38, 0},
	DarkWood = {"WoodPlanks", 52, 34, 26, 0},
	Gold = {"Metal", 236, 186, 70, 0},
	KoiOrange = {"SmoothPlastic", 255, 120, 40, 0},
	KoiWhite = {"SmoothPlastic", 250, 246, 240, 0},
	LanternGlow = {"Neon", 255, 214, 140, 0},
	LanternStone = {"Slate", 150, 150, 144, 0},
	LilyPads = {"SmoothPlastic", 70, 150, 70, 0},
	Petals = {"Neon", 255, 196, 220, 0},
	PondWater = {"Glass", 60, 150, 180, 0.25},
	RoofTiles = {"Slate", 54, 60, 76, 0},
	VermilionLacquer = {"SmoothPlastic", 205, 46, 30, 0},
	ZenStone = {"SmoothPlastic", 176, 176, 170, 0}
}
local LIGHTS = {
	LanternGlow = {255, 180, 90, 9, 1.3}
}
local ORE_PART = "BlossomOre"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SakuraShrineMine_Roblox", true) or workspace:FindFirstChild("SakuraShrineMine", true) end
assert(model, "Select the imported SakuraShrineMine model first.")
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
print(("[SakuraShrineMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
