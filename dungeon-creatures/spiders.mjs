// Magma Spiders: Spiderling -> Magma Spider -> Brood Queen (boss).
// Basalt-rock bodies with glowing lava cracks, eye clusters and 8 legs.
// node spiders.mjs -> spiders.json + MagmaSpiders.server.lua
import { part, group, mirror, scale, exportCreatures, rng } from './lib.mjs';

const BASALT = [96, 80, 74], BASALT_DARK = [58, 48, 45], BASALT_LIGHT = [128, 104, 92];
const LAVA = [255, 125, 25], LAVA_LIGHT = [255, 205, 90], EYE = [255, 60, 25];

function spider(level, seed) {
  const rand = rng(seed);
  const j = (amount) => (rand() * 2 - 1) * amount;
  const shade = (c, amount = 8) => { const d = j(amount); return c.map((v) => Math.round(v + d)); };
  const rock = (name, size, pos, rot = [0, 0, 0], color = BASALT) =>
    part(name, 'Block', size, shade(color), 'Basalt', pos, [rot[0] + j(4), rot[1] + j(4), rot[2] + j(4)]);
  const lava = (name, size, pos, rot = [0, 0, 0], color = LAVA) => part(name, 'Block', size, color, 'Neon', pos, rot);
  const spike = (name, pos, rot, len, w, color = BASALT_DARK) => group(pos, rot, [
    rock(name, [w, len, w], [0, len / 2, 0], [0, 0, 0], color),
    part(name + 'Tip', 'Block', [w * 0.6, w * 0.8, w * 0.6], level === 3 ? LAVA : BASALT_LIGHT, level === 3 ? 'Neon' : 'Basalt', [0, len + w * 0.3, 0]),
  ]);

  // one leg, pointing out along +X from the hip: thigh goes up, shin comes down to the floor
  const leg = (n, pos, yaw) => group(pos, [0, yaw, 0], [
    group([0, 0, 0], [0, 0, 40], [
      rock('Thigh' + n, [1.45, 0.34, 0.34], [0.7, 0, 0]),
      level >= 2 && lava('ThighCrack' + n, [0.6, 0.06, 0.36], [0.75, 0.05, 0]),
      level >= 3 && spike('LegSpike' + n, [0.9, 0.15, 0], [0, 0, 20], 0.5, 0.16),
      rock('Knee' + n, [0.48, 0.48, 0.48], [1.42, 0, 0], [0, 0, 0], BASALT_DARK),
      group([1.42, 0, 0], [0, 0, -110], [
        rock('Shin' + n, [1.85, 0.28, 0.28], [0.92, 0, 0]),
        lava('Claw' + n, [0.3, 0.2, 0.2], [1.9, 0, 0], [0, 0, 0], level >= 2 ? LAVA : BASALT_LIGHT),
      ]),
    ].filter(Boolean)),
  ]);

  const eyes = [
    mirror(lava('Eye', [0.24, 0.2, 0.06], [0.22, 1.24, -2.04], [0, 0, 0], EYE)),
    mirror(lava('SmallEye', [0.14, 0.12, 0.06], [0.44, 1.38, -2.03], [0, 0, 0], EYE)),
    level >= 2 && mirror(lava('TopEye', [0.12, 0.1, 0.06], [0.1, 1.44, -2.04], [0, 0, 0], EYE)),
    level >= 3 && mirror(lava('BrowEye', [0.1, 0.08, 0.06], [0.34, 1.5, -2.03], [0, 0, 0], EYE)),
  ];

  const abdomen = group([0, 1.55, 1.35], [-12, 0, 0], [
    rock('Abdomen', [2.2, 1.7, 2.5], [0, 0, 0]),
    rock('AbdomenTop', [1.7, 0.4, 1.9], [0, 0.95, 0.1], [0, 0, 0], BASALT_LIGHT),
    rock('AbdomenBack', [1.6, 1.3, 0.35], [0, -0.05, 1.35], [0, 0, 0], BASALT_DARK),
    mirror(rock('AbdomenSide', [0.3, 1.2, 1.9], [1.2, 0, 0.1])),
    lava('LavaStripe1', [1.2, 0.08, 0.14], [0, 1.16, -0.4]),
    lava('LavaStripe2', [1.0, 0.08, 0.14], [0, 1.16, 0.25]),
    level >= 2 && lava('LavaStripe3', [0.8, 0.08, 0.14], [0, 1.16, 0.85]),
    level >= 2 && lava('BackCrack', [0.08, 0.9, 0.06], [0.3, 0, 1.54], [0, 0, 20]),
    level >= 2 && spike('BackSpike1', [-0.45, 1.1, -0.3], [-15, 0, 15], 0.7, 0.22),
    level >= 2 && spike('BackSpike2', [0.45, 1.1, -0.3], [-15, 0, -15], 0.7, 0.22),
    ...(level >= 3 ? [
      // glowing egg-sac core on the back, framed in dark rock
      part('CoreFrame', 'Block', [1.25, 0.15, 1.25], BASALT_DARK, 'Basalt', [0, 1.2, 0.3], [0, 45, 0]),
      part('Core', 'Block', [0.9, 0.2, 0.9], LAVA, 'Neon', [0, 1.24, 0.3], [0, 45, 0], 10),
      part('CoreInner', 'Block', [0.45, 0.22, 0.45], LAVA_LIGHT, 'Neon', [0, 1.26, 0.3], [0, 45, 0]),
      spike('BackSpike3', [0, 1.1, -0.75], [-25, 0, 0], 1.0, 0.26),
      spike('BackSpike4', [-0.6, 1.0, 0.8], [15, 0, 25], 0.8, 0.22),
      spike('BackSpike5', [0.6, 1.0, 0.8], [15, 0, -25], 0.8, 0.22),
      ...[-0.5, 0, 0.5].map((x, i) => part('EggSac' + (i + 1), 'Ball', [0.38, 0.38, 0.38], LAVA_LIGHT, 'Neon', [x, -0.55, 1.45])),
    ] : []),
  ].filter(Boolean));

  return [
    rock('Thorax', [1.7, 0.95, 1.7], [0, 1.1, -0.45]),
    rock('ThoraxTop', [1.2, 0.3, 1.2], [0, 1.65, -0.45], [0, 0, 0], BASALT_LIGHT),
    rock('Head', [1.25, 0.85, 0.95], [0, 1.2, -1.5]),
    rock('Brow', [1.35, 0.25, 0.4], [0, 1.6, -1.75], [-10, 0, 0], BASALT_DARK),
    part('Face', 'Block', [1.1, 0.5, 0.05], [18, 12, 12], 'SmoothPlastic', [0, 1.3, -2.0]),
    eyes,
    mirror(group([0.27, 0.85, -1.85], [-20, 0, -8], [
      rock('Fang', [0.26, 0.6, 0.26], [0, -0.25, 0], [0, 0, 0], BASALT_DARK),
      lava('FangTip', [0.14, 0.24, 0.14], [0, -0.62, -0.02], [0, 0, 0], level >= 2 ? LAVA : BASALT_LIGHT),
    ])),
    level >= 2 && lava('ThoraxCrack', [0.07, 0.6, 0.05], [0.35, 1.1, -1.31], [0, 0, 30]),
    // queen: crown of obsidian spikes + big pincers
    ...(level >= 3 ? [
      ...[-0.45, -0.15, 0.15, 0.45].map((x, i) => spike('CrownSpike' + (i + 1), [x, 1.65, -1.45], [-45, 0, x * -40], i === 1 || i === 2 ? 0.5 : 0.35, 0.14)),
      mirror(group([0.6, 0.8, -1.8], [-15, 20, 0], [
        rock('Pincer', [0.22, 0.22, 0.75], [0, 0, -0.35]),
        rock('PincerClaw', [0.18, 0.18, 0.45], [-0.12, 0, -0.85], [0, -40, 0], BASALT_DARK),
        lava('PincerTip', [0.1, 0.1, 0.16], [-0.28, 0, -1.05], [0, -40, 0]),
      ])),
    ] : []),
    abdomen,
    [leg(1, [0.75, 1.1, -0.95], 42), leg(2, [0.8, 1.1, -0.5], 14), leg(3, [0.8, 1.1, -0.05], -14), leg(4, [0.75, 1.1, 0.4], -42)].map(mirror),
  ].flat(Infinity).filter(Boolean);
}

const sized = (level, s, seed) => spider(level, seed).map((n) => scale(n, s));

exportCreatures([
  { name: 'Ember Spiderling', stage: 1, health: 40, offset: [28, 0, 0], parts: sized(1, 1.2, 7) },
  { name: 'Magma Spider', stage: 2, health: 280, offset: [14, 0, 0], parts: sized(2, 2.3, 8) },
  { name: 'Brood Queen', stage: 3, health: 3200, offset: [-8, 0, 0], parts: sized(3, 4.2, 9) },
], { title: 'Magma Spiders', source: 'spiders.mjs', jsonFile: 'spiders.json', luaFile: 'MagmaSpiders.server.lua' });
