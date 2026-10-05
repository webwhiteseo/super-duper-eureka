-- TwinSerpentsMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import TwinSerpentsMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	CharredHorn = {"SmoothPlastic", 40, 30, 30, 0},
	DrakeBelly = {"SmoothPlastic", 236, 164, 80, 0},
	DrakeScales = {"SmoothPlastic", 168, 32, 28, 0},
	EmberEye = {"Neon", 255, 220, 80, 0},
	EquinoxOrb = {"Neon", 200, 140, 255, 0},
	EquinoxOre = {"Neon", 210, 160, 255, 0},
	EquinoxTrim = {"Neon", 180, 120, 255, 0},
	Fang = {"SmoothPlastic", 245, 240, 228, 0},
	FireRune = {"Neon", 255, 100, 40, 0},
	FlameBreath = {"Neon", 255, 150, 40, 0},
	FrostBelly = {"SmoothPlastic", 210, 230, 244, 0},
	FrostBreath = {"Neon", 170, 240, 255, 0},
	FrostEye = {"Neon", 180, 250, 255, 0},
	FrostRune = {"Neon", 120, 220, 255, 0},
	FrostScales = {"SmoothPlastic", 64, 116, 178, 0},
	IceCrystal = {"Glass", 150, 225, 255, 0.15},
	IceHorn = {"SmoothPlastic", 230, 240, 250, 0},
	LavaGlow = {"Neon", 255, 110, 20, 0},
	MagmaCrust = {"Basalt", 44, 30, 28, 0},
	ObsidianPillar = {"Basalt", 34, 26, 44, 0},
	Snow = {"Snow", 240, 246, 255, 0}
}
local LIGHTS = {
	EquinoxOrb = {170, 100, 255, 16, 2},
	FireRune = {255, 70, 20, 6, 0.8},
	FrostRune = {80, 200, 255, 6, 0.8},
	IceCrystal = {110, 200, 255, 8, 0.6},
	LavaGlow = {255, 80, 10, 12, 1.5}
}
local ORE_PART = "EquinoxOre"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TwinSerpentsMine_Roblox", true) or workspace:FindFirstChild("TwinSerpentsMine", true) end
assert(model, "Select the imported TwinSerpentsMine model first.")
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
print(("[TwinSerpentsMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
