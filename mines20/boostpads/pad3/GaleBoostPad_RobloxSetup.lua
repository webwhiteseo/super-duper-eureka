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
local model = game:GetService("Selection"):Get()[1]
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
