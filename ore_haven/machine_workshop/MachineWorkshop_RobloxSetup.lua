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
for _, model in ipairs(game:GetService("Selection"):Get()) do
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
for _, model in ipairs(game:GetService("Selection"):Get()) do
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
