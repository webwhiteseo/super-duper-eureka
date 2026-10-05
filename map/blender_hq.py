"""High-quality Blender version of the Ore Factory map.
Builds the scene with OreFactory_Blender.py, then: subdivision + smooth-by-angle on terrain,
cloud displacement on hill/mountain slopes, procedural PBR materials, bevels on built objects,
Geometry Nodes scatter (grass, flowers, pebbles), low-poly pine/oak trees, Nishita sky, fog,
Cycles renders. Layout is untouched.
Run inside Blender (Scripting > Run Script) or headless:  python3 blender_hq.py [--samples N] [--res W H] [--only NAME]
"""
import bpy,math,random,sys
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent if '__file__' in globals() else Path(bpy.path.abspath('//'))
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
def arg(name,default,n=1,cast=int):
 if name in args:
  i=args.index(name);v=[cast(a) for a in args[i+1:i+1+n]];return v if n>1 else v[0]
 return default
LOWPOLY='--lowpoly' in args  # faceted low-poly look: triangles, flat shading, flat colours
PREFIX='LP_' if LOWPOLY else 'HQ_'
SAMPLES=arg('--samples',128);RES=arg('--res',[1920,1080],2);ONLY=arg('--only',None,cast=str)
random.seed(7)

# ---------- 1. Build the map exactly as before ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
G={'__file__':str(HERE/'OreFactory_Blender.py'),'__name__':'__main__'}
exec(compile((HERE/'OreFactory_Blender.py').read_text(),'OreFactory_Blender.py','exec'),G)
scene=bpy.context.scene;col=bpy.data.collections['OreFactory_SmoothTerrain']
objs={o.name:o for o in col.objects}

# ---------- 2. Procedural PBR materials (no downloads needed) ----------
def node_mat(name,kind,c1,c2,rough=.85,bump=.3,scale=.25,extra=None):
 m=bpy.data.materials.get('OF_'+name) or bpy.data.materials.new('OF_'+name)
 m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();N=nt.nodes.new;L=nt.links.new
 out=N('ShaderNodeOutputMaterial');bs=N('ShaderNodeBsdfPrincipled');L(bs.outputs[0],out.inputs[0])
 if LOWPOLY:  # one flat colour per material
  bs.inputs['Base Color'].default_value=(*[(a+b)/2 for a,b in zip(c1,c2)],1);bs.inputs['Roughness'].default_value=max(rough,.7)
  if extra:extra(nt,bs)
  return m
 tc=N('ShaderNodeTexCoord');src=tc.outputs['Object']
 if kind=='voronoi':tex=N('ShaderNodeTexVoronoi');tex.inputs['Scale'].default_value=scale;fac=tex.outputs['Distance']
 elif kind=='wave':tex=N('ShaderNodeTexWave');tex.inputs['Scale'].default_value=scale;tex.inputs['Distortion'].default_value=6;fac=tex.outputs['Fac']
 else:tex=N('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=8;tex.inputs['Roughness'].default_value=.6;fac=tex.outputs['Fac']
 L(src,tex.inputs['Vector'])
 fine=N('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=scale*9;fine.inputs['Detail'].default_value=6;L(src,fine.inputs['Vector'])
 mix=N('ShaderNodeMath');mix.operation='MULTIPLY_ADD';L(fac,mix.inputs[0]);mix.inputs[1].default_value=.75;L(fine.outputs['Fac'],mix.inputs[2])
 ramp=N('ShaderNodeValToRGB');L(mix.outputs[0],ramp.inputs['Fac'])
 ramp.color_ramp.elements[0].position=.35;ramp.color_ramp.elements[0].color=(*c1,1)
 ramp.color_ramp.elements[1].position=1.0;ramp.color_ramp.elements[1].color=(*c2,1)
 L(ramp.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=rough
 bp=N('ShaderNodeBump');bp.inputs['Strength'].default_value=bump;bp.inputs['Distance'].default_value=.4
 L(mix.outputs[0],bp.inputs['Height']);L(bp.outputs['Normal'],bs.inputs['Normal'])
 if extra:extra(nt,bs)
 return m
def emissive(strength):
 def f(nt,bs):
  for k in ('Emission Color','Emission'):
   if k in bs.inputs:bs.inputs[k].default_value=(1,.75,.4,1)
  bs.inputs['Emission Strength'].default_value=strength
 return f
def water(nt,bs):
 bs.inputs['Roughness'].default_value=.05
 bs.inputs['IOR'].default_value=1.33
G_=lambda r,g,b:(r,g,b)
SPEC={
 'Grass':('noise',(.12,.25,.06),(.24,.38,.11),.9,.35,.08),'GrassLight':('noise',(.16,.29,.08),(.30,.43,.14),.9,.35,.08),
 'GrassDark':('noise',(.09,.20,.05),(.19,.32,.09),.9,.35,.08),
 'Rock':('voronoi',(.28,.27,.25),(.52,.50,.46),.8,1.2,.12),'RockDark':('voronoi',(.18,.18,.17),(.36,.35,.32),.8,1.2,.12),
 'CaveRock':('voronoi',(.12,.12,.12),(.26,.25,.24),.85,1.0,.15),'Scree':('voronoi',(.32,.30,.27),(.55,.52,.47),.85,1.0,.6),
 'Gravel':('voronoi',(.32,.31,.28),(.56,.54,.49),.9,.8,1.2),'Dirt':('noise',(.26,.19,.11),(.45,.35,.22),.95,.5,.2),
 'Sand':('noise',(.70,.60,.40),(.86,.77,.57),.95,.25,.6),'DrySand':('noise',(.80,.71,.52),(.93,.86,.68),.95,.25,.6),
 'WetSand':('noise',(.48,.43,.31),(.62,.57,.43),.5,.2,.6),'RiverBed':('voronoi',(.30,.27,.21),(.48,.44,.36),.9,.6,.5),
 'Concrete':('noise',(.50,.50,.47),(.66,.66,.62),.9,.15,.4),'Spawn':('noise',(.58,.60,.52),(.70,.72,.64),.8,.1,.4),
 'CastleStone':('voronoi',(.07,.068,.065),(.12,.115,.11),.9,.6,.4),'CastleStoneDark':('voronoi',(.04,.038,.036),(.07,.067,.064),.9,.6,.4),
 'Stone':('voronoi',(.36,.35,.32),(.52,.50,.46),.85,.6,.5),'StoneDark':('voronoi',(.24,.23,.22),(.36,.35,.32),.85,.6,.5),
 'Wood':('wave',(.32,.20,.10),(.55,.37,.20),.75,.3,.6),'WoodDark':('wave',(.16,.10,.05),(.32,.21,.12),.75,.3,.6),
 'RoofWood':('wave',(.24,.12,.07),(.44,.24,.13),.8,.3,.6),'Bark':('wave',(.15,.10,.06),(.30,.21,.13),.9,.6,.8),
 'PalmTrunk':('wave',(.36,.27,.17),(.58,.46,.31),.9,.5,1.2),
 'Leaf':('noise',(.10,.22,.07),(.22,.38,.13),.8,.4,.5),'LeafLight':('noise',(.16,.30,.09),(.32,.46,.17),.8,.4,.5),
 'Bush':('noise',(.10,.24,.07),(.22,.40,.13),.8,.4,.6),'BushLight':('noise',(.15,.30,.09),(.30,.47,.17),.8,.4,.6),
 'PalmLeaf':('noise',(.13,.32,.09),(.28,.50,.16),.7,.3,.6),'Coconut':('noise',(.20,.13,.07),(.36,.25,.14),.8,.3,1.0),
 'TallGrass':('noise',(.12,.25,.06),(.24,.40,.11),.8,.1,.5),'TallGrassDry':('noise',(.32,.32,.14),(.46,.44,.22),.8,.1,.5),
 'Iron':('noise',(.06,.06,.07),(.16,.16,.17),.4,.2,1.0),
}
for name,(kind,c1,c2,rough,bump,scale) in SPEC.items():node_mat(name,kind,c1,c2,rough,bump,scale)
node_mat('Foam','noise',(.85,.9,.92),(.97,.99,1),.4,.1,.6)
node_mat('Bone','noise',(.70,.65,.53),(.90,.86,.74),.8,.3,.8)
node_mat('BoneDark','noise',(.50,.44,.34),(.66,.60,.48),.8,.3,.8)
node_mat('Waterfall','wave',(.35,.62,.75),(.75,.90,.96),.15,.2,.25)
node_mat('Water','noise',(.02,.09,.11),(.04,.15,.18),.05,.15,.3,water)
node_mat('LanternGlow','noise',(1,.8,.5),(1,.85,.55),.5,0,.5,emissive(25))
for fl,c in [('FlowerRed',(.85,.12,.10)),('FlowerYellow',(.95,.75,.10)),('FlowerWhite',(.92,.92,.88)),('FlowerPurple',(.50,.25,.75))]:
 node_mat(fl,'noise',tuple(x*.8 for x in c),c,.6,.1,.5)

# ---------- 3. Terrain: subdivision, smooth by angle, slope displacement ----------
clouds=bpy.data.textures.new('OF_Clouds','CLOUDS');clouds.noise_scale=6;clouds.noise_depth=3
hill_info=G['hill_info'];mountain_height=G['mountain_height'];path_info=G['path_info'];plot_clearance=G['plot_clearance']
CAVES=G['CAVES'];seg_dist=G['seg_dist']
def near_cave(x,y,m=10):
 if y>G['CH_Y']-20 and abs(x-G['river_x'](y))<G['river_half'](y)+14:return True  # river channel + waterfall lip stay exact
 return any(seg_dist(x,y,a,b)<hw+m or math.hypot(x-b[0],y-b[1])<cr+m for a,b,hw,cr,fl in CAVES)
def slope_weight(x,y):
 if plot_clearance(x,y)<6 or path_info(x,y)[0]>0 or near_cave(x,y):return 0.
 h,zone=hill_info(x,y)
 if zone in (2,3,4):return 1.
 return 1. if mountain_height(x,y)>8 else 0.
if LOWPOLY:
 # One ground mesh (so decimation leaves no cracks between tiles), chunky slope detail,
 # then collapse into irregular triangles with flat shading. Edges are kept in place.
 import bmesh
 tiles=[o for n,o in objs.items() if n.startswith('Ground_')]
 with bpy.context.temp_override(active_object=tiles[0],object=tiles[0],selected_objects=tiles,selected_editable_objects=tiles):bpy.ops.object.join()
 gnd=tiles[0];gnd.name='Ground_LowPoly';objs={o.name:o for o in col.objects}
 for o in col.objects:
  if o.type=='MESH':
   for p in o.data.polygons:p.use_smooth=False
 for name,o in objs.items():
  if not (name.startswith('Ground_') or name.startswith('Cliff_') or name.startswith('CaveRoof_')):continue
  me=o.data;bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table()
  edge=[v.index for v in bm.verts if any(e.is_boundary for e in v.link_edges) or near_cave(v.co.x,v.co.y)];bm.free()  # keep cave surroundings exact so the roofs fit
  keep=o.vertex_groups.new(name='Decimate');keep.add(list(range(len(me.vertices))),1.,'REPLACE');keep.add(edge,0.,'REPLACE')
  if name.startswith('Ground_'):
   vg=o.vertex_groups.new(name='Slopes')
   for i,v in enumerate(me.vertices):
    w=slope_weight(v.co.x,v.co.y)
    if w>0:vg.add([i],w,'REPLACE')
   d=o.modifiers.new('SlopeDetail','DISPLACE');d.texture=clouds;d.strength=3.5;d.vertex_group='Slopes';d.texture_coords='GLOBAL'
  if name.startswith('CaveRoof_') or name.startswith('Cliff_'):continue  # skirt stays as built (waterfall recess)
  dm=o.modifiers.new('LowPoly','DECIMATE');dm.decimate_type='COLLAPSE';dm.ratio=.1 if name.startswith('Ground_') else .3
  dm.use_collapse_triangulate=True;dm.vertex_group='Decimate';dm.vertex_group_factor=1.
for name,o in ([] if LOWPOLY else objs.items()):
 if not (name.startswith('Ground_') or name.startswith('CaveRoof_') or name.startswith('Cliff_')):continue
 me=o.data
 try:me.set_sharp_from_angle(angle=math.radians(40))
 except Exception:pass
 for p in me.polygons:p.use_smooth=True
 sub=o.modifiers.new('Subdivision','SUBSURF');sub.levels=1;sub.render_levels=2;sub.boundary_smooth='PRESERVE_CORNERS'
 if name.startswith('Ground_') or name.startswith('CaveRoof_'):
  vg=o.vertex_groups.new(name='Slopes');ws=[slope_weight(v.co.x,v.co.y) for v in me.vertices]
  for i,w in enumerate(ws):
   if w>0:vg.add([i],w,'REPLACE')
  if any(ws):
   d=o.modifiers.new('SlopeDetail','DISPLACE');d.texture=clouds;d.strength=.6;d.vertex_group='Slopes';d.texture_coords='GLOBAL'

# Cave roofs: Blender renders both sides, so swap the doubled faces for a solid rock slab.
import bmesh
for name,o in objs.items():
 if not name.startswith('CaveRoof_'):continue
 bm=bmesh.new();bm.from_mesh(o.data);ci=[i for i,m in enumerate(o.data.materials) if m.name=='OF_CaveRock']
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in ci],context='FACES');bm.to_mesh(o.data);bm.free()
 so=o.modifiers.new('Thickness','SOLIDIFY');so.thickness=1.5;so.offset=-1
 if ci:so.material_offset=ci[0]-0  # inner/rim faces use the cave rock slot
 o.modifiers.move(len(o.modifiers)-1,0)
# ---------- 4. Bevel built objects ----------
for name,o in objs.items():
 if name in ('WoodenBridge','StonePath') or name.startswith('Lantern_') or name.startswith('Plot_') or name=='CentralSpawn':
  b=o.modifiers.new('Bevel','BEVEL');b.width=.1;b.segments=2;b.limit_method='ANGLE';b.harden_normals=False

# ---------- 5. Low-poly pine and oak trees replace the ball trees ----------
proto=bpy.data.collections.new('OF_Prototypes')  # not linked to the scene: only used as instance sources
def mesh_obj(name,verts,faces,mats,parent_col):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 for m in dict.fromkeys(mats):me.materials.append(bpy.data.materials['OF_'+m])
 names=list(dict.fromkeys(mats))
 for i,p in enumerate(me.polygons):p.material_index=names.index(mats[i]);p.use_smooth=False
 ob=bpy.data.objects.new(name,me);parent_col.objects.link(ob);return ob
def cyl(n,r0,r1,z0,z1,cx=0,cy=0,cap=True):
 v=[(cx+r0*math.cos(2*math.pi*i/n),cy+r0*math.sin(2*math.pi*i/n),z0) for i in range(n)]+[(cx+r1*math.cos(2*math.pi*i/n+.3),cy+r1*math.sin(2*math.pi*i/n+.3),z1) for i in range(n)]
 f=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 if cap:f.append(tuple(range(n-1,-1,-1)))
 if r1>0 and cap:f.append(tuple(range(n,2*n)))
 return v,f
def cone(n,r,z0,z1,jit,rnd):
 v=[(r*(1+rnd.uniform(-jit,jit))*math.cos(2*math.pi*i/n),r*(1+rnd.uniform(-jit,jit))*math.sin(2*math.pi*i/n),z0+rnd.uniform(-.4,.4)) for i in range(n)]+[(0,0,z1)]
 return v,[(i,(i+1)%n,n) for i in range(n)]+[tuple(range(n-1,-1,-1))]
def ico(r,cx,cy,cz,rnd,sz=1.):
 t=(1+5**.5)/2;base=[(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
 F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
 v=[]
 for x,y,z in base:
  l=(x*x+y*y+z*z)**.5;k=r*(1+rnd.uniform(-.12,.12))/l;v.append((cx+x*k,cy+y*k,cz+z*k*sz))
 return v,F
def merge(parts):
 V=[];F=[];M=[]
 for (v,f),m in parts:
  o=len(V);V+=v;F+=[tuple(q+o for q in fc) for fc in f];M+=[m]*len(f)
 return V,F,M
TREES=[]
for k in range(3):
 rnd=random.Random(100+k);parts=[(cyl(7,.9,.5,-1,6),'Bark')]
 for j,(r,z0,z1) in enumerate([(6.5,4,13),(5,9,17),(3.4,13.5,21)]):parts.append((cone(9,r,z0,z1,.15,rnd),'Leaf' if j%2==0 else 'LeafLight'))
 TREES.append(mesh_obj('OF_Pine_%d'%k,*merge(parts),proto))
for k in range(3):
 rnd=random.Random(200+k);parts=[(cyl(7,1.3,.8,-1,9),'Bark'),(cyl(5,.6,.3,7,11.5,2.5,0),'Bark'),(cyl(5,.6,.3,7,11,-2,1.5),'Bark')]
 for j in range(5):
  a=rnd.uniform(0,6.28);d=rnd.uniform(1.5,4)
  parts.append((ico(rnd.uniform(4,5.5),d*math.cos(a),d*math.sin(a),rnd.uniform(11,15),rnd,.85),rnd.choice(['Leaf','LeafLight'])))
 TREES.append(mesh_obj('OF_Oak_%d'%k,*merge(parts),proto))
trees_col=bpy.data.collections.new('OF_Trees');col.children.link(trees_col)
gone=[]
for name,o in list(objs.items()):
 if (name.startswith('Tree_') or name.startswith('InteriorTree_')) and name.endswith('_Trunk'):
  bb=[o.matrix_world@Vector(c) for c in o.bound_box];x=sum(v.x for v in bb)/8;y=sum(v.y for v in bb)/8;z=min(v.z for v in bb);h=max(v.z for v in bb)-z
  proto_ob=random.choice(TREES[:3] if random.random()<.45 else TREES[3:])
  t=bpy.data.objects.new(name.replace('_Trunk',''),proto_ob.data);trees_col.objects.link(t)
  t.location=(x,y,z);t.rotation_euler=(0,0,random.uniform(0,6.28));s=h/16*random.uniform(.9,1.15);t.scale=(s,s,s)
 if name.startswith('Tree_') or name.startswith('InteriorTree_'):gone.append(o)
for o in gone:bpy.data.objects.remove(o,do_unlink=True)

# ---------- 6. Geometry Nodes scatter on grass areas ----------
def scatter_proto(name,parts):return mesh_obj(name,*merge(parts),proto)
grass_col=bpy.data.collections.new('OF_ScatterGrass');proto.children.link(grass_col)
for k in range(4):
 rnd=random.Random(300+k);V=[];F=[];M=[]
 for j in range(9):
  a=rnd.uniform(0,6.28);x,y=rnd.uniform(-.5,.5),rnd.uniform(-.5,.5);h=rnd.uniform(.9,1.9);lx,ly=rnd.uniform(-.35,.35),rnd.uniform(-.35,.35);o=len(V)
  V+=[(x-.07*math.cos(a),y-.07*math.sin(a),0),(x+.07*math.cos(a),y+.07*math.sin(a),0),(x+lx,y+ly,h)];F+=[(o,o+1,o+2),(o,o+2,o+1)]
  M+=['TallGrass' if k<3 else 'TallGrassDry']*2
 grass_col.objects.link(mesh_obj('OF_GrassClump_%d'%k,V,F,M,proto));proto.objects.unlink(bpy.data.objects['OF_GrassClump_%d'%k])
flower_col=bpy.data.collections.new('OF_ScatterFlowers');proto.children.link(flower_col)
for k,fl in enumerate(['FlowerRed','FlowerYellow','FlowerWhite','FlowerPurple']):
 rnd=random.Random(400+k);parts=[]
 for j in range(4):
  x,y=rnd.uniform(-.6,.6),rnd.uniform(-.6,.6);h=rnd.uniform(.6,1.0)
  parts+=[(cyl(4,.04,.03,0,h,x,y,False),'TallGrass'),(ico(.18,x,y,h,rnd,.6),fl)]
 ob=scatter_proto('OF_Flowers_%d'%k,parts);flower_col.objects.link(ob);proto.objects.unlink(ob)
pebble_col=bpy.data.collections.new('OF_ScatterPebbles');proto.children.link(pebble_col)
for k in range(3):
 rnd=random.Random(500+k);ob=scatter_proto('OF_Pebble_%d'%k,[(ico(rnd.uniform(.3,.7),0,0,0,rnd,.55),rnd.choice(['Rock','RockDark','Scree']))]);pebble_col.objects.link(ob);proto.objects.unlink(ob)

def scatter_group():
 ng=bpy.data.node_groups.new('OF_Scatter','GeometryNodeTree');N=ng.nodes.new;L=ng.links.new
 ng.interface.new_socket('Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
 ng.interface.new_socket('Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
 gi=N('NodeGroupInput');go=N('NodeGroupOutput');join=N('GeometryNodeJoinGeometry');L(gi.outputs[0],join.inputs[0])
 sel=None
 for mname in ('Grass','GrassLight','GrassDark'):
  ms=N('GeometryNodeMaterialSelection');ms.inputs['Material'].default_value=bpy.data.materials['OF_'+mname]
  if sel is None:sel=ms.outputs[0]
  else:o=N('FunctionNodeBooleanMath');o.operation='OR';L(sel,o.inputs[0]);L(ms.outputs[0],o.inputs[1]);sel=o.outputs[0]
 for coll,density,smin,smax,seed in ((flower_col,.006,.8,1.3,2),)+(() if LOWPOLY else ((pebble_col,.01,.6,1.6,3),)):  # no grass scatter
  dp=N('GeometryNodeDistributePointsOnFaces');dp.inputs['Density'].default_value=density;dp.inputs['Seed'].default_value=seed
  L(gi.outputs[0],dp.inputs['Mesh']);L(sel,dp.inputs['Selection'])
  ci=N('GeometryNodeCollectionInfo');ci.inputs['Collection'].default_value=coll;ci.inputs['Separate Children'].default_value=True;ci.inputs['Reset Children'].default_value=True
  iop=N('GeometryNodeInstanceOnPoints');iop.inputs['Pick Instance'].default_value=True
  L(dp.outputs['Points'],iop.inputs['Points']);L(ci.outputs[0],iop.inputs['Instance'])
  rr=N('FunctionNodeRandomValue');rr.data_type='FLOAT_VECTOR';rr.inputs['Max'].default_value=(0,0,6.283);rr.inputs['Seed'].default_value=seed+10
  L(rr.outputs['Value'],iop.inputs['Rotation'])
  rs=N('FunctionNodeRandomValue');rs.data_type='FLOAT';rs.inputs[2].default_value=smin;rs.inputs[3].default_value=smax;rs.inputs['Seed'].default_value=seed+20
  L(rs.outputs[1],iop.inputs['Scale'])
  ri=N('FunctionNodeRandomValue');ri.data_type='INT';ri.inputs['Min'].default_value=0;ri.inputs['Max'].default_value=len(coll.objects)-1;ri.inputs['Seed'].default_value=seed+30
  L(ri.outputs[2],iop.inputs['Instance Index'])
  L(iop.outputs[0],join.inputs[0])
 L(join.outputs[0],go.inputs[0]);return ng
SC=scatter_group()
for name,o in objs.items():
 if (name.startswith('Ground_') or name.startswith('CaveRoof_')) and o.name in bpy.data.objects:
  gm=o.modifiers.new('Scatter','NODES');gm.node_group=SC

# ---------- 7. Sky, sun, fog, Cycles ----------
sun=bpy.data.objects['OF_Sun'];sun.rotation_euler=(math.radians(90-35),0,math.radians(-40));sun.data.energy=3.5;sun.data.angle=math.radians(1.5)
w=scene.world;w.use_nodes=True;nt=w.node_tree;nt.nodes.clear();N=nt.nodes.new;L=nt.links.new
out=N('ShaderNodeOutputWorld');bg=N('ShaderNodeBackground');sky=N('ShaderNodeTexSky')
for t in ('NISHITA','MULTIPLE_SCATTERING','SINGLE_SCATTERING'):
 try:sky.sky_type=t;break
 except TypeError:pass
try:sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(220)
except AttributeError:pass
bg.inputs['Strength'].default_value=.35;L(sky.outputs[0],bg.inputs[0]);L(bg.outputs[0],out.inputs['Surface'])
# Fog lives in a big box around the map (a world volume would block the sun and sky).
bpy.ops.mesh.primitive_cube_add(size=1,location=(60,0,140));fog=bpy.context.active_object;fog.name='OF_Fog';fog.scale=(3200,2400,400)
for c in fog.users_collection:c.objects.unlink(fog)
col.objects.link(fog);fm=bpy.data.materials.new('OF_FogVolume');fm.use_nodes=True;fnt=fm.node_tree;fnt.nodes.clear()
fo=fnt.nodes.new('ShaderNodeOutputMaterial');vs=fnt.nodes.new('ShaderNodeVolumeScatter');vs.inputs['Density'].default_value=.00006;vs.inputs['Anisotropy'].default_value=.3
fnt.links.new(vs.outputs[0],fo.inputs['Volume']);fog.data.materials.append(fm)
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=SAMPLES;scene.cycles.use_denoising=True
scene.cycles.max_bounces=6;scene.cycles.volume_step_rate=8;scene.cycles.volume_max_steps=96
scene.view_settings.view_transform='AgX' if 'AgX' in [v.identifier for v in scene.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
looks=[l.identifier for l in scene.view_settings.bl_rna.properties['look'].enum_items]
scene.view_settings.look=next((l for l in looks if 'Punchy' in l),'None');scene.view_settings.exposure=-1.8
scene.render.resolution_x,scene.render.resolution_y=RES;scene.render.resolution_percentage=100

CAMS={PREFIX+'Overview':((760,1120,760),(50,-60,0),40),PREFIX+'Bridge':((-10,470,30),(0,-60,80),60),
      PREFIX+'West':((-430,120,25),(0,-60,70),62),PREFIX+'SummitPath':((14,-40,125),(0,-150,140),60),
      PREFIX+'Tower':((95,-60,165),(0,-150,165),55),PREFIX+'TowerInside':((0,-150,127),(0,-138,143),80),
      PREFIX+'Waterfall':((95,800,10),(0,690,-30),50)}
def cam(name,loc,target,fov):
 cd=bpy.data.cameras.new(name);cd.lens_unit='FOV';cd.angle=math.radians(fov);cd.clip_end=5000
 c=bpy.data.objects.new(name,cd);col.objects.link(c);c.location=loc
 c.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();return c
cams={n:cam(n,*v) for n,v in CAMS.items()}
for kind,fx,fy,R,rot in G.get('FOSSILS',[]):  # one close-up camera per fossil
 a=math.radians(rot+120);gz=G['height'](fx,fy)
 cams[PREFIX+'Fossil_'+kind]=cam(PREFIX+'Fossil_'+kind,(fx+R*1.25*math.cos(a),fy+R*1.25*math.sin(a),gz+R*.55),(fx,fy,gz+3),55)
if 'OF_Overview' in bpy.data.objects:bpy.data.objects.remove(bpy.data.objects['OF_Overview'],do_unlink=True)
scene.camera=cams[PREFIX+'Overview']
BLEND='OreFactory_LowPoly.blend' if LOWPOLY else 'OreFactory_HQ.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/BLEND),compress=True)
print('Saved',BLEND)
if '--render' in args:
 for n,c in cams.items():
  if ONLY and n!=ONLY:continue
  scene.camera=c;scene.render.filepath=str(HERE/(n+'.png'));bpy.ops.render.render(write_still=True);print('Rendered',n)
