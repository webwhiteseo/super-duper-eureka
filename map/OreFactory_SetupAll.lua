-- ORE FACTORY MAP: ONE-PASTE SETUP (colours + Roblox materials + collision + fog/lighting + lantern lights)
-- 1. Import OreFactory_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. View > Command Bar: paste this whole file, press Enter. (No need to select anything.)
-- 3. Check View > Output for the summary.
-- This is for the MAP. For mines use MineLighting.lua instead.

local M = Enum.Material
local LOOK = {
	Grass = {M.Grass, 75, 120, 45}, GrassDark = {M.Grass, 60, 100, 38}, GrassLight = {M.Grass, 95, 135, 55},
	Rock = {M.Slate, 110, 110, 105}, RockDark = {M.Slate, 80, 80, 78}, CaveRock = {M.Slate, 55, 55, 55},
	Scree = {M.Pebble, 120, 116, 108}, Dirt = {M.Ground, 115, 90, 60}, Gravel = {M.Pebble, 125, 120, 110},
	RiverBed = {M.Pebble, 100, 90, 70}, Sand = {M.Sand, 210, 190, 140}, DrySand = {M.Sand, 225, 205, 160},
	WetSand = {M.Sand, 160, 148, 110}, Concrete = {M.Concrete, 160, 160, 155}, Spawn = {M.Concrete, 170, 175, 160},
	Stone = {M.Cobblestone, 140, 138, 130}, StoneDark = {M.Cobblestone, 105, 103, 98},
	CastleStone = {M.Slate, 60, 58, 56}, CastleStoneDark = {M.Slate, 40, 38, 37},
	Wood = {M.WoodPlanks, 140, 95, 55}, WoodDark = {M.Wood, 80, 55, 35}, RoofWood = {M.WoodPlanks, 100, 55, 35},
	RoofTile = {M.Slate, 130, 38, 30}, Bark = {M.Wood, 75, 52, 32}, Leaf = {M.SmoothPlastic, 55, 95, 40},
	LeafLight = {M.SmoothPlastic, 75, 115, 50}, PalmTrunk = {M.Wood, 150, 120, 80}, PalmLeaf = {M.SmoothPlastic, 70, 135, 55},
	Coconut = {M.SmoothPlastic, 90, 62, 35}, Iron = {M.Metal, 40, 40, 42}, Gold = {M.Metal, 215, 165, 45},
	Banner = {M.Fabric, 140, 20, 20}, LanternGlow = {M.Neon, 255, 200, 120}, Water = {M.Glass, 40, 110, 130},
	Waterfall = {M.Glass, 120, 185, 215}, Bone = {M.Limestone, 222, 212, 182}, BoneDark = {M.Limestone, 165, 150, 120}, Foam = {M.SmoothPlastic, 225, 238, 245},
	FlowerRed = {M.SmoothPlastic, 220, 60, 50}, FlowerYellow = {M.SmoothPlastic, 240, 200, 50},
	FlowerWhite = {M.SmoothPlastic, 240, 240, 230}, FlowerPurple = {M.SmoothPlastic, 150, 90, 210},
}
-- Walkable / enterable shapes need precise collision (hills, cliffs, cave roofs, castle, bridge, path).
local PRECISE = {"^Ground_", "^Cliff_", "^CaveRoof_", "^SummitTower_", "^WoodenBridge_", "^StonePath_", "^CavePortal_"}
local NO_COLLIDE = {Water = true, Waterfall = true, Foam = true, LanternGlow = true,
	FlowerRed = true, FlowerYellow = true, FlowerWhite = true, FlowerPurple = true}

-- find the imported map: selected model, or a model named OreFactory_Roblox, or a model holding Ground_ parts
local root = game:GetService("Selection"):Get()[1]
if not (root and root:FindFirstChild("Plot_01_Concrete", true)) then root = workspace:FindFirstChild("OreFactory_Roblox", true) end
if not root then
	for _, d in ipairs(workspace:GetDescendants()) do
		if d:IsA("BasePart") and d.Name:match("^Ground_") then root = d.Parent break end
	end
end
assert(root, "Couldn't find the imported map (OreFactory_Roblox) in Workspace.")
print("[OreFactory] setting up " .. root:GetFullName())

local counts, unknown, styled, precise, failed = {}, {}, 0, 0, 0
for _, p in ipairs(root:GetDescendants()) do
	if p:IsA("BasePart") then
		local name = p.Name:gsub("%.%d+$", "")
		local mat = name:match("_([%a]+)$") or name
		local look = LOOK[mat]
		local ok = pcall(function()
			p.Anchored = true
			for _, sa in ipairs(p:GetChildren()) do
				if sa:IsA("SurfaceAppearance") then sa:Destroy() end -- importer textures would hide our colours
			end
			if look then
				p.Material = look[1]
				p.Color = Color3.fromRGB(look[2], look[3], look[4])
				if p:IsA("MeshPart") then p.TextureID = "" end
			end
			if mat == "Water" then p.Transparency = 0.3 elseif mat == "Waterfall" then p.Transparency = 0.15 end
			if NO_COLLIDE[mat] then p.CanCollide = false end
		end)
		if not ok then failed += 1 end
		if look then
			styled += 1
			counts[mat] = (counts[mat] or 0) + 1
		elseif #unknown < 15 then
			table.insert(unknown, p.Name)
		end
		for _, pattern in ipairs(PRECISE) do
			if name:match(pattern) and p:IsA("MeshPart") then
				if pcall(function() p.CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition end) then precise += 1 end
				break
			end
		end
	end
end

local Lighting = game:GetService("Lighting")

-- Players can't walk up slopes steeper than 50 degrees, so hill cliffs act as cliffs.
-- Ramps stay walkable; the ledge route on each cliff is climbed by jumping.
game:GetService("StarterPlayer").CharacterMaxSlopeAngle = 50

Lighting.ClockTime = 15.5
Lighting.Brightness = 2.2
Lighting.Ambient = Color3.fromRGB(70, 78, 70)
Lighting.OutdoorAmbient = Color3.fromRGB(128, 138, 124)
Lighting.EnvironmentDiffuseScale = 0.6
Lighting.EnvironmentSpecularScale = 0.4
Lighting.GlobalShadows = true

local function fresh(className, name)
	local old = Lighting:FindFirstChild(name)
	if old then old:Destroy() end
	local obj = Instance.new(className)
	obj.Name = name
	obj.Parent = Lighting
	return obj
end

-- Atmosphere controls the fog (Lighting.FogStart/FogEnd are ignored while it exists).
local atmosphere = fresh("Atmosphere", "OF_Atmosphere")
atmosphere.Density = 0.32
atmosphere.Offset = 0.25
atmosphere.Color = Color3.fromRGB(199, 213, 199)
atmosphere.Decay = Color3.fromRGB(106, 122, 104)
atmosphere.Glare = 0.2
atmosphere.Haze = 1.6

local bloom = fresh("BloomEffect", "OF_Bloom")
bloom.Intensity = 0.4
bloom.Size = 24
bloom.Threshold = 1.6

local grade = fresh("ColorCorrectionEffect", "OF_ColorCorrection")
grade.Brightness = 0.02
grade.Contrast = 0.08
grade.Saturation = 0.08
grade.TintColor = Color3.fromRGB(255, 250, 240)

local rays = fresh("SunRaysEffect", "OF_SunRays")
rays.Intensity = 0.06
rays.Spread = 0.7

-- Lanterns glow and light up the caves.
local lit = 0
for _, p in ipairs(root:GetDescendants()) do
	if p:IsA("BasePart") and p.Name:match("LanternGlow") then
		local light = p:FindFirstChild("OF_Light") or Instance.new("PointLight")
		light.Name = "OF_Light"
		light.Color = Color3.fromRGB(255, 190, 110)
		light.Brightness = 1.6
		light.Range = 18
		light.Parent = p
		lit += 1
	end
end

local summary = {}
for mat, n in pairs(counts) do table.insert(summary, mat .. "=" .. n) end
table.sort(summary)
print(("[OreFactory] coloured %d parts (%s)"):format(styled, table.concat(summary, ", ")))
print(("[OreFactory] precise collision on %d parts, %d lantern lights, %d errors"):format(precise, lit, failed))
if #unknown > 0 then warn("[OreFactory] parts with no colour: " .. table.concat(unknown, ", ")) end
