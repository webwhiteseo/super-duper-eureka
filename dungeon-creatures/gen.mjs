// Defines the 3 dungeon creatures out of plain Roblox parts (Block / Ball / Cylinder),
// then writes:
//   creatures.json              -> used by preview.html to render the picture
//   DungeonCreatures.server.lua -> paste into Roblox Studio to build the exact same models
// Roblox axes: Y up, front of each creature faces -Z. Units are studs.
import * as THREE from 'three';
import fs from 'fs';

const part = (name, shape, size, color, mat, pos = [0, 0, 0], rot = [0, 0, 0], light = 0) =>
  ({ kind: 'part', name, shape, size, color, mat, pos, rot, light });
const group = (pos, rot, children) => ({ kind: 'group', pos, rot, children: children.flat(Infinity) });

// Copy a node to the other side of the body (x -> -x). Names get L/R.
function mirror(node) {
  const flip = (n) => {
    const c = { ...n, pos: [-n.pos[0], n.pos[1], n.pos[2]], rot: [n.rot[0], -n.rot[1], -n.rot[2]] };
    if (n.kind === 'group') c.children = n.children.map(flip);
    else c.name = n.name.replace(/^R/, 'L');
    return c;
  };
  const tagRight = (n) => n.kind === 'group' ? { ...n, children: n.children.map(tagRight) } : { ...n, name: 'R' + n.name };
  const right = tagRight(node);
  return [right, flip(right)];
}

// Scale every size/position in a subtree (used to build the boss bigger).
function scale(node, s) {
  if (node.kind === 'group') return { ...node, pos: node.pos.map((v) => v * s), children: node.children.map((c) => scale(c, s)) };
  return { ...node, pos: node.pos.map((v) => v * s), size: node.size.map((v) => v * s), light: node.light * s };
}

const flat = (arr) => arr.flatMap((n) => (Array.isArray(n) ? flat(n) : [n]));

// ---------------- STAGE 1: GHOUL WHELP (weak, ~4 studs) ----------------
function whelp() {
  const skin = [150, 160, 125], dark = [95, 105, 80], light = [180, 185, 150];
  const bone = [230, 220, 195], eye = [140, 255, 90], mouth = [35, 15, 15];
  return flat([
    mirror(group([0.55, 0, 0], [0, 0, 0], [
      part('Leg', 'Block', [0.7, 1.1, 0.7], skin, 'SmoothPlastic', [0, 0.85, 0]),
      part('Foot', 'Block', [0.85, 0.35, 1.1], dark, 'SmoothPlastic', [0, 0.175, -0.15]),
      part('ToeClaw1', 'Block', [0.12, 0.14, 0.35], bone, 'SmoothPlastic', [-0.22, 0.1, -0.8]),
      part('ToeClaw2', 'Block', [0.12, 0.14, 0.35], bone, 'SmoothPlastic', [0.22, 0.1, -0.8]),
    ])),
    group([0, 1.3, 0], [-18, 0, 0], [
      part('Torso', 'Block', [1.9, 1.6, 1.3], skin, 'SmoothPlastic', [0, 0.8, 0]),
      part('Belly', 'Block', [1.3, 1.0, 0.1], light, 'SmoothPlastic', [0, 0.65, -0.66]),
      part('SpineBump1', 'Ball', [0.4, 0.4, 0.4], dark, 'SmoothPlastic', [0, 0.45, 0.62]),
      part('SpineBump2', 'Ball', [0.4, 0.4, 0.4], dark, 'SmoothPlastic', [0, 0.95, 0.62]),
      part('SpineBump3', 'Ball', [0.4, 0.4, 0.4], dark, 'SmoothPlastic', [0, 1.45, 0.62]),
      group([0, 2.3, -0.3], [12, 0, 0], [
        part('Head', 'Block', [1.8, 1.4, 1.5], skin, 'SmoothPlastic'),
        part('Brow', 'Block', [1.9, 0.25, 0.4], dark, 'SmoothPlastic', [0, 0.32, -0.62]),
        part('EyeSocket', 'Block', [1.4, 0.5, 0.1], mouth, 'SmoothPlastic', [0, 0.05, -0.76]),
        mirror(part('Eye', 'Ball', [0.45, 0.45, 0.45], eye, 'Neon', [0.38, 0.05, -0.76])),
        part('Mouth', 'Block', [1.1, 0.3, 0.1], mouth, 'SmoothPlastic', [0, -0.38, -0.76]),
        mirror(part('Fang', 'Block', [0.14, 0.3, 0.1], bone, 'SmoothPlastic', [0.3, -0.4, -0.82])),
        mirror(part('Ear', 'Block', [0.15, 0.9, 0.45], dark, 'SmoothPlastic', [1.12, 0.45, 0.1], [0, 0, -45])),
      ]),
      mirror(group([1.1, 1.35, 0], [40, 0, 8], [
        part('Arm', 'Block', [0.45, 1.4, 0.45], skin, 'SmoothPlastic', [0, -0.6, 0]),
        part('Hand', 'Block', [0.55, 0.4, 0.55], dark, 'SmoothPlastic', [0, -1.45, 0]),
        part('Claw1', 'Block', [0.1, 0.45, 0.1], bone, 'SmoothPlastic', [-0.18, -1.8, -0.12]),
        part('Claw2', 'Block', [0.1, 0.45, 0.1], bone, 'SmoothPlastic', [0, -1.8, -0.12]),
        part('Claw3', 'Block', [0.1, 0.45, 0.1], bone, 'SmoothPlastic', [0.18, -1.8, -0.12]),
      ])),
    ]),
  ]);
}

// ---------------- STAGE 2: DUNGEON GHOUL (normal, ~9 studs) ----------------
// `opt` lets the boss reuse this body with darker colours.
function ghoulBody(opt) {
  const { skin, dark, bone, eye, mouth, cloth } = opt;
  const teeth = [-0.7, -0.35, 0, 0.35, 0.7];
  return flat([
    mirror(group([0.95, 0, 0], [0, 0, 0], [
      part('Thigh', 'Block', [1.0, 1.8, 1.1], skin, 'SmoothPlastic', [0, 3.0, 0]),
      part('Knee', 'Ball', [0.8, 0.8, 0.8], dark, 'SmoothPlastic', [0, 2.1, -0.3]),
      part('Shin', 'Block', [0.85, 1.7, 0.85], skin, 'SmoothPlastic', [0, 1.25, 0.05]),
      part('Foot', 'Block', [1.2, 0.5, 1.8], dark, 'SmoothPlastic', [0, 0.25, -0.3]),
      part('ToeClaw1', 'Block', [0.16, 0.2, 0.5], bone, 'SmoothPlastic', [-0.38, 0.12, -1.4]),
      part('ToeClaw2', 'Block', [0.16, 0.2, 0.5], bone, 'SmoothPlastic', [0, 0.12, -1.4]),
      part('ToeClaw3', 'Block', [0.16, 0.2, 0.5], bone, 'SmoothPlastic', [0.38, 0.12, -1.4]),
    ])),
    part('Pelvis', 'Block', [2.7, 0.9, 1.6], cloth, 'Fabric', [0, 4.05, 0]),
    part('Belt', 'Block', [2.8, 0.3, 1.7], [50, 35, 25], 'SmoothPlastic', [0, 4.45, 0]),
    part('BeltSkull', 'Ball', [0.6, 0.6, 0.6], bone, 'SmoothPlastic', [0, 4.45, -0.85]),
    part('ClothFlap', 'Block', [1.3, 1.5, 0.12], cloth, 'Fabric', [0, 3.35, -0.82]),
    group([0, 4.5, 0], [-15, 0, 0], [
      part('Torso', 'Block', [3.4, 2.8, 2.0], skin, 'SmoothPlastic', [0, 1.4, 0]),
      part('Chest', 'Block', [3.9, 1.3, 2.2], skin, 'SmoothPlastic', [0, 2.45, 0]),
      part('Rib1', 'Block', [2.2, 0.2, 0.12], bone, 'SmoothPlastic', [0, 0.7, -1.05]),
      part('Rib2', 'Block', [2.4, 0.2, 0.12], bone, 'SmoothPlastic', [0, 1.15, -1.05]),
      part('Rib3', 'Block', [2.6, 0.2, 0.12], bone, 'SmoothPlastic', [0, 1.6, -1.05]),
      part('Sternum', 'Block', [0.3, 1.5, 0.16], bone, 'SmoothPlastic', [0, 1.2, -1.08]),
      part('BackSpike1', 'Block', [0.3, 0.9, 0.3], bone, 'SmoothPlastic', [0, 1.0, 1.25], [35, 0, 0]),
      part('BackSpike2', 'Block', [0.3, 1.0, 0.3], bone, 'SmoothPlastic', [0, 1.9, 1.3], [35, 0, 0]),
      part('BackSpike3', 'Block', [0.3, 1.1, 0.3], bone, 'SmoothPlastic', [0, 2.8, 1.35], [35, 0, 0]),
      mirror(group([1.9, 3.05, 0], [0, 0, -15], [
        part('ShoulderPad', 'Block', [1.3, 0.5, 1.4], bone, 'SmoothPlastic'),
        part('ShoulderSpike1', 'Block', [0.25, 0.9, 0.25], bone, 'SmoothPlastic', [0.25, 0.6, -0.3], [0, 0, -20]),
        part('ShoulderSpike2', 'Block', [0.25, 0.7, 0.25], bone, 'SmoothPlastic', [-0.2, 0.5, 0.3], [0, 0, -10]),
      ])),
      group([0, 3.3, -0.7], [12, 0, 0], [
        part('Neck', 'Block', [1.2, 0.8, 1.0], dark, 'SmoothPlastic', [0, -0.25, 0.3]),
        part('Head', 'Block', [2.2, 1.8, 1.9], skin, 'SmoothPlastic', [0, 0.7, 0]),
        part('Brow', 'Block', [2.3, 0.35, 0.5], dark, 'SmoothPlastic', [0, 1.15, -0.8], [-10, 0, 0]),
        part('EyeSocket', 'Block', [1.7, 0.55, 0.1], mouth, 'SmoothPlastic', [0, 0.82, -0.95]),
        mirror(part('Eye', 'Ball', [0.5, 0.5, 0.5], eye, 'Neon', [0.45, 0.82, -0.97])),
        part('MouthInside', 'Block', [1.9, 0.7, 1.6], mouth, 'SmoothPlastic', [0, -0.15, -0.1]),
        ...teeth.map((x, i) => part('Tooth' + (i + 1), 'Block', [0.18, 0.3, 0.12], bone, 'SmoothPlastic', [x, -0.32, -0.92])),
        mirror(part('Fang', 'Block', [0.22, 0.65, 0.15], bone, 'SmoothPlastic', [0.88, -0.45, -0.92])),
        group([0, -0.2, 0.1], [-18, 0, 0], [
          part('Jaw', 'Block', [2.0, 0.55, 1.85], skin, 'SmoothPlastic', [0, -0.3, -0.1]),
          ...[-0.6, -0.2, 0.2, 0.6].map((x, i) => part('LowerTooth' + (i + 1), 'Block', [0.16, 0.3, 0.12], bone, 'SmoothPlastic', [x, 0.05, -0.92])),
        ]),
        mirror(group([0.8, 1.55, 0.1], [25, 0, -30], [
          part('Horn', 'Block', [0.35, 0.8, 0.35], bone, 'SmoothPlastic', [0, 0.4, 0]),
          group([0, 0.8, 0], [25, 0, 0], [part('HornTip', 'Block', [0.22, 0.7, 0.22], bone, 'SmoothPlastic', [0, 0.35, 0])]),
        ])),
      ]),
      mirror(group([2.35, 2.5, 0], [25, 0, 10], [
        part('UpperArm', 'Block', [0.9, 2.0, 0.9], skin, 'SmoothPlastic', [0, -1.0, 0]),
        part('Elbow', 'Ball', [0.95, 0.95, 0.95], dark, 'SmoothPlastic', [0, -2.0, 0]),
        group([0, -2.0, 0], [25, 0, 0], [
          part('Forearm', 'Block', [0.8, 1.9, 0.8], skin, 'SmoothPlastic', [0, -1.0, 0]),
          part('Bracer', 'Block', [0.95, 0.6, 0.95], [60, 45, 35], 'SmoothPlastic', [0, -1.35, 0]),
          part('Hand', 'Block', [1.0, 0.6, 0.9], dark, 'SmoothPlastic', [0, -2.2, 0]),
          ...[-0.36, -0.12, 0.12, 0.36].map((x, i) => part('Claw' + (i + 1), 'Block', [0.14, 0.8, 0.14], bone, 'SmoothPlastic', [x, -2.85, -0.2], [20, 0, 0])),
        ]),
      ])),
    ]),
  ]);
}

function ghoul() {
  return ghoulBody({ skin: [110, 120, 90], dark: [70, 78, 58], bone: [225, 215, 185], eye: [255, 130, 30], mouth: [25, 10, 10], cloth: [75, 50, 35] });
}

// ---------------- STAGE 3: GHOUL OVERLORD (boss, ~20 studs) ----------------
// Same skeleton as the ghoul scaled x2.1, then armour, crown, horns, cape, core and a cleaver.
function overlord() {
  const S = 2.1;
  const skin = [100, 80, 105], dark = [55, 40, 60], bone = [200, 185, 160], red = [255, 35, 35];
  const metal = [80, 80, 92], gold = [190, 145, 55], cape = [90, 10, 18];
  const body = ghoulBody({ skin, dark, bone, eye: red, mouth: [15, 0, 0], cloth: [35, 25, 30] })
    .filter((p) => !/Horn|ShoulderPad|ShoulderSpike/.test(p.name));
  // Rebuild the ghoul tree just for the extras: torso frame at (0,4.5,0) tilted -15, head frame inside it.
  const extras = group([0, 4.5, 0], [-15, 0, 0], [
    part('ChestPlate', 'Block', [3.6, 1.9, 0.3], metal, 'Metal', [0, 2.0, -1.1]),
    part('ChestTrim', 'Block', [3.7, 0.18, 0.34], gold, 'Metal', [0, 2.95, -1.1]),
    part('CoreFrame', 'Cylinder', [0.2, 1.0, 1.0], gold, 'Metal', [0, 1.95, -1.27], [0, 90, 0]),
    part('Core', 'Ball', [0.75, 0.75, 0.75], [255, 60, 20], 'Neon', [0, 1.95, -1.3], [0, 0, 0], 6),
    mirror(group([2.0, 3.15, 0], [0, 0, -18], [
      part('Pauldron', 'Block', [1.7, 0.7, 1.9], metal, 'Metal'),
      part('PauldronTrim', 'Block', [1.75, 0.15, 1.95], gold, 'Metal', [0, -0.3, 0]),
      part('PauldronSpike1', 'Block', [0.3, 1.4, 0.3], bone, 'SmoothPlastic', [0.4, 0.95, -0.5], [-10, 0, -25]),
      part('PauldronSpike2', 'Block', [0.3, 1.7, 0.3], bone, 'SmoothPlastic', [0.1, 1.1, 0], [0, 0, -15]),
      part('PauldronSpike3', 'Block', [0.3, 1.4, 0.3], bone, 'SmoothPlastic', [-0.2, 0.95, 0.5], [10, 0, -5]),
    ])),
    group([0, 3.3, -0.7], [12, 0, 0], [
      part('Crown', 'Block', [2.4, 0.35, 2.1], gold, 'Metal', [0, 1.7, 0]),
      ...[-0.9, -0.45, 0, 0.45, 0.9].map((x, i) => part('CrownSpike' + (i + 1), 'Block', [0.2, i === 2 ? 1.0 : 0.65, 0.2], gold, 'Metal', [x, i === 2 ? 2.35 : 2.18, -0.95])),
      part('CrownGem', 'Ball', [0.35, 0.35, 0.35], red, 'Neon', [0, 1.7, -1.08]),
      // big curling horns: 4 segments, each bending further
      mirror(group([1.0, 1.4, 0.1], [0, 0, -70], [
        part('Horn1', 'Block', [0.6, 1.0, 0.6], bone, 'SmoothPlastic', [0, 0.5, 0]),
        part('HornJoint1', 'Ball', [0.6, 0.6, 0.6], bone, 'SmoothPlastic', [0, 1.0, 0]),
        group([0, 1.0, 0], [0, 0, 35], [
          part('Horn2', 'Block', [0.5, 0.9, 0.5], bone, 'SmoothPlastic', [0, 0.45, 0]),
          part('HornJoint2', 'Ball', [0.5, 0.5, 0.5], bone, 'SmoothPlastic', [0, 0.9, 0]),
          group([0, 0.9, 0], [-20, 0, 30], [
            part('Horn3', 'Block', [0.38, 0.8, 0.38], bone, 'SmoothPlastic', [0, 0.4, 0]),
            part('HornJoint3', 'Ball', [0.38, 0.38, 0.38], bone, 'SmoothPlastic', [0, 0.8, 0]),
            group([0, 0.8, 0], [-30, 0, 25], [part('Horn4', 'Block', [0.24, 0.7, 0.24], [30, 25, 25], 'SmoothPlastic', [0, 0.35, 0])]),
          ]),
        ]),
      ])),
    ]),
    // tattered cape hanging from the shoulders
    part('CapeTop', 'Block', [3.8, 0.4, 0.4], gold, 'Metal', [0, 3.0, 1.2]),
    group([0, 3.0, 1.25], [12, 0, 0], [
      part('Cape1', 'Block', [1.3, 6.2, 0.12], cape, 'Fabric', [-1.25, -3.1, 0]),
      part('Cape2', 'Block', [1.3, 6.8, 0.12], cape, 'Fabric', [0, -3.4, 0.05]),
      part('Cape3', 'Block', [1.3, 5.6, 0.12], cape, 'Fabric', [1.25, -2.8, 0]),
    ]),
    // cleaver raised up in the right hand (follows the right arm joints)
    group([2.35, 2.5, 0], [25, 0, 10], [group([0, -2.0, 0], [25, 0, 0], [
      group([0, -2.2, 0], [100, 0, 0], [
        part('CleaverHandle', 'Cylinder', [3.2, 0.35, 0.35], [45, 30, 20], 'Wood', [0, 0, 0], [0, 0, 90]),
        part('CleaverGuard', 'Block', [0.25, 0.25, 1.0], gold, 'Metal', [0, -1.6, 0]),
        part('CleaverBlade', 'Block', [0.15, 3.8, 1.8], metal, 'Metal', [0, -3.5, 0.4]),
        part('CleaverEdge', 'Block', [0.17, 3.8, 0.15], red, 'Neon', [0, -3.5, 1.33]),
        part('CleaverTip', 'Block', [0.16, 1.2, 1.2], metal, 'Metal', [0, -5.2, 0.35], [-45, 0, 0]),
      ]),
    ])]),
    // armoured greaves on the legs (outside the torso frame, so undo it below)
  ]);
  const legs = mirror(group([0.95, 0, 0], [0, 0, 0], [
    part('Greave', 'Block', [1.0, 1.4, 1.0], metal, 'Metal', [0, 1.3, -0.05]),
    part('KneeSpike', 'Block', [0.25, 0.8, 0.25], bone, 'SmoothPlastic', [0, 2.3, -0.75], [-55, 0, 0]),
    part('Sabaton', 'Block', [1.3, 0.3, 1.9], metal, 'Metal', [0, 0.55, -0.3]),
  ]));
  return flat([body, extras, legs].flat()).map((n) => scale(n, S));
}

// ---------------- flatten tree -> world parts ----------------
function toWorld(nodes) {
  const out = [];
  const walk = (n, parent) => {
    const e = new THREE.Euler(...n.rot.map(THREE.MathUtils.degToRad), 'YXZ');
    const m = parent.clone().multiply(new THREE.Matrix4().compose(new THREE.Vector3(...n.pos), new THREE.Quaternion().setFromEuler(e), new THREE.Vector3(1, 1, 1)));
    if (n.kind === 'group') return n.children.forEach((c) => walk(c, m));
    const p = new THREE.Vector3(), q = new THREE.Quaternion();
    m.decompose(p, q, new THREE.Vector3());
    const r = new THREE.Euler().setFromQuaternion(q, 'YXZ');
    const round = (v) => Math.round(v * 1000) / 1000;
    out.push({ name: n.name, shape: n.shape, size: n.size.map(round), pos: [p.x, p.y, p.z].map(round),
      rot: [r.x, r.y, r.z].map((a) => round(THREE.MathUtils.radToDeg(a))), color: n.color, mat: n.mat, light: round(n.light) });
  };
  nodes.forEach((n) => walk(n, new THREE.Matrix4()));
  return out;
}

const creatures = [
  { name: 'Ghoul Whelp', stage: 1, health: 50, offset: [16, 0, 0], parts: toWorld(whelp()) },
  { name: 'Dungeon Ghoul', stage: 2, health: 250, offset: [8, 0, 0], parts: toWorld(ghoul()) },
  { name: 'Ghoul Overlord', stage: 3, health: 3000, offset: [-7, 0, 0], parts: toWorld(overlord()) },
];
for (const c of creatures) {
  const ys = c.parts.map((p) => p.pos[1] + Math.max(...p.size) / 2);
  c.height = Math.round(Math.max(...ys) * 10) / 10;
}
fs.writeFileSync(new URL('./creatures.json', import.meta.url), JSON.stringify(creatures));

// ---------------- Luau output ----------------
const v3 = (a) => `Vector3.new(${a.join(', ')})`;
const rgb = (a) => `Color3.fromRGB(${a.join(', ')})`;
let lua = `-- DUNGEON CREATURES (auto-generated by gen.mjs - edit gen.mjs, not this file)
-- Stage 1: Ghoul Whelp  |  Stage 2: Dungeon Ghoul  |  Stage 3: Ghoul Overlord (boss)
--
-- HOW TO USE:
--   Option A (keep them in your place): View > Command Bar, paste this whole file, press Enter.
--   Option B (spawn on Play): put it in a Script inside ServerScriptService.
-- Built only from normal Parts (Block / Ball / Cylinder), welded to an anchored HumanoidRootPart.
-- Unanchor HumanoidRootPart when you add AI/movement.

local CREATURES = {
`;
for (const c of creatures) {
  lua += `\t{\n\t\tname = "${c.name}",\n\t\tstage = ${c.stage},\n\t\thealth = ${c.health},\n\t\toffset = ${v3(c.offset)},\n\t\tparts = {\n`;
  for (const p of c.parts) {
    lua += `\t\t\t{ "${p.name}", "${p.shape}", ${v3(p.size)}, ${v3(p.pos)}, ${v3(p.rot)}, ${rgb(p.color)}, "${p.mat}"${p.light ? `, ${p.light}` : ''} },\n`;
  }
  lua += `\t\t},\n\t},\n`;
}
lua += `}

local function buildCreature(def)
	local old = workspace:FindFirstChild(def.name)
	if old then
		old:Destroy()
	end

	local model = Instance.new("Model")
	model.Name = def.name

	local scale = def.stage == 3 and 2.1 or (def.stage == 2 and 1 or 0.5)
	local root = Instance.new("Part")
	root.Name = "HumanoidRootPart"
	root.Size = Vector3.new(2, 2, 1) * scale
	root.CFrame = CFrame.new(def.offset + Vector3.new(0, 4 * scale, 0))
	root.Transparency = 1
	root.CanCollide = false
	root.Anchored = true
	root.Parent = model
	model.PrimaryPart = root

	for _, p in def.parts do
		local name, shape, size, pos, rot, color, material, lightRange = table.unpack(p)
		local part = Instance.new("Part")
		part.Name = name
		part.Shape = Enum.PartType[shape]
		part.Size = size
		part.CFrame = CFrame.new(def.offset + pos) * CFrame.fromOrientation(math.rad(rot.X), math.rad(rot.Y), math.rad(rot.Z))
		part.Color = color
		part.Material = Enum.Material[material]
		part.TopSurface = Enum.SurfaceType.Smooth
		part.BottomSurface = Enum.SurfaceType.Smooth
		part.CanCollide = false
		part.Massless = true
		part.CastShadow = material ~= "Neon"
		part.Parent = model

		local weld = Instance.new("WeldConstraint")
		weld.Part0 = root
		weld.Part1 = part
		weld.Parent = part

		if lightRange then
			local light = Instance.new("PointLight")
			light.Color = color
			light.Range = lightRange
			light.Brightness = 3
			light.Parent = part
		end
	end

	local humanoid = Instance.new("Humanoid")
	humanoid.MaxHealth = def.health
	humanoid.Health = def.health
	humanoid.DisplayName = "[" .. def.stage .. "] " .. def.name
	humanoid.Parent = model

	model.Parent = workspace
	return model
end

for _, def in CREATURES do
	buildCreature(def)
end
print("Dungeon creatures built!")
`;
fs.writeFileSync(new URL('./DungeonCreatures.server.lua', import.meta.url), lua);
console.log(creatures.map((c) => `${c.name}: ${c.parts.length} parts, ${c.height} studs tall`).join('\n'));
