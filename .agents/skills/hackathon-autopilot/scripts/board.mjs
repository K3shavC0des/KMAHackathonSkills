import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, sep } from 'node:path';
import { randomUUID } from 'node:crypto';

// One shared Git branch provides serialized updates across independent machines.
const branch = 'hackathon-board';
const request = JSON.parse(readFileSync(0, 'utf8'));
const requestId = request.request_id || randomUUID();
const temporaryRoot = resolve(tmpdir());
const directory = mkdtempSync(join(temporaryRoot, 'hackathon-board-'));
const actor = request.actor;

function git(args, cwd = directory) {
  return execFileSync('git', args, {
    cwd, encoding: 'utf8', timeout: 30000,
    env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}

function text(value, label, limit = 1200) {
  requireCondition(typeof value === 'string' && value.length > 0 && value.length <= limit,
    `${label} must contain 1-${limit} characters`);
  return value;
}

function overlaps(left, right) {
  return left === right || left.startsWith(`${right}/`) || right.startsWith(`${left}/`);
}

function mutate(state) {
  if (state.applied.includes(requestId)) return state;
  const task = Object.hasOwn(state.tasks, request.task) ? state.tasks[request.task] : undefined;
  switch (request.action) {
    case 'init':
      break;
    case 'task': {
      requireCondition(!task, 'Task already exists');
      requireCondition(/^[a-z0-9-]{1,64}$/.test(request.task), 'Use a lowercase task slug');
      requireCondition(Array.isArray(request.paths) && request.paths.length > 0, 'Supply owned paths');
      for (const path of request.paths) {
        requireCondition(typeof path === 'string' && /^[a-zA-Z0-9_.\/-]+$/.test(path)
          && !path.startsWith('/') && !path.includes('..') && !path.includes('//'), 'Invalid owned path');
        for (const existing of Object.values(state.tasks).filter(item => item.status !== 'done')) {
          requireCondition(!existing.paths.some(other => overlaps(path, other)), `Path overlaps ${existing.id}`);
        }
      }
      state.tasks[request.task] = {
        id: request.task, owner: text(request.owner ?? actor, 'owner', 80),
        goal: text(request.goal, 'goal'), acceptance: text(request.acceptance, 'acceptance'),
        paths: request.paths, status: 'queued', evidence: '',
      };
      break;
    }
    case 'start':
    case 'claim':
    case 'review':
    case 'done':
    case 'blocked': {
      requireCondition(task, 'Unknown task');
      const allowed = { start: ['queued', 'blocked'], claim: ['queued', 'blocked'], review: ['working'], done: ['review'], blocked: ['queued', 'working', 'review'] };
      requireCondition(allowed[request.action].includes(task.status), `Cannot ${request.action} from ${task.status}`);
      if (request.action === 'start' || request.action === 'claim') task.owner = actor;
      task.status = { start: 'working', claim: 'working', review: 'review', done: 'done', blocked: 'blocked' }[request.action];
      task.evidence = text(request.evidence, 'evidence');
      break;
    }
    case 'post':
      state.messages.push({ id: requestId, from: actor, to: text(request.to, 'recipient', 80),
        task: request.task || null, body: text(request.body, 'body'), at: new Date().toISOString() });
      break;
    default:
      throw new Error('Unknown action');
  }
  state.applied.push(requestId);
  return state;
}

try {
  text(actor, 'actor', 80);
  requireCondition(typeof requestId === 'string' && requestId.length <= 100, 'Invalid request_id');
  const remote = git(['remote', 'get-url', 'origin'], process.cwd());
  const origin = /^[a-z][a-z0-9+.-]*:\/\//i.test(remote) || /^[^/]+@[^:]+:/.test(remote) ? remote : resolve(remote);
  git(['init', '--quiet']);
  git(['remote', 'add', 'origin', origin]);
  git(['config', 'user.name', 'Hackathon Board']);
  git(['config', 'user.email', 'hackathon-board@users.noreply.github.com']);
  let completed = false;
  for (let attempt = 0; attempt < 5; attempt++) {
    const exists = git(['ls-remote', '--heads', 'origin', `refs/heads/${branch}`]);
    let state;
    if (exists) {
      git(['fetch', '--quiet', '--depth=1', 'origin', branch]);
      git(['checkout', '--quiet', '-B', branch, 'FETCH_HEAD']);
      state = JSON.parse(readFileSync(join(directory, 'board.json'), 'utf8'));
    } else {
      requireCondition(request.action === 'init', 'Initialize the board first');
      git(['symbolic-ref', 'HEAD', 'refs/heads/' + branch]);
      state = { version: 1, coordinator: actor, tasks: {}, messages: [], applied: [] };
    }
    if (request.action === 'read') {
      let messages = state.messages.filter(message => message.to === actor || message.to === 'all');
      if (request.after) {
        const index = messages.findIndex(message => message.id === request.after);
        requireCondition(index >= 0, 'Unknown cursor for this recipient');
        messages = messages.slice(index + 1);
      }
      const page = messages.slice(0, 20);
      console.log(JSON.stringify({ mode: 'peer', coordinator: state.coordinator, tasks: state.tasks, messages: page,
        cursor: page.at(-1)?.id || request.after || null, has_more: messages.length > 20 }));
      completed = true;
      break;
    }
    if (state.applied.includes(requestId)) {
      console.log(JSON.stringify({ ok: true, request_id: requestId, already_applied: true }));
      completed = true;
      break;
    }
    writeFileSync(join(directory, 'board.json'), JSON.stringify(mutate(state), null, 2) + '\n');
    git(['add', 'board.json']);
    git(['commit', '--quiet', '-m', `board: ${request.action}`]);
    try {
      git(['push', '--quiet', 'origin', `HEAD:refs/heads/${branch}`]);
      console.log(JSON.stringify({ ok: true, request_id: requestId }));
      completed = true;
      break;
    } catch (error) {
      if (attempt === 4) throw error;
      // Re-read the winning state and reapply the same request ID after races.
    }
  }
  requireCondition(completed, 'Update did not complete');
} catch (error) {
  // Avoid printing remote URLs or Git diagnostics that could contain credentials.
  console.error(JSON.stringify({ ok: false, request_id: requestId,
    error: error.status !== undefined ? 'Git operation failed. Check access/network and retry the same request_id.' : error.message }));
  process.exitCode = 1;
} finally {
  const target = resolve(directory);
  if (target.startsWith(temporaryRoot + sep) && target !== temporaryRoot) {
    rmSync(target, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 });
  }
}
