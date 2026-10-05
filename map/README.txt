ORE FACTORY — BLENDER TERRAIN (v2)

CHANGES IN THIS VERSION
- Beach 30% wider. Beach water removed (use your Roblox water).
- Centre hill: 24 studs high, walkable, flat top (~48 stud wide) for builds. Spawn pad sits on top.
- Tall hill behind it (between plots 1 and 2): 31 studs (30% higher), walkable.
- Ridge joins the centre hill top to the tall hill top: 28-stud flat crest, gentle 4-degree climb.
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
- Import the Ground tiles, CaveRoof meshes and Cliff meshes as MeshParts.
- Set CollisionFidelity = PreciseConvexDecomposition on Ground and CaveRoof meshes, or players fall through hills/caves.
- Anchor everything.

NOT TESTED
Blender is not installed here, so the bpy branch has not been run. PNGs are software previews of the exact geometry, not Blender renders. Play-test slopes, cave headroom and collisions in Studio.
