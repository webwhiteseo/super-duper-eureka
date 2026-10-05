-- Ore Factory: colours, Roblox materials and collision for the imported map (OreFactory_Roblox.fbx).
-- After importing, paste this into View > Command Bar and press Enter. Then run OreFactory_Lighting.lua.
-- Part names end in _<Material> (e.g. Ground_LowPoly_0_1_Grass, SummitTower_CastleStone).
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
	FlowerRed = {M.SmoothPlastic, 220, 60, 50}, FlowerYellow = {M.SmoothPlastic, 240, 200, 50},
	FlowerWhite = {M.SmoothPlastic, 240, 240, 230}, FlowerPurple = {M.SmoothPlastic, 150, 90, 210},
}
-- Walkable / enterable shapes need precise collision (hills, cliffs, cave roofs, castle, bridge, path).
local PRECISE = {"^Ground_", "^Cliff_", "^CaveRoof_", "^SummitTower_", "^WoodenBridge_", "^StonePath_"}
local NO_COLLIDE = {Water = true, LanternGlow = true, FlowerRed = true, FlowerYellow = true, FlowerWhite = true, FlowerPurple = true}

local root = workspace:FindFirstChild("OreFactory_Roblox") or workspace
local done, precise = 0, 0
for _, p in ipairs(root:GetDescendants()) do
	if p:IsA("MeshPart") then
		local mat = p.Name:match("_([%a]+)$")
		local look = mat and LOOK[mat]
		if look then
			p.Material = look[1]
			p.Color = Color3.fromRGB(look[2], look[3], look[4])
			p.TextureID = ""
			done += 1
		end
		p.Anchored = true
		if mat == "Water" then p.Transparency = 0.3 end
		if NO_COLLIDE[mat] then p.CanCollide = false end
		for _, pattern in ipairs(PRECISE) do
			if p.Name:match(pattern) then
				p.CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition
				precise += 1
				break
			end
		end
	end
end
print(("Ore Factory setup: styled %d parts, precise collision on %d"):format(done, precise))
