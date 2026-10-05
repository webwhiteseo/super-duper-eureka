"""Run in Blender's Scripting workspace. Builds a separate collection; preserves other objects.
Without bpy, exports the identical mesh geometry to OBJ and renders a geometry preview.
One Blender unit equals one Roblox stud. Save your .blend after running.
"""
import math, random, os
from pathlib import Path
TAU=math.tau
OUT=Path(__file__).resolve().parent if '__file__' in globals() else Path.home()/'OreFactory_Blender'
OUT.mkdir(parents=True,exist_ok=True)
LAND=[(0,0,990,690),(-310,-100,450,440),(285,82,560,465),(-135,208,540,300),(165,-214,540,300)]
PLOTS=[(-155,-195,-5),(155,-211,9),(355,15,69),(162,204,-8),(-165,188,7),(-359,-12,-77)]
MATS={'Grass':(.32,.47,.22),'GrassLight':(.37,.52,.26),'Rock':(.38,.41,.36),'Sand':(.79,.70,.49),'Concrete':(.59,.60,.56),'Bark':(.28,.19,.12),'Leaf':(.19,.34,.17),'LeafLight':(.29,.43,.21),'Spawn':(.62,.65,.56)}
MATS.update({'DrySand':(.88,.79,.60),'WetSand':(.64,.60,.44),'CaveRock':(.27,.27,.26),'RiverBed':(.47,.43,.35),'Water':(.22,.52,.62)})
MATS.update({'Wood':(.50,.34,.20),'WoodDark':(.30,.20,.12),'Iron':(.16,.16,.17),'LanternGlow':(1.0,.78,.42),'Bush':(.22,.40,.17),'BushLight':(.30,.48,.20),
 'TallGrass':(.40,.56,.24),'TallGrassDry':(.58,.60,.30),'FlowerRed':(.86,.24,.22),'FlowerYellow':(.96,.80,.22),'FlowerWhite':(.94,.93,.88),'FlowerPurple':(.58,.38,.80),
 'PalmTrunk':(.55,.42,.27),'PalmLeaf':(.25,.52,.20),'Coconut':(.35,.24,.13)})
SCENE=[];random.seed(37)
def boundary(a):
 c,s=math.cos(a),math.sin(a);roots=[]
 for x,y,w,d in LAND:
  rx,ry=w/2,d/2;A=(c/rx)**2+(s/ry)**2;B=-2*(x*c/rx**2+y*s/ry**2);C=(x/rx)**2+(y/ry)**2-1
  disc=B*B-4*A*C
  if disc>=0:roots.append((-B+math.sqrt(disc))/(2*A))
 return max(roots)
def smooth_boundary(a):
 return sum(boundary(a+q*.0075) for q in range(-4,5))/9 + 115*max(0,math.cos(a))**4
BEACH_ANGLE=.55
# Sand is 30% wider than the previous version and has no water.
RINNER=335
BEACH_HALF=0.07358036935329436*2.5*1.3

def beach(x,y):
 a=math.atan2(y,x); da=(a-BEACH_ANGLE+math.pi)%TAU-math.pi
 if abs(da)>BEACH_HALF:return False
 inner=RINNER+9*math.cos(da/BEACH_HALF*math.pi)
 return math.hypot(x,y)>inner

def plot_clearance(x,y):
 out=1e9
 for px,py,deg in PLOTS:
  a=math.radians(deg);dx,dy=x-px,y-py
  xx=math.cos(a)*dx-math.sin(a)*dy;yy=math.sin(a)*dx+math.cos(a)*dy
  out=min(out,math.hypot(max(abs(xx)-77,0),max(abs(yy)-77,0)))
 return out
HILLS=[]
for i in range(23):
 a=i*TAU/23+.06*math.sin(i*2.6);r=smooth_boundary(a)-45;x,y=r*math.cos(a),r*math.sin(a)
 if plot_clearance(x,y)>32 and not beach(x,y):HILLS.append((x,y,random.uniform(13,30),random.uniform(24,42)))
HILLS.extend([(-48,-175,6,24),(-215,63,7,31),(215,-82,8,32)])
def ss(t):t=min(1,max(0,t));return t*t*(3-2*t)
# Twin hills. The tall hill (30% higher) sits half inside the centre hill, behind it.
# Each hill: flat top, a long walkable ramp on one side, an uneven rock cliff on the other.
# Most of each cliff is two tall drops (too high to jump); one gully is a staircase of ~5-stud
# ledges that players can jump up. Other sides are steady slopes.
# (name, centre, height, top radius, ramp dir, ramp length, side-slope length, cliff dir, gully dir, phase)
SMALL_H=36
HILL_DEFS=[('Centre',(0,0),SMALL_H,26,180,80,56,0,32,.4),
           ('Tall',(0,-62),SMALL_H*1.3,18,0,90,72,180,206,2.1)]
SMALL_TOP=26
# Mountains on the left and right sides: (x, y, height, spread).
MOUNTAINS=[(592,48,78,52),(492,-214,62,46),(-420,-212,66,48),(-386,186,56,44)]
# River runs from the front edge (+Y) into a walk-in cave in the centre hill.
def river_x(y):return 10*math.sin((y-70)/46)*ss((y-70)/40)
def river_half(y):return 5+4*ss((y-80)/22)
# Walk-in caves: mouth, chamber centre, half width, chamber radius, floor height.
CAVES=[((0,98),(0,4),12,17,0.)]
def base_height(x,y):
 r=math.hypot(x,y);a=math.atan2(y,x)
 central=min(1,max(0,(r-45)/50))
 h=sum(amp*math.exp(-((x-hx)**2+(y-hy)**2)/(2*w*w)) for hx,hy,amp,w in HILLS)
 h+=1.5*(math.sin(x*.018)*math.cos(y*.02)+1)
 h*=central
 da=abs((a-BEACH_ANGLE+math.pi)%TAU-math.pi)
 blend=max(0,1-max(0,da-BEACH_HALF)/.075)
 if r>RINNER-18 and blend>0:
  t=min(1,max(0,(r-RINNER)/(smooth_boundary(a)-RINNER)))
  h=h*(1-blend)-14*(t*t*(3-2*t))*blend
 return h
def mountain_height(x,y):
 h=0
 for mx,my,amp,s in MOUNTAINS:
  d2=(x-mx)**2+(y-my)**2;a=math.atan2(y-my,x-mx)
  n=d2/(d2+s*s)  # noise fades out at the peak so it stays smooth
  h+=amp*math.exp(-d2/(2*s*s))*(1+n*(.13*math.sin(a*3+mx)+.07*math.sin(a*7+my)))
 return h
def angdiff(a,b):return abs((a-b+180)%360-180)
def stairs(t,n,w=.3):
 # n flat ledges; each drop takes the last w of its step, so ledges stay level.
 u=min(max(t,0),.9999)*n;i=math.floor(u);return (i+ss((u-i-(1-w))/w))/n
def hill_shape(x,y,hd):
 """Height of one hill and its outer footprint radius in this direction."""
 name,(cx,cy),H,top,ramp,ramp_len,side_len,cliff,gully,ph=hd
 dx,dy=x-cx,y-cy;r=math.hypot(dx,dy);th=math.degrees(math.atan2(dy,dx));tr=math.radians(th)
 rt=top+1.6*math.sin(5*tr+ph)+1.0*math.sin(11*tr+2*ph)
 wr=max(0,math.cos(math.radians(angdiff(th,ramp))))**2
 wc=max(0,math.cos(math.radians(angdiff(th,cliff))))**2;k=ss((wc-.35)/.3)
 L=side_len+(ramp_len-side_len)*wr
 t=max(0,(r-rt)/L);smooth=1-(.6*min(t,1)+.4*ss(t))
 g=ss(1-angdiff(th,gully)/14);n_g=max(3,round(H/5.2))
 Lc=14+2.5*math.sin(7*tr+ph)+(n_g*6-14)*g;n=n_g if g>.5 else 2
 tc=(r-rt)/Lc+.05*math.sin(9*tr+ph)+.03*math.sin(17*tr+3*ph)
 cliffp=1-stairs(tc,n) if r>rt else 1.
 p=smooth*(1-k)+cliffp*k
 return H*max(0,p),rt+L*(1-k)+Lc*k
def hill_height(x,y):return max(hill_shape(x,y,hd)[0] for hd in HILL_DEFS)
def on_hill(x,y,margin=0):
 for hd in HILL_DEFS:
  h,foot=hill_shape(x,y,hd)
  if math.hypot(x-hd[1][0],y-hd[1][1])<foot+margin:return True
 return False
def feature_height(x,y):return hill_height(x,y)
for mx,my,amp,s in MOUNTAINS:
 d=math.hypot(mx,my);ux,uy=-mx/d,-my/d
 mouth=(mx+ux*s*1.95,my+uy*s*1.95);floor=base_height(*mouth)
 CAVES.append((mouth,(mx+ux*s*.15,my+uy*s*.15),8,15,floor))
def seg_dist(x,y,a,b):
 ax,ay=a;bx,by=b;vx,vy=bx-ax,by-ay;t=max(0,min(1,((x-ax)*vx+(y-ay)*vy)/(vx*vx+vy*vy)))
 return math.hypot(x-ax-t*vx,y-ay-t*vy)
def cave_mask(x,y,c):
 a,b,hw,cr,floor=c;inside=min(seg_dist(x,y,a,b)-hw,math.hypot(x-b[0],y-b[1])-cr)
 return 1-ss(inside/3)
def river_profile(x,y):
 if y<4:return max(0,1-ss((math.hypot(x,y-4)-7)/3))
 d=abs(x-river_x(y));w=river_half(y)
 return max(1-ss((d-w+3)/3),1-ss((math.hypot(x,y-4)-7)/3))
def terrain(x,y):
 """Returns carved height, uncarved height, mountain height, cave index or -1, river profile, hill height."""
 fade=min(1,plot_clearance(x,y)/22);fade=fade*fade*(3-2*fade)
 m=mountain_height(x,y);hf=feature_height(x,y)
 orig=(base_height(x,y)+hf+m)*fade
 h=orig;cave=-1
 if y>60:
  d=abs(x-river_x(y));v=(1-ss((d-river_half(y)-2)/14))*ss((math.hypot(x,y)-70)/12)
  h=h*(1-v)
 for i,c in enumerate(CAVES):
  k=cave_mask(x,y,c)
  if k>0:
   h=h*(1-k)+c[4]*k
   if k>.5:cave=i
 rp=river_profile(x,y) if y>-14 and abs(x)<60 else 0
 if rp>0:h=min(h,-5*rp)
 return h,orig,m,cave,rp,hf*fade
def height(x,y):return terrain(x,y)[0]
def mesh(name,verts,faces,mat,smooth=False):
 SCENE.append(dict(name=name,v=verts,f=faces,mat=mat,smooth=smooth))
def box(name,x,y,z,sx,sy,sz,deg,mat):
 a=math.radians(deg);v=[]
 for zz in [-sz/2,sz/2]:
  for dx,dy in [(-sx/2,-sy/2),(sx/2,-sy/2),(sx/2,sy/2),(-sx/2,sy/2)]:v.append((x+math.cos(a)*dx+math.sin(a)*dy,y-math.sin(a)*dx+math.cos(a)*dy,z+zz))
 mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
def ellipsoid(name,x,y,z,sx,sy,sz,mat,segments=9,rings=5):
 v=[]
 for j in range(rings+1):
  p=math.pi*j/rings
  for i in range(segments):
   a=TAU*i/segments;v.append((x+sx*math.sin(p)*math.cos(a),y+sy*math.sin(p)*math.sin(a),z+sz*math.cos(p)))
 f=[]
 for j in range(rings):
  for i in range(segments):f.append(((j+1)*segments+i,(j+1)*segments+(i+1)%segments,j*segments+(i+1)%segments,j*segments+i))
 mesh(name,v,f,mat)
# Ground: 2-stud grid around the hills (sharp cliffs and ledges), 4-stud elsewhere,
# split into 128-stud tiles (under 8,200 triangles each).
# Edge vertices are pulled onto the coastline; hills, river and caves are carved into it.
TILE=128
xs=list(range(-560,-110,4))+list(range(-110,130,2))+list(range(130,704,4))
ys=list(range(-400,-170,4))+list(range(-170,110,2))+list(range(110,404,4))
CELLS=[(xs[i],xs[i+1],ys[j],ys[j+1]) for i in range(len(xs)-1) for j in range(len(ys)-1)]
V={}
for gx in xs:
 for gy in ys:
  a=math.atan2(gy,gx);rb=smooth_boundary(a);r=math.hypot(gx,gy);out=r>rb
  x,y=(gx*rb/r,gy*rb/r) if out else (gx,gy)
  V[gx,gy]=(x,y,out)+terrain(x,y)
def ground_mat(c,size):
 x=sum(p[0] for p in c)/4;y=sum(p[1] for p in c)/4
 if any(p[6]>=0 for p in c):return 'CaveRock'
 if max(p[7] for p in c)>.3:return 'RiverBed'
 slope=(max(p[3] for p in c)-min(p[3] for p in c))/size
 if max(p[5] for p in c)>18 and slope>.75:return 'Rock'
 if max(p[8] for p in c)>3 and slope>1.1:return 'Rock'
 a=math.atan2(y,x);da=(a-BEACH_ANGLE+math.pi)%TAU-math.pi;r=math.hypot(x,y);rb=smooth_boundary(a)
 half=BEACH_HALF*(.82+.3*min(1,max(0,(r-RINNER)/(rb-RINNER))))
 if abs(da)<half and r>RINNER+9*math.cos(da/half*math.pi):
  t=(r-RINNER)/(rb-RINNER);return 'WetSand' if t>.93 else 'DrySand' if t>.68 else 'Sand'
 return 'Grass'
tiles={}
for gx,gx2,gy,gy2 in CELLS:
  ks=[(gx,gy),(gx2,gy),(gx2,gy2),(gx,gy2)];c=[V[k] for k in ks]
  if all(p[2] for p in c):continue
  tiles.setdefault((gx//TILE,gy//TILE),[]).append((ks,ground_mat(c,gx2-gx)))
for (tx,ty),cells in sorted(tiles.items()):
 idx={};verts=[];faces=[];mi=[]
 for ks,mat in cells:
  f=[]
  for k in ks:
   if k not in idx:idx[k]=len(verts);verts.append((V[k][0],V[k][1],V[k][3]))
   f.append(idx[k])
  faces.append(tuple(f));mi.append(mat)
 mesh('Ground_%+d_%+d'%(tx,ty),verts,faces,mi,True)
# Cave roofs: the original hill/mountain surface over each tunnel, double sided (rock ceiling inside).
for ci,c in enumerate(CAVES):
 idx={};verts=[];faces=[];mi=[]
 for gx,gx2,gy,gy2 in CELLS:
  if True:
   ks=[(gx,gy),(gx2,gy),(gx2,gy2),(gx,gy2)];p=[V[k] for k in ks]
   if any(q[2] for q in p) or not any(cave_mask(q[0],q[1],c)>.01 for q in p):continue
   if min(q[4] for q in p)-c[4]<13:continue
   f=[]
   for k in ks:
    if k not in idx:idx[k]=len(verts);verts.append((V[k][0],V[k][1],V[k][4]+.15))
    f.append(idx[k])
   slope=(max(q[4] for q in p)-min(q[4] for q in p))/(gx2-gx)
   faces.append(tuple(f));mi.append('Rock' if (max(q[5] for q in p)>18 and slope>.75) or (max(q[8] for q in p)>3 and slope>1.1) else 'Grass')
   faces.append(tuple(reversed(f)));mi.append('CaveRock')
 if faces:mesh('CaveRoof_%s'%('CentreHill' if ci==0 else 'Mountain%d'%ci),verts,faces,mi,True)
# Continuous sculpted cliff skirt; no repeated block or ball cliff pieces.
N=512
for sector in range(8):
 verts=[];faces=[]
 for j in range(5):
  t=j/4
  for i in range(65):
   a=TAU*(sector*64+i)/N;r=smooth_boundary(a)
   offset=math.sin(t*math.pi)*5+math.sin(a*17+t*2)*3*t
   x,y=(r+offset)*math.cos(a),(r+offset)*math.sin(a)
   top=height(r*math.cos(a),r*math.sin(a));z=top*(1-t)+(-43-3*math.sin(a*5))*t
   verts.append((x,y,z))
 for j in range(4):
  for i in range(64):
   k=j*65+i;faces.append((k,k+65,k+66,k+1))
 mesh('Cliff_%02d'%sector,verts,faces,'Rock',True)
# River water surface: a separate mesh, easy to delete if you use Roblox terrain water instead.
wv=[];wf=[];ylist=[4+i*4 for i in range(120)]
ylist=[y for y in ylist if y<smooth_boundary(math.atan2(y,river_x(y)))-1]
for y in ylist:
 w=river_half(y)+1
 for s in (-1,1):wv.append((river_x(y)+s*w,y,-1.6))
for i in range(len(ylist)-1):wf.append((2*i,2*i+1,2*i+3,2*i+2))
mesh('RiverWater',wv,wf,'Water',True)
pv=[(0,4,-1.6)]+[(0+10*math.cos(TAU*i/24),4+10*math.sin(TAU*i/24),-1.6) for i in range(24)]
mesh('RiverPool',pv,[(0,i+1,(i+1)%24+1) for i in range(24)],'Water',True)
for i,(x,y,deg) in enumerate(PLOTS):box('Plot_%02d'%(i+1),x,y,1,150,150,2,deg,'Concrete')
box('CentralSpawn',0,0,SMALL_H+.4,16,16,.8,0,'Spawn')
def feature_clear(x,y,radius):
 if on_hill(x,y,radius+6):return False
 if y>30 and abs(x-river_x(y))<river_half(y)+radius+16:return False
 for a,b,hw,cr,floor in CAVES:
  if seg_dist(x,y,a,b)<hw+radius+10 or math.hypot(x-b[0],y-b[1])<cr+radius+10:return False
 return True
for i in range(112):
 a=random.uniform(0,TAU);r=smooth_boundary(a)-random.uniform(24,73);x,y=r*math.cos(a),r*math.sin(a)
 if plot_clearance(x,y)<25 or abs(a-BEACH_ANGLE)<BEACH_HALF+.12 or not feature_clear(x,y,8):continue
 z=height(x,y);h=random.uniform(15,23)
 box('Tree_%03d_Trunk'%i,x,y,z+h/2,3,3,h,random.uniform(0,90),'Bark')
 ellipsoid('Tree_%03d_Crown'%i,x,y,z+h,random.uniform(11,16),random.uniform(10,15),random.uniform(9,14),random.choice(['Leaf','LeafLight']))
 for k in range(2):ellipsoid('Tree_%03d_Branch_%d'%(i,k),x+random.uniform(-7,7),y+random.uniform(-7,7),z+h-3,8,9,7,'Leaf',7,4)

# A few small groves and boulders in the shared grassy areas.
# Full decoration footprint stays off the sand, plots, hills, river and caves.
def decoration_clear(x,y,radius):
 if plot_clearance(x,y)<radius+9 or not feature_clear(x,y,radius):return False
 if abs((math.atan2(y,x)-BEACH_ANGLE+math.pi)%TAU-math.pi)<BEACH_HALF+.12 and math.hypot(x,y)>RINNER-35:return False
 if mountain_height(x,y)>12:return False
 for k in range(12):
  a=k*TAU/12
  if beach(x+radius*math.cos(a),y+radius*math.sin(a)):return False
 return not beach(x,y)
placed=[]
for i in range(24):
 for attempt in range(300):
  a=random.uniform(0,TAU);r=random.uniform(95,340);x,y=r*math.cos(a),r*math.sin(a)
  if decoration_clear(x,y,19) and all(math.hypot(x-px,y-py)>37 for px,py in placed):break
 else:continue
 placed.append((x,y));z=height(x,y);h=random.uniform(13,18)
 box('InteriorTree_%02d_Trunk'%i,x,y,z+h/2,2.8,2.8,h,20,'Bark')
 ellipsoid('InteriorTree_%02d_Crown'%i,x,y,z+h,11,11,10,'LeafLight')
 ellipsoid('InteriorTree_%02d_Branch'%i,x+5,y-3,z+h-2,8,8,7,'Leaf')
for i in range(30):
 for attempt in range(300):
  a=random.uniform(0,TAU);r=random.uniform(95,350);x,y=r*math.cos(a),r*math.sin(a)
  if decoration_clear(x,y,12):break
 else:continue
 z=height(x,y);w=random.uniform(5,10)
 ellipsoid('InteriorRock_%02d'%i,x,y,z+2,w,w*.7,random.uniform(3,6),'Rock',10,6)

# ---------- Merged decoration meshes (fewer parts in Roblox) ----------
class Batch:
 def __init__(s,name):s.name=name;s.v=[];s.f=[];s.m=[]
 def add(s,v,f,mat):o=len(s.v);s.v+=list(v);s.f+=[tuple(q+o for q in face) for face in f];s.m+=[mat]*len(f)
 def put(s,fn,*a):fn('tmp',*a);ob=SCENE.pop();s.add(ob['v'],ob['f'],ob['mat'])
 def emit(s):
  if s.f:mesh(s.name,s.v,s.f,s.m,False)
QUAD={}
def quad_batch(kind,x,y):
 key=kind+'_'+('N' if y<0 else 'S')+('W' if x<0 else 'E')
 return QUAD.setdefault(key,Batch(key))
def lantern(name,x,y,z,h=5):
 frame=Batch(name+'_Frame')
 frame.put(box,x,y,z+h/2,.7,.7,h,0,'WoodDark')
 frame.put(box,x,y,z+h-.1,1.8,1.8,.3,0,'Iron')
 frame.put(box,x,y,z+h+1.75,2.1,2.1,.4,0,'Iron')
 frame.emit()
 box(name+'_Glow',x,y,z+h+.75,1.4,1.4,1.6,0,'LanternGlow')

# ---------- Wooden bridge over the river, between plots 4 and 5 ----------
BRIDGE_Y=196;BRIDGE_X=river_x(BRIDGE_Y);SPAN,PLANKS,DECK_W=34,17,10
bridge=Batch('WoodenBridge')
deck=[]
for i in range(PLANKS):
 t=(i+.5)/PLANKS;x=BRIDGE_X-SPAN/2+SPAN*t;z=.55+2.6*math.sin(math.pi*t);deck.append((x,z))
 bridge.put(box,x,BRIDGE_Y,z,SPAN/PLANKS-.18,DECK_W,.5,0,'Wood')
for side in (-1,1):
 yy=BRIDGE_Y+side*(DECK_W/2+.1)
 for i in range(0,PLANKS,2):
  x,z=deck[i];bridge.put(box,x,yy,z+1.9,.6,.6,3.4,0,'WoodDark')
 for i in range(0,PLANKS-2,2):
  (x0,z0),(x1,z1)=deck[i],deck[i+2];bridge.put(box,(x0+x1)/2,yy,(z0+z1)/2+3.3,x1-x0+.6,.45,.4,0,'Wood')
 for dx in (-9,-4.5,4.5,9):
  x=BRIDGE_X+dx;z=.55+2.6*math.sin(math.pi*(dx+SPAN/2)/SPAN);bridge.put(box,x,BRIDGE_Y+side*3.5,(z-5.5)/2,1,1,z+5.5,0,'WoodDark')
bridge.emit()
for side in (-1,1):lantern('Lantern_Bridge_%s'%('W' if side<0 else 'E'),BRIDGE_X+side*(SPAN/2+2.5),BRIDGE_Y+DECK_W/2+1.5,height(BRIDGE_X+side*(SPAN/2+2.5),BRIDGE_Y+DECK_W/2+1.5))

# ---------- Lanterns inside the caves ----------
n=0
for x,y in [(-10,70),(10,58),(-10,44),(10,30),(-10,18)]+[(14*math.cos(math.radians(d)),4+14*math.sin(math.radians(d))) for d in (205,270,335)]:
 lantern('Lantern_CentreCave_%02d'%n,x,y,height(x,y));n+=1
for ci,(a,b,hw,cr,floor) in enumerate(CAVES[1:],1):
 ux,uy=b[0]-a[0],b[1]-a[1];L=math.hypot(ux,uy);ux,uy=ux/L,uy/L;px,py=-uy,ux
 spots=[(a[0]+ux*L*t+px*s*(hw-1.8),a[1]+uy*L*t+py*s*(hw-1.8)) for t,s in ((.3,1),(.55,-1),(.8,1))]
 spots+=[(b[0]+(cr-3.5)*math.cos(math.atan2(uy,ux)+d),b[1]+(cr-3.5)*math.sin(math.atan2(uy,ux)+d)) for d in (-1.1,0,1.1)]
 for k,(x,y) in enumerate(spots):lantern('Lantern_Mountain%dCave_%02d'%(ci,k),x,y,height(x,y))

# ---------- Flowers, bushes and tall grass ----------
def grassy(x,y,margin):
 a=math.atan2(y,x);r=math.hypot(x,y)
 if r>smooth_boundary(a)-8:return False
 hh=hill_height(x,y)
 if any(hh>hd[2]-.5 and math.hypot(x-hd[1][0],y-hd[1][1])<hd[3]+4 for hd in HILL_DEFS):return False
 if abs(height(x+1.5,y)-height(x-1.5,y))>2.2 or abs(height(x,y+1.5)-height(x,y-1.5))>2.2:return False
 if plot_clearance(x,y)<margin:return False
 if abs((a-BEACH_ANGLE+math.pi)%TAU-math.pi)<BEACH_HALF+.12 and r>RINNER-30:return False
 if y>30 and abs(x-river_x(y))<river_half(y)+5+margin:return False
 if abs(y-BRIDGE_Y)<DECK_W and abs(x-BRIDGE_X)<SPAN/2+8:return False
 for ca,cb,hw,cr,floor in CAVES:
  if seg_dist(x,y,ca,cb)<hw+8+margin or math.hypot(x-cb[0],y-cb[1])<cr+8+margin:return False
 return mountain_height(x,y)<20
deco=random.Random(91)
def spot(margin,tries=400):
 for _ in range(tries):
  a=deco.uniform(0,TAU);r=deco.uniform(30,smooth_boundary(a));x,y=r*math.cos(a),r*math.sin(a)
  if grassy(x,y,margin):return x,y
centres=[c for c in (spot(10) for _ in range(46)) if c]
for i in range(70):
 c=spot(8)
 if not c:continue
 x,y=c;bt=quad_batch('Bushes',x,y)
 for k in range(deco.randint(2,3)):
  bx,by=x+deco.uniform(-3,3),y+deco.uniform(-3,3);w=deco.uniform(2.8,4.6)
  bt.put(ellipsoid,bx,by,height(bx,by)+w*.45,w,w*deco.uniform(.8,1.1),w*.75,deco.choice(['Bush','BushLight']),8,4)
for cx,cy in centres:
 for k in range(3):
  x,y=cx+deco.uniform(-14,14),cy+deco.uniform(-14,14)
  if not grassy(x,y,3):continue
  bt=quad_batch('Flowers',x,y);col=deco.choice(['FlowerRed','FlowerYellow','FlowerWhite','FlowerPurple'])
  bt.put(ellipsoid,x,y,height(x,y)+.2,2.6,2.6,.7,'Leaf',7,3)
  for j in range(deco.randint(5,8)):
   fx,fy=x+deco.uniform(-2.4,2.4),y+deco.uniform(-2.4,2.4)
   bt.put(ellipsoid,fx,fy,height(fx,fy)+deco.uniform(1,1.6),.75,.75,.45,col,6,3)
def tuft(bt,x,y):
 z=height(x,y);mat=deco.choice(['TallGrass','TallGrass','TallGrassDry'])
 for j in range(deco.randint(6,9)):
  gx,gy=x+deco.uniform(-1.4,1.4),y+deco.uniform(-1.4,1.4);a=deco.uniform(0,TAU);h=deco.uniform(2.4,4.4);lean=deco.uniform(.3,1.2);la=deco.uniform(0,TAU)
  v=[(gx-.3*math.cos(a),gy-.3*math.sin(a),z-.2),(gx+.3*math.cos(a),gy+.3*math.sin(a),z-.2),(gx+lean*math.cos(la),gy+lean*math.sin(la),z+h)]
  bt.add(v,[(0,1,2),(0,2,1)],mat)
for cx,cy in centres:
 for k in range(5):
  x,y=cx+deco.uniform(-20,20),cy+deco.uniform(-20,20)
  if grassy(x,y,2):tuft(quad_batch('TallGrass',x,y),x,y)
for y in range(110,330,9):
 for side in (-1,1):
  x=river_x(y)+side*(river_half(y)+deco.uniform(9,14))
  if grassy(x,y,2) or abs(x-river_x(y))>river_half(y)+5:
   if plot_clearance(x,y)>2 and not (abs(y-BRIDGE_Y)<DECK_W and abs(x-BRIDGE_X)<SPAN/2+8):tuft(quad_batch('TallGrass',x,y),x,y)
for i in range(80):
 c=spot(2)
 if c:tuft(quad_batch('TallGrass',*c),*c)

# ---------- Palm trees on the beach ----------
palms=[]
for i in range(60):
 a=BEACH_ANGLE+deco.uniform(-.8,.8)*BEACH_HALF;rb=smooth_boundary(a);r=deco.uniform(RINNER+30,rb-40);x,y=r*math.cos(a),r*math.sin(a)
 if not beach(x,y) or plot_clearance(x,y)<14 or any(math.hypot(x-px,y-py)<30 for px,py in palms):continue
 palms.append((x,y))
 if len(palms)==8:break
for i,(x,y) in enumerate(palms):
 pt=Batch('PalmTree_%02d'%(i+1));z=height(x,y);la=math.atan2(y,x)+deco.uniform(-.7,.7);lean=deco.uniform(4,8);segs=9;H=deco.uniform(20,26)
 for k in range(segs):
  t=k/segs;w=2.1-.6*t
  pt.put(box,x+lean*t*t*math.cos(la),y+lean*t*t*math.sin(la),z+H*(t+.5/segs),w,w,H/segs+.3,deco.uniform(0,90),'PalmTrunk')
 tx,ty,tz=x+lean*math.cos(la),y+lean*math.sin(la),z+H
 for k in range(3):pt.put(ellipsoid,tx+.9*math.cos(k*2.1),ty+.9*math.sin(k*2.1),tz-.6,.8,.8,.8,'Coconut',6,4)
 for k in range(8):
  fa=k*TAU/8+deco.uniform(-.2,.2);L=deco.uniform(10,13);v=[]
  for j in range(5):
   t=j/4;w=(1.7*math.sin(math.pi*min(1,t*1.15+.05)))+.15;cx,cy=tx+L*t*math.cos(fa),ty+L*t*math.sin(fa);cz=tz+1.2*math.sin(math.pi*t*.8)-4*t*t
   v+=[(cx-w*math.sin(fa),cy+w*math.cos(fa),cz),(cx+w*math.sin(fa),cy-w*math.cos(fa),cz)]
  f=[]
  for j in range(4):q=(2*j,2*j+1,2*j+3,2*j+2);f+=[q,q[::-1]]
  pt.add(v,f,'PalmLeaf')
 pt.emit()
# ---------- Boulders along the foot of each hill cliff ----------
hr=Batch('HillBoulders')
for hd in HILL_DEFS:
 cx,cy=hd[1]
 for i in range(26):
  th=hd[7]+deco.uniform(-62,62);h,foot=hill_shape(cx+math.cos(math.radians(th))*300,cy+math.sin(math.radians(th))*300,hd)
  rr=foot*deco.uniform(.93,1.12);x,y=cx+rr*math.cos(math.radians(th)),cy+rr*math.sin(math.radians(th))
  if plot_clearance(x,y)<8 or any(seg_dist(x,y,ca,cb)<hw+4 for ca,cb,hw,cr,fl in CAVES):continue
  w=deco.uniform(2.5,6);hr.put(ellipsoid,x,y,height(x,y)+w*.25,w,w*deco.uniform(.6,.9),w*deco.uniform(.5,.8),'Rock',8,5)
hr.emit()
for b in QUAD.values():b.emit()

try:import bpy
except ImportError:bpy=None
if bpy:
 from mathutils import Vector
 col=bpy.data.collections.new('OreFactory_SmoothTerrain');bpy.context.scene.collection.children.link(col)
 mats={}
 for name,color in MATS.items():
  m=bpy.data.materials.new('OF_'+name);m.diffuse_color=(*color,1);m.use_nodes=True
  m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*color,1)
  m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85;mats[name]=m
  if name=='LanternGlow':
   ins=m.node_tree.nodes['Principled BSDF'].inputs
   for key in ('Emission Color','Emission'):
    if key in ins:ins[key].default_value=(*color,1)
   if 'Emission Strength' in ins:ins['Emission Strength'].default_value=6
 for ob in SCENE:
  data=bpy.data.meshes.new(ob['name']);data.from_pydata(ob['v'],[],ob['f']);data.update()
  obj=bpy.data.objects.new(ob['name'],data);col.objects.link(obj)
  names=list(dict.fromkeys(ob['mat'])) if isinstance(ob['mat'],list) else [ob['mat']]
  for n in names:data.materials.append(mats[n])
  for i,poly in enumerate(data.polygons):
   poly.use_smooth=ob['smooth'];poly.material_index=names.index(ob['mat'][i]) if isinstance(ob['mat'],list) else 0
 # Dedicated camera and lighting; existing objects are preserved.
 scene=bpy.context.scene;camdata=bpy.data.cameras.new('OF_Overview');cam=bpy.data.objects.new('OF_Overview',camdata);col.objects.link(cam)
 cam.location=(1040,1180,1150);target=Vector((20,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=1400;scene.camera=cam
 data=bpy.data.lights.new('OF_Sun','SUN');sun=bpy.data.objects.new('OF_Sun',data);col.objects.link(sun);sun.rotation_euler=(.5,-.4,-.6);data.energy=2.5;data.angle=.15
 scene.world=scene.world or bpy.data.worlds.new('OF_World');scene.world.color=(.55,.62,.7)
 # Soft fog: thin volume scatter in the world, plus a pale sky colour.
 try:
  w=scene.world;w.use_nodes=True;nt=w.node_tree
  nt.nodes['Background'].inputs['Color'].default_value=(.66,.74,.76,1)
  vs=nt.nodes.new('ShaderNodeVolumeScatter');vs.inputs['Density'].default_value=.00035;vs.inputs['Color'].default_value=(.85,.9,.87,1)
  out=[n for n in nt.nodes if n.type=='OUTPUT_WORLD'][0];nt.links.new(vs.outputs['Volume'],out.inputs['Volume'])
 except Exception as e:print('World fog skipped:',e)
 scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
 scene.render.filepath=str(OUT/'OreFactory_BlenderRender.png')
 print('Ore Factory scene created. Save As a .blend, then F12 to render. Existing scene objects are preserved.')
else:
 # OBJ/MTL are generated from the same scene data used above, not approximated concept art.
 with open(OUT/'OreFactory_SmoothTerrain.mtl','w') as f:
  for n,c in MATS.items():f.write('newmtl '+n+'\nKd '+' '.join(map(str,c))+'\nKa 0.1 0.1 0.1\nd 1\n\n')
 with open(OUT/'OreFactory_SmoothTerrain.obj','w') as f:
  f.write('mtllib OreFactory_SmoothTerrain.mtl\n');offset=1
  for ob in SCENE:
   f.write('o '+ob['name']+'\n')
   for v in ob['v']:f.write('v %.5f %.5f %.5f\n'%tuple(v))
   current=None
   for i,face in enumerate(ob['f']):
    mat=ob['mat'][i] if isinstance(ob['mat'],list) else ob['mat']
    if mat!=current:f.write('usemtl '+mat+'\n');current=mat
    f.write('f '+' '.join(str(q+offset) for q in face)+'\n')
   offset+=len(ob['v'])
 print('Exported',len(SCENE),'objects')
 import json
 (OUT/'mesh_scene.json').write_text(json.dumps(SCENE))
