// Phantom Wraiths: Wisp -> Wraith -> Wraith King (boss).
// Smooth floating hooded ghosts: stacked oval robes, glowing eyes in a dark hood, bone claws.
// node wraiths.mjs -> wraiths.json + PhantomWraiths.server.lua
import { part, group, mirror, scale, exportCreatures, rng } from './lib.mjs';

const ROBE = [52, 44, 78], ROBE_DARK = [30, 24, 48], ROBE_LIGHT = [84, 72, 120];
const SPIRIT = [150, 95, 255], SOUL = [80, 255, 205], BONE = [222, 216, 200], VOID = [8, 6, 14];

function wraith(level, seed) {
  const rand = rng(seed);
  const shade = (c) => { const d = (rand() * 2 - 1) * 5; return c.map((v) => Math.round(v + d)); };
  const oval = (name, size, pos, rot = [0, 0, 0], color = ROBE, mat = 'Fabric') => part(name, 'Ellipsoid', size, shade(color), mat, pos, rot);
  const glow = (name, size, pos, rot = [0, 0, 0], color = SPIRIT, light = 0) => part(name, 'Ellipsoid', size, color, 'Neon', pos, rot, light);
  const orb = (name, d, pos, color = SOUL, light = 0) => part(name, 'Ball', [d, d, d], color, 'Neon', pos, [0, 0, 0], light);
  const H = 0.7; // hover height: the whole ghost floats off the floor

  // ragged strips hanging round the bottom of the robe
  const tatters = (count, y, radius, len) => Array.from({ length: count }, (_, i) => {
    const a = (i / count) * Math.PI * 2 + 0.3;
    const deg = (a * 180) / Math.PI;
    return group([Math.sin(a) * radius, y, Math.cos(a) * radius], [0, deg, 0], [
      oval('Tatter' + (i + 1), [0.3, len, 0.14], [0, -len / 2, 0], [12, 0, 0], ROBE_DARK),
    ]);
  });

  const claws = (tipGlow) => [-0.13, 0, 0.13].map((x, i) => group([x, -1.35, -0.05], [10, 0, x * -60], [
    oval('Claw' + (i + 1), [0.1, 0.6, 0.1], [0, -0.3, 0], [0, 0, 0], BONE, 'SmoothPlastic'),
    tipGlow && glow('ClawTip' + (i + 1), [0.07, 0.18, 0.07], [0, -0.58, 0], [0, 0, 0], SOUL),
  ].filter(Boolean)));

  const arm = group([0.95, 2.45 + H, -0.1], [30, 0, 20], [
    oval('Sleeve', [0.62, 1.25, 0.62], [0, -0.55, 0]),
    oval('Cuff', [0.78, 0.32, 0.78], [0, -1.12, 0], [0, 0, 0], ROBE_LIGHT),
    oval('Hand', [0.3, 0.3, 0.3], [0, -1.28, 0], [0, 0, 0], BONE, 'SmoothPlastic'),
    claws(level >= 2),
    level >= 2 && glow('SleeveRune', [0.66, 0.1, 0.66], [0, -0.75, 0]),
  ].filter(Boolean));

  const face = [
    oval('HoodRim', [1.3, 1.35, 0.3], [0, 2.95 + H, -0.55], [0, 0, 0], ROBE_LIGHT),
    part('FaceVoid', 'Ellipsoid', [1.05, 1.12, 0.4], VOID, 'SmoothPlastic', [0, 2.92 + H, -0.62]),
    mirror(orb('Eye', level === 3 ? 0.28 : 0.22, [0.22, 3.02 + H, -0.79])),
    level >= 2 && glow('Mouth', [0.42, 0.08, 0.05], [0, 2.62 + H, -0.81], [0, 0, 0], SOUL),
    level >= 3 && orb('ThirdEye', 0.16, [0, 3.3 + H, -0.74], SPIRIT),
  ];

  const body = [
    oval('Hood', [1.5, 1.6, 1.5], [0, 3.0 + H, 0]),
    oval('HoodPeak', [0.7, 0.95, 0.7], [0, 3.75 + H, 0.35], [35, 0, 0]),
    oval('Shoulders', [2.0, 1.3, 1.4], [0, 2.2 + H, 0]),
    oval('Robe1', [1.8, 1.0, 1.3], [0, 1.6 + H, 0]),
    oval('Robe2', [1.5, 1.0, 1.1], [0, 1.05 + H, 0], [0, 0, 0], ROBE_DARK),
    oval('Robe3', [1.1, 0.9, 0.85], [0, 0.55 + H, 0.05]),
    oval('RobeTail', [0.5, 0.85, 0.42], [0, 0.1 + H, 0.3], [-35, 0, 0], ROBE_DARK),
    tatters(level === 1 ? 5 : 8, 1.2 + H, 0.65, level === 3 ? 1.4 : 1.0),
    level === 1 && orb('SoulCore', 0.3, [0, 2.2 + H, -0.68], SPIRIT),
    level >= 2 && glow('SpiritBelt', [1.86, 0.12, 1.36], [0, 1.95 + H, 0]),
    level >= 2 && glow('RobeRune', [1.54, 0.1, 1.14], [0, 1.15 + H, 0]),
    face,
    mirror(arm),
  ];

  const boss = level < 3 ? [] : [
    // spectral crown: dark band + glowing spikes around the hood
    oval('CrownBand', [1.3, 0.22, 1.3], [0, 3.6 + H, 0], [0, 0, 0], ROBE_DARK),
    ...Array.from({ length: 6 }, (_, i) => {
      const a = ((i + 0.5) / 6) * Math.PI * 2;
      return glow('CrownSpike' + (i + 1), [0.14, 0.6, 0.14], [Math.sin(a) * 0.62, 3.95 + H, Math.cos(a) * 0.62], [Math.cos(a) * 15, 0, -Math.sin(a) * 15]);
    }),
    glow('CrownGem', [0.24, 0.32, 0.12], [0, 3.62 + H, -0.78], [0, 0, 0], SOUL),
    // bone shoulder guards with spikes
    mirror(group([0.95, 2.75 + H, 0], [0, 0, -25], [
      oval('Pauldron', [0.9, 0.5, 1.0], [0, 0, 0], [0, 0, 0], BONE, 'SmoothPlastic'),
      oval('PauldronSpike1', [0.16, 0.7, 0.16], [0.15, 0.45, -0.2], [-10, 0, -15], BONE, 'SmoothPlastic'),
      oval('PauldronSpike2', [0.14, 0.55, 0.14], [0.05, 0.38, 0.25], [15, 0, -5], BONE, 'SmoothPlastic'),
    ])),
    // glowing heart showing through ribs
    orb('Heart', 0.5, [0, 2.2 + H, -0.62], SPIRIT, 9),
    ...[0.3, 0.05, -0.2].map((dy, i) => oval('Rib' + (i + 1), [1.1 - i * 0.12, 0.08, 0.08], [0, 2.2 + H + dy, -0.72], [0, 0, 0], BONE, 'SmoothPlastic')),
    // floating soul orbs circling the king
    ...[0, 1, 2, 3].map((i) => {
      const a = (i / 4) * Math.PI * 2 + Math.PI / 4;
      return orb('SoulOrb' + (i + 1), 0.35, [Math.sin(a) * 2.0, 2.4 + H + (i % 2) * 0.6, Math.cos(a) * 1.4], SOUL);
    }),
    // scythe in the right hand (same joint as the right arm, then straightened up)
    group([0.95, 2.45 + H, -0.1], [30, 0, 20], [group([0, -1.28, 0], [-30, 0, -20], [
      part('ScytheHandle', 'Cylinder', [5.6, 0.16, 0.16], ROBE_DARK, 'Wood', [0, 0.8, 0], [0, 0, 90]),
      oval('ScytheCap', [0.3, 0.3, 0.3], [0, -2.0, 0], [0, 0, 0], BONE, 'SmoothPlastic'),
      oval('ScytheCollar', [0.3, 0.4, 0.3], [0, 3.5, 0], [0, 0, 0], BONE, 'SmoothPlastic'),
      group([0, 3.55, 0], [0, 0, 0], [
        oval('Blade1', [1.3, 0.38, 0.1], [0.62, 0, 0], [0, 0, -8], [150, 160, 175], 'Metal'),
        glow('BladeEdge1', [1.2, 0.08, 0.11], [0.62, -0.18, 0], [0, 0, -8], SOUL),
        group([1.25, -0.15, 0], [0, 0, -28], [
          oval('Blade2', [1.0, 0.3, 0.09], [0.48, 0, 0], [0, 0, 0], [150, 160, 175], 'Metal'),
          glow('BladeEdge2', [0.95, 0.07, 0.1], [0.48, -0.14, 0], [0, 0, 0], SOUL),
          group([0.95, 0, 0], [0, 0, -32], [
            oval('Blade3', [0.75, 0.2, 0.08], [0.35, 0, 0], [0, 0, 0], [150, 160, 175], 'Metal'),
            glow('BladeEdge3', [0.7, 0.06, 0.09], [0.35, -0.09, 0], [0, 0, 0], SOUL),
          ]),
        ]),
      ]),
    ])]),
  ];

  return [body, boss].flat(Infinity).filter(Boolean);
}

const sized = (level, s, seed) => wraith(level, seed).map((n) => scale(n, s));

exportCreatures([
  { name: 'Wisp', stage: 1, health: 45, offset: [29, 0, 0], parts: sized(1, 1.3, 3) },
  { name: 'Phantom Wraith', stage: 2, health: 260, offset: [15, 0, 0], parts: sized(2, 2.2, 4) },
  { name: 'Wraith King', stage: 3, health: 3300, offset: [-4, 0, 0], parts: sized(3, 3.8, 5) },
], { title: 'Phantom Wraiths', source: 'wraiths.mjs', jsonFile: 'wraiths.json', luaFile: 'PhantomWraiths.server.lua' });
