# Team coordination

Use the hackathon app repository's `origin` as the coordination remote. The board is a separate `hackathon-board` branch, with normal Git authentication and fast-forward pushes. Board messages are visible to everyone who can read the repo and remain in Git history. Recipient filters are inbox views. Use the board for task logistics and links. Keep credentials and private information out of it.

One integration lead initializes the board, assigns nonoverlapping paths and verifies integrated work. Each human uses their own Git credentials and a consistent actor handle. The board's actor field is a coordination convention. Git repository access controls who can push. Only the lead edits shared contracts, lockfiles and the project checkpoint. Keep a separate branch/worktree for every parallel writer. Use one branch per task and name it `hackathon/<handle>/<task>`. Agree on contracts before parallel implementation.

Run the script from any app checkout or worktree. Pipe one JSON request to it. These examples work in PowerShell and POSIX shells.

```sh
echo '{"actor":"lead","action":"init"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
echo '{"actor":"lead","action":"task","task":"demo","owner":"dev","paths":["app/demo"],"goal":"Build the demo","acceptance":"Demo loads offline"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
echo '{"actor":"dev","action":"read"}' | node .agents/skills/hackathon-autopilot/scripts/board.mjs
```

| Action | Required fields beyond actor/action |
| --- | --- |
| init | None |
| read | Optional `after` cursor from the prior response |
| task | `task`, `owner`, `paths`, `goal`, `acceptance` |
| start, blocked, review, done | `task`, `evidence` |
| post | `to` (handle or `all`), `body`, optional `task` |

For writes, generate a unique `request_id` before the first attempt and reuse it when retrying the same operation. Keep the returned inbox cursor locally per actor. Read again at task start, on a dependency change, and before handing off. Fetch more pages while `has_more` is true. Avoid idle polling. Teammate sessions exchange updates through the board and PRs. Within each session, the teammate lead relays only relevant updates to their own workers.

Move a task to `review` with the PR URL, verification evidence, and integration notes. Include unresolved dependencies and assumptions. The lead marks `done` after integrating and verifying. If the board is unavailable, use the existing issue tracker or an agreed task list and keep the same ownership and handoff protocol.
