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
local model = game:GetService("Selection"):Get()[1]
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
