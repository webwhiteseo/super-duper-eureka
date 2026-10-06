"""Nightmare Lament Furnace - an original dream-horror furnace (inspired by the 'sad dream' furnace style).
A weeping porcelain mask rises from a violet obsidian altar; its glowing tears run down into a swirling dream
vortex in the altar's mouth. Ore that touches the vortex is sold. Crescent moon, dream clouds, candles, crystals.
Built with mine_kit; writes NightmareLamentFurnace_RobloxSetup.lua (colours, lights, working sell script)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from mine_kit import *

C_ALTAR, C_MASK, C_DREAM, C_DETAIL = begin("NightmareLamentFurnace", ["Altar", "Mask", "Dream", "Details"], seed=31)
OBS = M("Dream Obsidian", (40, 26, 60), rough=0.25, metal=0.3, rbx="Basalt", noise=((28, 18, 44), (62, 42, 90), 3.0, 0.2))
TRIM = M("Pink Trim (Metal)", (255, 120, 210), rough=0.3, metal=0.6, glow=(255, 90, 200), glow_strength=1.0, rbx="Neon")
SILVER = M("Moon Silver (Metal)", (200, 196, 220), rough=0.25, metal=0.9, rbx="Metal")
PORC = M("Porcelain Mask", (236, 228, 244), rough=0.3, rbx="SmoothPlastic")
CRACK = M("Mask Crack", (40, 20, 50), rough=0.5)
TEAR = M("Dream Tears", (130, 230, 255), rough=0.1, glow=(90, 210, 255), glow_strength=4.0, rbx="Neon", light=(10, 1.2))
VORTEX = M("Dream Vortex", (220, 120, 255), rough=0.2, glow=(190, 80, 255), glow_strength=5.0, rbx="Neon", light=(16, 2.0))
BURN = M("Burn Zone", (255, 160, 240), rough=0.2, glow=(255, 120, 230), glow_strength=2.0, rbx="ForceField", alpha=0.35)
VOID = M("Void Black", (8, 4, 14), rough=0.6)
CLOUD = M("Dream Cloud", (240, 196, 236), rough=0.8, glow=(200, 140, 220), glow_strength=0.3, rbx="SmoothPlastic")
CRYS = M("Dream Crystal", (190, 140, 255), rough=0.05, glow=(150, 90, 255), glow_strength=1.2, rbx="Glass", alpha=0.15, light=(8, 0.7))
FLAME = M("Candle Flame", (170, 230, 255), rough=0.4, glow=(120, 200, 255), glow_strength=8.0, rbx="Neon", light=(8, 1.2))
WAX = M("Candle Wax", (220, 210, 236), rough=0.6)
STAR = M("Starlight", (255, 240, 200), rough=0.3, glow=(255, 220, 160), glow_strength=5.0, rbx="Neon")
X_AX, Y_AX, Z_AX = V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)
rnd = random.Random(31)

# ---- altar with a mouth on the front (ore enters at ground level)
lathe("Altar", V(0, 0.6, 0), [(4.2, 0), (4.2, 0.4), (3.8, 0.6), (3.6, 2.6), (4.0, 2.8), (4.0, 3.2), (3.2, 3.3)], OBS, C_ALTAR, n=8, smooth=False)
for z in (0.5, 2.95):
    torus(f"Altar Band {z}", V(0, 0.6, z), Z_AX, Y_AX, 4.05 if z < 1 else 4.0, 0.08, TRIM, C_ALTAR, n_major=8, n_minor=4)
MY = 0.6 - 3.75                                           # mouth plane (front face)
abox("Mouth Recess", -1.7, 1.7, MY + 0.35, MY + 0.9, 0.0, 2.3, VOID, C_ALTAR)
tube("Mouth Frame", V(0, MY - 0.1, 1.15), Y_AX, Z_AX, 1.95, 1.65, 0.35, SILVER, C_ALTAR, n=24)
cyl("Vortex Disc", V(0, MY + 0.3, 1.15), V(0, MY + 0.2, 1.15), 1.6, 1.6, VORTEX, C_DREAM, n=28, hint=Z_AX)
for k in range(5):                                        # spiral arms
    pts = []
    for i in range(9):
        t = i / 8;a = 2 * math.pi * k / 5 + t * 2.6;r = 0.2 + 1.3 * t
        pts.append(V(r * math.cos(a), MY + 0.12, 1.15 + r * math.sin(a)))
    path_tube(f"Vortex Arm {k + 1}", pts, [0.05 + 0.08 * (i / 8) for i in range(9)], CRACK, C_DREAM, n=5)
dot("Vortex Eye", V(0, MY + 0.08, 1.15), 0.28, STAR, C_DREAM)
bz = abox("Burn Zone", -1.6, 1.6, MY - 0.55, MY - 0.15, 0.05, 2.25, BURN, C_DREAM)  # the sell part (see-through in Roblox)
bz.hide_render = True
for s in (-1, 1):                                         # intake lip / guide rails for the conveyor
    beam(f"Guide Rail {s}", V(s * 1.85, MY - 1.6, 0.35), V(s * 1.85, MY - 0.1, 0.35), 0.18, 0.5, Y_AX, SILVER, C_ALTAR)
    crystal(f"Mouth Fang {s}", V(s * 1.5, MY - 0.2, 2.3), V(-s * 0.3, -0.3, -1), 0.9, 0.18, CRYS, C_ALTAR, sides=4)

# ---- weeping mask rising from the altar
MC = V(0, 1.2, 6.9)
ellip("Mask", MC, 2.3, 1.0, 3.0, PORC, C_MASK, n=24, m=8)
ellip("Mask Back", MC + V(0, 0.7, 0), 2.35, 0.6, 3.05, OBS, C_MASK, n=20, m=6)
cyl("Mask Neck", V(0, 1.4, 3.2), MC + V(0, 0.4, -2.4), 1.3, 0.9, OBS, C_MASK, n=12)
for s in (-1, 1):
    E = MC + V(s * 0.85, -0.92, 0.6)
    path_tube(f"Closed Eye {s}", [E + V(-s * 0.45, 0, 0.12), E + V(0, -0.06, -0.12), E + V(s * 0.45, 0, 0.12)], [0.06, 0.09, 0.06], VOID, C_MASK, n=6)
    path_tube(f"Brow {s}", [E + V(-s * 0.5, 0.0, 0.75), E + V(0, -0.05, 0.6), E + V(s * 0.55, 0.05, 0.95)], [0.05, 0.08, 0.04], VOID, C_MASK, n=6)
    tear = [E + V(s * 0.1, -0.08, -0.1), E + V(s * 0.25, -0.15, -1.2), E + V(s * 0.3, -0.25, -2.4), MC + V(s * 1.1, -1.0, -3.0)]
    path_tube(f"Tear Stream {s}", tear, [0.09, 0.12, 0.13, 0.1], TEAR, C_MASK, n=8)
    for k in range(3):
        dot(f"Tear Drop {s}{k}", V(s * (1.2 + 0.1 * k), MY + 0.9 + 0.5 * k, 3.4 - 0.25 * k), 0.13, TEAR, C_DREAM)
path_tube("Mouth Frown", [MC + V(-0.6, -0.97, -1.3), MC + V(0, -1.0, -1.05), MC + V(0.6, -0.97, -1.3)], [0.05, 0.08, 0.05], VOID, C_MASK, n=6)
crack = [MC + V(0.3, -1.0, 2.6), MC + V(0.55, -1.02, 1.9), MC + V(0.35, -1.02, 1.4), MC + V(0.7, -0.95, 0.9)]
path_tube("Mask Crack", crack, [0.04, 0.05, 0.04, 0.02], CRACK, C_MASK, n=5)
for k in range(9):                                        # crown of dream crystals behind the mask
    a = math.radians(20 + k * 17.5)
    b = MC + V(2.1 * math.cos(a), 0.9, 2.6 * math.sin(a))
    crystal(f"Halo Crystal {k + 1}", b, V(math.cos(a), 0.15, math.sin(a)), 1.2 + 0.9 * math.sin(a), 0.22, CRYS, C_MASK, sides=5)

# ---- crescent moon, dream clouds, stars
MM = MC + V(0, 0.9, 4.6);R = 1.5
outer = [MM + R * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in range(90, 271, 15)]
r2 = math.hypot(0.7, R)
a0, a1 = math.degrees(math.atan2(-R, -0.7)) % 360, math.degrees(math.atan2(R, -0.7))
inner = [MM + V(0.7, 0, 0) + r2 * V(math.cos(math.radians(a)), 0, math.sin(math.radians(a))) for a in [a0 - (a0 - a1) * k / 8 for k in range(1, 8)]]
blade("Crescent Moon", outer + inner, 0.35, SILVER, C_DREAM)
dot("Moon Star", MM + V(0.9, 0, 0.6), 0.22, STAR, C_DREAM)
for k, (x, y, z, s_) in enumerate(((-4.6, 1.5, 5.6, 1.0), (4.8, 1.8, 7.2, 1.2), (-3.8, 2.6, 9.8, 0.8), (3.6, 2.4, 10.6, 0.9))):
    for j in range(4):
        rock_f(f"Cloud {k + 1}-{j + 1}", V(x + (j - 1.5) * 0.7 * s_, y + rnd.uniform(-0.2, 0.2), z + rnd.uniform(-0.2, 0.3)),
               (0.75 * s_, 0.6 * s_, 0.5 * s_), CLOUD, C_DREAM, rough=0.15, subd=2)
for k in range(10):
    a = rnd.uniform(0, 6.28);r = rnd.uniform(4.5, 6.0)
    crystal(f"Star {k + 1}a", V(r * math.cos(a), 0.6 + r * math.sin(a), rnd.uniform(4, 12)), Z_AX, 0.25, 0.1, STAR, C_DREAM, sides=4)

# ---- candle pillars and crystal clusters
for s in (-1, 1):
    P = V(s * 5.2, -1.6, 0)
    lathe(f"Candle Pillar {s}", P, [(0.7, 0), (0.6, 0.3), (0.4, 0.5), (0.38, 3.0), (0.65, 3.2), (0.65, 3.4)], OBS, C_DETAIL, n=8, smooth=False)
    torus(f"Pillar Band {s}", P + V(0, 0, 2.6), Z_AX, Y_AX, 0.42, 0.06, TRIM, C_DETAIL, n_major=8, n_minor=4)
    for j, (dx, dy, h) in enumerate(((0, 0, 1.1), (0.3, 0.2, 0.7), (-0.28, 0.15, 0.55))):
        c = P + V(dx, dy, 3.4)
        cyl(f"Candle {s}{j}", c, c + V(0, 0, h), 0.14, 0.14, WAX, C_DETAIL, n=8)
        lathe(f"Candle Flame {s}{j}", c + V(0, 0, h + 0.05), [(0.1, 0), (0.12, 0.12), (0.0, 0.42)], FLAME, C_DETAIL, n=8)
    crystal_cluster(f"Dream Cluster {s}", V(s * 4.6, 3.6, 0.2), 5, 0.5, CRYS, OBS, C_DETAIL, seed=s + 5)

finish_mine(bg=(0.02, 0.012, 0.035), tint=(0.85, 0.75, 1.0))

# ---- replace the dropper setup with a furnace (sell) setup
used = {export_name(ob.data.materials[0].name) for ob in MINE_OBJECTS}
items = sorted((k, v) for k, v in RBX.items() if k in used)
look = ",\n".join('\t%s = {"%s", %d, %d, %d, %g}' % (k, v[0], *v[1], v[2]) for k, v in items)
lights = ",\n".join('\t%s = {%d, %d, %d, %g, %g}' % (k, *v[3]) for k, v in items if v[3])
lua = f'''-- NightmareLamentFurnace: colours, Roblox materials, glow lights and a working SELL script.
-- 1. Import NightmareLamentFurnace_Roblox.fbx (Import 3D, Scale Unit = Stud, untick "Import as single mesh", tick Anchored).
-- 2. Select the imported model.  3. View > Command Bar: paste this file, press Enter.
-- Ore (any Part named "Ore" with a "Value" attribute - what the mine droppers make) that touches the glowing
-- vortex mouth is destroyed and its Value x Multiplier is added to the owner's leaderstats Cash.
-- Owner = model attribute OwnerUserId (set it per plot), otherwise the first player in the server.
local LOOK = {{
{look}
}}
local LIGHTS = {{
{lights}
}}
local model = game:GetService("Selection"):Get()[1]
if not (model and model:IsA("Model")) then model = workspace:FindFirstChild("NightmareLamentFurnace_Roblox", true) or workspace:FindFirstChild("NightmareLamentFurnace", true) end
assert(model, "Select the imported NightmareLamentFurnace model first.")
local styled, lit, burn = 0, 0, nil
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
		if key == "BurnZone" then burn = p end
	end
end
if burn then
	burn.Name = "Burn"; burn.CanCollide = false; burn.CanTouch = true; burn.CanQuery = false
	model:SetAttribute("Multiplier", model:GetAttribute("Multiplier") or 2)
	local old = model:FindFirstChild("Furnace"); if old then old:Destroy() end
	local s = Instance.new("Script")
	s.Name = "Furnace"
	s.Source = [[
local Players = game:GetService("Players")
local furnace = script.Parent
local burn = furnace:FindFirstChild("Burn", true)
local function owner()
	local id = furnace:GetAttribute("OwnerUserId")
	if id then return Players:GetPlayerByUserId(id) end
	return Players:GetPlayers()[1]
end
burn.Touched:Connect(function(hit)
	if hit.Name ~= "Ore" or hit:GetAttribute("Sold") then return end
	hit:SetAttribute("Sold", true)
	local value = (hit:GetAttribute("Value") or 0) * (furnace:GetAttribute("Multiplier") or 1)
	local plr = owner()
	local stats = plr and plr:FindFirstChild("leaderstats")
	local cash = stats and stats:FindFirstChild("Cash")
	if cash then cash.Value += value end
	hit:Destroy()
end)
]]
	s.Parent = model
end
print(("[NightmareLamentFurnace] %d parts coloured, %d lights, sell script %s"):format(styled, lit, burn and "added" or "NOT found"))
-- No leaderstats yet? Add a Script in ServerScriptService:
--   game.Players.PlayerAdded:Connect(function(p) local ls = Instance.new("Folder"); ls.Name = "leaderstats"; ls.Parent = p
--   local c = Instance.new("IntValue"); c.Name = "Cash"; c.Parent = ls end)
'''
open(os.path.join(OUT, "NightmareLamentFurnace_RobloxSetup.lua"), "w").write(lua)
print("[mine] wrote furnace setup lua")
