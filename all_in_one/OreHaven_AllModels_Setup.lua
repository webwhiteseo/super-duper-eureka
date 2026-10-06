-- OreHaven_AllModels: styles every imported item and adds its working scripts (droppers, furnaces, upgrader).
-- 1. Import OreHaven_AllModels_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh").
-- 2. Select the imported OreHaven_AllModels model in the Explorer.  3. Paste this whole file into View > Command Bar, press Enter.
local ROOT = game:GetService("Selection"):Get()[1]
assert(ROOT, "Select the imported OreHaven_AllModels model first.")
local done, missing = 0, {}
do local __M = ROOT:FindFirstChild("CryoReactorDropper", true)
if __M then local ok, err = pcall(function()
-- CryoReactorDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import CryoReactorDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 120, 255, 230, 0},
	CoreGlow = {"Neon", 60, 240, 220, 0},
	Crystal = {"Glass", 100, 255, 255, 0.15},
	DarkPlate = {"DiamondPlate", 54, 79, 93, 0},
	Ore = {"Neon", 120, 255, 255, 0},
	SteelPlate = {"DiamondPlate", 96, 136, 158, 0}
}
local LIGHTS = {
	AccentNeon = {120, 255, 230, 8, 1},
	CoreGlow = {60, 240, 220, 14, 1.8},
	Crystal = {60, 240, 220, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("CryoReactorDropper_Roblox", true) or workspace:FindFirstChild("CryoReactorDropper", true) end
assert(model, "Select the imported CryoReactorDropper model first.")
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
print(("[CryoReactorDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("CryoReactorDropper: " .. tostring(err)) end else table.insert(missing, "CryoReactorDropper") end end
do local __M = ROOT:FindFirstChild("HiveExtractorDropper", true)
if __M then local ok, err = pcall(function()
-- HiveExtractorDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import HiveExtractorDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 240, 160, 0},
	CoreGlow = {"Neon", 255, 190, 40, 0},
	Crystal = {"Glass", 255, 230, 80, 0.15},
	DarkPlate = {"DiamondPlate", 86, 72, 50, 0},
	HoneycombWax = {"SmoothPlastic", 230, 170, 50, 0},
	Ore = {"Neon", 255, 250, 100, 0},
	SteelPlate = {"DiamondPlate", 147, 125, 90, 0}
}
local LIGHTS = {
	AccentNeon = {255, 240, 160, 8, 1},
	CoreGlow = {255, 190, 40, 14, 1.8},
	Crystal = {255, 190, 40, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("HiveExtractorDropper_Roblox", true) or workspace:FindFirstChild("HiveExtractorDropper", true) end
assert(model, "Select the imported HiveExtractorDropper model first.")
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
print(("[HiveExtractorDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("HiveExtractorDropper: " .. tostring(err)) end else table.insert(missing, "HiveExtractorDropper") end end
do local __M = ROOT:FindFirstChild("BlastCraneDropper", true)
if __M then local ok, err = pcall(function()
-- BlastCraneDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import BlastCraneDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 200, 80, 0},
	CoreGlow = {"Neon", 255, 120, 40, 0},
	DarkPlate = {"DiamondPlate", 72, 64, 61, 0},
	DynamiteRed = {"SmoothPlastic", 200, 30, 30, 0},
	KegWood = {"WoodPlanks", 150, 104, 60, 0},
	Ore = {"Neon", 255, 180, 100, 0},
	QuarryStone = {"Slate", 110, 110, 112, 0},
	SteelPlate = {"DiamondPlate", 125, 112, 107, 0}
}
local LIGHTS = {
	AccentNeon = {255, 200, 80, 8, 1},
	CoreGlow = {255, 120, 40, 14, 1.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("BlastCraneDropper_Roblox", true) or workspace:FindFirstChild("BlastCraneDropper", true) end
assert(model, "Select the imported BlastCraneDropper model first.")
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
print(("[BlastCraneDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("BlastCraneDropper: " .. tostring(err)) end else table.insert(missing, "BlastCraneDropper") end end
do local __M = ROOT:FindFirstChild("FurnaceEngineDropper", true)
if __M then local ok, err = pcall(function()
-- FurnaceEngineDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import FurnaceEngineDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 80, 40, 0},
	Copper = {"Metal", 200, 120, 70, 0},
	CoreGlow = {"Neon", 255, 180, 50, 0},
	Crystal = {"Glass", 255, 220, 90, 0.15},
	DarkPlate = {"DiamondPlate", 97, 79, 64, 0},
	Ore = {"Neon", 255, 240, 110, 0},
	Screen = {"Neon", 255, 220, 120, 0},
	SteelPlate = {"DiamondPlate", 165, 136, 112, 0}
}
local LIGHTS = {
	AccentNeon = {255, 80, 40, 8, 1},
	CoreGlow = {255, 180, 50, 14, 1.8},
	Crystal = {255, 180, 50, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("FurnaceEngineDropper_Roblox", true) or workspace:FindFirstChild("FurnaceEngineDropper", true) end
assert(model, "Select the imported FurnaceEngineDropper model first.")
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
print(("[FurnaceEngineDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("FurnaceEngineDropper: " .. tostring(err)) end else table.insert(missing, "FurnaceEngineDropper") end end
do local __M = ROOT:FindFirstChild("EmberCrusherDropper", true)
if __M then local ok, err = pcall(function()
-- EmberCrusherDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import EmberCrusherDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 230, 200, 0},
	Crystal = {"Glass", 255, 100, 90, 0.15},
	DarkPlate = {"DiamondPlate", 72, 68, 64, 0},
	Ore = {"Neon", 255, 120, 110, 0},
	Rubble = {"Slate", 70, 66, 60, 0},
	SteelPlate = {"DiamondPlate", 125, 118, 112, 0}
}
local LIGHTS = {
	AccentNeon = {255, 230, 200, 8, 1},
	Crystal = {255, 60, 50, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("EmberCrusherDropper_Roblox", true) or workspace:FindFirstChild("EmberCrusherDropper", true) end
assert(model, "Select the imported EmberCrusherDropper model first.")
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
print(("[EmberCrusherDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("EmberCrusherDropper: " .. tostring(err)) end else table.insert(missing, "EmberCrusherDropper") end end
do local __M = ROOT:FindFirstChild("SapphireColossusDropper", true)
if __M then local ok, err = pcall(function()
-- SapphireColossusDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SapphireColossusDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 150, 230, 255, 0},
	CoreGlow = {"Neon", 70, 190, 255, 0},
	Crystal = {"Glass", 110, 230, 255, 0.15},
	DarkPlate = {"DiamondPlate", 61, 72, 86, 0},
	Ore = {"Neon", 130, 250, 255, 0},
	SteelPlate = {"DiamondPlate", 107, 125, 147, 0}
}
local LIGHTS = {
	AccentNeon = {150, 230, 255, 8, 1},
	CoreGlow = {70, 190, 255, 14, 1.8},
	Crystal = {70, 190, 255, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SapphireColossusDropper_Roblox", true) or workspace:FindFirstChild("SapphireColossusDropper", true) end
assert(model, "Select the imported SapphireColossusDropper model first.")
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
print(("[SapphireColossusDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("SapphireColossusDropper: " .. tostring(err)) end else table.insert(missing, "SapphireColossusDropper") end end
do local __M = ROOT:FindFirstChild("PlasmaPylonDropper", true)
if __M then local ok, err = pcall(function()
-- PlasmaPylonDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import PlasmaPylonDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 140, 255, 0},
	CoreGlow = {"Neon", 190, 90, 255, 0},
	DarkPlate = {"DiamondPlate", 64, 54, 93, 0},
	Ore = {"Neon", 250, 150, 255, 0},
	SteelPlate = {"DiamondPlate", 112, 96, 158, 0}
}
local LIGHTS = {
	AccentNeon = {255, 140, 255, 8, 1},
	CoreGlow = {190, 90, 255, 14, 1.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("PlasmaPylonDropper_Roblox", true) or workspace:FindFirstChild("PlasmaPylonDropper", true) end
assert(model, "Select the imported PlasmaPylonDropper model first.")
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
print(("[PlasmaPylonDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("PlasmaPylonDropper: " .. tostring(err)) end else table.insert(missing, "PlasmaPylonDropper") end end
do local __M = ROOT:FindFirstChild("MagmaPumpDropper", true)
if __M then local ok, err = pcall(function()
-- MagmaPumpDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import MagmaPumpDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 200, 60, 0},
	Basalt = {"Basalt", 54, 44, 42, 0},
	CoreGlow = {"Neon", 255, 110, 30, 0},
	DarkPlate = {"DiamondPlate", 79, 64, 61, 0},
	Ore = {"Neon", 255, 170, 90, 0},
	SteelPlate = {"DiamondPlate", 136, 112, 107, 0}
}
local LIGHTS = {
	AccentNeon = {255, 200, 60, 8, 1},
	CoreGlow = {255, 110, 30, 14, 1.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("MagmaPumpDropper_Roblox", true) or workspace:FindFirstChild("MagmaPumpDropper", true) end
assert(model, "Select the imported MagmaPumpDropper model first.")
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
print(("[MagmaPumpDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("MagmaPumpDropper: " .. tostring(err)) end else table.insert(missing, "MagmaPumpDropper") end end
do local __M = ROOT:FindFirstChild("StarforgeAnvilDropper", true)
if __M then local ok, err = pcall(function()
-- StarforgeAnvilDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import StarforgeAnvilDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 255, 240, 180, 0},
	CoreGlow = {"Neon", 120, 200, 255, 0},
	Crystal = {"Glass", 160, 240, 255, 0.15},
	DarkPlate = {"DiamondPlate", 72, 72, 90, 0},
	Ore = {"Neon", 180, 255, 255, 0},
	SteelPlate = {"DiamondPlate", 125, 125, 154, 0}
}
local LIGHTS = {
	AccentNeon = {255, 240, 180, 8, 1},
	CoreGlow = {120, 200, 255, 14, 1.8},
	Crystal = {120, 200, 255, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("StarforgeAnvilDropper_Roblox", true) or workspace:FindFirstChild("StarforgeAnvilDropper", true) end
assert(model, "Select the imported StarforgeAnvilDropper model first.")
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
print(("[StarforgeAnvilDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("StarforgeAnvilDropper: " .. tostring(err)) end else table.insert(missing, "StarforgeAnvilDropper") end end
do local __M = ROOT:FindFirstChild("GeyserVentDropper", true)
if __M then local ok, err = pcall(function()
-- GeyserVentDropper: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import GeyserVentDropper_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AccentNeon = {"Neon", 200, 255, 240, 0},
	CoreGlow = {"Neon", 110, 255, 200, 0},
	Crystal = {"Glass", 150, 255, 240, 0.15},
	DarkPlate = {"DiamondPlate", 86, 93, 100, 0},
	Ore = {"Neon", 170, 255, 255, 0},
	Steam = {"SmoothPlastic", 236, 240, 244, 0.3},
	SteelPlate = {"DiamondPlate", 147, 158, 170, 0},
	VentRock = {"Slate", 80, 76, 72, 0}
}
local LIGHTS = {
	AccentNeon = {200, 255, 240, 8, 1},
	CoreGlow = {110, 255, 200, 14, 1.8},
	Crystal = {110, 255, 200, 8, 0.8}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("GeyserVentDropper_Roblox", true) or workspace:FindFirstChild("GeyserVentDropper", true) end
assert(model, "Select the imported GeyserVentDropper model first.")
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
print(("[GeyserVentDropper] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("GeyserVentDropper: " .. tostring(err)) end else table.insert(missing, "GeyserVentDropper") end end
do local __M = ROOT:FindFirstChild("AstralOwlMine", true)
if __M then local ok, err = pcall(function()
-- AstralOwlMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import AstralOwlMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 10, 10, 20, 0},
	DuskFeathers = {"Metal", 74, 52, 146, 0},
	GoldTrim = {"Metal", 232, 182, 72, 0},
	LensGlow = {"Neon", 120, 230, 255, 0},
	MeteorRock = {"Slate", 38, 34, 52, 0},
	MoonSilver = {"SmoothPlastic", 214, 214, 226, 0},
	NightMetal = {"Metal", 28, 36, 86, 0},
	PlanetPurple = {"SmoothPlastic", 140, 90, 210, 0},
	PlanetRed = {"SmoothPlastic", 220, 90, 60, 0},
	PlanetTeal = {"SmoothPlastic", 60, 190, 170, 0},
	Pupil = {"SmoothPlastic", 8, 8, 14, 0},
	StarCore = {"Neon", 255, 228, 180, 0},
	StarfeatherOre = {"Neon", 205, 225, 255, 0},
	StarglassCrystal = {"Glass", 175, 135, 255, 0.15},
	Starlight = {"Neon", 190, 245, 255, 0}
}
local LIGHTS = {
	LensGlow = {90, 210, 255, 10, 1.4},
	StarCore = {255, 190, 110, 14, 1.8},
	Starlight = {160, 235, 255, 8, 0.9}
}
local ORE_PART = "StarfeatherOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("AstralOwlMine_Roblox", true) or workspace:FindFirstChild("AstralOwlMine", true) end
assert(model, "Select the imported AstralOwlMine model first.")
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
print(("[AstralOwlMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("AstralOwlMine: " .. tostring(err)) end else table.insert(missing, "AstralOwlMine") end end
do local __M = ROOT:FindFirstChild("CorsairCannonMine", true)
if __M then local ok, err = pcall(function()
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

local model = __M
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

end) if ok then done += 1 else warn("CorsairCannonMine: " .. tostring(err)) end else table.insert(missing, "CorsairCannonMine") end end
do local __M = ROOT:FindFirstChild("GlowshroomGroveMine", true)
if __M then local ok, err = pcall(function()
-- GlowshroomGroveMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import GlowshroomGroveMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	DoorWood = {"WoodPlanks", 128, 82, 46, 0},
	FairyLight = {"Neon", 240, 255, 160, 0},
	GlowSpots = {"Neon", 150, 255, 240, 0},
	GlowingGills = {"Neon", 210, 160, 255, 0},
	MagentaCap = {"SmoothPlastic", 220, 60, 160, 0},
	Moss = {"LeafyGrass", 64, 130, 56, 0},
	MossyStone = {"Slate", 88, 96, 92, 0},
	MushroomStem = {"SmoothPlastic", 232, 222, 196, 0},
	Roots = {"Wood", 92, 70, 50, 0},
	SporeOre = {"Neon", 180, 255, 225, 0},
	SporePod = {"Glass", 190, 255, 220, 0.2},
	TealCap = {"SmoothPlastic", 40, 170, 160, 0},
	Vine = {"SmoothPlastic", 50, 110, 60, 0},
	VioletCap = {"SmoothPlastic", 112, 62, 205, 0},
	WindowGlow = {"Neon", 255, 210, 130, 0}
}
local LIGHTS = {
	FairyLight = {220, 255, 120, 6, 0.8},
	GlowSpots = {90, 255, 230, 9, 1},
	GlowingGills = {170, 110, 255, 12, 1.4},
	WindowGlow = {255, 170, 70, 8, 1.2}
}
local ORE_PART = "SporeOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("GlowshroomGroveMine_Roblox", true) or workspace:FindFirstChild("GlowshroomGroveMine", true) end
assert(model, "Select the imported GlowshroomGroveMine model first.")
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
print(("[GlowshroomGroveMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("GlowshroomGroveMine: " .. tostring(err)) end else table.insert(missing, "GlowshroomGroveMine") end end
do local __M = ROOT:FindFirstChild("KrakenDepthsMine", true)
if __M then local ok, err = pcall(function()
-- KrakenDepthsMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import KrakenDepthsMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AnchorIron = {"Metal", 50, 56, 64, 0},
	Brass = {"Metal", 200, 150, 70, 0},
	Bubbles = {"Glass", 200, 245, 255, 0.35},
	Coral = {"SmoothPlastic", 255, 110, 100, 0},
	GlowCoral = {"Neon", 180, 120, 255, 0},
	KrakenEye = {"Neon", 255, 220, 70, 0},
	KrakenSkin = {"SmoothPlastic", 150, 50, 120, 0},
	KrakenSuckers = {"SmoothPlastic", 240, 190, 200, 0},
	PearlOre = {"Neon", 230, 245, 255, 0},
	PortholeGlass = {"Neon", 120, 240, 230, 0},
	Pupil = {"SmoothPlastic", 10, 6, 10, 0},
	SeaSand = {"Sand", 196, 176, 130, 0},
	Seaweed = {"SmoothPlastic", 40, 140, 80, 0},
	VerdigrisCopper = {"Metal", 70, 150, 130, 0}
}
local LIGHTS = {
	GlowCoral = {150, 90, 255, 6, 0.8},
	KrakenEye = {255, 200, 40, 8, 1.2},
	PortholeGlass = {60, 220, 210, 12, 1.4}
}
local ORE_PART = "PearlOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("KrakenDepthsMine_Roblox", true) or workspace:FindFirstChild("KrakenDepthsMine", true) end
assert(model, "Select the imported KrakenDepthsMine model first.")
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
print(("[KrakenDepthsMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("KrakenDepthsMine: " .. tostring(err)) end else table.insert(missing, "KrakenDepthsMine") end end
do local __M = ROOT:FindFirstChild("OreExpressMine", true)
if __M then local ok, err = pcall(function()
-- OreExpressMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import OreExpressMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	BlackPaint = {"SmoothPlastic", 18, 18, 20, 0},
	Brass = {"Metal", 226, 172, 70, 0},
	BufferRed = {"SmoothPlastic", 184, 34, 28, 0},
	Coal = {"Slate", 36, 34, 36, 0},
	EngineGreen = {"SmoothPlastic", 22, 92, 54, 0},
	ExpressOre = {"Neon", 255, 196, 90, 0},
	FireboxFire = {"Neon", 255, 120, 30, 0},
	LampGlow = {"Neon", 255, 222, 150, 0},
	PlatformBrick = {"Brick", 150, 70, 52, 0},
	PlatformPlanks = {"WoodPlanks", 150, 112, 74, 0},
	RailSteel = {"Metal", 150, 150, 158, 0},
	SleeperWood = {"Wood", 82, 58, 40, 0},
	SootIron = {"DiamondPlate", 34, 34, 38, 0},
	StationCream = {"SmoothPlastic", 234, 222, 190, 0},
	Steam = {"SmoothPlastic", 236, 238, 242, 0.15}
}
local LIGHTS = {
	FireboxFire = {255, 100, 20, 10, 1.6},
	LampGlow = {255, 190, 100, 12, 1.4}
}
local ORE_PART = "ExpressOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("OreExpressMine_Roblox", true) or workspace:FindFirstChild("OreExpressMine", true) end
assert(model, "Select the imported OreExpressMine model first.")
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
print(("[OreExpressMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("OreExpressMine: " .. tostring(err)) end else table.insert(missing, "OreExpressMine") end end
do local __M = ROOT:FindFirstChild("MagmaGolemForge", true)
if __M then local ok, err = pcall(function()
-- MagmaGolemForge: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import MagmaGolemForge_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Basalt = {"Basalt", 58, 50, 48, 0},
	Brass = {"Metal", 205, 150, 60, 0},
	CharredWood = {"Wood", 60, 36, 24, 0},
	EmberOre = {"Neon", 255, 160, 90, 0},
	FireCrystal = {"Glass", 255, 150, 60, 0.1},
	ForgeIron = {"Metal", 64, 62, 68, 0},
	LavaGlow = {"Neon", 255, 120, 40, 0},
	MagmaCore = {"Neon", 255, 190, 90, 0}
}
local LIGHTS = {
	FireCrystal = {255, 110, 30, 7, 0.6},
	LavaGlow = {255, 100, 20, 10, 1.2},
	MagmaCore = {255, 150, 40, 18, 2.5}
}
local ORE_PART = "EmberOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("MagmaGolemForge_Roblox", true) or workspace:FindFirstChild("MagmaGolemForge", true) end
assert(model, "Select the imported MagmaGolemForge model first.")
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
print(("[MagmaGolemForge] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("MagmaGolemForge: " .. tostring(err)) end else table.insert(missing, "MagmaGolemForge") end end
do local __M = ROOT:FindFirstChild("ClockworkOwlMine", true)
if __M then local ok, err = pcall(function()
-- ClockworkOwlMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import ClockworkOwlMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AmberLens = {"Neon", 255, 190, 80, 0},
	Brass = {"Metal", 212, 160, 72, 0},
	ClockFace = {"SmoothPlastic", 244, 238, 222, 0},
	Copper = {"Metal", 198, 112, 64, 0},
	DarkIron = {"Metal", 46, 44, 48, 0},
	GearOre = {"Neon", 255, 210, 120, 0},
	Glass = {"Glass", 200, 230, 255, 0.5},
	InkBlack = {"SmoothPlastic", 18, 16, 16, 0},
	MainspringCore = {"Neon", 255, 220, 140, 0},
	Walnut = {"WoodPlanks", 74, 46, 30, 0}
}
local LIGHTS = {
	AmberLens = {255, 160, 40, 10, 1.6},
	MainspringCore = {255, 180, 60, 12, 1.8}
}
local ORE_PART = "GearOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ClockworkOwlMine_Roblox", true) or workspace:FindFirstChild("ClockworkOwlMine", true) end
assert(model, "Select the imported ClockworkOwlMine model first.")
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
print(("[ClockworkOwlMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("ClockworkOwlMine: " .. tostring(err)) end else table.insert(missing, "ClockworkOwlMine") end end
do local __M = ROOT:FindFirstChild("PhoenixNestMine", true)
if __M then local ok, err = pcall(function()
-- PhoenixNestMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import PhoenixNestMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	DarkTwigs = {"Wood", 78, 52, 32, 0},
	EggShell = {"Metal", 235, 190, 90, 0},
	EyeGlow = {"Neon", 255, 255, 220, 0},
	FlameYellow = {"Neon", 255, 176, 0, 0},
	Gold = {"Metal", 240, 190, 70, 0},
	Obsidian = {"Basalt", 24, 18, 20, 0},
	PhoenixOrange = {"Neon", 255, 84, 0, 0},
	PhoenixOre = {"Neon", 255, 150, 30, 0},
	PhoenixRed = {"SmoothPlastic", 196, 22, 12, 0},
	Ruby = {"Glass", 230, 20, 40, 0.1},
	Twigs = {"Wood", 112, 78, 46, 0},
	VolcanicRock = {"Slate", 62, 50, 46, 0}
}
local LIGHTS = {
	FlameYellow = {255, 140, 0, 12, 1.6},
	PhoenixOrange = {255, 60, 0, 10, 1.2}
}
local ORE_PART = "PhoenixOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("PhoenixNestMine_Roblox", true) or workspace:FindFirstChild("PhoenixNestMine", true) end
assert(model, "Select the imported PhoenixNestMine model first.")
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
print(("[PhoenixNestMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("PhoenixNestMine: " .. tostring(err)) end else table.insert(missing, "PhoenixNestMine") end end
do local __M = ROOT:FindFirstChild("SunPyramidMine", true)
if __M then local ok, err = pcall(function()
-- SunPyramidMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SunPyramidMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 16, 12, 10, 0},
	BrazierFlame = {"Neon", 255, 170, 60, 0},
	DarkStone = {"SmoothPlastic", 44, 32, 22, 0},
	Gold = {"Metal", 236, 186, 70, 0},
	Lapis = {"SmoothPlastic", 30, 62, 170, 0},
	PaleSandstone = {"Sandstone", 232, 206, 156, 0},
	Sandstone = {"Sandstone", 214, 180, 124, 0},
	SunCore = {"Neon", 255, 236, 170, 0},
	SunstoneOre = {"Neon", 255, 220, 120, 0},
	TurquoiseGlow = {"Neon", 80, 230, 210, 0}
}
local LIGHTS = {
	BrazierFlame = {255, 120, 30, 10, 1.6},
	SunCore = {255, 190, 70, 24, 2.6},
	TurquoiseGlow = {40, 220, 200, 7, 0.8}
}
local ORE_PART = "SunstoneOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SunPyramidMine_Roblox", true) or workspace:FindFirstChild("SunPyramidMine", true) end
assert(model, "Select the imported SunPyramidMine model first.")
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
print(("[SunPyramidMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("SunPyramidMine: " .. tostring(err)) end else table.insert(missing, "SunPyramidMine") end end
do local __M = ROOT:FindFirstChild("SakuraShrineMine", true)
if __M then local ok, err = pcall(function()
-- SakuraShrineMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SakuraShrineMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Bamboo = {"SmoothPlastic", 150, 182, 82, 0},
	BlackLacquer = {"SmoothPlastic", 20, 18, 20, 0},
	Blossom = {"SmoothPlastic", 255, 150, 196, 0},
	BlossomOre = {"Neon", 255, 190, 220, 0},
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
	VermilionLacquer = {"SmoothPlastic", 205, 46, 30, 0}
}
local LIGHTS = {
	LanternGlow = {255, 180, 90, 9, 1.3}
}
local ORE_PART = "BlossomOre"

local model = __M
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

end) if ok then done += 1 else warn("SakuraShrineMine: " .. tostring(err)) end else table.insert(missing, "SakuraShrineMine") end end
do local __M = ROOT:FindFirstChild("SandstingerMine", true)
if __M then local ok, err = pcall(function()
-- SandstingerMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SandstingerMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	BleachedBone = {"SmoothPlastic", 232, 222, 196, 0},
	BronzeArmour = {"Metal", 178, 104, 46, 0},
	Cactus = {"SmoothPlastic", 70, 128, 66, 0},
	CactusBloom = {"Neon", 255, 90, 140, 0},
	DesertRock = {"Slate", 140, 92, 62, 0},
	DuneSand = {"Sand", 226, 186, 128, 0},
	EyeGlow = {"Neon", 255, 40, 20, 0},
	GoldTrim = {"Metal", 240, 186, 70, 0},
	JointSteel = {"DiamondPlate", 54, 48, 46, 0},
	Sandstone = {"Sandstone", 176, 128, 82, 0},
	TopazCrystal = {"Glass", 255, 140, 10, 0.15},
	TopazOre = {"Neon", 255, 170, 40, 0},
	VenomGlow = {"Neon", 255, 110, 10, 0}
}
local LIGHTS = {
	EyeGlow = {255, 20, 10, 6, 1},
	TopazCrystal = {255, 110, 0, 10, 1.2},
	VenomGlow = {255, 80, 0, 14, 1.8}
}
local ORE_PART = "TopazOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SandstingerMine_Roblox", true) or workspace:FindFirstChild("SandstingerMine", true) end
assert(model, "Select the imported SandstingerMine model first.")
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
print(("[SandstingerMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("SandstingerMine: " .. tostring(err)) end else table.insert(missing, "SandstingerMine") end end
do local __M = ROOT:FindFirstChild("TempestCoilMine", true)
if __M then local ok, err = pcall(function()
-- TempestCoilMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import TempestCoilMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 12, 12, 18, 0},
	BlueGlaze = {"SmoothPlastic", 60, 90, 190, 0},
	CableRubber = {"SmoothPlastic", 24, 24, 28, 0},
	Ceramic = {"SmoothPlastic", 232, 236, 246, 0},
	ChargedOre = {"Neon", 200, 225, 255, 0},
	Copper = {"Metal", 205, 115, 62, 0},
	HazardYellow = {"SmoothPlastic", 250, 200, 30, 0},
	JarGlass = {"Glass", 170, 210, 255, 0.3},
	Lightning = {"Neon", 210, 230, 255, 0},
	Steel = {"Metal", 110, 116, 128, 0},
	StormCloud = {"SmoothPlastic", 78, 82, 104, 0},
	VioletArc = {"Neon", 220, 170, 255, 0}
}
local LIGHTS = {
	Lightning = {150, 200, 255, 14, 2},
	VioletArc = {180, 110, 255, 8, 1}
}
local ORE_PART = "ChargedOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TempestCoilMine_Roblox", true) or workspace:FindFirstChild("TempestCoilMine", true) end
assert(model, "Select the imported TempestCoilMine model first.")
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
print(("[TempestCoilMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("TempestCoilMine: " .. tostring(err)) end else table.insert(missing, "TempestCoilMine") end end
do local __M = ROOT:FindFirstChild("TitanDrillMine", true)
if __M then local ok, err = pcall(function()
-- TitanDrillMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import TitanDrillMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Beacon = {"Neon", 255, 130, 20, 0},
	CabGlass = {"Glass", 150, 210, 240, 0.2},
	CopperPipe = {"Metal", 190, 110, 60, 0},
	ExhaustSmoke = {"SmoothPlastic", 110, 110, 116, 0.25},
	HazardBlack = {"SmoothPlastic", 24, 24, 26, 0},
	HazardYellow = {"SmoothPlastic", 246, 184, 20, 0},
	PitDark = {"SmoothPlastic", 18, 16, 16, 0},
	QuarryRock = {"Slate", 108, 92, 80, 0},
	RigSteel = {"Metal", 130, 134, 140, 0},
	RigYellow = {"SmoothPlastic", 240, 176, 20, 0},
	TitanCrystal = {"Neon", 60, 255, 190, 0},
	TitanOre = {"Neon", 90, 255, 200, 0},
	TrackRubber = {"SmoothPlastic", 34, 34, 36, 0}
}
local LIGHTS = {
	Beacon = {255, 100, 0, 12, 1.6},
	TitanCrystal = {30, 230, 160, 10, 1.2}
}
local ORE_PART = "TitanOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TitanDrillMine_Roblox", true) or workspace:FindFirstChild("TitanDrillMine", true) end
assert(model, "Select the imported TitanDrillMine model first.")
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
print(("[TitanDrillMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("TitanDrillMine: " .. tostring(err)) end else table.insert(missing, "TitanDrillMine") end end
do local __M = ROOT:FindFirstChild("TwinSerpentsMine", true)
if __M then local ok, err = pcall(function()
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

local model = __M
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

end) if ok then done += 1 else warn("TwinSerpentsMine: " .. tostring(err)) end else table.insert(missing, "TwinSerpentsMine") end end
do local __M = ROOT:FindFirstChild("VoidRiftMine", true)
if __M then local ok, err = pcall(function()
-- VoidRiftMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import VoidRiftMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	ChainIron = {"Metal", 60, 58, 70, 0},
	EyeWhite = {"Neon", 230, 240, 200, 0},
	Obsidian = {"Basalt", 22, 16, 32, 0},
	Pupil = {"SmoothPlastic", 10, 0, 10, 0},
	RiftSwirl = {"Neon", 200, 90, 255, 0},
	RiftSwirlPink = {"Neon", 255, 120, 220, 0},
	RuneGlow = {"Neon", 230, 140, 255, 0},
	TentacleFlesh = {"SmoothPlastic", 70, 30, 90, 0},
	VoidCore = {"SmoothPlastic", 6, 2, 12, 0},
	VoidOre = {"Neon", 210, 130, 255, 0},
	VoidShard = {"Glass", 120, 50, 220, 0.1}
}
local LIGHTS = {
	EyeWhite = {200, 255, 140, 9, 1.2},
	RiftSwirl = {170, 50, 255, 20, 2.4},
	RuneGlow = {200, 80, 255, 8, 1},
	VoidShard = {110, 40, 230, 6, 0.6}
}
local ORE_PART = "VoidOre"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("VoidRiftMine_Roblox", true) or workspace:FindFirstChild("VoidRiftMine", true) end
assert(model, "Select the imported VoidRiftMine model first.")
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
print(("[VoidRiftMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("VoidRiftMine: " .. tostring(err)) end else table.insert(missing, "VoidRiftMine") end end
do local __M = ROOT:FindFirstChild("CyberNeonMine", true)
if __M then local ok, err = pcall(function()
-- CyberNeonMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import CyberNeonMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Antenna = {"Metal", 156, 162, 176, 0},
	Black = {"SmoothPlastic", 6, 6, 10, 0},
	CarbonShell = {"Metal", 34, 36, 46, 0},
	Chrome = {"Metal", 156, 162, 176, 0},
	Crystal = {"Glass", 255, 70, 225, 0.2},
	CyanKnob = {"Neon", 0, 240, 255, 0},
	Flame = {"Neon", 255, 90, 235, 0},
	Hologram = {"ForceField", 90, 240, 255, 0.5},
	Magenta = {"Neon", 255, 50, 210, 0},
	MagentaLED = {"Neon", 255, 40, 200, 0},
	Neon = {"Neon", 130, 250, 255, 0},
	Ore = {"Neon", 130, 255, 255, 0},
	Screen = {"Neon", 120, 255, 255, 0},
	ServerBlock = {"SmoothPlastic", 24, 26, 34, 0},
	WingPanel = {"SmoothPlastic", 18, 20, 28, 0},
	WingStrut = {"Neon", 0, 230, 255, 0}
}
local LIGHTS = {
	Crystal = {255, 30, 210, 8, 0.7},
	Flame = {255, 40, 220, 12, 2},
	Magenta = {255, 30, 200, 10, 1.2},
	Neon = {0, 230, 255, 10, 1}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("CyberNeonMine_Roblox", true) or workspace:FindFirstChild("CyberNeonMine", true) end
assert(model, "Select the imported CyberNeonMine model first.")
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
print(("[CyberNeonMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("CyberNeonMine: " .. tostring(err)) end else table.insert(missing, "CyberNeonMine") end end
do local __M = ROOT:FindFirstChild("JadeEmperorMine", true)
if __M then local ok, err = pcall(function()
-- JadeEmperorMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import JadeEmperorMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 16, 10, 8, 0},
	Crystal = {"Glass", 120, 255, 180, 0.15},
	DragonPearl = {"Neon", 255, 250, 232, 0},
	Flame = {"Neon", 255, 190, 90, 0},
	GoldAntler = {"Metal", 236, 186, 70, 0},
	GoldBone = {"Metal", 236, 186, 70, 0},
	GoldLED = {"Neon", 255, 200, 60, 0},
	Jade = {"Marble", 62, 152, 112, 0},
	Neon = {"Neon", 255, 236, 190, 0},
	Ore = {"Neon", 160, 255, 200, 0},
	PaperLantern = {"Neon", 224, 44, 32, 0},
	PearlKnob = {"Neon", 245, 245, 235, 0},
	RedLacquer = {"SmoothPlastic", 176, 30, 26, 0},
	RedSilk = {"Fabric", 196, 36, 30, 0},
	Rock = {"Slate", 44, 42, 38, 0},
	Screen = {"Neon", 255, 220, 150, 0}
}
local LIGHTS = {
	Crystal = {60, 220, 140, 8, 0.6},
	DragonPearl = {255, 240, 200, 14, 1.6},
	Flame = {255, 150, 50, 12, 2},
	Neon = {255, 210, 130, 10, 1},
	PaperLantern = {255, 70, 30, 10, 1.2}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("JadeEmperorMine_Roblox", true) or workspace:FindFirstChild("JadeEmperorMine", true) end
assert(model, "Select the imported JadeEmperorMine model first.")
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
print(("[JadeEmperorMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("JadeEmperorMine: " .. tostring(err)) end else table.insert(missing, "JadeEmperorMine") end end
do local __M = ROOT:FindFirstChild("BoneNecroMine", true)
if __M then local ok, err = pcall(function()
-- BoneNecroMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import BoneNecroMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 12, 14, 12, 0},
	Bone = {"Limestone", 214, 204, 180, 0},
	Crystal = {"Glass", 100, 255, 170, 0.15},
	DarkHorn = {"SmoothPlastic", 42, 38, 34, 0},
	GhostMembrane = {"Glass", 120, 255, 170, 0.45},
	GraveIron = {"DiamondPlate", 46, 52, 46, 0},
	Gravestone = {"Slate", 96, 100, 96, 0},
	Neon = {"Neon", 190, 255, 210, 0},
	Ore = {"Neon", 170, 255, 200, 0},
	Rock = {"Slate", 42, 46, 40, 0},
	Screen = {"Neon", 160, 255, 190, 0},
	SoulFire = {"Neon", 120, 255, 160, 0},
	SoulFlame = {"Neon", 150, 255, 190, 0},
	SoulKnob = {"Neon", 120, 255, 170, 0},
	SoulLED = {"Neon", 90, 255, 140, 0},
	WingBone = {"SmoothPlastic", 228, 220, 198, 0}
}
local LIGHTS = {
	Crystal = {40, 230, 120, 8, 0.6},
	Neon = {90, 255, 150, 10, 1},
	SoulFire = {60, 255, 120, 14, 1.6},
	SoulFlame = {60, 255, 130, 12, 2}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("BoneNecroMine_Roblox", true) or workspace:FindFirstChild("BoneNecroMine", true) end
assert(model, "Select the imported BoneNecroMine model first.")
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
print(("[BoneNecroMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("BoneNecroMine: " .. tostring(err)) end else table.insert(missing, "BoneNecroMine") end end
do local __M = ROOT:FindFirstChild("RoseQuartzMine", true)
if __M then local ok, err = pcall(function()
-- RoseQuartzMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import RoseQuartzMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 46, 22, 34, 0},
	Crystal = {"Glass", 255, 150, 205, 0.15},
	Flame = {"Neon", 255, 160, 225, 0},
	HeartGem = {"Neon", 255, 46, 116, 0},
	HeartLED = {"Neon", 255, 60, 140, 0},
	LilacCrystal = {"Glass", 200, 160, 255, 0.15},
	LilacKnob = {"Neon", 205, 150, 255, 0},
	Neon = {"Neon", 255, 232, 245, 0},
	Ore = {"Neon", 255, 190, 230, 0},
	Rock = {"Slate", 206, 186, 214, 0},
	RoseGold = {"Metal", 232, 162, 142, 0},
	Screen = {"Neon", 255, 200, 235, 0},
	Stone = {"Slate", 236, 172, 192, 0},
	WingBone = {"Metal", 232, 162, 142, 0},
	WingMembrane = {"Fabric", 255, 204, 228, 0}
}
local LIGHTS = {
	Crystal = {255, 100, 180, 8, 0.6},
	Flame = {255, 100, 200, 12, 2},
	HeartGem = {255, 20, 90, 14, 1.6},
	Neon = {255, 170, 220, 10, 1}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RoseQuartzMine_Roblox", true) or workspace:FindFirstChild("RoseQuartzMine", true) end
assert(model, "Select the imported RoseQuartzMine model first.")
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
print(("[RoseQuartzMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("RoseQuartzMine: " .. tostring(err)) end else table.insert(missing, "RoseQuartzMine") end end
do local __M = ROOT:FindFirstChild("SapphireTideMine", true)
if __M then local ok, err = pcall(function()
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

local model = __M
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

end) if ok then done += 1 else warn("SapphireTideMine: " .. tostring(err)) end else table.insert(missing, "SapphireTideMine") end end
do local __M = ROOT:FindFirstChild("ShadowAmethystMine", true)
if __M then local ok, err = pcall(function()
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

local model = __M
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

end) if ok then done += 1 else warn("ShadowAmethystMine: " .. tostring(err)) end else table.insert(missing, "ShadowAmethystMine") end end
do local __M = ROOT:FindFirstChild("SolarGoldMine", true)
if __M then local ok, err = pcall(function()
-- SolarGoldMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import SolarGoldMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 26, 20, 12, 0},
	BronzePlate = {"DiamondPlate", 112, 72, 30, 0},
	Crystal = {"Glass", 255, 190, 60, 0.15},
	Flame = {"Neon", 255, 250, 220, 0},
	GoldHorn = {"Metal", 240, 190, 70, 0},
	GoldKnob = {"Neon", 255, 190, 40, 0},
	Neon = {"Neon", 255, 240, 200, 0},
	Ore = {"Neon", 255, 220, 120, 0},
	Rock = {"Slate", 72, 56, 38, 0},
	Screen = {"Neon", 255, 230, 170, 0},
	Stone = {"Sandstone", 206, 164, 84, 0},
	SunCore = {"Neon", 255, 220, 120, 0},
	SunLED = {"Neon", 255, 140, 40, 0},
	WingBone = {"SmoothPlastic", 250, 240, 220, 0},
	WingMembrane = {"Fabric", 236, 204, 130, 0}
}
local LIGHTS = {
	Crystal = {255, 160, 20, 8, 0.6},
	Flame = {255, 230, 150, 12, 2},
	Neon = {255, 220, 140, 10, 1},
	SunCore = {255, 180, 60, 16, 2}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SolarGoldMine_Roblox", true) or workspace:FindFirstChild("SolarGoldMine", true) end
assert(model, "Select the imported SolarGoldMine model first.")
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
print(("[SolarGoldMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("SolarGoldMine: " .. tostring(err)) end else table.insert(missing, "SolarGoldMine") end end
do local __M = ROOT:FindFirstChild("CopperSteamMine", true)
if __M then local ok, err = pcall(function()
-- CopperSteamMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import CopperSteamMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	AmberLED = {"Neon", 255, 170, 40, 0},
	Black = {"SmoothPlastic", 22, 18, 16, 0},
	Brass = {"Metal", 212, 162, 70, 0},
	Coal = {"Slate", 32, 30, 30, 0},
	CopperPlate = {"Metal", 186, 104, 58, 0},
	Crystal = {"Glass", 255, 160, 50, 0.15},
	Flame = {"Neon", 255, 180, 80, 0},
	GaugeFace = {"SmoothPlastic", 240, 234, 216, 0},
	Iron = {"Metal", 54, 52, 54, 0},
	Neon = {"Neon", 255, 222, 160, 0},
	Ore = {"Neon", 255, 200, 120, 0},
	Patina = {"SmoothPlastic", 92, 170, 150, 0},
	Screen = {"Neon", 255, 210, 140, 0},
	Steam = {"SmoothPlastic", 232, 232, 236, 0.3},
	ValveRed = {"SmoothPlastic", 196, 40, 30, 0},
	WingCanvas = {"Fabric", 198, 172, 130, 0},
	WingSpar = {"Wood", 102, 66, 40, 0}
}
local LIGHTS = {
	Crystal = {255, 120, 20, 8, 0.6},
	Flame = {255, 140, 40, 12, 2},
	Neon = {255, 180, 90, 10, 1}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("CopperSteamMine_Roblox", true) or workspace:FindFirstChild("CopperSteamMine", true) end
assert(model, "Select the imported CopperSteamMine model first.")
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
print(("[CopperSteamMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("CopperSteamMine: " .. tostring(err)) end else table.insert(missing, "CopperSteamMine") end end
do local __M = ROOT:FindFirstChild("StormDrakeMine", true)
if __M then local ok, err = pcall(function()
-- StormDrakeMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import StormDrakeMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 14, 16, 22, 0},
	CopperCoil = {"Metal", 200, 110, 60, 0},
	Crystal = {"Glass", 140, 220, 255, 0.15},
	Flame = {"Neon", 150, 220, 255, 0},
	Horn = {"SmoothPlastic", 30, 34, 46, 0},
	Lightning = {"Neon", 255, 240, 120, 0},
	Neon = {"Neon", 255, 250, 210, 0},
	Ore = {"Neon", 255, 240, 150, 0},
	Rock = {"Slate", 40, 44, 54, 0},
	Screen = {"Neon", 255, 240, 170, 0},
	SparkKnob = {"Neon", 120, 200, 255, 0},
	Stone = {"Slate", 104, 112, 130, 0},
	StormCloud = {"SmoothPlastic", 92, 98, 112, 0},
	StormSteel = {"DiamondPlate", 40, 46, 62, 0},
	VoltLED = {"Neon", 255, 230, 40, 0},
	WingBone = {"SmoothPlastic", 30, 34, 46, 0},
	WingMembrane = {"Fabric", 72, 82, 106, 0}
}
local LIGHTS = {
	Crystal = {90, 190, 255, 8, 0.6},
	Flame = {100, 190, 255, 12, 2},
	Lightning = {255, 220, 60, 12, 1.5},
	Neon = {255, 236, 140, 10, 1}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("StormDrakeMine_Roblox", true) or workspace:FindFirstChild("StormDrakeMine", true) end
assert(model, "Select the imported StormDrakeMine model first.")
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
print(("[StormDrakeMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("StormDrakeMine: " .. tostring(err)) end else table.insert(missing, "StormDrakeMine") end end
do local __M = ROOT:FindFirstChild("VenomDrakeMine", true)
if __M then local ok, err = pcall(function()
-- VenomDrakeMine: colours, Roblox materials, glow lights and a working ore dropper.
-- 1. Import VenomDrakeMine_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model in the Explorer.  3. View > Command Bar: paste this file, press Enter.
-- The dropper spawns ore at the glowing ore cube every DropInterval seconds (model attributes).
local LOOK = {
	Black = {"SmoothPlastic", 10, 14, 8, 0},
	CanisterGlass = {"Glass", 200, 255, 200, 0.45},
	Crystal = {"Glass", 150, 255, 60, 0.15},
	Flame = {"Neon", 180, 255, 80, 0},
	HazardLED = {"Neon", 255, 210, 30, 0},
	HazardYellow = {"SmoothPlastic", 240, 200, 20, 0},
	Horn = {"SmoothPlastic", 30, 30, 24, 0},
	Neon = {"Neon", 220, 255, 190, 0},
	Ore = {"Neon", 190, 255, 120, 0},
	Rock = {"Slate", 30, 36, 24, 0},
	RustedIron = {"DiamondPlate", 56, 48, 30, 0},
	Screen = {"Neon", 200, 255, 150, 0},
	Stone = {"Slate", 72, 98, 46, 0},
	ToxicKnob = {"Neon", 150, 255, 40, 0},
	Venom = {"Neon", 140, 255, 50, 0},
	WingBone = {"SmoothPlastic", 40, 52, 20, 0},
	WingMembrane = {"Fabric", 122, 150, 42, 0}
}
local LIGHTS = {
	Crystal = {100, 230, 20, 8, 0.6},
	Flame = {120, 255, 30, 12, 2},
	Neon = {170, 255, 100, 10, 1},
	Venom = {100, 255, 20, 12, 1.4}
}
local ORE_PART = "Ore"

local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("VenomDrakeMine_Roblox", true) or workspace:FindFirstChild("VenomDrakeMine", true) end
assert(model, "Select the imported VenomDrakeMine model first.")
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
print(("[VenomDrakeMine] %d parts coloured, %d lights, dropper %s"):format(styled, lit, drop and "added" or "NOT found"))

end) if ok then done += 1 else warn("VenomDrakeMine: " .. tostring(err)) end else table.insert(missing, "VenomDrakeMine") end end
do local __M = ROOT:FindFirstChild("AbyssMawFurnace", true)
if __M then local ok, err = pcall(function()
-- AbyssMawFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import AbyssMawFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AnglerBelly = {"SmoothPlastic", 120, 136, 150, 0},
	AnglerSkin = {"Slate", 46, 64, 92, 0},
	Bubbles = {"Glass", 190, 240, 255, 0.5},
	BurnZone = {"ForceField", 80, 255, 220, 0.7},
	Coral = {"SmoothPlastic", 255, 110, 120, 0},
	EyeGlow = {"Neon", 255, 230, 120, 0},
	FinMembrane = {"Fabric", 60, 140, 160, 0.1},
	LureGlow = {"Neon", 180, 255, 240, 0},
	SeabedSand = {"Sand", 196, 176, 130, 0},
	Seaweed = {"SmoothPlastic", 50, 150, 80, 0},
	Shell = {"SmoothPlastic", 240, 220, 210, 0},
	Teeth = {"SmoothPlastic", 236, 232, 214, 0},
	ThroatDark = {"SmoothPlastic", 6, 10, 16, 0},
	ThroatGlow = {"Neon", 80, 255, 220, 0}
}
local LIGHTS = {
	EyeGlow = {255, 210, 60, 6, 0.8},
	LureGlow = {120, 255, 230, 16, 2.2},
	ThroatGlow = {40, 255, 200, 14, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("AbyssMawFurnace_Roblox", true) or workspace:FindFirstChild("AbyssMawFurnace", true) end
assert(model, "Select the imported AbyssMawFurnace model first.")
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
print(("[AbyssMawFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("AbyssMawFurnace: " .. tostring(err)) end else table.insert(missing, "AbyssMawFurnace") end end
do local __M = ROOT:FindFirstChild("AcidCrusherFurnace", true)
if __M then local ok, err = pcall(function()
-- AcidCrusherFurnace: colours, Roblox materials, glow lights and a working SELL script.
-- 1. Import AcidCrusherFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (any Part named "Ore" with a "Value" attribute - what the mine droppers make) that touches the glowing
-- intake pool is destroyed and its Value x Multiplier is added to the owner's leaderstats Cash.
-- Owner = model attribute OwnerUserId (set it per plot), otherwise the first player in the server.
local LOOK = {
	AcidCore = {"Neon", 200, 255, 150, 0},
	AcidNeon = {"Neon", 140, 255, 40, 0},
	AcidPool = {"Neon", 120, 255, 60, 0},
	Black = {"SmoothPlastic", 14, 14, 18, 0},
	BurnZone = {"ForceField", 140, 255, 80, 0.6},
	Conveyor = {"DiamondPlate", 30, 32, 38, 0},
	DarkPlate = {"DiamondPlate", 58, 60, 66, 0},
	HazardNeon = {"Neon", 255, 200, 20, 0},
	HazardYellow = {"SmoothPlastic", 240, 196, 20, 0},
	PipeSteel = {"Metal", 140, 146, 150, 0},
	PoolGlass = {"Glass", 190, 255, 170, 0.5},
	SteelPlate = {"DiamondPlate", 96, 100, 108, 0},
	TankGlass = {"Glass", 170, 255, 140, 0.4}
}
local LIGHTS = {
	AcidCore = {120, 255, 60, 20, 2.5},
	AcidNeon = {100, 255, 10, 8, 1},
	AcidPool = {80, 255, 20, 16, 2},
	HazardNeon = {255, 170, 0, 8, 1}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("AcidCrusherFurnace_Roblox", true) or workspace:FindFirstChild("AcidCrusherFurnace", true) end
assert(model, "Select the imported AcidCrusherFurnace model first.")
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
-- conveyor ramp: push ore up the ramp and into the pool
local speed = model:GetAttribute("ConveyorSpeed") or 8
model:SetAttribute("ConveyorSpeed", speed)
local nConv = 0
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") and p.Name:gsub("%.%d+$", "") == "Conveyor" and burn then
		local dir = burn.Position - p.Position
		p.AssemblyLinearVelocity = dir.Unit * speed
		p.Anchored = true
		nConv += 1
	end
end
print(("[AcidCrusherFurnace] conveyor ramp parts: %d (speed attribute ConveyorSpeed)"):format(nConv))
print(("[AcidCrusherFurnace] %d parts coloured, %d lights, sell script %s"):format(styled, lit, burn and "added" or "NOT found"))
-- No leaderstats yet? Add a Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("AcidCrusherFurnace: " .. tostring(err)) end else table.insert(missing, "AcidCrusherFurnace") end end
do local __M = ROOT:FindFirstChild("ArcadeCabinetFurnace", true)
if __M then local ok, err = pcall(function()
-- ArcadeCabinetFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import ArcadeCabinetFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 220, 80, 0.7},
	ButtonRed = {"SmoothPlastic", 240, 40, 50, 0},
	ButtonYellow = {"SmoothPlastic", 255, 220, 40, 0},
	CabinetBlack = {"SmoothPlastic", 20, 18, 26, 0},
	CabinetPurple = {"SmoothPlastic", 90, 40, 170, 0},
	Chrome = {"Metal", 190, 194, 204, 0},
	FloorBlack = {"SmoothPlastic", 24, 24, 30, 0},
	FloorWhite = {"SmoothPlastic", 232, 232, 236, 0},
	NeonCyan = {"Neon", 40, 230, 255, 0},
	NeonPink = {"Neon", 255, 60, 200, 0},
	PixelGreen = {"Neon", 80, 255, 120, 0},
	PrizeSlotGlow = {"Neon", 255, 220, 80, 0},
	Screen = {"Neon", 20, 30, 60, 0}
}
local LIGHTS = {
	NeonCyan = {0, 220, 255, 10, 1.4},
	NeonPink = {255, 30, 190, 10, 1.4},
	PrizeSlotGlow = {255, 190, 40, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ArcadeCabinetFurnace_Roblox", true) or workspace:FindFirstChild("ArcadeCabinetFurnace", true) end
assert(model, "Select the imported ArcadeCabinetFurnace model first.")
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
print(("[ArcadeCabinetFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("ArcadeCabinetFurnace: " .. tostring(err)) end else table.insert(missing, "ArcadeCabinetFurnace") end end
do local __M = ROOT:FindFirstChild("CandyOvenFurnace", true)
if __M then local ok, err = pcall(function()
-- CandyOvenFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import CandyOvenFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 160, 80, 0.7},
	CandyRed = {"SmoothPlastic", 230, 40, 60, 0},
	CandyWhite = {"SmoothPlastic", 250, 250, 250, 0},
	Cherry = {"SmoothPlastic", 210, 20, 40, 0},
	Chocolate = {"SmoothPlastic", 92, 52, 32, 0},
	CupcakeWrapper = {"SmoothPlastic", 120, 210, 255, 0},
	Frosting = {"SmoothPlastic", 255, 190, 220, 0},
	GumGreen = {"Glass", 90, 230, 120, 0.1},
	GumPurple = {"Glass", 190, 110, 255, 0.1},
	GumYellow = {"Glass", 255, 220, 60, 0.1},
	Icing = {"SmoothPlastic", 255, 248, 250, 0},
	MilkChocolate = {"SmoothPlastic", 130, 80, 50, 0},
	OvenDark = {"SmoothPlastic", 40, 20, 20, 0},
	OvenGlow = {"Neon", 255, 150, 60, 0},
	OvenPink = {"SmoothPlastic", 255, 150, 190, 0},
	SprinkleBlue = {"Neon", 60, 160, 255, 0},
	SprinkleGreen = {"Neon", 80, 230, 120, 0},
	SprinkleYellow = {"Neon", 255, 230, 60, 0}
}
local LIGHTS = {
	OvenGlow = {255, 110, 30, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("CandyOvenFurnace_Roblox", true) or workspace:FindFirstChild("CandyOvenFurnace", true) end
assert(model, "Select the imported CandyOvenFurnace model first.")
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
print(("[CandyOvenFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("CandyOvenFurnace: " .. tostring(err)) end else table.insert(missing, "CandyOvenFurnace") end end
do local __M = ROOT:FindFirstChild("ClassicIncineratorFurnace", true)
if __M then local ok, err = pcall(function()
-- ClassicIncineratorFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import ClassicIncineratorFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	Black = {"SmoothPlastic", 16, 16, 20, 0},
	BurnZone = {"ForceField", 255, 130, 40, 0.7},
	DarkPlate = {"DiamondPlate", 70, 72, 80, 0},
	Flame = {"Neon", 255, 190, 80, 0},
	HazardYellow = {"SmoothPlastic", 240, 196, 20, 0},
	LavaPit = {"Neon", 255, 110, 30, 0},
	OrangeNeon = {"Neon", 255, 150, 50, 0},
	SteelPlate = {"DiamondPlate", 128, 132, 142, 0},
	WarningRed = {"Neon", 255, 40, 30, 0}
}
local LIGHTS = {
	LavaPit = {255, 80, 10, 18, 2.4},
	OrangeNeon = {255, 120, 20, 8, 1},
	WarningRed = {255, 20, 10, 6, 0.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ClassicIncineratorFurnace_Roblox", true) or workspace:FindFirstChild("ClassicIncineratorFurnace", true) end
assert(model, "Select the imported ClassicIncineratorFurnace model first.")
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
print(("[ClassicIncineratorFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("ClassicIncineratorFurnace: " .. tostring(err)) end else table.insert(missing, "ClassicIncineratorFurnace") end end
do local __M = ROOT:FindFirstChild("ClockworkGrinderFurnace", true)
if __M then local ok, err = pcall(function()
-- ClockworkGrinderFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import ClockworkGrinderFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AmberGlow = {"Neon", 255, 190, 80, 0},
	Brass = {"Metal", 214, 166, 74, 0},
	BurnZone = {"ForceField", 255, 150, 60, 0.7},
	Conveyor = {"DiamondPlate", 60, 50, 44, 0},
	Copper = {"Metal", 196, 112, 62, 0},
	DarkIron = {"Metal", 52, 50, 54, 0},
	DarkPlanks = {"WoodPlanks", 94, 62, 38, 0},
	DeckPlanks = {"WoodPlanks", 130, 90, 56, 0},
	FurnaceFire = {"Neon", 255, 140, 40, 0},
	GaugeFace = {"SmoothPlastic", 240, 232, 210, 0},
	LeatherBelt = {"Fabric", 70, 40, 26, 0},
	Steam = {"SmoothPlastic", 230, 230, 234, 0.3}
}
local LIGHTS = {
	AmberGlow = {255, 160, 40, 8, 1},
	FurnaceFire = {255, 100, 10, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ClockworkGrinderFurnace_Roblox", true) or workspace:FindFirstChild("ClockworkGrinderFurnace", true) end
assert(model, "Select the imported ClockworkGrinderFurnace model first.")
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
print(("[ClockworkGrinderFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("ClockworkGrinderFurnace: " .. tostring(err)) end else table.insert(missing, "ClockworkGrinderFurnace") end end
do local __M = ROOT:FindFirstChild("DragonSkullFurnace", true)
if __M then local ok, err = pcall(function()
-- DragonSkullFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import DragonSkullFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AshRock = {"Basalt", 50, 44, 42, 0},
	BlackHorn = {"SmoothPlastic", 36, 30, 30, 0},
	BurnZone = {"ForceField", 255, 130, 40, 0.7},
	DragonBone = {"Limestone", 222, 210, 182, 0},
	EyeFire = {"Neon", 255, 60, 20, 0},
	ScorchedEarth = {"Ground", 60, 46, 40, 0},
	SkullFire = {"Neon", 255, 120, 30, 0},
	SocketDark = {"SmoothPlastic", 14, 8, 6, 0}
}
local LIGHTS = {
	EyeFire = {255, 40, 0, 8, 1.2},
	SkullFire = {255, 90, 10, 16, 2.2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("DragonSkullFurnace_Roblox", true) or workspace:FindFirstChild("DragonSkullFurnace", true) end
assert(model, "Select the imported DragonSkullFurnace model first.")
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
print(("[DragonSkullFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("DragonSkullFurnace: " .. tostring(err)) end else table.insert(missing, "DragonSkullFurnace") end end
do local __M = ROOT:FindFirstChild("FrostSpireFurnace", true)
if __M then local ok, err = pcall(function()
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
local model = __M
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

end) if ok then done += 1 else warn("FrostSpireFurnace: " .. tostring(err)) end else table.insert(missing, "FrostSpireFurnace") end end
do local __M = ROOT:FindFirstChild("GeodeCavernFurnace", true)
if __M then local ok, err = pcall(function()
-- GeodeCavernFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import GeodeCavernFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AgateBand = {"SmoothPlastic", 230, 220, 240, 0},
	Amethyst = {"Glass", 180, 100, 255, 0.15},
	BurnZone = {"ForceField", 210, 150, 255, 0.7},
	CaveRock = {"Slate", 70, 64, 72, 0},
	Conveyor = {"DiamondPlate", 60, 54, 64, 0},
	CrystalLiquid = {"Neon", 210, 150, 255, 0},
	GeodeShell = {"Rock", 150, 136, 120, 0},
	GlowMushroom = {"Neon", 100, 230, 255, 0},
	MushroomStem = {"SmoothPlastic", 220, 220, 230, 0},
	PaleAmethyst = {"Glass", 230, 190, 255, 0.15}
}
local LIGHTS = {
	Amethyst = {150, 60, 255, 10, 1.2},
	CrystalLiquid = {180, 100, 255, 16, 2.2},
	GlowMushroom = {60, 210, 255, 6, 0.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("GeodeCavernFurnace_Roblox", true) or workspace:FindFirstChild("GeodeCavernFurnace", true) end
assert(model, "Select the imported GeodeCavernFurnace model first.")
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
print(("[GeodeCavernFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("GeodeCavernFurnace: " .. tostring(err)) end else table.insert(missing, "GeodeCavernFurnace") end end
do local __M = ROOT:FindFirstChild("GoldVaultFurnace", true)
if __M then local ok, err = pcall(function()
-- GoldVaultFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import GoldVaultFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BlackMarble = {"SmoothPlastic", 30, 30, 36, 0},
	BurnZone = {"ForceField", 255, 220, 120, 0.7},
	CashGreen = {"SmoothPlastic", 90, 170, 90, 0},
	DarkSteel = {"DiamondPlate", 70, 74, 82, 0},
	Gold = {"Metal", 245, 196, 70, 0},
	MarbleFloor = {"SmoothPlastic", 232, 228, 220, 0},
	MoneyBag = {"Fabric", 190, 160, 110, 0},
	VaultGlow = {"Neon", 255, 220, 120, 0},
	VaultSteel = {"Metal", 150, 156, 166, 0},
	Velvet = {"Fabric", 170, 20, 40, 0}
}
local LIGHTS = {
	VaultGlow = {255, 190, 60, 16, 2.2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("GoldVaultFurnace_Roblox", true) or workspace:FindFirstChild("GoldVaultFurnace", true) end
assert(model, "Select the imported GoldVaultFurnace model first.")
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
print(("[GoldVaultFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("GoldVaultFurnace: " .. tostring(err)) end else table.insert(missing, "GoldVaultFurnace") end end
do local __M = ROOT:FindFirstChild("HauntedCryptFurnace", true)
if __M then local ok, err = pcall(function()
-- HauntedCryptFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import HauntedCryptFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 110, 255, 160, 0.7},
	CryptStone = {"Slate", 110, 112, 116, 0},
	DarkStone = {"Slate", 64, 66, 72, 0},
	DeadGrass = {"Grass", 90, 100, 60, 0},
	DeadWood = {"Wood", 64, 50, 40, 0},
	GhostFire = {"Neon", 110, 255, 160, 0},
	GraveSoil = {"Ground", 62, 54, 46, 0},
	Moss = {"Grass", 70, 110, 50, 0},
	Pumpkin = {"SmoothPlastic", 240, 120, 20, 0},
	PumpkinGlow = {"Neon", 255, 200, 60, 0},
	Wisp = {"Neon", 200, 255, 220, 0},
	WroughtIron = {"Metal", 36, 34, 38, 0}
}
local LIGHTS = {
	GhostFire = {60, 255, 120, 16, 2},
	PumpkinGlow = {255, 160, 20, 6, 0.8},
	Wisp = {150, 255, 190, 6, 0.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("HauntedCryptFurnace_Roblox", true) or workspace:FindFirstChild("HauntedCryptFurnace", true) end
assert(model, "Select the imported HauntedCryptFurnace model first.")
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
print(("[HauntedCryptFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("HauntedCryptFurnace: " .. tostring(err)) end else table.insert(missing, "HauntedCryptFurnace") end end
do local __M = ROOT:FindFirstChild("NightmareLamentFurnace", true)
if __M then local ok, err = pcall(function()
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
local model = __M
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

end) if ok then done += 1 else warn("NightmareLamentFurnace: " .. tostring(err)) end else table.insert(missing, "NightmareLamentFurnace") end end
do local __M = ROOT:FindFirstChild("PrismReactorFurnace", true)
if __M then local ok, err = pcall(function()
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
	Conveyor = {"DiamondPlate", 30, 32, 38, 0},
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
local model = __M
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
-- conveyor ramp: push ore up the ramp and into the pool
local speed = model:GetAttribute("ConveyorSpeed") or 8
model:SetAttribute("ConveyorSpeed", speed)
local nConv = 0
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") and p.Name:gsub("%.%d+$", "") == "Conveyor" and burn then
		local dir = burn.Position - p.Position
		p.AssemblyLinearVelocity = dir.Unit * speed
		p.Anchored = true
		nConv += 1
	end
end
print(("[PrismReactorFurnace] conveyor ramp parts: %d (speed attribute ConveyorSpeed)"):format(nConv))
print(("[PrismReactorFurnace] %d parts coloured, %d lights, sell script %s"):format(styled, lit, burn and "added" or "NOT found"))
-- No leaderstats yet? Add a Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("PrismReactorFurnace: " .. tostring(err)) end else table.insert(missing, "PrismReactorFurnace") end end
do local __M = ROOT:FindFirstChild("RobotChomperFurnace", true)
if __M then local ok, err = pcall(function()
-- RobotChomperFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import RobotChomperFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AntennaLight = {"Neon", 255, 60, 60, 0},
	BurnZone = {"ForceField", 255, 80, 60, 0.7},
	Conveyor = {"DiamondPlate", 40, 42, 50, 0},
	DarkPanel = {"SmoothPlastic", 30, 32, 40, 0},
	GrinderGlow = {"Neon", 255, 80, 60, 0},
	HazardYellow = {"SmoothPlastic", 240, 196, 20, 0},
	LEDEyes = {"Neon", 80, 255, 255, 0},
	RobotBlue = {"SmoothPlastic", 40, 110, 220, 0},
	RobotSteel = {"Metal", 170, 176, 186, 0},
	SteelTeeth = {"Metal", 220, 224, 230, 0},
	TreadRubber = {"SmoothPlastic", 26, 26, 30, 0}
}
local LIGHTS = {
	AntennaLight = {255, 30, 30, 6, 1},
	GrinderGlow = {255, 50, 30, 16, 2},
	LEDEyes = {30, 240, 255, 10, 1.4}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RobotChomperFurnace_Roblox", true) or workspace:FindFirstChild("RobotChomperFurnace", true) end
assert(model, "Select the imported RobotChomperFurnace model first.")
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
print(("[RobotChomperFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("RobotChomperFurnace: " .. tostring(err)) end else table.insert(missing, "RobotChomperFurnace") end end
do local __M = ROOT:FindFirstChild("RocketPadFurnace", true)
if __M then local ok, err = pcall(function()
-- RocketPadFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import RocketPadFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 170, 60, 0.7},
	Conveyor = {"DiamondPlate", 50, 52, 58, 0},
	EngineDark = {"Metal", 50, 52, 58, 0},
	FlameCore = {"Neon", 140, 200, 255, 0},
	FloodLight = {"Neon", 255, 250, 220, 0},
	GantrySteel = {"Metal", 140, 60, 40, 0},
	LaunchPad = {"Concrete", 120, 122, 128, 0},
	PadStripe = {"SmoothPlastic", 240, 196, 20, 0},
	Porthole = {"Neon", 120, 200, 255, 0},
	RocketFlame = {"Neon", 255, 170, 60, 0},
	RocketRed = {"SmoothPlastic", 220, 40, 40, 0},
	RocketWhite = {"SmoothPlastic", 238, 240, 244, 0},
	Smoke = {"SmoothPlastic", 200, 200, 204, 0.2}
}
local LIGHTS = {
	FloodLight = {255, 240, 190, 10, 1.2},
	RocketFlame = {255, 130, 20, 18, 2.4}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RocketPadFurnace_Roblox", true) or workspace:FindFirstChild("RocketPadFurnace", true) end
assert(model, "Select the imported RocketPadFurnace model first.")
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
print(("[RocketPadFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("RocketPadFurnace: " .. tostring(err)) end else table.insert(missing, "RocketPadFurnace") end end
do local __M = ROOT:FindFirstChild("RunePortalFurnace", true)
if __M then local ok, err = pcall(function()
-- RunePortalFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import RunePortalFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AncientStone = {"Slate", 120, 118, 112, 0},
	BurnZone = {"ForceField", 100, 200, 255, 0.7},
	DarkStone = {"Slate", 70, 70, 74, 0},
	Moss = {"Grass", 70, 120, 50, 0},
	OldBronze = {"Metal", 170, 130, 70, 0},
	PortalArms = {"Neon", 220, 255, 255, 0},
	PortalSwirl = {"Neon", 120, 200, 255, 0},
	RuneCrystal = {"Glass", 120, 255, 220, 0.2},
	RuneGlow = {"Neon", 90, 255, 210, 0}
}
local LIGHTS = {
	PortalSwirl = {70, 170, 255, 18, 2.2},
	RuneGlow = {40, 255, 190, 8, 1}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RunePortalFurnace_Roblox", true) or workspace:FindFirstChild("RunePortalFurnace", true) end
assert(model, "Select the imported RunePortalFurnace model first.")
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
print(("[RunePortalFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("RunePortalFurnace: " .. tostring(err)) end else table.insert(missing, "RunePortalFurnace") end end
do local __M = ROOT:FindFirstChild("SingularityFurnace", true)
if __M then local ok, err = pcall(function()
-- SingularityFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import SingularityFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	AccretionGlow = {"Neon", 255, 170, 90, 0},
	BurnZone = {"ForceField", 170, 110, 255, 0.6},
	Conveyor = {"DiamondPlate", 40, 34, 58, 0},
	EventHorizon = {"SmoothPlastic", 4, 2, 8, 0},
	Gold = {"Metal", 236, 186, 70, 0},
	HullPlate = {"DiamondPlate", 34, 30, 48, 0},
	Stardust = {"Neon", 255, 230, 200, 0},
	VoidNeon = {"Neon", 190, 110, 255, 0},
	VortexSwirl = {"Neon", 150, 80, 255, 0}
}
local LIGHTS = {
	AccretionGlow = {255, 130, 60, 18, 2.2},
	VoidNeon = {160, 70, 255, 8, 1},
	VortexSwirl = {130, 50, 255, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SingularityFurnace_Roblox", true) or workspace:FindFirstChild("SingularityFurnace", true) end
assert(model, "Select the imported SingularityFurnace model first.")
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
print(("[SingularityFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("SingularityFurnace: " .. tostring(err)) end else table.insert(missing, "SingularityFurnace") end end
do local __M = ROOT:FindFirstChild("SolarCrucibleFurnace", true)
if __M then local ok, err = pcall(function()
-- SolarCrucibleFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import SolarCrucibleFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 200, 80, 0.7},
	Conveyor = {"DiamondPlate", 180, 170, 150, 0},
	Gold = {"Metal", 240, 190, 70, 0},
	Lapis = {"SmoothPlastic", 40, 70, 170, 0},
	Mirror = {"Glass", 200, 220, 240, 0},
	MoltenGold = {"Neon", 255, 200, 70, 0},
	SunBeam = {"Neon", 255, 240, 170, 0.3},
	SunCore = {"Neon", 255, 230, 140, 0},
	WhiteMarble = {"SmoothPlastic", 238, 234, 226, 0}
}
local LIGHTS = {
	MoltenGold = {255, 170, 30, 16, 2.2},
	SunCore = {255, 190, 60, 22, 2.6}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SolarCrucibleFurnace_Roblox", true) or workspace:FindFirstChild("SolarCrucibleFurnace", true) end
assert(model, "Select the imported SolarCrucibleFurnace model first.")
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
print(("[SolarCrucibleFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("SolarCrucibleFurnace: " .. tostring(err)) end else table.insert(missing, "SolarCrucibleFurnace") end end
do local __M = ROOT:FindFirstChild("TeslaCageFurnace", true)
if __M then local ok, err = pcall(function()
-- TeslaCageFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import TeslaCageFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	Black = {"SmoothPlastic", 16, 16, 20, 0},
	BurnZone = {"ForceField", 150, 200, 255, 0.7},
	Concrete = {"Concrete", 150, 150, 146, 0},
	Conveyor = {"DiamondPlate", 40, 42, 48, 0},
	CopperCoil = {"Metal", 200, 110, 60, 0},
	HazardYellow = {"SmoothPlastic", 240, 196, 20, 0},
	Lightning = {"Neon", 220, 230, 255, 0},
	PlasmaPool = {"Neon", 150, 200, 255, 0},
	Steel = {"Metal", 130, 136, 146, 0},
	WarningLight = {"Neon", 255, 60, 40, 0}
}
local LIGHTS = {
	Lightning = {170, 200, 255, 10, 1.4},
	PlasmaPool = {110, 170, 255, 16, 2.2},
	WarningLight = {255, 30, 20, 6, 1}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TeslaCageFurnace_Roblox", true) or workspace:FindFirstChild("TeslaCageFurnace", true) end
assert(model, "Select the imported TeslaCageFurnace model first.")
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
print(("[TeslaCageFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("TeslaCageFurnace: " .. tostring(err)) end else table.insert(missing, "TeslaCageFurnace") end end
do local __M = ROOT:FindFirstChild("TikiIdolFurnace", true)
if __M then local ok, err = pcall(function()
-- TikiIdolFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import TikiIdolFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 140, 40, 0.7},
	DarkCarving = {"Wood", 60, 36, 20, 0},
	IdolEyes = {"Neon", 120, 255, 120, 0},
	IdolFire = {"Neon", 255, 140, 40, 0},
	IdolWood = {"Wood", 120, 74, 40, 0},
	JungleLeaf = {"SmoothPlastic", 50, 140, 60, 0},
	Moss = {"Grass", 80, 130, 50, 0},
	RedPaint = {"SmoothPlastic", 200, 50, 40, 0},
	TealPaint = {"SmoothPlastic", 40, 170, 160, 0},
	TempleStone = {"Cobblestone", 120, 118, 96, 0},
	TorchFlame = {"Neon", 255, 180, 60, 0},
	Vine = {"SmoothPlastic", 60, 110, 40, 0}
}
local LIGHTS = {
	IdolEyes = {80, 255, 80, 8, 1},
	IdolFire = {255, 100, 10, 16, 2},
	TorchFlame = {255, 140, 20, 8, 1}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TikiIdolFurnace_Roblox", true) or workspace:FindFirstChild("TikiIdolFurnace", true) end
assert(model, "Select the imported TikiIdolFurnace model first.")
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
print(("[TikiIdolFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("TikiIdolFurnace: " .. tostring(err)) end else table.insert(missing, "TikiIdolFurnace") end end
do local __M = ROOT:FindFirstChild("VolcanoForgeFurnace", true)
if __M then local ok, err = pcall(function()
-- VolcanoForgeFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import VolcanoForgeFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BasaltRock = {"Basalt", 54, 44, 42, 0},
	BurnZone = {"ForceField", 255, 140, 40, 0.6},
	Conveyor = {"DiamondPlate", 44, 34, 32, 0},
	CooledLava = {"CrackedLava", 30, 22, 22, 0},
	ForgeIron = {"Metal", 60, 58, 62, 0},
	Lava = {"Neon", 255, 110, 20, 0},
	LavaNeon = {"Neon", 255, 150, 40, 0},
	Obsidian = {"Glass", 24, 16, 30, 0},
	Smoke = {"SmoothPlastic", 70, 66, 68, 0.2}
}
local LIGHTS = {
	Lava = {255, 80, 0, 16, 2},
	LavaNeon = {255, 110, 10, 8, 1}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("VolcanoForgeFurnace_Roblox", true) or workspace:FindFirstChild("VolcanoForgeFurnace", true) end
assert(model, "Select the imported VolcanoForgeFurnace model first.")
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
print(("[VolcanoForgeFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("VolcanoForgeFurnace: " .. tostring(err)) end else table.insert(missing, "VolcanoForgeFurnace") end end
do local __M = ROOT:FindFirstChild("TreasureChestFurnace", true)
if __M then local ok, err = pcall(function()
-- TreasureChestFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import TreasureChestFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 220, 100, 0.7},
	ChestWood = {"WoodPlanks", 120, 74, 40, 0},
	Gold = {"Metal", 245, 196, 70, 0},
	PalmLeaf = {"SmoothPlastic", 60, 150, 60, 0},
	Ruby = {"Glass", 230, 30, 60, 0.1},
	Sand = {"Sand", 222, 196, 140, 0},
	TreasureGlow = {"Neon", 255, 220, 100, 0}
}
local LIGHTS = {
	TreasureGlow = {255, 190, 40, 16, 2.2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("TreasureChestFurnace_Roblox", true) or workspace:FindFirstChild("TreasureChestFurnace", true) end
assert(model, "Select the imported TreasureChestFurnace model first.")
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
print(("[TreasureChestFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("TreasureChestFurnace: " .. tostring(err)) end else table.insert(missing, "TreasureChestFurnace") end end
do local __M = ROOT:FindFirstChild("WitchCauldronFurnace", true)
if __M then local ok, err = pcall(function()
-- WitchCauldronFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import WitchCauldronFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BroomWood = {"Wood", 110, 74, 44, 0},
	BurnZone = {"ForceField", 120, 255, 90, 0.7},
	CauldronIron = {"Metal", 40, 38, 44, 0},
	Conveyor = {"DiamondPlate", 60, 52, 66, 0},
	HearthStone = {"Slate", 90, 86, 96, 0},
	PotionBlue = {"Glass", 80, 160, 255, 0.2},
	PotionPink = {"Glass", 255, 80, 180, 0.2},
	Straw = {"SmoothPlastic", 210, 180, 90, 0},
	WitchBrew = {"Neon", 120, 255, 90, 0},
	WitchFire = {"Neon", 190, 80, 255, 0}
}
local LIGHTS = {
	WitchBrew = {80, 255, 40, 16, 2},
	WitchFire = {160, 40, 255, 10, 1.4}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("WitchCauldronFurnace_Roblox", true) or workspace:FindFirstChild("WitchCauldronFurnace", true) end
assert(model, "Select the imported WitchCauldronFurnace model first.")
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
print(("[WitchCauldronFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("WitchCauldronFurnace: " .. tostring(err)) end else table.insert(missing, "WitchCauldronFurnace") end end
do local __M = ROOT:FindFirstChild("RecyclerFurnace", true)
if __M then local ok, err = pcall(function()
-- RecyclerFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import RecyclerFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 120, 255, 140, 0.7},
	EmblemWhite = {"SmoothPlastic", 240, 244, 240, 0},
	HatchDark = {"SmoothPlastic", 24, 26, 30, 0},
	HazardYellow = {"SmoothPlastic", 240, 196, 20, 0},
	RecycleGlow = {"Neon", 120, 255, 140, 0},
	RecyclerGreen = {"SmoothPlastic", 60, 150, 80, 0},
	SteelPlate = {"DiamondPlate", 120, 126, 134, 0}
}
local LIGHTS = {
	RecycleGlow = {70, 255, 100, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RecyclerFurnace_Roblox", true) or workspace:FindFirstChild("RecyclerFurnace", true) end
assert(model, "Select the imported RecyclerFurnace model first.")
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
print(("[RecyclerFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("RecyclerFurnace: " .. tostring(err)) end else table.insert(missing, "RecyclerFurnace") end end
do local __M = ROOT:FindFirstChild("SnowGlobeFurnace", true)
if __M then local ok, err = pcall(function()
-- SnowGlobeFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import SnowGlobeFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 160, 220, 255, 0.7},
	DrawerGlow = {"Neon", 160, 220, 255, 0},
	GlobeBase = {"Wood", 110, 64, 36, 0},
	GlobeGlass = {"Glass", 230, 245, 255, 0.7},
	GoldTrim = {"Metal", 240, 190, 70, 0},
	HouseRed = {"SmoothPlastic", 200, 50, 50, 0},
	Pine = {"SmoothPlastic", 40, 110, 60, 0},
	Snow = {"Snow", 245, 250, 255, 0},
	WindowWarm = {"Neon", 255, 210, 120, 0}
}
local LIGHTS = {
	DrawerGlow = {110, 200, 255, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SnowGlobeFurnace_Roblox", true) or workspace:FindFirstChild("SnowGlobeFurnace", true) end
assert(model, "Select the imported SnowGlobeFurnace model first.")
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
print(("[SnowGlobeFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("SnowGlobeFurnace: " .. tostring(err)) end else table.insert(missing, "SnowGlobeFurnace") end end
do local __M = ROOT:FindFirstChild("FairyRingFurnace", true)
if __M then local ok, err = pcall(function()
-- FairyRingFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import FairyRingFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 200, 160, 255, 0.7},
	CapBlue = {"SmoothPlastic", 90, 170, 255, 0},
	CapDots = {"SmoothPlastic", 255, 250, 240, 0},
	CapPink = {"SmoothPlastic", 255, 120, 190, 0},
	CapPurple = {"SmoothPlastic", 170, 100, 255, 0},
	FairyLight = {"Neon", 255, 250, 200, 0},
	FairyPool = {"Neon", 200, 160, 255, 0},
	FairyWing = {"Glass", 200, 240, 255, 0.4},
	Moss = {"Grass", 70, 130, 60, 0},
	MushroomStem = {"SmoothPlastic", 236, 226, 210, 0}
}
local LIGHTS = {
	FairyLight = {255, 240, 160, 6, 0.8},
	FairyPool = {170, 120, 255, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("FairyRingFurnace_Roblox", true) or workspace:FindFirstChild("FairyRingFurnace", true) end
assert(model, "Select the imported FairyRingFurnace model first.")
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
print(("[FairyRingFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("FairyRingFurnace: " .. tostring(err)) end else table.insert(missing, "FairyRingFurnace") end end
do local __M = ROOT:FindFirstChild("MeteorCraterFurnace", true)
if __M then local ok, err = pcall(function()
-- MeteorCraterFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import MeteorCraterFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 120, 40, 0.7},
	CraterRock = {"Slate", 84, 72, 64, 0},
	MeteorCore = {"Neon", 255, 120, 40, 0},
	MeteorCrust = {"Basalt", 40, 32, 34, 0},
	Smoke = {"SmoothPlastic", 90, 86, 86, 0.25},
	SpaceCrystal = {"Glass", 130, 220, 255, 0.15}
}
local LIGHTS = {
	MeteorCore = {255, 80, 10, 18, 2.4},
	SpaceCrystal = {80, 190, 255, 8, 0.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("MeteorCraterFurnace_Roblox", true) or workspace:FindFirstChild("MeteorCraterFurnace", true) end
assert(model, "Select the imported MeteorCraterFurnace model first.")
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
print(("[MeteorCraterFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("MeteorCraterFurnace: " .. tostring(err)) end else table.insert(missing, "MeteorCraterFurnace") end end
do local __M = ROOT:FindFirstChild("HourglassFurnace", true)
if __M then local ok, err = pcall(function()
-- HourglassFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import HourglassFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 200, 90, 0.7},
	DarkWood = {"Wood", 70, 42, 26, 0},
	Gold = {"Metal", 240, 190, 70, 0},
	HourglassGlass = {"Glass", 230, 245, 255, 0.7},
	PedestalMarble = {"SmoothPlastic", 230, 226, 216, 0},
	SlotGlow = {"Neon", 255, 200, 90, 0},
	TimeSand = {"Neon", 255, 210, 120, 0}
}
local LIGHTS = {
	SlotGlow = {255, 170, 40, 12, 1.6},
	TimeSand = {255, 180, 60, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("HourglassFurnace_Roblox", true) or workspace:FindFirstChild("HourglassFurnace", true) end
assert(model, "Select the imported HourglassFurnace model first.")
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
print(("[HourglassFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("HourglassFurnace: " .. tostring(err)) end else table.insert(missing, "HourglassFurnace") end end
do local __M = ROOT:FindFirstChild("LighthouseFurnace", true)
if __M then local ok, err = pcall(function()
-- LighthouseFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import LighthouseFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 210, 120, 0.7},
	DoorGlow = {"Neon", 255, 210, 120, 0},
	LanternIron = {"Metal", 36, 36, 40, 0},
	LighthouseBeam = {"Neon", 255, 250, 200, 0},
	Shallows = {"Glass", 60, 150, 180, 0.2},
	ShoreRock = {"Slate", 100, 96, 92, 0},
	TowerRed = {"SmoothPlastic", 200, 40, 40, 0},
	TowerWhite = {"SmoothPlastic", 240, 240, 236, 0}
}
local LIGHTS = {
	DoorGlow = {255, 180, 60, 12, 1.6},
	LighthouseBeam = {255, 240, 160, 22, 2.6}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("LighthouseFurnace_Roblox", true) or workspace:FindFirstChild("LighthouseFurnace", true) end
assert(model, "Select the imported LighthouseFurnace model first.")
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
print(("[LighthouseFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("LighthouseFurnace: " .. tostring(err)) end else table.insert(missing, "LighthouseFurnace") end end
do local __M = ROOT:FindFirstChild("JackpotFurnace", true)
if __M then local ok, err = pcall(function()
-- JackpotFurnace: colours, Roblox materials, glow lights, a working SELL script and a conveyor ramp.
-- 1. Import JackpotFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute, as the mine droppers make) that touches the intake is sold:
-- Value x Multiplier goes to the owner's leaderstats Cash (OwnerUserId attribute, else the first player).
-- The ramp pushes ore into the intake (ConveyorSpeed attribute).
local LOOK = {
	BurnZone = {"ForceField", 255, 220, 100, 0.7},
	CabinetRed = {"SmoothPlastic", 200, 30, 40, 0},
	CasinoCarpet = {"Fabric", 110, 20, 40, 0},
	Gold = {"Metal", 245, 196, 70, 0},
	MarqueeBulbs = {"Neon", 255, 240, 160, 0},
	PayoutGlow = {"Neon", 255, 220, 100, 0},
	ReelWhite = {"SmoothPlastic", 250, 248, 240, 0},
	SymbolBell = {"SmoothPlastic", 60, 160, 255, 0},
	SymbolCherry = {"SmoothPlastic", 230, 30, 50, 0},
	SymbolSeven = {"SmoothPlastic", 255, 200, 30, 0}
}
local LIGHTS = {
	MarqueeBulbs = {255, 220, 100, 8, 1},
	PayoutGlow = {255, 190, 40, 14, 1.8}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("JackpotFurnace_Roblox", true) or workspace:FindFirstChild("JackpotFurnace", true) end
assert(model, "Select the imported JackpotFurnace model first.")
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
print(("[JackpotFurnace] %d parts coloured, %d lights, %d conveyor parts, sell script %s"):format(styled, lit, #conv, burn and "added" or "NOT found"))
-- No leaderstats yet? Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)

end) if ok then done += 1 else warn("JackpotFurnace: " .. tostring(err)) end else table.insert(missing, "JackpotFurnace") end end
do local __M = ROOT:FindFirstChild("PrismUpgrader", true)
if __M then local ok, err = pcall(function()
-- PrismUpgrader: colours, materials, lights, a moving conveyor belt and the UPGRADE script.
-- 1. Import PrismUpgrader_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (Parts named "Ore" with a "Value" attribute) passing through the laser gate gets Value x Multiplier, once per ore.
-- Attributes on the model: Multiplier (default 1.5), ConveyorSpeed (default 8).
local LOOK = {
	BeltArrows = {"Neon", 120, 255, 140, 0},
	BeltEnd = {"SmoothPlastic", 40, 40, 40, 1},
	Conveyor = {"SmoothPlastic", 34, 36, 42, 0},
	DarkPlate = {"DiamondPlate", 70, 74, 84, 0},
	GateLamp = {"Neon", 255, 220, 90, 0},
	PrismCore = {"Glass", 190, 255, 210, 0.25},
	SteelPlate = {"DiamondPlate", 130, 136, 148, 0},
	UpgradeLaser = {"Neon", 110, 255, 140, 0},
	UpgradeZone = {"ForceField", 110, 255, 140, 1}
}
local LIGHTS = {
	GateLamp = {255, 190, 40, 6, 0.8},
	PrismCore = {120, 255, 160, 10, 1.2},
	UpgradeLaser = {60, 255, 100, 14, 2}
}
local model = __M
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

end) if ok then done += 1 else warn("PrismUpgrader: " .. tostring(err)) end else table.insert(missing, "PrismUpgrader") end end
do local __M = ROOT:FindFirstChild("HexSpeedPad", true)
if __M then local ok, err = pcall(function()
-- HexSpeedPad: colours, Roblox materials and glow lights. The glowing part named BoostPad is the trigger for your speed/jump boost script.
-- 1. Import HexSpeedPad_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AccentNeon = {"Neon", 120, 255, 240, 0},
	BoostPad = {"Neon", 80, 255, 255, 0},
	DarkPlate = {"DiamondPlate", 30, 52, 56, 0},
	EnergyGlass = {"Glass", 100, 255, 255, 0.35},
	EnergyGlow = {"Neon", 40, 230, 255, 0},
	TrimPlate = {"DiamondPlate", 45, 78, 84, 0}
}
local LIGHTS = {
	AccentNeon = {120, 255, 240, 8, 1},
	BoostPad = {40, 230, 255, 14, 1.8},
	EnergyGlow = {40, 230, 255, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("HexSpeedPad_Roblox", true) or workspace:FindFirstChild("HexSpeedPad", true) end
assert(model, "Select the imported HexSpeedPad model first.")
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
print(("[HexSpeedPad] %d parts coloured, %d lights"):format(styled, lit))

end) if ok then done += 1 else warn("HexSpeedPad: " .. tostring(err)) end else table.insert(missing, "HexSpeedPad") end end
do local __M = ROOT:FindFirstChild("SpringJumpPad", true)
if __M then local ok, err = pcall(function()
-- SpringJumpPad: colours, Roblox materials and glow lights. The glowing part named BoostPad is the trigger for your speed/jump boost script.
-- 1. Import SpringJumpPad_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AccentNeon = {"Neon", 200, 255, 120, 0},
	BoostPad = {"Neon", 120, 255, 150, 0},
	DarkPlate = {"DiamondPlate", 34, 54, 36, 0},
	EnergyGlass = {"Glass", 140, 255, 170, 0.35},
	EnergyGlow = {"Neon", 80, 255, 110, 0},
	TrimPlate = {"DiamondPlate", 51, 81, 54, 0}
}
local LIGHTS = {
	AccentNeon = {200, 255, 120, 8, 1},
	BoostPad = {80, 255, 110, 14, 1.8},
	EnergyGlow = {80, 255, 110, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("SpringJumpPad_Roblox", true) or workspace:FindFirstChild("SpringJumpPad", true) end
assert(model, "Select the imported SpringJumpPad model first.")
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
print(("[SpringJumpPad] %d parts coloured, %d lights"):format(styled, lit))

end) if ok then done += 1 else warn("SpringJumpPad: " .. tostring(err)) end else table.insert(missing, "SpringJumpPad") end end
do local __M = ROOT:FindFirstChild("GaleBoostPad", true)
if __M then local ok, err = pcall(function()
-- GaleBoostPad: colours, Roblox materials and glow lights. The glowing part named BoostPad is the trigger for your speed/jump boost script.
-- 1. Import GaleBoostPad_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AccentNeon = {"Neon", 120, 200, 255, 0},
	BoostPad = {"Neon", 220, 255, 255, 0},
	DarkPlate = {"DiamondPlate", 40, 46, 58, 0},
	EnergyGlass = {"Glass", 240, 255, 255, 0.35},
	EnergyGlow = {"Neon", 180, 240, 255, 0},
	TrimPlate = {"DiamondPlate", 60, 69, 87, 0}
}
local LIGHTS = {
	AccentNeon = {120, 200, 255, 8, 1},
	BoostPad = {180, 240, 255, 14, 1.8},
	EnergyGlow = {180, 240, 255, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("GaleBoostPad_Roblox", true) or workspace:FindFirstChild("GaleBoostPad", true) end
assert(model, "Select the imported GaleBoostPad model first.")
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
print(("[GaleBoostPad] %d parts coloured, %d lights"):format(styled, lit))

end) if ok then done += 1 else warn("GaleBoostPad: " .. tostring(err)) end else table.insert(missing, "GaleBoostPad") end end
do local __M = ROOT:FindFirstChild("ThunderBoostPad", true)
if __M then local ok, err = pcall(function()
-- ThunderBoostPad: colours, Roblox materials and glow lights. The glowing part named BoostPad is the trigger for your speed/jump boost script.
-- 1. Import ThunderBoostPad_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AccentNeon = {"Neon", 255, 250, 180, 0},
	BoostPad = {"Neon", 255, 255, 100, 0},
	DarkPlate = {"DiamondPlate", 40, 38, 30, 0},
	EnergyGlass = {"Glass", 255, 255, 120, 0.35},
	EnergyGlow = {"Neon", 255, 220, 60, 0},
	TrimPlate = {"DiamondPlate", 60, 57, 45, 0}
}
local LIGHTS = {
	AccentNeon = {255, 250, 180, 8, 1},
	BoostPad = {255, 220, 60, 14, 1.8},
	EnergyGlow = {255, 220, 60, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("ThunderBoostPad_Roblox", true) or workspace:FindFirstChild("ThunderBoostPad", true) end
assert(model, "Select the imported ThunderBoostPad model first.")
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
print(("[ThunderBoostPad] %d parts coloured, %d lights"):format(styled, lit))

end) if ok then done += 1 else warn("ThunderBoostPad: " .. tostring(err)) end else table.insert(missing, "ThunderBoostPad") end end
do local __M = ROOT:FindFirstChild("RocketBoostPad", true)
if __M then local ok, err = pcall(function()
-- RocketBoostPad: colours, Roblox materials and glow lights. The glowing part named BoostPad is the trigger for your speed/jump boost script.
-- 1. Import RocketBoostPad_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AccentNeon = {"Neon", 255, 200, 80, 0},
	BoostPad = {"Neon", 255, 170, 80, 0},
	DarkPlate = {"DiamondPlate", 50, 34, 30, 0},
	EnergyGlass = {"Glass", 255, 190, 100, 0.35},
	EnergyGlow = {"Neon", 255, 130, 40, 0},
	TrimPlate = {"DiamondPlate", 75, 51, 45, 0}
}
local LIGHTS = {
	AccentNeon = {255, 200, 80, 8, 1},
	BoostPad = {255, 130, 40, 14, 1.8},
	EnergyGlow = {255, 130, 40, 16, 2}
}
local model = __M
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("RocketBoostPad_Roblox", true) or workspace:FindFirstChild("RocketBoostPad", true) end
assert(model, "Select the imported RocketBoostPad model first.")
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
print(("[RocketBoostPad] %d parts coloured, %d lights"):format(styled, lit))

end) if ok then done += 1 else warn("RocketBoostPad: " .. tostring(err)) end else table.insert(missing, "RocketBoostPad") end end
do local __M = ROOT:FindFirstChild("MachineWorkshop", true)
if __M then local ok, err = pcall(function()
-- MachineWorkshop: colours, Roblox materials, transparency and soft lights for both imported models.
-- Import MachineWorkshop_Foundation_Roblox.fbx and MachineWorkshop_Building_Roblox.fbx (Scale Unit = Stud,
-- untick "Import as single mesh"), select both models, paste this file into the Command Bar.
local LOOK = {
	["ArchiveControlPanel"] = {"SmoothPlastic", 24, 30, 40, 0},
	["ArchiveCyan"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["ArchiveLabel"] = {"Neon", 90, 235, 250, 0},
	["ArchiveScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["BannerRed"] = {"Fabric", 190, 50, 44, 0},
	["BlueWallPanel"] = {"SmoothPlastic", 100, 130, 166, 0},
	["CastleBaseStone"] = {"Slate", 64, 70, 68, 0},
	["CastleWallStone"] = {"Slate", 84, 92, 88, 0},
	["CharcoalSteel"] = {"Metal", 52, 54, 60, 0},
	["CollectionDisplay1"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionDisplay2"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionDisplay3"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionPlaque1"] = {"SmoothPlastic", 210, 206, 196, 0},
	["CollectionPlaque2"] = {"SmoothPlastic", 210, 206, 196, 0},
	["CollectionPlaque3"] = {"SmoothPlastic", 210, 206, 196, 0},
	["CollectionReward2"] = {"Metal", 236, 186, 70, 0},
	["CollectionReward3"] = {"Glass", 190, 110, 250, 0.15},
	["ConcreteFloor"] = {"Concrete", 182, 178, 170, 0},
	["Copper"] = {"Metal", 196, 116, 62, 0},
	["CrateWood"] = {"WoodPlanks", 150, 110, 70, 0},
	["DarkBluePanel"] = {"SmoothPlastic", 62, 84, 114, 0},
	["DarkStoneBand"] = {"Slate", 56, 62, 60, 0},
	["DisplayPlaceholder"] = {"ForceField", 90, 220, 255, 1},
	["EvolutionCentrePedestal"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionControlScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["EvolutionLabel"] = {"Neon", 200, 130, 255, 0},
	["EvolutionPreviewPlinthL"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionPreviewPlinthR"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionPurple"] = {"Neon", 170, 90, 240, 0, {150, 70, 240, 16, 1.6}},
	["EvolutionStarEmblem"] = {"Metal", 236, 186, 70, 0},
	["FusionArmL"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionArmR"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionEnergyCore"] = {"Neon", 255, 140, 40, 0, {255, 110, 20, 16, 1.8}},
	["FusionLabel"] = {"Neon", 255, 160, 60, 0},
	["FusionOrange"] = {"Neon", 255, 140, 40, 0, {255, 110, 20, 16, 1.8}},
	["FusionOutputPlatform"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionTerminalScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["GoldDetail"] = {"Metal", 236, 186, 70, 0},
	["HazardBlack"] = {"SmoothPlastic", 30, 30, 34, 0},
	["HazardYellow"] = {"SmoothPlastic", 236, 190, 40, 0},
	["HillGrass"] = {"Grass", 128, 178, 96, 0},
	["HillRock"] = {"Slate", 196, 198, 196, 0},
	["HologramBeam"] = {"Neon", 110, 230, 255, 0.8},
	["IndustrialOrange"] = {"SmoothPlastic", 232, 124, 40, 0},
	["InfoPanelScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["IngredientTray1"] = {"DiamondPlate", 120, 124, 132, 0},
	["IngredientTray2"] = {"DiamondPlate", 120, 124, 132, 0},
	["IngredientTray3"] = {"DiamondPlate", 120, 124, 132, 0},
	["LabelArchive"] = {"Neon", 90, 235, 250, 0},
	["LabelBoard"] = {"SmoothPlastic", 30, 34, 44, 0},
	["LabelEvolution"] = {"Neon", 200, 130, 255, 0},
	["LabelFusion"] = {"Neon", 255, 160, 60, 0},
	["LightSteel"] = {"DiamondPlate", 120, 124, 132, 0},
	["MachineHologram"] = {"Neon", 110, 230, 255, 0.35, {60, 210, 255, 18, 1.5}},
	["PathAHologram"] = {"Neon", 255, 210, 90, 0.3, {255, 190, 60, 10, 1.2}},
	["PathALabel"] = {"Neon", 255, 210, 90, 0.3, {255, 190, 60, 10, 1.2}},
	["PathBHologram"] = {"Neon", 220, 120, 255, 0.3, {190, 90, 255, 10, 1.2}},
	["PathBLabel"] = {"Neon", 220, 120, 255, 0.3, {190, 90, 255, 10, 1.2}},
	["PathStone"] = {"Slate", 150, 150, 146, 0},
	["PineGreen"] = {"SmoothPlastic", 70, 140, 80, 0},
	["ProjectionSurface"] = {"SmoothPlastic", 40, 60, 76, 0},
	["Projector1"] = {"Metal", 52, 54, 60, 0},
	["Projector1Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["Projector2"] = {"Metal", 52, 54, 60, 0},
	["Projector2Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["Projector3"] = {"Metal", 52, 54, 60, 0},
	["Projector3Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["Projector4"] = {"Metal", 52, 54, 60, 0},
	["Projector4Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["RampSurface"] = {"Slate", 64, 70, 68, 0},
	["RewardCrystal"] = {"Glass", 90, 230, 250, 0.15},
	["RoofRed"] = {"Slate", 178, 72, 64, 0},
	["ShowcaseLightRing"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 16, 1.6}},
	["SignSurface"] = {"SmoothPlastic", 62, 84, 114, 0},
	["SignText"] = {"Neon", 255, 206, 90, 0},
	["SoftLamp"] = {"Neon", 255, 244, 214, 0, {255, 236, 200, 30, 1.8}},
	["Trunk"] = {"Wood", 110, 80, 54, 0},
	["WindowGlass"] = {"Glass", 190, 220, 240, 0.6},
}
for _, model in ipairs({__M}) do
	for _, p in ipairs(model:GetDescendants()) do
		if p:IsA("BasePart") then
			local l = LOOK[(p.Name:gsub("%.%d+$", ""))]
			p.Anchored = true
			if l then
				p.Material = Enum.Material[l[1]]; p.Color = Color3.fromRGB(l[2], l[3], l[4]); p.Transparency = l[5]
				if p:IsA("MeshPart") then p.TextureID = "" end
				if l[6] then
					local light = p:FindFirstChild("SoftLight") or Instance.new("PointLight")
					light.Name = "SoftLight"; light.Color = Color3.fromRGB(l[6][1], l[6][2], l[6][3]); light.Range = l[6][4]; light.Brightness = l[6][5]; light.Shadows = true
					light.Parent = p
				end
			end
			if p.Name == "DisplayPlaceholder" or p.Name:find("Hologram") or p.Name == "HologramBeam" then p.CanCollide = false; p.CastShadow = false end
		end
	end
end
-- editable text: reward names + unlock requirements on the three collection plaques (change the strings freely)
local PLAQUES = {
	CollectionPlaque1 = {"Crystal Core", "Unlock: Reach $1M total cash"},
	CollectionPlaque2 = {"Golden Gear", "Unlock: Fuse 10 machines"},
	CollectionPlaque3 = {"Amethyst Crown", "Unlock: Evolve a machine to 5 stars"},
}
for _, model in ipairs({__M}) do
	local centre = model:GetBoundingBox().Position
	for _, p in ipairs(model:GetDescendants()) do
		local t = p:IsA("BasePart") and PLAQUES[(p.Name:gsub("%.%d+$", ""))]
		if t then
			local best, bestDot = Enum.NormalId.Front, -2
			for _, id in ipairs(Enum.NormalId:GetEnumItems()) do   -- face that points into the room
				local d = p.CFrame:VectorToWorldSpace(Vector3.FromNormalId(id)):Dot((centre - p.Position).Unit)
				if d > bestDot then best, bestDot = id, d end
			end
			local gui = p:FindFirstChild("PlaqueGui") or Instance.new("SurfaceGui")
			gui.Name = "PlaqueGui"; gui.Face = best; gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; gui.PixelsPerStud = 60; gui.Parent = p
			for i, txt in ipairs(t) do
				local l = gui:FindFirstChild("Line" .. i) or Instance.new("TextLabel")
				l.Name = "Line" .. i; l.BackgroundTransparency = 1; l.TextScaled = true; l.Font = Enum.Font.GothamBold
				l.TextColor3 = i == 1 and Color3.fromRGB(30, 34, 44) or Color3.fromRGB(90, 90, 100)
				l.Size = UDim2.fromScale(0.9, i == 1 and 0.5 or 0.32); l.Position = UDim2.fromScale(0.05, i == 1 and 0.06 or 0.6)
				l.Text = txt; l.Parent = gui
			end
		end
	end
end
print("[MachineWorkshop] styled")

end) if ok then done += 1 else warn("MachineWorkshop: " .. tostring(err)) end else table.insert(missing, "MachineWorkshop") end end
print("[OreHaven] set up " .. done .. " items" .. (#missing > 0 and (", not found: " .. table.concat(missing, ", ")) or ""))