# Dungeon Creatures (Roblox)

3-stage enemy line, built only from normal Roblox Parts.

| Stage | Name | HP | Height |
|---|---|---|---|
| 1 (weak) | Ghoul Whelp | 50 | 4.6 studs |
| 2 (normal) | Dungeon Ghoul | 250 | 10.3 studs |
| 3 (boss) | Ghoul Overlord | 3000 | 23.8 studs |

## Put them in Roblox Studio
1. Open `DungeonCreatures.server.lua`, copy everything.
2. Studio: **View > Command Bar**, paste, press Enter. They appear at the world centre.
   (Or put it in a Script in ServerScriptService to spawn on Play.)

## Change them
Edit `gen.mjs`, then `node gen.mjs` (rebuilds the Lua + data) and `node render.cjs` (rebuilds the pictures).
