# Team coordination

Use the hackathon app repository's `origin` as the coordination remote. The board is a separate `hackathon-board` branch, with normal Git authentication and fast-forward pushes. Board messages are visible to everyone who can read the repo and remain in Git history. Recipient filters are inbox views. Use the board for task logistics and links. Keep credentials and private information out of it.

Everyone works as an equal teammate. Anyone can initialize the board, create or assign tasks, claim queued or blocked work, update progress, review, integrate, and mark verified work done. Every teammate can work on frontend, backend, shared contracts, lockfiles, and the checkpoint. Use task ownership to coordinate active edits and handoffs. Claim shared files before editing them and keep a separate branch/worktree for every parallel writer. Use one branch per task and name it `hackathon/<handle>/<task>`. Agree on contracts before parallel implementation.

Each human uses their own Git credentials and a consistent actor handle. The board's actor field is a coordination convention. Git repository access controls who can push. Existing boards work with these peer rules immediately when accessed through the updated script. The legacy `coordinator` field records who initialized the board and grants no special authority. Reads include `mode: "peer"`. Have every teammate use the updated script.

Run the script from any app checkout or worktree. Pipe one JSON request to it. These examples work in PowerShell and POSIX shells.

```sh
echo '{"actor":"keshav","action":"init"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
echo '{"actor":"teammate","action":"task","task":"demo","paths":["app/demo"],"goal":"Build the demo","acceptance":"Demo loads offline"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
echo '{"actor":"keshav","action":"claim","task":"demo","evidence":"Taking the demo task"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs

echo '{"actor":"teammate","action":"read"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
```

| Action | Required fields beyond actor/action |
| --- | --- |
| init | None |
| read | Optional `after` cursor from the prior response |
| task | `task`, `paths`, `goal`, `acceptance`, optional `owner` defaults to actor |
| claim, start | `task`, `evidence` — claims queued or blocked work for the actor and marks it working |
| blocked, review, done | `task`, `evidence` — any teammate can update progress |
| post | `to` (handle or `all`), `body`, optional `task` |

For writes, generate a unique `request_id` before the first attempt and reuse it when retrying the same operation. Keep the returned inbox cursor locally per actor. Read again at task start, on a dependency change, and before handing off. Fetch more pages while `has_more` is true. Avoid idle polling. Teammate sessions exchange updates through the board and PRs. Within each session, relay relevant updates to any workers it started.

Move a task to `review` with the PR URL, verification evidence, and integration notes. Include unresolved dependencies and assumptions. Any teammate can mark `done` after integrating and verifying. A working task stays claimed until it is blocked or handed off through a coordinated status update. Concurrent claims are serialized by Git pushes so one claim wins. If the board is unavailable, use the existing issue tracker or an agreed task list and keep the same ownership and handoff protocol.
