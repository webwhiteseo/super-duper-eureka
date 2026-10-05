-- Ore Factory: fog, atmosphere, lantern lights and decoration settings.
-- Studio: View > Command Bar, paste this whole file, press Enter. Safe to run again.
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

-- Lanterns glow and light up the caves; small decorations don't block players.
local lit = 0
for _, part in ipairs(workspace:GetDescendants()) do
	if part:IsA("BasePart") then
		local name = part.Name
		if name:match("^Lantern_.*Glow") or name:match("_LanternGlow$") then
			part.Material = Enum.Material.Neon
			part.Color = Color3.fromRGB(255, 200, 120)
			part.CanCollide = false
			local light = part:FindFirstChild("OF_Light") or Instance.new("PointLight")
			light.Name = "OF_Light"
			light.Color = Color3.fromRGB(255, 190, 110)
			light.Brightness = 1.6
			light.Range = 18
			light.Shadows = true
			light.Parent = part
			lit += 1
		elseif name:match("^Flowers_") or name:match("^TallGrass_") then
			part.CanCollide = false
			part.CastShadow = false
		elseif name == "RiverWater" or name == "RiverPool" then
			part.Transparency = 0.3
			part.CanCollide = false
		end
	end
end
print("Ore Factory lighting applied. Lanterns lit:", lit)
