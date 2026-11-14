import assert from 'node:assert/strict';
import { execFileSync, spawn, spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = mkdtempSync(join(tmpdir(), 'kma-peer-check-'));
const board = fileURLToPath(new URL('../.agents/skills/hackathon-autopilot/scripts/board.mjs', import.meta.url));

function git(args) {
  return execFileSync('git', args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

function call(cwd, request, expectedSuccess = true) {
  const result = spawnSync(process.execPath, [board], {
    cwd, input: JSON.stringify(request), encoding: 'utf8',
  });
  assert.equal(result.status === 0, expectedSuccess, result.stderr);
  return JSON.parse(result.status === 0 ? result.stdout : result.stderr);
}

function claim(cwd, actor) {
  return new Promise((resolveResult, reject) => {
    const child = spawn(process.execPath, [board], { cwd, stdio: ['pipe', 'pipe', 'pipe'] });
    child.stdout.resume();
    child.stderr.resume();
    child.on('error', reject);
    child.on('exit', code => resolveResult({ actor, code }));
    child.stdin.end(JSON.stringify({ actor, action: 'claim', task: 'race', evidence: 'Taking task' }));
  });
}

try {
  const origin = join(root, 'origin.git');
  const alice = join(root, 'alice');
  const bob = join(root, 'bob');
  git(['init', '--bare', origin]);
  git(['clone', origin, alice]);
  git(['clone', origin, bob]);
  call(alice, { actor: 'alice', action: 'init' });
  call(bob, { actor: 'bob', action: 'init' });
  call(bob, { actor: 'bob', action: 'task', task: 'demo', paths: ['app/demo'], goal: 'Demo', acceptance: 'Works' });
  assert.equal(call(alice, { actor: 'alice', action: 'read' }).tasks.demo.owner, 'bob');
  call(alice, { actor: 'alice', action: 'claim', task: 'demo', evidence: 'Taking work' });
  call(bob, { actor: 'bob', action: 'review', task: 'demo', evidence: 'PR tested' });
  call(bob, { actor: 'bob', action: 'done', task: 'demo', evidence: 'Integrated and verified' });
  call(alice, { actor: 'alice', action: 'task', task: 'race', owner: 'bob', paths: ['app/demo'], goal: 'Next demo', acceptance: 'Works' });
  const claims = await Promise.all([claim(alice, 'alice'), claim(bob, 'bob')]);
  assert.equal(claims.filter(result => result.code === 0).length, 1);
  const state = call(alice, { actor: 'alice', action: 'read' });
  assert.equal(state.mode, 'peer');
  assert.equal(state.coordinator, 'alice'); // Legacy initializer metadata remains readable.
  assert.equal(state.tasks.race.owner, claims.find(result => result.code === 0).actor);
  call(bob, { actor: 'bob', action: 'task', task: 'overlap', paths: ['app/demo/nested'], goal: 'Overlap', acceptance: 'Works' }, false);
  call(alice, { actor: 'alice', action: 'post', to: 'bob', body: 'Ready' });
  assert.equal(call(bob, { actor: 'bob', action: 'read' }).messages.at(-1).body, 'Ready');
  console.log('PASS: equal teammate actions, legacy board, messages, concurrent claims, and overlap protection');
} finally {
  if (resolve(root).startsWith(resolve(tmpdir()) + sep)) {
    rmSync(root, { recursive: true, force: true });
  }
}
