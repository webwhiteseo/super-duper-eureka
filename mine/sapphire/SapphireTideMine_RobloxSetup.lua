-- SapphireTideMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SapphireTideMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AquaLED = {"Neon", 80, 255, 220, 0},
	Black = {"SmoothPlastic", 8, 16, 24, 0},
	Coral = {"SmoothPlastic", 255, 112, 104, 0},
	Crystal = {"Glass", 90, 220, 255, 0.15},
	DeepSteel = {"DiamondPlate", 18, 40, 70, 0},
	FinBone = {"SmoothPlastic", 16, 60, 90, 0},
	FinMembrane = {"Fabric", 40, 150, 170, 0},
	FinSpine = {"SmoothPlastic", 12, 44, 70, 0},
	Flame = {"Neon", 150, 240, 255, 0},
	Neon = {"Neon", 200, 250, 255, 0},
	Ore = {"Neon", 170, 240, 255, 0},
	Pearl = {"SmoothPlastic", 240, 240, 250, 0},
	PearlKnob = {"Neon", 230, 240, 255, 0},
	Rock = {"Slate", 22, 34, 46, 0},
	Screen = {"Neon", 170, 240, 255, 0},
	Stone = {"Slate", 44, 112, 168, 0},
	WaterOrb = {"Glass", 60, 170, 230, 0.25}
}
local LIGHTS = {
	Crystal = {30, 180, 240, 8, 0.6},
	Flame = {80, 220, 255, 12, 2},
	Neon = {120, 230, 255, 10, 1},
	WaterOrb = {30, 140, 220, 14, 1.6}
}
local ORE_PART = "Ore"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SapphireTideMine_Roblox", true) or workspace:FindFirstChild("SapphireTideMine", true) end
assert(model, "Select the imported SapphireTideMine model first.")
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
print(("[SapphireTideMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
