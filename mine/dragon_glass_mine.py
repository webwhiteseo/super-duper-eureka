"""Builds the Dragon Glass Mine: writes a Roblox Studio Command Bar script (DragonGlassMine.lua)
and a preview render (DragonGlassMine_Preview.png) from the same part list.
Roblox axes: Y up, front of the mine is -Z (the model's LookVector). Units are studs."""
import math
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
PARTS=[]
def rx(d):a=math.radians(d);c,s=math.cos(a),math.sin(a);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(d):a=math.radians(d);c,s=math.cos(a),math.sin(a);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(d):a=math.radians(d);c,s=math.cos(a),math.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def align(v,to=(0,1,0)):
 """Rotation taking unit vector v onto `to`... used inverted: maps local `to` onto v."""
 a=np.array(to,float);b=np.array(v,float);b/=np.linalg.norm(b);c=np.cross(a,b);d=float(a@b)
 if np.linalg.norm(c)<1e-9:return np.eye(3) if d>0 else rx(180)
 k=np.array([[0,-c[2],c[1]],[c[2],0,-c[0]],[-c[1],c[0],0]]);return np.eye(3)+k+k@k/(1+d)
def part(name,size,pos,rot=None,color=(60,60,60),mat='Slate',trans=0.,refl=0.,collide=True):
 PARTS.append(dict(name=name,size=size,pos=np.array(pos,float),rot=np.eye(3) if rot is None else rot,color=color,mat=mat,trans=trans,refl=refl,collide=collide))
OBSIDIAN=(30,25,38);STONE=(52,50,58);BONE=(214,204,182);GLASS=(48,14,74);CORE=(160,60,245);EYE=(255,80,40)

# Base plate, trim and four clawed feet
part('Base',(8,1,8),(0,.5,0),color=STONE)
part('BaseTrim',(8.4,.4,8.4),(0,.2,0),color=(34,32,40),mat='Metal')
for i,(sx,sz) in enumerate([(-1,-1),(1,-1),(1,1),(-1,1)]):
 cx,cz=sx*3.55,sz*3.55
 part('Foot%d'%i,(1.6,.9,1.6),(cx,1.3,cz),ry(45),color=OBSIDIAN)
 for k,spread in enumerate((-28,0,28)):
  yaw=math.degrees(math.atan2(sx,sz))+spread;d=np.array([math.sin(math.radians(yaw)),-.45,math.cos(math.radians(yaw))])
  part('Foot%dClaw%d'%(i,k),(.35,1.3,.35),np.array([cx,1.05,cz])+d/np.linalg.norm(d)*.95,align(d),color=BONE,mat='SmoothPlastic')

# Obsidian body with glowing side vents and folded wing fins
part('Body',(6,5,6),(0,3.5,.5),color=OBSIDIAN)
part('BodyCap',(6.4,.5,6.4),(0,6.1,.5),color=STONE)
for sx in (-1,1):
 for k,y in enumerate((2.5,3.5,4.5)):part('Vent%s%d'%('L' if sx<0 else 'R',k),(.2,.35,4.2),(sx*3.05,y,.6),color=CORE,mat='Neon',collide=False)
 part('Wing'+('L' if sx<0 else 'R'),(.25,3.2,4.6),(sx*3.6,5.6,1.6),rz(-sx*32)@rx(-12),color=(58,26,82))
 part('WingEdge'+('L' if sx<0 else 'R'),(.3,.25,4.6),(sx*4.45,7.0,1.4),rz(-sx*32)@rx(-12),color=CORE,mat='Neon',collide=False)

# Dragon head: ore pours out of the mouth
part('UpperJaw',(4.4,1.3,3.2),(0,5.15,-3.7),rx(12),color=(36,31,46))
part('LowerJaw',(4.0,.8,2.8),(0,2.75,-3.5),rx(-10),color=(36,31,46))
part('Throat',(3.0,1.4,.4),(0,3.9,-2.2),color=(200,90,255),mat='Neon',collide=False)
for k,x in enumerate((-1.5,-.5,.5,1.5)):part('ToothUpper%d'%k,(.35,.75,.35),(x,4.3,-4.8),ry(45),color=BONE,mat='SmoothPlastic',collide=False)
for k,x in enumerate((-1.0,0,1.0)):part('ToothLower%d'%k,(.3,.6,.3),(x,3.3,-4.55),ry(45),color=BONE,mat='SmoothPlastic',collide=False)
for sx in (-1,1):
 part('Eye'+('L' if sx<0 else 'R'),(.8,.4,.3),(sx*1.3,6.05,-4.55),rz(sx*12),color=EYE,mat='Neon',collide=False)
 part('Brow'+('L' if sx<0 else 'R'),(1.5,.45,1.1),(sx*1.3,6.45,-4.2),rz(sx*18),color=(24,20,30))
 part('Nostril'+('L' if sx<0 else 'R'),(.35,.25,.2),(sx*.8,5.3,-5.35),color=(12,10,14),collide=False)
part('Drop',(1,1,1),(0,3.5,-5.6),color=(160,60,245),trans=1,collide=False)

# Curved horns from the back of the head
for sx in (-1,1):
 p=np.array([sx*2.2,6.3,2.4])
 for k in range(5):
  R=rz(-sx*(10+7*k))@rx(20+17*k);L=1.5;w=.95-.14*k
  part('Horn%s%d'%('L' if sx<0 else 'R',k),(w,L,w),p+R@np.array([0,L/2,0]),R,color=BONE if k<4 else CORE,mat='SmoothPlastic' if k<4 else 'Neon')
  p=p+R@np.array([0,L*.88,0])

# Back spikes
for k,z in enumerate((1.6,2.6,3.6)):
 part('Spike%d'%k,(.6,1.4-.2*k,.6),(0,6.9-.1*k,z),rx(28)@ry(45),color=(70,36,98))

# Dragon glass crystal cluster (glass shell, neon core, pointed tip)
TIP=align((1,1,1),(0,1,0)).T  # cube stood on its corner
for k,(x,z,h,tx,tz,w) in enumerate([(0,1.0,7.2,0,0,1.6),(-1.7,.2,4.6,-10,18,1.1),(1.7,.4,5.1,8,-20,1.2),(-.7,2.5,4.1,25,8,1.0),(1.1,2.3,3.7,22,-14,.9),(.3,-1.2,3.2,-26,5,.9)]):
 T=rx(tx)@rz(tz);R=T@ry(45);b=np.array([x,6.2,z])
 part('Crystal%d'%k,(w,h,w),b+T@np.array([0,h/2,0]),R,color=GLASS,mat='Glass',trans=.15,refl=.25)
 part('Crystal%dCore'%k,(w*.45,h*.85,w*.45),b+T@np.array([0,h*.45,0]),R,color=CORE,mat='Neon',collide=False)
 s=w*.72;part('Crystal%dTip'%k,(s,s,s),b+T@np.array([0,h+s*.45,0]),T@ry(45)@TIP,color=GLASS,mat='Glass',trans=.15,refl=.25)

# ---------- Roblox Studio script ----------
def lua_part(p):
 R=p['rot'];x,y,z=p['pos']
 cf='CFrame.new(%s)'%','.join('%.4f'%v for v in [x,y,z]+list(R.flatten()))
 return '\t{"%s",Vector3.new(%s),%s,Color3.fromRGB(%d,%d,%d),Enum.Material.%s,%g,%g,%s},'%(
  p['name'],','.join('%g'%v for v in p['size']),cf,*p['color'],p['mat'],p['trans'],p['refl'],'true' if p['collide'] else 'false')
DROPPER='''local Debris = game:GetService("Debris")
local mine = script.Parent
local drop = mine:WaitForChild("Drop")
while true do
	task.wait(mine:GetAttribute("DropInterval") or 1.5)
	if mine:GetAttribute("Enabled") ~= false then
		local size = mine:GetAttribute("OreSize") or 1
		local ore = Instance.new("Part")
		ore.Name = "DragonGlassOre"
		ore.Size = Vector3.new(size, size, size)
		ore.Material = Enum.Material.Glass
		ore.Color = Color3.fromRGB(120, 40, 200)
		ore.Transparency = 0.15
		ore.Reflectance = 0.2
		ore.CFrame = drop.CFrame * CFrame.Angles(math.random() * 6.28, math.random() * 6.28, 0)
		ore:SetAttribute("Value", mine:GetAttribute("OreValue") or 40)
		ore:SetAttribute("OreType", "DragonGlass")
		ore.Parent = workspace
		ore.AssemblyLinearVelocity = drop.CFrame.LookVector * 6
		Debris:AddItem(ore, 30)
	end
end
'''
lua='''-- Dragon Glass Mine (Ore Factory). Original design.
-- Studio: View > Command Bar, paste this whole file, press Enter.
-- The mine appears on the ground where your camera is looking, facing the camera's direction.
-- Ore drops out of the dragon's mouth (front). Tune it with the model's attributes:
--   OreValue, DropInterval (seconds), OreSize, Enabled.

local P = {
%s
}

local model = Instance.new("Model")
model.Name = "DragonGlassMine"
for _, s in ipairs(P) do
	local p = Instance.new("Part")
	p.Name = s[1]
	p.Size = s[2]
	p.CFrame = s[3]
	p.Color = s[4]
	p.Material = s[5]
	p.Transparency = s[6]
	p.Reflectance = s[7]
	p.CanCollide = s[8]
	p.CanQuery = s[8]
	p.Anchored = true
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.CastShadow = p.Material ~= Enum.Material.Neon
	p.Parent = model
end
model.PrimaryPart = model.Base
model.Base.PivotOffset = CFrame.new(0, -0.5, 0) -- pivot at the bottom centre
model:SetAttribute("OreValue", 40)
model:SetAttribute("DropInterval", 1.5)
model:SetAttribute("OreSize", 1)
model:SetAttribute("Enabled", true)

local core = model.Crystal0Core
local light = Instance.new("PointLight")
light.Color = Color3.fromRGB(170, 70, 255)
light.Brightness = 2
light.Range = 14
light.Parent = core
local sparks = Instance.new("ParticleEmitter")
sparks.Color = ColorSequence.new(Color3.fromRGB(190, 110, 255))
sparks.LightEmission = 1
sparks.Rate = 6
sparks.Lifetime = NumberRange.new(1.5, 2.5)
sparks.Speed = NumberRange.new(0.5, 1.5)
sparks.SpreadAngle = Vector2.new(30, 30)
sparks.Size = NumberSequence.new(0.3, 0)
sparks.Parent = core
local mouth = Instance.new("PointLight")
mouth.Color = Color3.fromRGB(200, 90, 255)
mouth.Brightness = 1.5
mouth.Range = 8
mouth.Parent = model.Throat

local dropper = Instance.new("Script")
dropper.Name = "Dropper"
dropper.Source = [[
%s]]
dropper.Parent = model

-- Place on the ground in front of the camera, front facing the camera.
local cam = workspace.CurrentCamera
local target = cam.CFrame.Position + cam.CFrame.LookVector * 30
local hit = workspace:Raycast(target + Vector3.new(0, 100, 0), Vector3.new(0, -400, 0))
local ground = hit and hit.Position or Vector3.new(target.X, 0, target.Z)
local look = Vector3.new(-cam.CFrame.LookVector.X, 0, -cam.CFrame.LookVector.Z)
if look.Magnitude < 0.01 then look = Vector3.new(0, 0, -1) end
model:PivotTo(CFrame.lookAt(ground, ground + look.Unit))
model.Parent = workspace
game:GetService("Selection"):Set({model})
print("Dragon Glass Mine created:", #P, "parts")
'''%('\n'.join(lua_part(p) for p in PARTS),DROPPER)
(OUT/'DragonGlassMine.lua').write_text(lua)

# ---------- Preview render (same parts) ----------
from PIL import Image,ImageDraw,ImageFont
W,H=1600,1000;img=np.zeros((H,W,3),np.uint8);img[:]=(28,26,34)
zb=np.full((H,W),-1e9,np.float32)
CORN=np.array([[x,y,z] for x in(-.5,.5) for y in(-.5,.5) for z in(-.5,.5)])
FACES=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
light=np.array([.4,.8,-.45]);light/=np.linalg.norm(light)
def render(view_yaw,cx,scale):
 d=ry(view_yaw)@np.array([0,0,-1.]);d=d+np.array([0,.55,0]);d/=np.linalg.norm(d)  # toward camera
 r=np.cross([0,1,0],d);r/=np.linalg.norm(r);u=np.cross(d,r)
 for p in PARTS:
  if p['trans']>=1:continue
  v=p['pos']+(CORN*np.array(p['size']))@p['rot'].T
  sp=np.stack([(v@r)*scale+cx,-(v@u)*scale+H*.62,v@d],1)
  for f in FACES:
   n=np.cross(v[f[1]]-v[f[0]],v[f[2]]-v[f[0]]);nn=np.linalg.norm(n)
   if nn<1e-9:continue
   n/=nn;c=np.array(p['color'])/255
   if p['mat']=='Neon':col=np.minimum(1,c*1.25)
   else:
    col=c*(.38+.62*max(0,float(n@light)))
    if p['mat']=='Glass':col=col*.85+np.array([.12,.04,.18])
   col=(np.clip(col,0,1)*255).astype(np.uint8)
   for tri in ((f[0],f[1],f[2]),(f[0],f[2],f[3])):
    a,b,c3=sp[list(tri)];den=(b[1]-c3[1])*(a[0]-c3[0])+(c3[0]-b[0])*(a[1]-c3[1])
    if abs(den)<1e-9:continue
    x0,x1=int(max(0,min(a[0],b[0],c3[0]))),int(min(W-1,max(a[0],b[0],c3[0])+1));y0,y1=int(max(0,min(a[1],b[1],c3[1]))),int(min(H-1,max(a[1],b[1],c3[1])+1))
    if x1<x0 or y1<y0:continue
    yy,xx=np.mgrid[y0:y1+1,x0:x1+1]+.5
    w1=((b[1]-c3[1])*(xx-c3[0])+(c3[0]-b[0])*(yy-c3[1]))/den;w2=((c3[1]-a[1])*(xx-c3[0])+(a[0]-c3[0])*(yy-c3[1]))/den;w3=1-w1-w2
    z=w1*a[2]+w2*b[2]+w3*c3[2];view=zb[y0:y1+1,x0:x1+1];m=(w1>=0)&(w2>=0)&(w3>=0)&(z>view)
    view[m]=z[m];img[y0:y1+1,x0:x1+1][m]=col
render(-35,W*.27,46);render(150,W*.75,46)
im=Image.fromarray(img);dr=ImageDraw.Draw(im);font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
dr.text((W/2,50),'DRAGON GLASS MINE',font=ImageFont.truetype(font,36),fill=(215,190,255),anchor='mm')
dr.text((W*.27,H-60),'Front: ore drops from the mouth',font=ImageFont.truetype(font,20),fill=(190,180,210),anchor='mm')
dr.text((W*.75,H-60),'Back: horns, wings and crystal cluster',font=ImageFont.truetype(font,20),fill=(190,180,210),anchor='mm')
dr.text((W/2,H-25),'Preview of the exact part list (not a Roblox screenshot). %d parts, 8 x 8 stud footprint.'%len(PARTS),font=ImageFont.truetype(font,15),fill=(140,132,160),anchor='mm')
im.save(OUT/'DragonGlassMine_Preview.png');print('parts',len(PARTS))
