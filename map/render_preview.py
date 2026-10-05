import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
scene=json.loads((P/'mesh_scene.json').read_text())
mats={'Grass':(.38,.53,.27),'GrassLight':(.42,.57,.30),'Rock':(.46,.48,.43),'Sand':(.85,.76,.55),'Concrete':(.67,.68,.64),'Bark':(.34,.25,.16),'Leaf':(.25,.41,.21),'LeafLight':(.36,.49,.26),'Spawn':(.72,.75,.65)}
mats.update({'DrySand':(.91,.83,.64),'WetSand':(.71,.66,.51),'CaveRock':(.33,.33,.32),'RiverBed':(.55,.50,.41),'Water':(.30,.60,.70)})
mats.update({'Wood':(.58,.40,.24),'WoodDark':(.36,.24,.14),'Iron':(.2,.2,.21),'LanternGlow':(1.0,.85,.5),'Bush':(.26,.45,.20),'BushLight':(.34,.53,.23),
 'TallGrass':(.46,.62,.28),'TallGrassDry':(.64,.66,.34),'FlowerRed':(.90,.28,.25),'FlowerYellow':(.98,.84,.26),'FlowerWhite':(.97,.96,.92),'FlowerPurple':(.64,.44,.86),
 'PalmTrunk':(.60,.47,.31),'PalmLeaf':(.30,.58,.24),'Coconut':(.40,.28,.16)})
FOG=np.array([.80,.85,.84])
W,H=1600,1180
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for name,top,region in [('OreFactory_3D_Preview',False,None),('OreFactory_Blender_TopDown',True,None),('OreFactory_CloseUp',False,(-95,95,-185,235))]:
 if top:r=np.array([1.,0,0]);u=np.array([0.,-1,0]);d=np.array([0.,0,1])
 else:
  d=np.array([.27,.76,.66]);d/=np.linalg.norm(d);r=np.array([d[1],-d[0],0]);r/=np.linalg.norm(r);u=np.cross(r,d)
 allv=np.concatenate([np.array(o['v']) for o in scene])
 if region:allv=allv[(allv[:,0]>region[0])&(allv[:,0]<region[1])&(allv[:,1]>region[2])&(allv[:,1]<region[3])]
 proj=np.stack([allv@r,allv@u],axis=1);dmin,dmax=(allv@d).min(),(allv@d).max()
 mn=proj.min(axis=0);mx=proj.max(axis=0);scale=min((W-130)/(mx[0]-mn[0]),(H-270)/(mx[1]-mn[1]));mid=(mn+mx)/2
 pix=np.zeros((H,W,3),dtype=np.uint8);pix[:]=[232,236,229];depth=np.full((H,W),-1e9,dtype=np.float32)
 light=np.array([-.55,-.45,.7]);light/=np.linalg.norm(light)
 for ob in scene:
  vs=np.array(ob['v']);ps=np.stack([(vs@r-mid[0])*scale+W/2,-(vs@u-mid[1])*scale+H/2+5,vs@d],axis=1)
  for fi,f in enumerate(ob['f']):
   mat=ob['mat'][fi] if isinstance(ob['mat'],list) else ob['mat']
   for k in range(1,len(f)-1):
    ids=[f[0],f[k],f[k+1]];v=vs[ids];t=ps[ids]
    normal=np.cross(v[1]-v[0],v[2]-v[0]);norm=np.linalg.norm(normal)
    if norm<1e-7:continue
    normal/=norm
    if ob['name'].startswith('CaveRoof') and normal@d<=0:continue
    shade=1. if mat=='LanternGlow' else .42+.58*max(0,float(normal@light))
    c=np.array(mats[mat])*shade
    if not top:fg=.5*(1-np.clip((float(v.mean(axis=0)@d)-dmin)/(dmax-dmin),0,1))**1.4;c=c*(1-fg)+FOG*fg
    color=np.clip(c*255,0,255).astype(np.uint8)
    x0=max(0,int(np.floor(t[:,0].min())));x1=min(W-1,int(np.ceil(t[:,0].max())));y0=max(0,int(np.floor(t[:,1].min())));y1=min(H-1,int(np.ceil(t[:,1].max())))
    if x1<x0 or y1<y0:continue
    a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-8:continue
    yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
    w1=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
    w2=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w3=1-w1-w2
    zz=w1*a[2]+w2*b[2]+w3*c[2];view=depth[y0:y1+1,x0:x1+1]
    mask=(w1>=-1e-5)&(w2>=-1e-5)&(w3>=-1e-5)&(zz>view)
    view[mask]=zz[mask];pix[y0:y1+1,x0:x1+1][mask]=color
 img=Image.fromarray(pix);draw=ImageDraw.Draw(img)
 draw.rectangle((0,0,W,88),fill=(232,236,229));draw.rectangle((0,H-110,W,H),fill=(232,236,229))
 draw.text((W/2,44),'ORE FACTORY / SMOOTH TERRAIN',font=ImageFont.truetype(font,32),fill='#30432f',anchor='mm')
 draw.text((W/2,H-76),{'OreFactory_CloseUp':'Twin hills • River cave • Wooden bridge • Lanterns • Flowers, bushes and tall grass'}.get(name,'Twin hills • River + bridge • Cave lanterns • Flowers and grass • Beach palms • Fog'),font=ImageFont.truetype(font,21),fill='#4d6149',anchor='mm')
 draw.text((W/2,H-39),'Geometry preview from the Blender script; not a Blender render. Import and play-testing still required.',font=ImageFont.truetype(font,16),fill='#63705f',anchor='mm')
 img.save(P/(name+'.png'));print(name)
