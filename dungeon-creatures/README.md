# Dungeon Creatures (Roblox)

Three 3-stage enemy sets, built only from normal Roblox Parts (Block / Ball / Cylinder).

## Crystal Cave Golems (`CrystalGolems.server.lua`) — picture: `golems.png`
| Stage | Name | HP | Height |
|---|---|---|---|
| 1 (weak) | Crystal Golem Weakling | 60 | 5.5 studs |
| 2 (normal) | Crystal Golem | 300 | 10.2 studs |
| 3 (boss) | Crystal Titan | 3500 | 19.2 studs |

## Magma Spiders (`MagmaSpiders.server.lua`) — picture: `spiders.png`
| Stage | Name | HP | Height |
|---|---|---|---|
| 1 (weak) | Ember Spiderling | 40 | 4.1 studs |
| 2 (normal) | Magma Spider | 280 | 7.9 studs |
| 3 (boss) | Brood Queen | 3200 | 15 studs |

## Ghouls (`DungeonCreatures.server.lua`) — picture: `preview.png`
| Stage | Name | HP | Height |
|---|---|---|---|
| 1 (weak) | Ghoul Whelp | 50 | 4.6 studs |
| 2 (normal) | Dungeon Ghoul | 250 | 10.3 studs |
| 3 (boss) | Ghoul Overlord | 3000 | 23.8 studs |

## Put them in Roblox Studio
1. Open the `.server.lua` file, copy everything.
2. Studio: **View > Command Bar**, paste, press Enter. They appear at the world centre.
   (Or put it in a Script in ServerScriptService to spawn on Play.)

## Change them
- Golems: edit `golems.mjs`, run `node golems.mjs`, then `node render.cjs golems`.
- Spiders: edit `spiders.mjs`, run `node spiders.mjs`, then `node render.cjs spiders`.
- Ghouls: edit `gen.mjs`, run `node gen.mjs`, then `node render.cjs`.
Shared building code is in `lib.mjs`.
