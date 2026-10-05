"""Zip each mine (script, mine_kit, .blend, Roblox FBX, setup Lua, renders) and build a gallery of all 25 mines."""
import os, glob, zipfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NEW = [("magma_golem", "Magma Golem Forge"), ("kraken", "Kraken Depths"), ("tempest", "Tempest Coil"), ("pyramid", "Sun Pyramid"),
       ("glowshroom", "Glowshroom Grove"), ("owl", "Clockwork Owl"), ("void", "Void Rift"), ("phoenix", "Phoenix Nest"),
       ("sakura", "Sakura Shrine"), ("locomotive", "Ore Express"), ("scorpion", "Sandstinger"), ("corsair", "Corsair Cannon"),
       ("twin_serpents", "Fire & Ice Serpents (fusion)"), ("titan_drill", "Titan Drill"), ("astral_owl", "Astral Owl (fusion)")]
DRAKES = [("sapphire", "Sapphire Tide"), ("solar", "Solar Gold"), ("shadow", "Shadow Amethyst"), ("venom", "Venom Drake"), ("storm", "Storm Drake")]
OLD = [("frost", "Frost Wyrm"), ("emerald", "Emerald Wyvern"), ("crimson", "Crimson Drake"), ("orrery", "Astral Orrery"),
       ("cosmic", "Cosmic Drake (fusion)")]

for d, _ in NEW:
    folder = os.path.join(HERE, d)
    fbx = glob.glob(os.path.join(folder, "*_Roblox.fbx"))[0]
    name = os.path.basename(fbx)[:-len("_Roblox.fbx")]
    zp = os.path.join(folder, f"{name}.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(folder, "*.py")) + [os.path.join(HERE, "mine_kit.py"), os.path.join(folder, f"{name}.blend"), fbx,
                                                             os.path.join(folder, f"{name}_RobloxSetup.lua")]:
            z.write(f, os.path.basename(f))
        for f in sorted(glob.glob(os.path.join(folder, "renders", "*.png"))):
            z.write(f, "renders/" + os.path.basename(f))
    print("zipped", zp, os.path.getsize(zp) // 1024, "KB")

for d, _ in DRAKES:                                          # Dragonglass-style variants (standalone scripts)
    folder = os.path.join(ROOT, "mine", d)
    fbx = glob.glob(os.path.join(folder, "*_Roblox.fbx"))[0]
    name = os.path.basename(fbx)[:-len("_Roblox.fbx")]
    zp = os.path.join(folder, f"{name}.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(folder, "*.py")) + [os.path.join(folder, f"{name}.blend"), fbx, os.path.join(folder, f"{name}_RobloxSetup.lua")]:
            z.write(f, os.path.basename(f))
        for f in sorted(glob.glob(os.path.join(folder, "renders", "*.png"))):
            z.write(f, "renders/" + os.path.basename(f))
    print("zipped", zp, os.path.getsize(zp) // 1024, "KB")

tiles = [(os.path.join(ROOT, "mine", d, "renders", "hero.png"), f"{i + 1}. {t}") for i, (d, t) in enumerate(OLD)]
tiles += [(os.path.join(HERE, d, "renders", "hero.png"), f"{i + 6}. {t}") for i, (d, t) in enumerate(NEW)]
tiles += [(os.path.join(ROOT, "mine", d, "renders", "hero.png"), f"{i + 21}. {t}") for i, (d, t) in enumerate(DRAKES)]
TW, TH, COLS = 440, 404, 5
sheet = Image.new("RGB", (TW * COLS, (TH + 34) * ((len(tiles) + COLS - 1) // COLS)), (14, 14, 20))
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except OSError:
    font = ImageFont.load_default()
dr = ImageDraw.Draw(sheet)
for i, (p, label) in enumerate(tiles):
    im = Image.open(p).convert("RGB")
    im = im.resize((TW, round(im.height * TW / im.width)), Image.LANCZOS)
    im = im.crop((0, (im.height - TH) // 2, TW, (im.height - TH) // 2 + TH))
    x, y = (i % COLS) * TW, (i // COLS) * (TH + 34)
    sheet.paste(im, (x, y + 34))
    dr.text((x + 10, y + 6), label, fill=(255, 255, 255), font=font)
sheet.save(os.path.join(HERE, "ALL_MINES.png"))
print("gallery saved")
