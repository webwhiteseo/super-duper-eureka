-- Dragon Glass Mine (Ore Factory). Original design.
-- Studio: View > Command Bar, paste this whole file, press Enter.
-- The mine appears on the ground where your camera is looking, facing the camera's direction.
-- Ore drops out of the dragon's mouth (front). Tune it with the model's attributes:
--   OreValue, DropInterval (seconds), OreSize, Enabled.

local P = {
	{"Base",Vector3.new(8,1,8),CFrame.new(0.0000,0.5000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(52,50,58),Enum.Material.Slate,0,0,true},
	{"BaseTrim",Vector3.new(8.4,0.4,8.4),CFrame.new(0.0000,0.2000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(34,32,40),Enum.Material.Metal,0,0,true},
	{"Foot0",Vector3.new(1.6,0.9,1.6),CFrame.new(-3.5500,1.3000,-3.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(30,25,38),Enum.Material.Slate,0,0,true},
	{"Foot0Claw0",Vector3.new(0.35,1.3,0.35),CFrame.new(-3.8033,0.6602,-4.3785,0.8794,-0.2666,-0.3943,0.2666,-0.4104,0.8721,-0.3943,-0.8721,-0.2898),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot0Claw1",Vector3.new(0.35,1.3,0.35),CFrame.new(-4.1626,0.6602,-4.1626,0.2948,-0.6448,-0.7052,0.6448,-0.4104,0.6448,-0.7052,-0.6448,0.2948),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot0Claw2",Vector3.new(0.35,1.3,0.35),CFrame.new(-4.3785,0.6602,-3.8033,-0.2898,-0.8721,-0.3943,0.8721,-0.4104,0.2666,-0.3943,-0.2666,0.8794),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot1",Vector3.new(1.6,0.9,1.6),CFrame.new(3.5500,1.3000,-3.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(30,25,38),Enum.Material.Slate,0,0,true},
	{"Foot1Claw0",Vector3.new(0.35,1.3,0.35),CFrame.new(4.3785,0.6602,-3.8033,-0.2898,0.8721,0.3943,-0.8721,-0.4104,0.2666,0.3943,-0.2666,0.8794),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot1Claw1",Vector3.new(0.35,1.3,0.35),CFrame.new(4.1626,0.6602,-4.1626,0.2948,0.6448,0.7052,-0.6448,-0.4104,0.6448,0.7052,-0.6448,0.2948),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot1Claw2",Vector3.new(0.35,1.3,0.35),CFrame.new(3.8033,0.6602,-4.3785,0.8794,0.2666,0.3943,-0.2666,-0.4104,0.8721,0.3943,-0.8721,-0.2898),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot2",Vector3.new(1.6,0.9,1.6),CFrame.new(3.5500,1.3000,3.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(30,25,38),Enum.Material.Slate,0,0,true},
	{"Foot2Claw0",Vector3.new(0.35,1.3,0.35),CFrame.new(3.8033,0.6602,4.3785,0.8794,0.2666,-0.3943,-0.2666,-0.4104,-0.8721,-0.3943,0.8721,-0.2898),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot2Claw1",Vector3.new(0.35,1.3,0.35),CFrame.new(4.1626,0.6602,4.1626,0.2948,0.6448,-0.7052,-0.6448,-0.4104,-0.6448,-0.7052,0.6448,0.2948),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot2Claw2",Vector3.new(0.35,1.3,0.35),CFrame.new(4.3785,0.6602,3.8033,-0.2898,0.8721,-0.3943,-0.8721,-0.4104,-0.2666,-0.3943,0.2666,0.8794),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot3",Vector3.new(1.6,0.9,1.6),CFrame.new(-3.5500,1.3000,3.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(30,25,38),Enum.Material.Slate,0,0,true},
	{"Foot3Claw0",Vector3.new(0.35,1.3,0.35),CFrame.new(-4.3785,0.6602,3.8033,-0.2898,-0.8721,0.3943,0.8721,-0.4104,-0.2666,0.3943,0.2666,0.8794),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot3Claw1",Vector3.new(0.35,1.3,0.35),CFrame.new(-4.1626,0.6602,4.1626,0.2948,-0.6448,0.7052,0.6448,-0.4104,-0.6448,0.7052,0.6448,0.2948),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Foot3Claw2",Vector3.new(0.35,1.3,0.35),CFrame.new(-3.8033,0.6602,4.3785,0.8794,-0.2666,0.3943,0.2666,-0.4104,-0.8721,0.3943,0.8721,-0.2898),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"Body",Vector3.new(6,5,6),CFrame.new(0.0000,3.5000,0.5000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(30,25,38),Enum.Material.Slate,0,0,true},
	{"BodyCap",Vector3.new(6.4,0.5,6.4),CFrame.new(0.0000,6.1000,0.5000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(52,50,58),Enum.Material.Slate,0,0,true},
	{"VentL0",Vector3.new(0.2,0.35,4.2),CFrame.new(-3.0500,2.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"VentL1",Vector3.new(0.2,0.35,4.2),CFrame.new(-3.0500,3.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"VentL2",Vector3.new(0.2,0.35,4.2),CFrame.new(-3.0500,4.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"WingL",Vector3.new(0.25,3.2,4.6),CFrame.new(-3.6000,5.6000,1.6000,0.8480,-0.5183,-0.1102,0.5299,0.8295,0.1763,0.0000,-0.2079,0.9781),Color3.fromRGB(58,26,82),Enum.Material.Slate,0,0,true},
	{"WingEdgeL",Vector3.new(0.3,0.25,4.6),CFrame.new(-4.4500,7.0000,1.4000,0.8480,-0.5183,-0.1102,0.5299,0.8295,0.1763,0.0000,-0.2079,0.9781),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"VentR0",Vector3.new(0.2,0.35,4.2),CFrame.new(3.0500,2.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"VentR1",Vector3.new(0.2,0.35,4.2),CFrame.new(3.0500,3.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"VentR2",Vector3.new(0.2,0.35,4.2),CFrame.new(3.0500,4.5000,0.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"WingR",Vector3.new(0.25,3.2,4.6),CFrame.new(3.6000,5.6000,1.6000,0.8480,0.5183,0.1102,-0.5299,0.8295,0.1763,0.0000,-0.2079,0.9781),Color3.fromRGB(58,26,82),Enum.Material.Slate,0,0,true},
	{"WingEdgeR",Vector3.new(0.3,0.25,4.6),CFrame.new(4.4500,7.0000,1.4000,0.8480,0.5183,0.1102,-0.5299,0.8295,0.1763,0.0000,-0.2079,0.9781),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"UpperJaw",Vector3.new(4.4,1.3,3.2),CFrame.new(0.0000,5.1500,-3.7000,1.0000,0.0000,0.0000,0.0000,0.9781,-0.2079,0.0000,0.2079,0.9781),Color3.fromRGB(36,31,46),Enum.Material.Slate,0,0,true},
	{"LowerJaw",Vector3.new(4,0.8,2.8),CFrame.new(0.0000,2.7500,-3.5000,1.0000,0.0000,0.0000,0.0000,0.9848,0.1736,0.0000,-0.1736,0.9848),Color3.fromRGB(36,31,46),Enum.Material.Slate,0,0,true},
	{"Throat",Vector3.new(3,1.4,0.4),CFrame.new(0.0000,3.9000,-2.2000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(200,90,255),Enum.Material.Neon,0,0,false},
	{"ToothUpper0",Vector3.new(0.35,0.75,0.35),CFrame.new(-1.5000,4.3000,-4.8000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothUpper1",Vector3.new(0.35,0.75,0.35),CFrame.new(-0.5000,4.3000,-4.8000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothUpper2",Vector3.new(0.35,0.75,0.35),CFrame.new(0.5000,4.3000,-4.8000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothUpper3",Vector3.new(0.35,0.75,0.35),CFrame.new(1.5000,4.3000,-4.8000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothLower0",Vector3.new(0.3,0.6,0.3),CFrame.new(-1.0000,3.3000,-4.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothLower1",Vector3.new(0.3,0.6,0.3),CFrame.new(0.0000,3.3000,-4.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"ToothLower2",Vector3.new(0.3,0.6,0.3),CFrame.new(1.0000,3.3000,-4.5500,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,false},
	{"EyeL",Vector3.new(0.8,0.4,0.3),CFrame.new(-1.3000,6.0500,-4.5500,0.9781,0.2079,0.0000,-0.2079,0.9781,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(255,80,40),Enum.Material.Neon,0,0,false},
	{"BrowL",Vector3.new(1.5,0.45,1.1),CFrame.new(-1.3000,6.4500,-4.2000,0.9511,0.3090,0.0000,-0.3090,0.9511,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(24,20,30),Enum.Material.Slate,0,0,true},
	{"NostrilL",Vector3.new(0.35,0.25,0.2),CFrame.new(-0.8000,5.3000,-5.3500,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(12,10,14),Enum.Material.Slate,0,0,false},
	{"EyeR",Vector3.new(0.8,0.4,0.3),CFrame.new(1.3000,6.0500,-4.5500,0.9781,-0.2079,0.0000,0.2079,0.9781,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(255,80,40),Enum.Material.Neon,0,0,false},
	{"BrowR",Vector3.new(1.5,0.45,1.1),CFrame.new(1.3000,6.4500,-4.2000,0.9511,-0.3090,0.0000,0.3090,0.9511,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(24,20,30),Enum.Material.Slate,0,0,true},
	{"NostrilR",Vector3.new(0.35,0.25,0.2),CFrame.new(0.8000,5.3000,-5.3500,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(12,10,14),Enum.Material.Slate,0,0,false},
	{"Drop",Vector3.new(1,1,1),CFrame.new(0.0000,3.5000,-5.6000,1.0000,0.0000,0.0000,0.0000,1.0000,0.0000,0.0000,0.0000,1.0000),Color3.fromRGB(160,60,245),Enum.Material.Slate,1,0,false},
	{"HornL0",Vector3.new(0.95,1.5,0.95),CFrame.new(-2.3224,6.9941,2.6565,0.9848,-0.1632,0.0594,0.1736,0.9254,-0.3368,0.0000,0.3420,0.9397),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornL1",Vector3.new(0.81,1.5,0.81),CFrame.new(-2.5905,8.0944,3.3028,0.9563,-0.2335,0.1760,0.2924,0.7637,-0.5755,0.0000,0.6018,0.7986),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornL2",Vector3.new(0.67,1.5,0.67),CFrame.new(-2.9029,8.9324,4.2526,0.9135,-0.2391,0.3291,0.4067,0.5370,-0.7391,0.0000,0.8090,0.5878),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornL3",Vector3.new(0.53,1.5,0.53),CFrame.new(-3.1649,9.4478,5.4229,0.8572,-0.1677,0.4870,0.5150,0.2791,-0.8105,0.0000,0.9455,0.3256),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornL4",Vector3.new(0.39,1.5,0.39),CFrame.new(-3.2766,9.6275,6.7114,0.7880,-0.0215,0.6153,0.6157,0.0275,-0.7875,0.0000,0.9994,0.0349),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,true},
	{"HornR0",Vector3.new(0.95,1.5,0.95),CFrame.new(2.3224,6.9941,2.6565,0.9848,0.1632,-0.0594,-0.1736,0.9254,-0.3368,0.0000,0.3420,0.9397),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornR1",Vector3.new(0.81,1.5,0.81),CFrame.new(2.5905,8.0944,3.3028,0.9563,0.2335,-0.1760,-0.2924,0.7637,-0.5755,0.0000,0.6018,0.7986),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornR2",Vector3.new(0.67,1.5,0.67),CFrame.new(2.9029,8.9324,4.2526,0.9135,0.2391,-0.3291,-0.4067,0.5370,-0.7391,0.0000,0.8090,0.5878),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornR3",Vector3.new(0.53,1.5,0.53),CFrame.new(3.1649,9.4478,5.4229,0.8572,0.1677,-0.4870,-0.5150,0.2791,-0.8105,0.0000,0.9455,0.3256),Color3.fromRGB(214,204,182),Enum.Material.SmoothPlastic,0,0,true},
	{"HornR4",Vector3.new(0.39,1.5,0.39),CFrame.new(3.2766,9.6275,6.7114,0.7880,0.0215,-0.6153,-0.6157,0.0275,-0.7875,0.0000,0.9994,0.0349),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,true},
	{"Spike0",Vector3.new(0.6,1.4,0.6),CFrame.new(0.0000,6.9000,1.6000,0.7071,0.0000,0.7071,0.3320,0.8829,-0.3320,-0.6243,0.4695,0.6243),Color3.fromRGB(70,36,98),Enum.Material.Slate,0,0,true},
	{"Spike1",Vector3.new(0.6,1.2,0.6),CFrame.new(0.0000,6.8000,2.6000,0.7071,0.0000,0.7071,0.3320,0.8829,-0.3320,-0.6243,0.4695,0.6243),Color3.fromRGB(70,36,98),Enum.Material.Slate,0,0,true},
	{"Spike2",Vector3.new(0.6,1,0.6),CFrame.new(0.0000,6.7000,3.6000,0.7071,0.0000,0.7071,0.3320,0.8829,-0.3320,-0.6243,0.4695,0.6243),Color3.fromRGB(70,36,98),Enum.Material.Slate,0,0,true},
	{"Crystal0",Vector3.new(1.6,7.2,1.6),CFrame.new(0.0000,9.8000,1.0000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal0Core",Vector3.new(0.72,6.12,0.72),CFrame.new(0.0000,9.4400,1.0000,0.7071,0.0000,0.7071,0.0000,1.0000,0.0000,-0.7071,0.0000,0.7071),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal0Tip",Vector3.new(1.152,1.152,1.152),CFrame.new(0.0000,13.9184,1.0000,0.4082,-0.8165,0.4082,0.5774,0.5774,0.5774,-0.7071,-0.0000,0.7071),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal1",Vector3.new(1.1,4.6,1.1),CFrame.new(-2.4107,8.3542,-0.1798,0.6725,-0.3090,0.6725,0.0924,0.9366,0.3380,-0.7343,-0.1651,0.6584),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal1Core",Vector3.new(0.495,3.91,0.495),CFrame.new(-2.3397,8.1388,-0.1419,0.6725,-0.3090,0.6725,0.0924,0.9366,0.3380,-0.7343,-0.1651,0.6584),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal1Tip",Vector3.new(0.792,0.792,0.792),CFrame.new(-3.2316,10.8422,-0.6185,0.2099,-0.9549,0.2099,0.5422,0.2923,0.7878,-0.8136,-0.0515,0.5791),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal2",Vector3.new(1.2,5.1,1.2),CFrame.new(2.5722,8.5729,0.7335,0.6645,0.3420,0.6645,-0.1411,0.9305,-0.3379,-0.7339,0.1308,0.6666),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal2Core",Vector3.new(0.54,4.335,0.54),CFrame.new(2.4849,8.3356,0.7001,0.6645,0.3420,0.6645,-0.1411,0.9305,-0.3379,-0.7339,0.1308,0.6666),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal2Tip",Vector3.new(0.864,0.864,0.864),CFrame.new(3.5773,11.3076,1.1178,0.5811,-0.5698,0.5811,0.4974,0.8138,0.3006,-0.6442,0.1144,0.7563),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal3",Vector3.new(1,4.1,1),CFrame.new(-0.9853,8.0398,3.3579,0.7002,-0.1392,0.7002,0.3880,0.8975,-0.2096,-0.5993,0.4185,0.6824),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal3Core",Vector3.new(0.45,3.485,0.45),CFrame.new(-0.9568,7.8559,3.2721,0.7002,-0.1392,0.7002,0.3880,0.8975,-0.2096,-0.5993,0.4185,0.6824),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal3Tip",Vector3.new(0.72,0.72,0.72),CFrame.new(-1.3157,10.1705,4.3515,0.3239,-0.8889,0.3239,0.8685,0.4152,0.2708,-0.3752,0.1936,0.9065),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal4",Vector3.new(0.9,3.7,0.9),CFrame.new(1.5476,7.8643,2.9724,0.6861,0.2419,0.6861,0.1063,0.8996,-0.4235,-0.7197,0.3635,0.5915),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal4Core",Vector3.new(0.405,3.145,0.405),CFrame.new(1.5028,7.6979,2.9052,0.6861,0.2419,0.6861,0.1063,0.8996,-0.4235,-0.7197,0.3635,0.5915),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal4Tip",Vector3.new(0.648,0.648,0.648),CFrame.new(2.0657,9.7910,3.7509,0.5358,-0.6526,0.5358,0.6927,0.7026,0.1629,-0.4828,0.2839,0.8285),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal5",Vector3.new(0.9,3.2,0.9),CFrame.new(0.1606,7.6326,-1.8987,0.7044,-0.0872,0.7044,-0.2546,0.8954,0.3654,-0.6626,-0.4367,0.6085),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
	{"Crystal5Core",Vector3.new(0.405,2.72,0.405),CFrame.new(0.1745,7.4893,-1.8289,0.7044,-0.0872,0.7044,-0.2546,0.8954,0.3654,-0.6626,-0.4367,0.6085),Color3.fromRGB(160,60,245),Enum.Material.Neon,0,0,false},
	{"Crystal5Tip",Vector3.new(0.648,0.648,0.648),CFrame.new(-0.0043,9.3263,-2.7248,0.3564,-0.8637,0.3564,0.2389,0.4530,0.8589,-0.9033,-0.2209,0.3678),Color3.fromRGB(48,14,74),Enum.Material.Glass,0.15,0.25,true},
}

local model = Instance.new("Model")
model.Name = "DragonGlassMine"
for _, s in ipairs(P) do
	local p = Instance.new("Part")
	p.Name = s[1]
	p.Size = s[2]
	p.CFrame = s[3]
	p.Color = s[4]
	p.Material = s[5]
	p.Transparency = s[6]
	p.Reflectance = s[7]
	p.CanCollide = s[8]
	p.CanQuery = s[8]
	p.Anchored = true
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.CastShadow = p.Material ~= Enum.Material.Neon
	p.Parent = model
end
model.PrimaryPart = model.Base
model.Base.PivotOffset = CFrame.new(0, -0.5, 0) -- pivot at the bottom centre
model:SetAttribute("OreValue", 40)
model:SetAttribute("DropInterval", 1.5)
model:SetAttribute("OreSize", 1)
model:SetAttribute("Enabled", true)

local core = model.Crystal0Core
local light = Instance.new("PointLight")
light.Color = Color3.fromRGB(170, 70, 255)
light.Brightness = 2
light.Range = 14
light.Parent = core
local sparks = Instance.new("ParticleEmitter")
sparks.Color = ColorSequence.new(Color3.fromRGB(190, 110, 255))
sparks.LightEmission = 1
sparks.Rate = 6
sparks.Lifetime = NumberRange.new(1.5, 2.5)
sparks.Speed = NumberRange.new(0.5, 1.5)
sparks.SpreadAngle = Vector2.new(30, 30)
sparks.Size = NumberSequence.new(0.3, 0)
sparks.Parent = core
local mouth = Instance.new("PointLight")
mouth.Color = Color3.fromRGB(200, 90, 255)
mouth.Brightness = 1.5
mouth.Range = 8
mouth.Parent = model.Throat

local dropper = Instance.new("Script")
dropper.Name = "Dropper"
dropper.Source = [[
local Debris = game:GetService("Debris")
local mine = script.Parent
local drop = mine:WaitForChild("Drop")
while true do
	task.wait(mine:GetAttribute("DropInterval") or 1.5)
	if mine:GetAttribute("Enabled") ~= false then
		local size = mine:GetAttribute("OreSize") or 1
		local ore = Instance.new("Part")
		ore.Name = "DragonGlassOre"
		ore.Size = Vector3.new(size, size, size)
		ore.Material = Enum.Material.Glass
		ore.Color = Color3.fromRGB(120, 40, 200)
		ore.Transparency = 0.15
		ore.Reflectance = 0.2
		ore.CFrame = drop.CFrame * CFrame.Angles(math.random() * 6.28, math.random() * 6.28, 0)
		ore:SetAttribute("Value", mine:GetAttribute("OreValue") or 40)
		ore:SetAttribute("OreType", "DragonGlass")
		ore.Parent = workspace
		ore.AssemblyLinearVelocity = drop.CFrame.LookVector * 6
		Debris:AddItem(ore, 30)
	end
end
]]
dropper.Parent = model

-- Place on the ground in front of the camera, front facing the camera.
local cam = workspace.CurrentCamera
local target = cam.CFrame.Position + cam.CFrame.LookVector * 30
local hit = workspace:Raycast(target + Vector3.new(0, 100, 0), Vector3.new(0, -400, 0))
local ground = hit and hit.Position or Vector3.new(target.X, 0, target.Z)
local look = Vector3.new(-cam.CFrame.LookVector.X, 0, -cam.CFrame.LookVector.Z)
if look.Magnitude < 0.01 then look = Vector3.new(0, 0, -1) end
model:PivotTo(CFrame.lookAt(ground, ground + look.Unit))
model.Parent = workspace
game:GetService("Selection"):Set({model})
print("Dragon Glass Mine created:", #P, "parts")
