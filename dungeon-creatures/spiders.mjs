// Magma Spiders: Spiderling -> Magma Spider -> Brood Queen (boss).
// Smooth rounded basalt bodies (ovals, balls, cylinder legs) with glowing lava bands and eye clusters.
// node spiders.mjs -> spiders.json + MagmaSpiders.server.lua
import { part, group, mirror, scale, exportCreatures, rng } from './lib.mjs';

const BASALT = [74, 58, 54], BASALT_DARK = [42, 34, 33], BASALT_LIGHT = [104, 82, 74];
const LAVA = [255, 125, 25], LAVA_LIGHT = [255, 205, 90], EYE = [255, 60, 25];

function spider(level, seed) {
  const rand = rng(seed);
  const shade = (c) => { const d = (rand() * 2 - 1) * 6; return c.map((v) => Math.round(v + d)); };
  const oval = (name, size, pos, rot = [0, 0, 0], color = BASALT) => part(name, 'Ellipsoid', size, shade(color), 'Basalt', pos, rot);
  const glowOval = (name, size, pos, rot = [0, 0, 0], color = LAVA) => part(name, 'Ellipsoid', size, color, 'Neon', pos, rot);
  const ball = (name, d, pos, color = BASALT_DARK) => part(name, 'Ball', [d, d, d], shade(color), 'Basalt', pos);
  const eye = (name, d, pos) => part(name, 'Ball', [d, d, d], EYE, 'Neon', pos);
  const cyl = (name, len, d, pos, color = BASALT) => part(name, 'Cylinder', [len, d, d], shade(color), 'Basalt', pos);
  const ring = (name, d, pos) => part(name, 'Cylinder', [0.1, d, d], LAVA, 'Neon', pos);
  // spike: long pointed oval, lava tip on the boss
  const spike = (name, pos, rot, len, w) => group(pos, rot, [
    oval(name, [w, len, w], [0, len / 2, 0], [0, 0, 0], BASALT_DARK),
    level === 3 && glowOval(name + 'Tip', [w * 0.5, len * 0.3, w * 0.5], [0, len * 0.85, 0]),
  ].filter(Boolean));
  // lava band around the abdomen at depth z (sized to the oval's cross-section there)
  const band = (name, z) => {
    const f = Math.sqrt(1 - (z / 1.45) ** 2) * 1.04;
    return glowOval(name, [2.4 * f, 1.9 * f, 0.28], [0, 0, z]);
  };

  // one leg pointing out along +X from the hip: thigh goes up, shin comes down to the floor
  const leg = (n, pos, yaw) => group(pos, [0, yaw, 0], [
    ball('Hip' + n, 0.34, [0, 0, 0]),
    group([0, 0, 0], [0, 0, 40], [
      cyl('Thigh' + n, 1.5, 0.26, [0.75, 0, 0]),
      level >= 2 && ring('ThighBand' + n, 0.29, [0.95, 0, 0]),
      level >= 3 && spike('LegSpike' + n, [0.8, 0.12, 0], [0, 0, 25], 0.5, 0.14),
      ball('Knee' + n, 0.34, [1.48, 0, 0]),
      group([1.48, 0, 0], [0, 0, -110], [
        cyl('Shin' + n, 1.85, 0.2, [0.92, 0, 0]),
        level >= 2 && ring('ShinBand' + n, 0.23, [1.2, 0, 0]),
        part('Claw' + n, 'Ellipsoid', [0.5, 0.17, 0.17], level >= 2 ? LAVA : BASALT_LIGHT, level >= 2 ? 'Neon' : 'Basalt', [1.85, 0, 0]),
      ].filter(Boolean)),
    ].filter(Boolean)),
  ]);

  const abdomen = group([0, 1.6, 1.4], [-12, 0, 0], [
    oval('Abdomen', [2.4, 1.9, 2.9], [0, 0, 0]),
    oval('AbdomenTop', [1.6, 0.5, 2.0], [0, 0.78, 0.05], [0, 0, 0], BASALT_LIGHT),
    band('LavaBand1', -0.55),
    band('LavaBand2', 0.2),
    level >= 2 && band('LavaBand3', 0.9),
    level >= 2 && spike('BackSpike1', [-0.45, 0.8, -0.4], [-20, 0, 18], 0.75, 0.2),
    level >= 2 && spike('BackSpike2', [0.45, 0.8, -0.4], [-20, 0, -18], 0.75, 0.2),
    ...(level >= 3 ? [
      // glowing egg core on the back in a dark rim
      oval('CoreRim', [1.35, 0.4, 1.35], [0, 0.88, 0.35], [0, 0, 0], BASALT_DARK),
      glowOval('Core', [1.0, 0.36, 1.0], [0, 0.97, 0.35]),
      part('CoreInner', 'Ellipsoid', [0.5, 0.3, 0.5], LAVA_LIGHT, 'Neon', [0, 1.06, 0.35], [0, 0, 0], 10),
      spike('BackSpike3', [0, 0.85, -0.75], [-30, 0, 0], 1.0, 0.24),
      spike('BackSpike4', [-0.6, 0.75, 0.9], [20, 0, 25], 0.8, 0.2),
      spike('BackSpike5', [0.6, 0.75, 0.9], [20, 0, -25], 0.8, 0.2),
      ...[-0.45, 0, 0.45].map((x, i) => part('EggSac' + (i + 1), 'Ball', [0.42, 0.42, 0.42], LAVA_LIGHT, 'Neon', [x, -0.45, 1.3])),
    ] : []),
  ].filter(Boolean));

  return [
    oval('Thorax', [1.8, 1.0, 1.9], [0, 1.15, -0.45]),
    oval('ThoraxTop', [1.3, 0.4, 1.4], [0, 1.55, -0.45], [0, 0, 0], BASALT_LIGHT),
    oval('Head', [1.35, 1.0, 1.1], [0, 1.25, -1.45]),
    mirror(eye('Eye', 0.28, [0.22, 1.38, -1.93])),
    mirror(eye('SmallEye', 0.16, [0.45, 1.5, -1.76])),
    level >= 2 && mirror(eye('TopEye', 0.13, [0.12, 1.6, -1.83])),
    level >= 3 && mirror(eye('BrowEye', 0.11, [0.33, 1.62, -1.7])),
    mirror(group([0.25, 0.9, -1.85], [-20, 0, -8], [
      oval('Fang', [0.28, 0.75, 0.28], [0, -0.25, 0], [0, 0, 0], BASALT_DARK),
      part('FangTip', 'Ellipsoid', [0.14, 0.3, 0.14], level >= 2 ? LAVA : BASALT_LIGHT, level >= 2 ? 'Neon' : 'Basalt', [0, -0.62, 0]),
    ])),
    level >= 2 && glowOval('ThoraxBand', [1.84, 0.12, 1.94], [0, 1.15, -0.45]),
    // queen: crown of spikes + pincers
    ...(level >= 3 ? [
      ...[-0.45, -0.15, 0.15, 0.45].map((x, i) => spike('CrownSpike' + (i + 1), [x, 1.6, -1.4], [-45, 0, x * -40], i === 1 || i === 2 ? 0.6 : 0.42, 0.14)),
      mirror(group([0.6, 0.85, -1.8], [-15, 20, 0], [
        oval('Pincer', [0.24, 0.24, 0.85], [0, 0, -0.35]),
        oval('PincerClaw', [0.2, 0.2, 0.55], [-0.12, 0, -0.85], [0, -40, 0], BASALT_DARK),
        glowOval('PincerTip', [0.1, 0.1, 0.22], [-0.3, 0, -1.07], [0, -40, 0]),
      ])),
    ] : []),
    abdomen,
    [leg(1, [0.75, 1.1, -0.95], 42), leg(2, [0.82, 1.1, -0.5], 14), leg(3, [0.82, 1.1, -0.05], -14), leg(4, [0.75, 1.1, 0.4], -42)].map(mirror),
  ].flat(Infinity).filter(Boolean);
}

const sized = (level, s, seed) => spider(level, seed).map((n) => scale(n, s));

exportCreatures([
  { name: 'Ember Spiderling', stage: 1, health: 40, offset: [28, 0, 0], parts: sized(1, 1.2, 7) },
  { name: 'Magma Spider', stage: 2, health: 280, offset: [14, 0, 0], parts: sized(2, 2.3, 8) },
  { name: 'Brood Queen', stage: 3, health: 3200, offset: [-8, 0, 0], parts: sized(3, 4.2, 9) },
], { title: 'Magma Spiders', source: 'spiders.mjs', jsonFile: 'spiders.json', luaFile: 'MagmaSpiders.server.lua' });
