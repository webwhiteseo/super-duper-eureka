"""Software preview of the exact OreFactory mesh data (mesh_scene.json).
Smooth shading (normals smoothed by angle), sun shadows, distance fog, ortho overviews
and two player-height perspective views. Needs Python, NumPy and Pillow; not needed by Blender."""
import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
scene=json.loads((P/'mesh_scene.json').read_text())
mats={'Grass':(.38,.53,.27),'GrassLight':(.41,.555,.285),'GrassDark':(.345,.495,.245),'Rock':(.50,.50,.46),'RockDark':(.38,.38,.36),
 'Sand':(.85,.76,.55),'Concrete':(.67,.68,.64),'Bark':(.34,.25,.16),'Leaf':(.25,.41,.21),'LeafLight':(.36,.49,.26),'Spawn':(.72,.75,.65),
 'DrySand':(.91,.83,.64),'WetSand':(.71,.66,.51),'CaveRock':(.33,.33,.32),'RiverBed':(.55,.50,.41),'Water':(.30,.60,.70),
 'Wood':(.58,.40,.24),'WoodDark':(.36,.24,.14),'Iron':(.2,.2,.21),'LanternGlow':(1.0,.85,.5),'Bush':(.26,.45,.20),'BushLight':(.34,.53,.23),
 'TallGrass':(.46,.62,.28),'TallGrassDry':(.64,.66,.34),'FlowerRed':(.90,.28,.25),'FlowerYellow':(.98,.84,.26),'FlowerWhite':(.97,.96,.92),
 'FlowerPurple':(.64,.44,.86),'PalmTrunk':(.60,.47,.31),'PalmLeaf':(.30,.58,.24),'Coconut':(.40,.28,.16),'Dirt':(.52,.42,.29),'Scree':(.56,.54,.50),'Stone':(.62,.61,.57),'StoneDark':(.48,.47,.44),'Gravel':(.55,.53,.49),'RoofWood':(.46,.26,.16),'RoofTile':(.50,.16,.12),'Banner':(.65,.09,.09),'Gold':(.92,.72,.22)}
SUN=np.array([-.55,-.45,.7]);SUN/=np.linalg.norm(SUN)
FOG=np.array([.80,.85,.86]);SKY_TOP=np.array([.55,.70,.86]);SKY_LOW=np.array([.83,.88,.90])
W,H=1600,1180;font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

# ---------- geometry: triangles with per-corner normals ----------
def tri_soup(objs,smooth,split=False,angle=55):
 """Returns world corners (T,3,3), corner normals (T,3,3), material ids (T,)."""
 V=[];F=[];M=[]
 for ob in objs:
  vs=np.array(ob['v'],float);o=sum(len(v) for v in V);V.append(vs)
  for i,f in enumerate(ob['f']):
   mat=ob['mat'][i] if isinstance(ob['mat'],list) else ob['mat']
   for k in range(1,len(f)-1):F.append((f[0]+o,f[k]+o,f[k+1]+o));M.append(mat)
 V=np.concatenate(V);F=np.array(F);tri=V[F]
 fn=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(fn,axis=1);ok=area>1e-9
 tri,fn,F,M=tri[ok],fn[ok],F[ok],[m for m,k in zip(M,ok) if k];fu=fn/np.linalg.norm(fn,axis=1)[:,None]
 if not smooth:return tri,np.repeat(fu[:,None,:],3,1),M
 key=np.round(V,3)
 if split:key=np.concatenate([key[F.reshape(-1)],np.repeat(fu[:,2]>=0,3)[:,None]],1)
 else:key=key[F.reshape(-1)]
 _,inv=np.unique(key,axis=0,return_inverse=True);inv=inv.reshape(-1)
 acc=np.zeros((inv.max()+1,3));np.add.at(acc,inv,np.repeat(fn,3,0))
 vn=acc[inv].reshape(-1,3,3);vn/=np.maximum(np.linalg.norm(vn,axis=2,keepdims=True),1e-9)
 sharp=(vn*fu[:,None,:]).sum(2)<math.cos(math.radians(angle))
 vn[sharp]=np.repeat(fu[:,None,:],3,1)[sharp]
 return tri,vn,M
parts=[]
ground=[o for o in scene if o['name'].startswith('Ground_')]
parts.append(tri_soup(ground,True))
for o in scene:
 if o['name'].startswith('Ground_'):continue
 parts.append(tri_soup([o],o['smooth'],split=o['name'].startswith('CaveRoof')))
TRI=np.concatenate([p[0] for p in parts]);NRM=np.concatenate([p[1] for p in parts]);MAT=sum((p[2] for p in parts),[])
COL=np.array([mats[m] for m in MAT]);GLOW=np.array([m=='LanternGlow' for m in MAT])
CULL=np.array([False]*len(MAT))
o=0
for p,ob in zip(parts,[None]+[x for x in scene if not x['name'].startswith('Ground_')]):
 if ob is not None and ob['name'].startswith('CaveRoof'):CULL[o:o+len(p[2])]=True
 o+=len(p[2])
print('triangles',len(TRI))

# ---------- rasteriser ----------
def raster(sp,w,h,on_pixel):
 """sp: (T,3,3) screen x,y,depth. Calls on_pixel(i,ys,xs,b1,b2,b3) for covered pixels."""
 for i in range(len(sp)):
  a,b,c=sp[i]
  x0=max(0,int(min(a[0],b[0],c[0])));x1=min(w-1,int(max(a[0],b[0],c[0]))+1)
  y0=max(0,int(min(a[1],b[1],c[1])));y1=min(h-1,int(max(a[1],b[1],c[1]))+1)
  if x1<x0 or y1<y0:continue
  den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-9:continue
  yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
  w1=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;w2=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w3=1-w1-w2
  m=(w1>=-1e-6)&(w2>=-1e-6)&(w3>=-1e-6)
  if m.any():on_pixel(i,yy[m].astype(int),xx[m].astype(int),w1[m],w2[m],w3[m])

# Shadow map along the sun direction (orthographic), covering the whole map.
SR=2400
sd=SUN;sr=np.cross([0,0,1.],sd);sr/=np.linalg.norm(sr);su=np.cross(sd,sr)
lp=np.stack([TRI@sr,TRI@su,TRI@sd],-1);mn=lp[...,:2].reshape(-1,2).min(0);mx=lp[...,:2].reshape(-1,2).max(0)
sscale=(SR-4)/max(mx-mn);lsp=lp.copy();lsp[...,0]=(lp[...,0]-mn[0])*sscale+2;lsp[...,1]=(lp[...,1]-mn[1])*sscale+2
SMAP=np.full((SR,SR),-1e9,np.float32)
def sh_pix(i,ys,xs,b1,b2,b3):
 z=b1*lsp[i,0,2]+b2*lsp[i,1,2]+b3*lsp[i,2,2];cur=SMAP[ys,xs];k=z>cur
 SMAP[ys[k],xs[k]]=z[k]
raster(lsp,SR,SR,sh_pix)
def lit_fraction(wp):
 x=(wp@sr-mn[0])*sscale+2;y=(wp@su-mn[1])*sscale+2;z=wp@sd;acc=np.zeros(len(wp))
 for dx in (-1,0,1):
  for dy in (-1,0,1):
   xi=np.clip((x+dx).astype(int),0,SR-1);yi=np.clip((y+dy).astype(int),0,SR-1)
   acc+=SMAP[yi,xi]<=z+1.2
 return acc/9

def render(name,mode,region=None,view=None,cam=None,caption=''):
 if mode=='persp':
  C=np.array(cam[0],float);T=np.array(cam[1],float);f=T-C;f/=np.linalg.norm(f)
  r=np.cross(f,[0,0,1.]);r/=np.linalg.norm(r);u=np.cross(r,f);foc=W/2/math.tan(math.radians(cam[2])/2)
  rel=TRI-C;zc=rel@f;keep=(zc>1.).all(1)
  sp=np.stack([(rel@r)/np.maximum(zc,1e-3)*foc+W/2,-(rel@u)/np.maximum(zc,1e-3)*foc+H/2,-zc],-1)
 else:
  if mode=='top':d=np.array([0,0,1.]);r=np.array([1.,0,0]);u=np.array([0,-1.,0])
  else:d=np.array(view,float);d/=np.linalg.norm(d);r=np.array([d[1],-d[0],0]);r/=np.linalg.norm(r);u=np.cross(r,d)
  pts=TRI.reshape(-1,3)
  if region:pts=pts[(pts[:,0]>region[0])&(pts[:,0]<region[1])&(pts[:,1]>region[2])&(pts[:,1]<region[3])]
  pr=np.stack([pts@r,pts@u],1);lo,hi=pr.min(0),pr.max(0);scale=min((W-130)/(hi[0]-lo[0]),(H-270)/(hi[1]-lo[1]));mid=(lo+hi)/2
  sp=np.stack([(TRI@r-mid[0])*scale+W/2,-(TRI@u-mid[1])*scale+H/2+5,TRI@d],-1);keep=np.ones(len(TRI),bool)
  f=-d
 # back-face cull double-sided roofs only
 fn=np.cross(TRI[:,1]-TRI[:,0],TRI[:,2]-TRI[:,0]);vdir=(TRI.mean(1)-C) if mode=='persp' else np.repeat(f[None],len(TRI),0)
 keep&=~(CULL&((fn*vdir).sum(1)>=0))
 idx=np.nonzero(keep)[0]
 Z=np.full((H,W),-1e18);ID=np.full((H,W),-1,int);B=np.zeros((H,W,3),np.float32)
 spk=sp[idx]
 def pix(j,ys,xs,b1,b2,b3):
  z=b1*spk[j,0,2]+b2*spk[j,1,2]+b3*spk[j,2,2];k=z>Z[ys,xs]
  if k.any():ys,xs=ys[k],xs[k];Z[ys,xs]=z[k];ID[ys,xs]=idx[j];B[ys,xs]=np.stack([b1[k],b2[k],b3[k]],1)
 raster(spk,W,H,pix)
 # deferred shading
 m=ID>=0;ids=ID[m];bw=B[m][...,None]
 wp=(TRI[ids]*bw).sum(1);n=(NRM[ids]*bw).sum(1);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-9)
 viewdir=(C-wp) if mode=='persp' else np.repeat(-f[None],len(wp),0)
 n[(n*viewdir).sum(1)<0]*=-1  # thin double-sided leaves/grass
 dif=np.clip(n@SUN,0,1);lit=lit_fraction(wp+n*.4);sky=.5+.5*n[:,2]
 c=COL[ids]*(.30*sky[:,None]+.95*(dif*lit)[:,None])
 c[GLOW[ids]]=COL[ids][GLOW[ids]]*1.1
 if mode=='persp':
  dist=np.linalg.norm(wp-C,axis=1);fg=1-np.exp(-dist/900);c=c*(1-fg[:,None])+FOG*fg[:,None]
  gy=np.linspace(0,1,H)[:,None,None];img=SKY_TOP*(1-gy)+SKY_LOW*gy;img=np.repeat(img,W,1).astype(np.float32)
 else:
  if mode!='top':
   dd=(wp@(-f));lo_,hi_=dd.min(),dd.max();fg=.45*(1-np.clip((dd-lo_)/(hi_-lo_),0,1))**1.4;c=c*(1-fg[:,None])+FOG*fg[:,None]
  img=np.zeros((H,W,3),np.float32);img[:]=np.array([232,236,229])/255
 img[m]=c;img=(np.clip(img,0,1)**(1/1.08)*255).astype(np.uint8)
 im=Image.fromarray(img);dr=ImageDraw.Draw(im)
 if mode=='persp':
  dr.rectangle((0,H-70,W,H),fill=(232,236,229))
  dr.text((W/2,H-46),caption,font=ImageFont.truetype(font,21),fill='#4d6149',anchor='mm')
  dr.text((W/2,H-18),'Preview of the exact mesh data (software render, not Blender or Roblox).',font=ImageFont.truetype(font,15),fill='#63705f',anchor='mm')
 else:
  dr.rectangle((0,0,W,88),fill=(232,236,229));dr.rectangle((0,H-110,W,H),fill=(232,236,229))
  dr.text((W/2,44),'ORE FACTORY / SMOOTH TERRAIN',font=ImageFont.truetype(font,32),fill='#30432f',anchor='mm')
  dr.text((W/2,H-76),caption,font=ImageFont.truetype(font,21),fill='#4d6149',anchor='mm')
  dr.text((W/2,H-39),'Geometry preview from the Blender script; not a Blender render. Import and play-testing still required.',font=ImageFont.truetype(font,16),fill='#63705f',anchor='mm')
 im.save(P/(name+'.png'));print(name)

render('OreFactory_PlayerView_Front','persp',cam=((-8,268,18),(0,-25,30),58),caption='Player view from the bridge: centre hill (cave + ledge route) with the tall hill behind')
render('OreFactory_PlayerView_Path','persp',cam=((14,4,52),(0,-70,64),60),caption='From the centre-hill top: stone path up to the lookout tower')
render('OreFactory_PlayerView_West','persp',cam=((-205,70,14),(0,-35,30),62),caption='Player view from the west: centre-hill ramp, tall-hill cliff with its ledge route')
render('OreFactory_Hills','ortho',region=(-130,130,-170,90),view=(.62,.42,.42),caption='Twin hills from the east: rounded shoulders, spurs and gullies, cliff with scree')
render('OreFactory_3D_Preview','ortho',view=(.27,.76,.66),caption='Twin hills • River + bridge • Cave lanterns • Flowers and grass • Beach palms • Fog')
render('OreFactory_Blender_TopDown','top',caption='Top-down layout')
