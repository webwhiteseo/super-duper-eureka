-- Ore Factory mines: colours, Roblox materials and glow lights for an imported mine FBX.
-- Works for: Cosmic Drake, Crimson Drake, Astral Orrery, Emerald Wyvern, Frost Wyrm.
-- 1. Import the mine's *_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh").
-- 2. Click the imported model in the Explorer to select it.
-- 3. View > Command Bar: paste this whole file, press Enter. Results are printed in View > Output.

local SET_SHOWCASE_LIGHTING = false -- true = also set a dark night sky + bloom (for screenshots/thumbnails)

local M = Enum.Material
local function c(r, g, b) return Color3.fromRGB(r, g, b) end

-- part name -> { material, colour, transparency }
local SHARED = {
	Black = {M.SmoothPlastic, c(20, 12, 14)}, Neon = {M.Neon, c(255, 215, 185)}, Flame = {M.Neon, c(255, 170, 60)},
	Screen = {M.Neon, c(255, 190, 140)}, Ore = {M.Neon, c(255, 175, 150)}, Horn = {M.Slate, c(60, 48, 44)},
	PlanetRed = {M.SmoothPlastic, c(220, 90, 60)}, PlanetTeal = {M.SmoothPlastic, c(60, 190, 170)},
	PlanetPurple = {M.SmoothPlastic, c(140, 90, 210)}, Gold = {M.Metal, c(232, 182, 72)},
	StarCore = {M.Neon, c(255, 230, 190)}, RuneGlow = {M.Neon, c(255, 225, 200)},
}
local MINES = {
	CosmicDrake = {
		Stone = {M.Slate, c(168, 58, 52)}, CharredIron = {M.DiamondPlate, c(62, 20, 18)}, GoldTrim = {M.Metal, c(232, 182, 72)},
		StarMarble = {M.Marble, c(30, 22, 60)}, Crystal = {M.Glass, c(190, 120, 255), 0.15}, Rock = {M.Slate, c(42, 22, 20)},
		WingMembrane = {M.Fabric, c(160, 38, 40)}, WingBone = {M.SmoothPlastic, c(70, 16, 18)},
		AmberLED = {M.Neon, c(255, 190, 50)}, EmberKnob = {M.Neon, c(255, 110, 30)}, Magma = {M.Neon, c(255, 120, 30)},
	},
	CrimsonDrake = {
		Stone = {M.Slate, c(168, 58, 52)}, CharredIron = {M.DiamondPlate, c(62, 20, 18)}, EmberTrim = {M.Metal, c(255, 84, 30)},
		DarkMarble = {M.Marble, c(50, 14, 14)}, Crystal = {M.Glass, c(255, 90, 90), 0.15}, Rock = {M.Slate, c(42, 22, 20)},
		WingMembrane = {M.Fabric, c(160, 38, 40)}, WingBone = {M.SmoothPlastic, c(70, 16, 18)},
		AmberLED = {M.Neon, c(255, 190, 50)}, EmberKnob = {M.Neon, c(255, 110, 30)}, Magma = {M.Neon, c(255, 120, 30)},
	},
	AstralOrrery = {
		Black = {M.SmoothPlastic, c(8, 8, 18)}, NightMetal = {M.Metal, c(26, 32, 78)}, StarMarble = {M.Marble, c(20, 22, 50)},
		Crystal = {M.Glass, c(175, 135, 255), 0.15}, LensGlass = {M.Glass, c(150, 210, 255), 0.2}, MeteorRock = {M.Slate, c(38, 34, 52)},
		Moon = {M.SmoothPlastic, c(210, 210, 220)}, Neon = {M.Neon, c(190, 245, 255)}, StarCore = {M.Neon, c(235, 250, 255)},
		RuneGlow = {M.Neon, c(200, 240, 255)}, StardustOre = {M.Neon, c(215, 225, 255)},
	},
	EmeraldWyvern = {
		Stone = {M.Slate, c(88, 168, 112)}, Black = {M.SmoothPlastic, c(10, 18, 14)}, Forest = {M.DiamondPlate, c(22, 74, 44)},
		EmeraldTrim = {M.Metal, c(34, 200, 96)}, DarkMarble = {M.Marble, c(18, 48, 32)}, Crystal = {M.Glass, c(110, 255, 160), 0.15},
		Rock = {M.Slate, c(30, 44, 36)}, WingMembrane = {M.Fabric, c(58, 160, 88)}, WingBone = {M.SmoothPlastic, c(22, 88, 48)},
		Horn = {M.SmoothPlastic, c(215, 225, 190)}, Neon = {M.Neon, c(215, 255, 225)}, Flame = {M.Neon, c(150, 255, 120)},
		Screen = {M.Neon, c(200, 255, 210)}, LimeLED = {M.Neon, c(220, 255, 80)}, GreenKnob = {M.Neon, c(40, 220, 90)},
		Ore = {M.Neon, c(190, 255, 210)},
	},
	FrostWyrm = {
		FrostStone = {M.Slate, c(150, 180, 205)}, Black = {M.SmoothPlastic, c(10, 14, 22)}, ColdIron = {M.Metal, c(70, 78, 92)},
		CyanTrim = {M.Metal, c(40, 200, 230)}, DeepIce = {M.Marble, c(24, 40, 80)}, Snow = {M.Snow, c(240, 246, 255)},
		WyrmScales = {M.Slate, c(60, 110, 170)}, WyrmBelly = {M.SmoothPlastic, c(205, 225, 240)}, Horn = {M.SmoothPlastic, c(225, 232, 240)},
		IceCrystal = {M.Glass, c(150, 230, 255), 0.15}, Neon = {M.Neon, c(200, 250, 255)}, EyeGlow = {M.Neon, c(200, 255, 255)},
		FrostFlame = {M.Neon, c(160, 240, 255)}, IceOre = {M.Neon, c(190, 245, 255)},
	},
}
-- part name -> { light colour, range, brightness }
local LIGHTS = {
	StarCore = {c(255, 190, 120), 24, 3}, Magma = {c(255, 120, 40), 14, 2}, Flame = {c(255, 170, 70), 12, 2},
	FrostFlame = {c(140, 230, 255), 12, 2}, Neon = {nil, 10, 1}, RuneGlow = {nil, 8, 0.8}, EyeGlow = {c(160, 255, 255), 8, 1.5},
	Crystal = {nil, 8, 0.6}, IceCrystal = {c(120, 220, 255), 8, 0.6},
}

local model = game:GetService("Selection"):Get()[1]
if not model then
	for _, m in ipairs(workspace:GetChildren()) do
		if m:IsA("Model") and m.Name:find("Mine") then model = m break end
	end
end
assert(model, "Select the imported mine model in the Explorer first.")

local names = {}
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") then names[(p.Name:gsub("%.%d+$", ""))] = true end
end
local kind = (names.StarCore and names.Magma and "CosmicDrake") or (names.Magma and "CrimsonDrake")
	or (names.NightMetal and "AstralOrrery") or (names.Forest and "EmeraldWyvern") or (names.FrostStone and "FrostWyrm")
assert(kind, "Couldn't tell which mine this is - check the part names.")
print(("[MineLighting] %s detected (%s)"):format(kind, model:GetFullName()))

local styled, lit = 0, 0
for _, p in ipairs(model:GetDescendants()) do
	if p:IsA("BasePart") then
		local name = p.Name:gsub("%.%d+$", "")
		local look = MINES[kind][name] or SHARED[name]
		if look then
			p.Material = look[1]
			p.Color = look[2]
			p.Transparency = look[3] or 0
			p.Reflectance = (look[1] == M.Glass) and 0.15 or 0
			if p:IsA("MeshPart") then p.TextureID = "" end
			styled += 1
			print(("  %-14s %-14s RGB(%d,%d,%d)"):format(name, look[1].Name,
				math.floor(look[2].R * 255 + 0.5), math.floor(look[2].G * 255 + 0.5), math.floor(look[2].B * 255 + 0.5)))
		else
			warn("  no colour for part: " .. p.Name)
		end
		p.Anchored = true
		local L = LIGHTS[name]
		if L then
			local light = p:FindFirstChild("MineLight") or Instance.new("PointLight")
			light.Name = "MineLight"
			light.Color = L[1] or p.Color
			light.Range = L[2]
			light.Brightness = L[3]
			light.Shadows = false
			light.Parent = p
			lit += 1
		end
		if name == "Ore" or name:find("Ore$") then p.CanCollide = false end
	end
end

if SET_SHOWCASE_LIGHTING then
	local Lighting = game:GetService("Lighting")
	Lighting.ClockTime = 0.5
	Lighting.Brightness = 1
	Lighting.Ambient = c(40, 34, 60)
	Lighting.OutdoorAmbient = c(60, 50, 90)
	local bloom = Lighting:FindFirstChild("MineBloom") or Instance.new("BloomEffect")
	bloom.Name = "MineBloom"
	bloom.Intensity = 0.8
	bloom.Size = 28
	bloom.Threshold = 1.2
	bloom.Parent = Lighting
	print("[MineLighting] showcase night lighting + bloom applied")
end
print(("[MineLighting] done: %d parts coloured, %d glow lights added"):format(styled, lit))
