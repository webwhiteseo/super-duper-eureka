-- MachineWorkshop: colours, Roblox materials, transparency and soft lights for both imported models.
-- Import MachineWorkshop_Foundation_Roblox.fbx and MachineWorkshop_Building_Roblox.fbx (Scale Unit = Stud,
-- untick "Import as single mesh"), select both models, paste this file into the Command Bar.
local LOOK = {
	["ArchiveControlPanel"] = {"SmoothPlastic", 24, 30, 40, 0},
	["ArchiveCyan"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["ArchiveScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["BannerRed"] = {"Fabric", 190, 50, 44, 0},
	["BlueWallPanel"] = {"SmoothPlastic", 84, 112, 146, 0},
	["CastleBaseStone"] = {"Slate", 64, 70, 68, 0},
	["CastleWallStone"] = {"Slate", 84, 92, 88, 0},
	["CharcoalSteel"] = {"Metal", 52, 54, 60, 0},
	["CollectionDisplay1"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionDisplay2"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionDisplay3"] = {"DiamondPlate", 120, 124, 132, 0},
	["CollectionPlaque1"] = {"SmoothPlastic", 210, 206, 196, 0},
	["CollectionPlaque2"] = {"SmoothPlastic", 210, 206, 196, 0},
	["CollectionPlaque3"] = {"SmoothPlastic", 210, 206, 196, 0},
	["ConcreteFloor"] = {"Concrete", 182, 178, 170, 0},
	["Copper"] = {"Metal", 196, 116, 62, 0},
	["CrateWood"] = {"WoodPlanks", 150, 110, 70, 0},
	["DarkBluePanel"] = {"SmoothPlastic", 62, 84, 114, 0},
	["DarkStoneBand"] = {"Slate", 56, 62, 60, 0},
	["DisplayPlaceholder"] = {"ForceField", 90, 220, 255, 1},
	["EvolutionCentrePedestal"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionControlScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["EvolutionPreviewPlinthL"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionPreviewPlinthR"] = {"DiamondPlate", 120, 124, 132, 0},
	["EvolutionPurple"] = {"Neon", 170, 90, 240, 0, {150, 70, 240, 10, 1}},
	["EvolutionStarEmblem"] = {"Metal", 236, 186, 70, 0},
	["FusionArmL"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionArmR"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionEnergyCore"] = {"Neon", 255, 140, 40, 0, {255, 110, 20, 12, 1.4}},
	["FusionOrange"] = {"Neon", 255, 140, 40, 0, {255, 110, 20, 12, 1.4}},
	["FusionOutputPlatform"] = {"DiamondPlate", 120, 124, 132, 0},
	["FusionTerminalScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["GoldDetail"] = {"Metal", 236, 186, 70, 0},
	["HazardBlack"] = {"SmoothPlastic", 30, 30, 34, 0},
	["HazardYellow"] = {"SmoothPlastic", 236, 190, 40, 0},
	["HillGrass"] = {"Grass", 128, 178, 96, 0},
	["HillRock"] = {"Slate", 196, 198, 196, 0},
	["IndustrialOrange"] = {"SmoothPlastic", 232, 124, 40, 0},
	["InfoPanelScreen"] = {"SmoothPlastic", 24, 30, 40, 0},
	["IngredientTray1"] = {"DiamondPlate", 120, 124, 132, 0},
	["IngredientTray2"] = {"DiamondPlate", 120, 124, 132, 0},
	["IngredientTray3"] = {"DiamondPlate", 120, 124, 132, 0},
	["LightSteel"] = {"DiamondPlate", 120, 124, 132, 0},
	["PathStone"] = {"Slate", 150, 150, 146, 0},
	["PineGreen"] = {"SmoothPlastic", 70, 140, 80, 0},
	["ProjectionSurface"] = {"SmoothPlastic", 40, 60, 76, 0},
	["Projector1"] = {"Metal", 52, 54, 60, 0},
	["Projector1Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["Projector2"] = {"Metal", 52, 54, 60, 0},
	["Projector2Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["Projector3"] = {"Metal", 52, 54, 60, 0},
	["Projector3Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["Projector4"] = {"Metal", 52, 54, 60, 0},
	["Projector4Lens"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["RoofRed"] = {"Slate", 178, 72, 64, 0},
	["ShowcaseLightRing"] = {"Neon", 60, 220, 240, 0, {30, 210, 240, 10, 1}},
	["SignSurface"] = {"SmoothPlastic", 62, 84, 114, 0},
	["SoftLamp"] = {"Neon", 255, 244, 214, 0, {255, 236, 200, 24, 1.2}},
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
			if p.Name == "DisplayPlaceholder" then p.CanCollide = false end
		end
	end
end
print("[MachineWorkshop] styled")
