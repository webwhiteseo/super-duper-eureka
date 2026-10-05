ORE FACTORY — BLENDER TERRAIN (v5)

CHANGES IN THIS VERSION
NEW IN v5
- Hills steeper: ramps about 40 degrees, other sides about 49 degrees (still walkable), cliffs unchanged.

NEW IN v4
- Both hills 50% taller: centre hill 36 studs, tall hill 47 studs (still 30% higher).
- Tall hill now sits half inside the centre hill (behind it).
- Each hill: flat top, a long walkable ramp on one side, an uneven rock cliff on the other.
  Centre hill: ramp west, cliff east. Tall hill: ramp east, cliff west.
- Each cliff has one climbable route: a staircase of ~5-stud ledges you jump up.
  The rest of the cliff is two big drops (18-23 studs), too high to jump.
- Boulders along the foot of each cliff (HillBoulders).
- Ground is now a 2-stud grid around the hills for sharper cliffs (4-stud elsewhere).
- OreFactory_Lighting.lua sets max walkable slope to 50 degrees so cliffs can't be walked up.

NEW IN v3
- Tall hill moved next to the centre hill. Ridge removed.
- Wooden bridge over the river, between plots 4 and 5, with a lantern at each end.
- Lanterns inside all 5 caves (Lantern_*_Frame + Lantern_*_Glow).
- Flowers, bushes and tall grass, merged into 12 meshes (Flowers_/Bushes_/TallGrass_ + NW/NE/SW/SE).
- 8 palm trees on the beach (PalmTree_01..08).
- Fog and atmosphere: run OreFactory_Lighting.lua in Studio's Command Bar. Blender script also adds light world fog.
- Tree crowns now face outward (they rendered inside-out in Roblox before).

FROM v2
- Beach 30% wider. Beach water removed (use your Roblox water).
- Centre hill: flat top (~52 studs wide) for builds. Spawn pad sits on top.
- River runs from the front edge (+Y) to the centre hill and flows into a walk-in cave inside it.
  Cave has 7-stud ledges on both sides of the water and a chamber with a pool under the hill top.
- Four mountains (two each side), each with a walk-in cave facing the middle of the map.
- Ground rebuilt as a 4-stud grid in 128-stud tiles (Ground_x_y) so hills, river and caves are carved in.
- RiverWater / RiverPool are separate placeholder meshes. Delete them if you fill the river with Roblox terrain water.
- Cave roofs are separate double-sided meshes (CaveRoof_*). Grass/rock outside, dark rock ceiling inside.

BLENDER
1. Open Blender > Scripting > open OreFactory_Blender.py > Run Script (use an empty scene).
2. Save As .blend. F12 renders with the included camera.
Or import OreFactory_SmoothTerrain.obj (keep the .mtl beside it). Z up, 1 unit = 1 stud.

ROBLOX
- In the 3D Importer, untick "Import as single mesh" so each object keeps its name.
- After importing, run OreFactory_Lighting.lua (Command Bar) for fog, lantern lights and decoration settings.
- Import the Ground tiles, CaveRoof meshes and Cliff meshes as MeshParts.
- Set CollisionFidelity = PreciseConvexDecomposition on Ground and CaveRoof meshes, or players fall through hills/caves.
- Anchor everything.

NOT TESTED
Blender is not installed here, so the bpy branch has not been run. PNGs are software previews of the exact geometry, not Blender renders. Play-test slopes, cave headroom and collisions in Studio.
