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
local model = game:GetService("Selection"):Get()[1]
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
