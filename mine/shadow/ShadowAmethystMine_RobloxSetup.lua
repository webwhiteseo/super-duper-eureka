-- ShadowAmethystMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import ShadowAmethystMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 8, 6, 12, 0},
	BoneHorn = {"SmoothPlastic", 222, 214, 198, 0},
	Chain = {"Metal", 64, 60, 74, 0},
	Crystal = {"Glass", 190, 110, 255, 0.15},
	Flame = {"Neon", 220, 140, 255, 0},
	IrisGlow = {"Neon", 210, 110, 255, 0},
	Neon = {"Neon", 230, 200, 255, 0},
	Ore = {"Neon", 220, 180, 255, 0},
	Rock = {"Slate", 26, 20, 34, 0},
	Screen = {"Neon", 220, 170, 255, 0},
	ShadowIron = {"DiamondPlate", 28, 20, 40, 0},
	Stone = {"Slate", 54, 38, 78, 0},
	VioletLED = {"Neon", 255, 90, 255, 0},
	VoidEye = {"SmoothPlastic", 14, 8, 22, 0},
	VoidKnob = {"Neon", 130, 70, 255, 0},
	WingBone = {"SmoothPlastic", 222, 214, 198, 0},
	WingMembrane = {"Fabric", 72, 40, 112, 0}
}
local LIGHTS = {
	Crystal = {150, 60, 255, 8, 0.6},
	Flame = {190, 80, 255, 12, 2},
	IrisGlow = {180, 70, 255, 14, 1.6},
	Neon = {190, 130, 255, 10, 1}
}
local ORE_PART = "Ore"

local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ShadowAmethystMine_Roblox", true) or workspace:FindFirstChild("ShadowAmethystMine", true) end
assert(model, "Select the imported ShadowAmethystMine model first.")
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
print(("[ShadowAmethystMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))
