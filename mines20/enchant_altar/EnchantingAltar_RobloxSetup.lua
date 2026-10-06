-- EnchantingAltar: colours, Roblox materials and glow lights. Book Cover/Pages/Runes, Rune Ring and Glow Ring import as their own parts - spin the Rune Ring or bob the book with a TweenService script.
-- 1. Import EnchantingAltar_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
local LOOK = {
	AltarCloth = {"Fabric", 176, 40, 44, 0},
	AmethystCrystal = {"Neon", 190, 110, 255, 0},
	BookCover = {"Fabric", 120, 30, 36, 0},
	BookPages = {"SmoothPlastic", 250, 238, 205, 0},
	BookRunes = {"Neon", 160, 110, 255, 0},
	GlowRing = {"Neon", 190, 140, 255, 0},
	GoldTrim = {"Metal", 236, 186, 70, 0},
	MagicBeam = {"Neon", 190, 140, 255, 0.6},
	Obsidian = {"Slate", 34, 26, 46, 0},
	ObsidianTrim = {"Slate", 58, 44, 78, 0},
	OreCrystal = {"Neon", 90, 230, 255, 0},
	RuneRing = {"Neon", 170, 120, 255, 0}
}
local LIGHTS = {
	AmethystCrystal = {160, 80, 255, 8, 1},
	BookPages = {255, 236, 190, 12, 1.2},
	GlowRing = {170, 110, 255, 14, 1.6},
	OreCrystal = {40, 210, 255, 8, 1},
	RuneRing = {150, 90, 255, 10, 1.4}
}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("EnchantingAltar_Roblox", true) or workspace:FindFirstChild("EnchantingAltar", true) end
assert(model, "Select the imported EnchantingAltar model first.")
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
print(("[EnchantingAltar] %d parts coloured, %d lights"):format(styled, lit))
