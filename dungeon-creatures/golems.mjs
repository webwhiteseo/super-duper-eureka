// Crystal Cave Golems: Weakling -> Dungeon Enemy -> Crystal Titan (boss).
// Chunky stacked-rock bodies with glowing crystal clusters.
// node golems.mjs -> golems.json + CrystalGolems.server.lua
import { part, group, mirror, scale, exportCreatures, rng } from './lib.mjs';

const STONE = [84, 92, 108], STONE_DARK = [52, 58, 72], STONE_LIGHT = [108, 117, 134];
const CRYSTAL = [25, 115, 235], CRYSTAL_LIGHT = [110, 205, 255], GLOW = [70, 215, 255];

// One golem body. level 1/2/3 adds more armour slabs, crystals and cracks.
function golem(level, seed) {
  const rand = rng(seed);
  const j = (amount) => (rand() * 2 - 1) * amount;
  const shade = (c, amount = 8) => { const d = j(amount); return c.map((v) => Math.round(v + d)); };
  // a rock: block with a little random tilt and colour change, so it looks hand-stacked
  const rock = (name, size, pos, rot = [0, 0, 0], color = STONE) =>
    part(name, 'Block', size, shade(color), 'Slate', pos, [rot[0] + j(5), rot[1] + j(5), rot[2] + j(5)]);
  const crack = (name, pos, rot) => part(name, 'Block', [0.06, 0.45, 0.05], GLOW, 'Neon', pos, [0, 0, rot]);
  // crystal: tall block + light cap + bright inner stripe
  const crystal = (name, pos, rot, len, w) => group(pos, rot, [
    part(name, 'Block', [w, len, w], CRYSTAL, 'Neon', [0, len / 2, 0]),
    part(name + 'Cap', 'Block', [w * 0.75, w * 0.6, w * 0.75], CRYSTAL_LIGHT, 'Neon', [0, len + w * 0.3, 0]),
    part(name + 'Shine', 'Block', [w * 0.22, len * 0.75, w * 1.04], CRYSTAL_LIGHT, 'Neon', [w * 0.18, len * 0.5, 0]),
  ]);

  const legs = mirror(group([0.75, 0, 0], [0, 0, 0], [
    rock('Thigh', [1.05, 0.95, 1.05], [0, 1.35, 0]),
    rock('Foot', [1.25, 0.85, 1.35], [0, 0.42, -0.05], [0, 0, 0], STONE_DARK),
    level >= 2 && rock('ThighPlate', [0.3, 0.8, 0.9], [0.55, 1.4, 0], [0, 0, -6], STONE_LIGHT),
    level >= 2 && crack('LegCrack', [0.1, 0.45, -0.69], 20),
    level >= 3 && rock('Toe', [1.0, 0.4, 0.5], [0, 0.2, -0.85], [0, 0, 0], STONE_DARK),
  ].filter(Boolean)));

  const shoulderCrystals = (lvl) => [
    crystal('ShoulderCrystal1', [0.1, 0.5, -0.1], [-12, 0, -22], [0.9, 1.3, 1.9][lvl - 1], [0.28, 0.32, 0.4][lvl - 1]),
    crystal('ShoulderCrystal2', [-0.3, 0.5, 0.3], [12, 0, -6], [0.7, 1.0, 1.5][lvl - 1], [0.24, 0.28, 0.34][lvl - 1]),
    lvl >= 2 && crystal('ShoulderCrystal3', [0.4, 0.45, 0.35], [15, 0, -45], [0.6, 0.8, 1.3][lvl - 1], 0.24),
    lvl >= 3 && crystal('ShoulderCrystal4', [-0.1, 0.5, -0.45], [-30, 0, -15], 1.1, 0.28),
  ].filter(Boolean);

  const arms = mirror(group([1.75, 1.6, 0], [0, 0, 8], [
    rock('UpperArm', [0.8, 1.0, 0.8], [0, -0.6, 0]),
    rock('Forearm', [1.15, 1.25, 1.15], [0, -1.65, -0.05]),
    rock('ForearmPlate', [0.3, 0.9, 1.0], [0.6, -1.6, 0], [0, 0, -5], STONE_LIGHT),
    rock('Fist', [1.05, 0.65, 1.05], [0, -2.55, -0.05], [0, 0, 0], STONE_DARK),
    rock('Knuckles', [1.1, 0.35, 0.3], [0, -2.45, -0.6], [0, 0, 0], STONE_LIGHT),
    level >= 2 && crystal('ArmCrystal1', [0.6, -1.2, 0], [0, 0, -35], level === 3 ? 1.2 : 0.6, level === 3 ? 0.3 : 0.2),
    level >= 2 && crystal('ArmCrystal2', [0.6, -1.5, -0.3], [-20, 0, -55], level === 3 ? 0.9 : 0.45, level === 3 ? 0.24 : 0.16),
    level >= 3 && crack('ArmCrack', [0.1, -1.6, -0.64], -25),
  ].filter(Boolean)));

  const head = group([0, 2.3, -0.45], [0, 0, 0], [
    rock('Head', [1.25, 0.95, 1.15], [0, 0, 0]),
    rock('Brow', [1.35, 0.28, 0.42], [0, 0.35, -0.42], [-8, 0, 0], STONE_DARK),
    part('EyeSocket', 'Block', [0.9, 0.3, 0.05], [12, 14, 20], 'SmoothPlastic', [0, 0.05, -0.58]),
    mirror(part('Eye', 'Block', [0.22, 0.16, 0.05], GLOW, 'Neon', [0.27, 0.05, -0.61])),
    level >= 3 && mirror(part('Tusk', 'Block', [0.12, 0.22, 0.06], CRYSTAL_LIGHT, 'Neon', [0.15, -0.3, -0.6])),
  ].filter(Boolean));

  const torso = group([0, 2.2, 0], [0, 0, 0], [
    rock('Core', [2.6, 2.0, 1.7], [0, 1.0, 0]),
    rock('Belly', [1.6, 0.7, 0.3], [0, 0.4, -0.9], [0, 0, 0], STONE_DARK),
    mirror(rock('ChestSlab', [1.2, 0.85, 0.35], [0.6, 1.25, -0.9], [0, 0, -4], STONE_LIGHT)),
    mirror(rock('SideSlab', [0.4, 1.3, 1.4], [1.38, 0.9, 0])),
    rock('BackSlab', [2.0, 1.4, 0.35], [0, 1.2, 0.9]),
    head,
    mirror(group([1.6, 1.85, 0], [0, 0, -10], [
      rock('Shoulder', [1.35, 1.1, 1.45], [0, 0, 0]),
      level >= 2 && rock('ShoulderTop', [1.0, 0.45, 1.1], [0.1, 0.65, 0], [0, 0, 0], STONE_LIGHT),
      ...shoulderCrystals(level),
    ].filter(Boolean))),
    level >= 2 && crack('ChestCrack1', [0.45, 1.2, -1.09], 25),
    level >= 2 && crack('ChestCrack2', [-0.5, 0.35, -1.06], -15),
    level >= 3 && crack('ChestCrack3', [-0.75, 1.3, -1.09], 15),
    level >= 3 && crack('BellyCrack', [0.3, 0.3, -1.06], -30),
    // crystal heart (boss): diamond in a dark frame + strap
    ...(level >= 3 ? [
      part('HeartFrame', 'Block', [1.15, 1.15, 0.2], [20, 24, 32], 'Slate', [0, 1.05, -1.12], [0, 0, 45]),
      part('Heart', 'Block', [0.85, 0.85, 0.24], CRYSTAL, 'Neon', [0, 1.05, -1.15], [0, 0, 45], 10),
      part('HeartCore', 'Block', [0.42, 0.42, 0.26], CRYSTAL_LIGHT, 'Neon', [0, 1.05, -1.17], [0, 0, 45]),
      part('Strap', 'Block', [0.14, 1.3, 0.1], [20, 24, 32], 'Slate', [0.62, 1.78, -1.12], [0, 0, 40]),
      // big crystal crown growing from the back
      crystal('BackCrystal1', [0, 1.8, 0.75], [-12, 0, 0], 2.6, 0.45),
      crystal('BackCrystal2', [0.35, 1.7, 0.85], [-5, 0, -18], 2.0, 0.38),
      crystal('BackCrystal3', [-0.35, 1.7, 0.85], [-5, 0, 18], 2.1, 0.38),
      crystal('BackCrystal4', [0.15, 1.75, 0.95], [-20, 0, -8], 1.6, 0.3),
      crystal('BackCrystal5', [-0.6, 1.6, 0.7], [-15, 0, 35], 1.3, 0.3),
      crystal('BackCrystal6', [0.65, 1.6, 0.7], [-15, 0, -35], 1.4, 0.3),
    ] : [
      crystal('BackCrystal1', [0.3, 1.8, 0.7], [-15, 0, -10], level === 2 ? 1.2 : 0.6, level === 2 ? 0.3 : 0.2),
    ]),
  ].filter(Boolean));

  return [
    legs,
    rock('Hips', [2.3, 0.75, 1.45], [0, 1.95, 0], [0, 0, 0], STONE_DARK),
    level >= 2 && rock('HipFront', [1.2, 0.55, 0.3], [0, 1.8, -0.8], [0, 0, 0], STONE_LIGHT),
    torso,
    arms,
  ].filter(Boolean).flat(Infinity);
}

const sized = (level, s, seed) => golem(level, seed).map((n) => scale(n, s));

exportCreatures([
  { name: 'Crystal Golem Weakling', stage: 1, health: 60, offset: [23, 0, 0], parts: sized(1, 1, 11) },
  { name: 'Crystal Golem', stage: 2, health: 300, offset: [8, 0, 0], parts: sized(2, 1.75, 22) },
  { name: 'Crystal Titan', stage: 3, health: 3500, offset: [-10, 0, 0], parts: sized(3, 2.8, 33) },
], { title: 'Crystal Cave Golems', source: 'golems.mjs', jsonFile: 'golems.json', luaFile: 'CrystalGolems.server.lua' });
