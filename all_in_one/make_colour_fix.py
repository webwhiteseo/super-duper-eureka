"""Builds OreHaven_ColourFix.lua: restores colours/materials/glow lights on every imported Ore Haven model (no selection needed)."""
import bpy, os, re, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "OreHaven_AllModels.blend"))
lua_for = {}
for f in glob.glob(os.path.join(ROOT, "**/*_RobloxSetup.lua"), recursive=True):
    lua_for[os.path.basename(f).replace("_RobloxSetup.lua", "")] = open(f).read()
ent = re.compile(r'\[?"?(\w+)"?\]?\s*=\s*\{"(\w+)",\s*(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)(?:,\s*\{(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+),\s*([\d.]+)\})?')
lit = re.compile(r'(\w+)\s*=\s*\{(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+),\s*([\d.]+)\}')
def srgb(c):
    c = max(0.0, min(1.0, c)); return round(255 * (c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055))
items = {}
for e in [o for o in bpy.data.objects if o.type == 'EMPTY']:
    look = {}
    src = lua_for.get(e.name)
    if src:
        lk = src.split("local LOOK", 1)[1]
        body = lk.split("\n}", 1)[0]
        for m in ent.finditer(body):
            k = m.group(1); row = [m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5)), float(m.group(6))]
            if m.group(7): row.append([int(m.group(7)), int(m.group(8)), int(m.group(9)), float(m.group(10)), float(m.group(11))])
            look[k] = row
        if "local LIGHTS" in src:
            for m in lit.finditer(src.split("local LIGHTS", 1)[1].split("\n}", 1)[0]):
                if m.group(1) in look and len(look[m.group(1)]) == 5:
                    look[m.group(1)].append([int(m.group(2)), int(m.group(3)), int(m.group(4)), float(m.group(5)), float(m.group(6))])
    for ch in e.children:                               # anything not in the script: use the Blender material colour
        k = re.sub(r"\.\d+$", "", ch.name)
        if k in look or not ch.data.materials: continue
        m = ch.data.materials[0]; bs = m.node_tree.nodes.get("Principled BSDF") if m.use_nodes else None
        col = bs.inputs["Base Color"].default_value if bs else m.diffuse_color
        em = bs.inputs["Emission Strength"].default_value if bs and "Emission Strength" in bs.inputs else 0
        met = bs.inputs["Metallic"].default_value if bs else 0
        look[k] = ["Neon" if em > 1 else "Metal" if met > 0.6 else "SmoothPlastic", srgb(col[0]), srgb(col[1]), srgb(col[2]), 0]
    items[e.name] = look
def row(r):
    s = '{"%s", %d, %d, %d, %g' % tuple(r[:5])
    return s + (', {%d, %d, %d, %g, %g}}' % tuple(r[5]) if len(r) > 5 else '}')
L = ["-- Ore Haven colour fix: paste into View > Command Bar and press Enter. Works on every imported Ore Haven model in Workspace.",
     "local ITEMS = {"]
for n, look in sorted(items.items()):
    L.append('\t["%s"] = {' % n + ", ".join('["%s"] = %s' % (k, row(v)) for k, v in sorted(look.items())) + "},")
L.append("}")
L.append('''local ANY = {}   -- fallback by part name only, if an item model was renamed
for _, look in pairs(ITEMS) do for k, v in pairs(look) do if ANY[k] == nil then ANY[k] = v end end end
local function key(n) return (n:gsub("%.%d+$", ""):gsub("_%d+$", "")) end
local function itemOf(p)
	local a = p.Parent
	while a and a ~= workspace do
		local look = ITEMS[a.Name] or ITEMS[(a.Name:gsub("_Roblox$", ""))]
		if look then return look end
		a = a.Parent
	end
end
local done, lights, missed = 0, 0, {}
for _, p in ipairs(workspace:GetDescendants()) do
	if p:IsA("BasePart") then
		local look = itemOf(p)
		local l = (look and look[key(p.Name)]) or ANY[key(p.Name)]
		if l then
			pcall(function()
				for _, c in ipairs(p:GetChildren()) do if c:IsA("SurfaceAppearance") then c:Destroy() end end
				if p:IsA("MeshPart") then p.TextureID = "" end
				p.Material = Enum.Material[l[1]]; p.Color = Color3.fromRGB(l[2], l[3], l[4]); p.Transparency = l[5]
				if l[6] then
					local pl = p:FindFirstChild("GlowLight") or Instance.new("PointLight")
					pl.Name = "GlowLight"; pl.Color = Color3.fromRGB(l[6][1], l[6][2], l[6][3]); pl.Range = l[6][4]; pl.Brightness = l[6][5]; pl.Parent = p
					lights += 1
				end
			end)
			done += 1
		elseif look then
			missed[key(p.Name)] = true
		end
	end
end
local m = {} for k in pairs(missed) do table.insert(m, k) end
print(("[OreHaven] coloured %d parts, %d lights%s"):format(done, lights, #m > 0 and (" | no colour for: " .. table.concat(m, ", ")) or ""))''')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "OreHaven_ColourFix.lua"), "w").write("\n".join(L))
print("[fix] items", len(items), "entries", sum(len(v) for v in items.values()))
