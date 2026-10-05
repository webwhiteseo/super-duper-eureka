"""Roblox export of the low-poly Ore Factory map.
Builds the low-poly Blender scene (blender_hq.py --lowpoly), applies all modifiers, splits every
object by material (names end in _<Material>), cuts the ground into chunks under 10k triangles,
and writes OreFactory_Roblox.fbx (1 unit = 1 stud). Apply colours/materials in Studio with
RobloxSetup.lua.   Run:  python3 export_roblox.py
"""
import bpy,bmesh,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.argv=[sys.argv[0],'--lowpoly']
G={'__file__':str(HERE/'blender_hq.py'),'__name__':'__main__'}
src=(HERE/'blender_hq.py').read_text().replace("bpy.ops.wm.save_as_mainfile(filepath=str(HERE/BLEND),compress=True)","pass")
exec(compile(src,'blender_hq.py','exec'),G)
scene=bpy.context.scene
# Drop render-only things: fog box, cameras, lights, flower scatter.
for o in list(scene.objects):
 if o.type in ('CAMERA','LIGHT') or o.name=='OF_Fog':bpy.data.objects.remove(o,do_unlink=True)
for o in scene.objects:
 for m in list(o.modifiers):
  if m.type=='NODES':o.modifiers.remove(m)
# Apply modifiers (decimate, displace, solidify) and make instanced trees real meshes.
dg=bpy.context.evaluated_depsgraph_get();meshes=[]
for o in list(scene.objects):
 if o.type!='MESH':continue
 me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg)
 me.transform(o.matrix_world);meshes.append((o.name,me))
for o in list(scene.objects):bpy.data.objects.remove(o,do_unlink=True)
out=bpy.data.collections.new('OreFactory_Roblox');scene.collection.children.link(out)
MAXTRI=10000;count=0;tris=0
def emit(name,bm):
 global count,tris
 if not bm.faces:return
 bmesh.ops.triangulate(bm,faces=bm.faces[:])
 me=bpy.data.meshes.new(name);bm.to_mesh(me)
 for p in me.polygons:p.use_smooth=False
 o=bpy.data.objects.new(name,me);out.objects.link(o);count+=1;tris+=len(me.polygons)
for name,me in meshes:
 mats=[m.name.replace('OF_','') if m else 'Default' for m in me.materials] or ['Default']
 bm=bmesh.new();bm.from_mesh(me)
 groups={}
 for f in bm.faces:groups.setdefault(mats[f.material_index] if f.material_index<len(mats) else 'Default',[]).append(f.index)
 for mat,idx in groups.items():
  sub=bm.copy();sub.faces.ensure_lookup_table();keep=set(idx)
  bmesh.ops.delete(sub,geom=[f for f in sub.faces if f.index not in keep],context='FACES')
  if len(sub.faces)<=MAXTRI//2:emit('%s_%s'%(name,mat),sub);continue
  # big pieces (ground): cut into grid chunks by face centre
  cell=256 if len(sub.faces)>MAXTRI*2 else 512;chunks={}
  for f in sub.faces:
   c=f.calc_center_median();chunks.setdefault((int(c.x//cell),int(c.y//cell)),[]).append(f.index)
  for (cx,cy),ci in chunks.items():
   part=sub.copy();part.faces.ensure_lookup_table();k=set(ci)
   bmesh.ops.delete(part,geom=[f for f in part.faces if f.index not in k],context='FACES')
   emit('%s_%d_%d_%s'%(name,cx,cy,mat),part)
  sub.free()
 bm.free()
big=[o.name for o in out.objects if len(o.data.polygons)>20000]
print('Parts',count,'triangles',tris,'over 20k:',big)
bpy.ops.export_scene.fbx(filepath=str(HERE/'OreFactory_Roblox.fbx'),use_selection=False,object_types={'MESH'},
 apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',global_scale=1.0,axis_forward='-Z',axis_up='Y',
 mesh_smooth_type='FACE',use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=False,path_mode='STRIP')
print('Wrote OreFactory_Roblox.fbx')
