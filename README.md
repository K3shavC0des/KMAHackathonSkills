# KMA Hackathon Skills for Codex

A shared toolkit for building a hackathon entry with Codex: a hackathon coordinator, a Git based team board, and original upstream skills for understanding code, compressing context, remembering work, routing models, and improving workflows.

**Start here:** install the skills in your hackathon app repository, open that project in Codex, and use `$hackathon-autopilot`. The installer copies skill instructions and reference files. External tools have separate runtime setup described below.

## What is included

| Component | What it does | What is bundled |
| --- | --- | --- |
| **Hackathon Autopilot** | Turns a challenge, deadline, and rubric into tasks; maintains project state; coordinates teammates; guides implementation, verification, demo rehearsal, and submission preparation. | The coordinator skill, guides, and optional Node.js team board. Uses [ECC](https://github.com/affaan-m/ECC/tree/main/.codex-plugin) workflows when installed. |
| **Graphify** | Builds knowledge graphs of code and documents to investigate architecture, relationships, and paths through a project. | Upstream's Codex specific skill and references. Graph generation requires the Graphify runtime. |
| **Headroom** | Compresses large tool results, logs, and other LLM context. Its CLI can wrap Codex through a local proxy. | Upstream's library integration skill. Installing this skill alone does not wrap Codex. |
| **Claude-Mem** | Records work across sessions and retrieves relevant memory. Its observer uses a configured AI provider. | Upstream's `mem-search` skill. Recording, the local worker, and Codex integration require its upstream installer. |
| **OmniRoute** | Runs a local gateway that routes requests to configured model providers, with routing and fallback options. | Upstream's `config-codex-cli` skill. The gateway and provider connections require separate setup. |
| **Task Observer** | Notices corrections and repeated workflows, records observations, and proposes improvements to skills for review. | The original skill and references. Read its environment instructions before choosing an observation folder or setting up automatic activation. |
| **Claude Code Setup** | Inspects a project and recommends useful automations. | Anthropic's original read-only recommender and references. Its Claude commands require interpretation for Codex. |

These are upstream skill snapshots, with their licenses retained. No replacement versions of the five requested tools were created. Exact source commits and bundled file hashes are in [upstream-lock.json](upstream-lock.json); [UPSTREAM.md](UPSTREAM.md) maps each snapshot to its source.

## Teammate installation

You need Git, Python 3.10 or newer, and a Codex client that supports project skills. On Windows, use `py` if that is your Python command; on macOS/Linux, use `python3` when needed.

```sh
git clone https://github.com/K3shavC0des/KMAHackathonSkills.git
cd KMAHackathonSkills
python install.py --project "/path/to/your/hackathon-app" --dry-run
python install.py --project "/path/to/your/hackathon-app"
python install.py --project "/path/to/your/hackathon-app" --check
```

The installer verifies bundled upstream files against their SHA-256 hashes, then copies seven skill folders into the target project's `.agents/skills/`, including Hackathon Autopilot. It preserves an existing folder with different contents and reports it; use `--force` only to intentionally replace that folder. Identical installs can be repeated. `--check` verifies installed files and returns a nonzero exit code for missing or changed content.

Commit the installed folders in the **app repository** so teammates receive the same snapshots. Open or restart Codex in that app project. If discovery is unavailable in your client, explicitly ask it to read the relevant `SKILL.md`.

The script does not install Python packages, npm programs, user configuration, services, credentials, or ECC. Skills are instructions for the agent; their underlying programs need the setup below.

## Install the original tool runtimes

These commands pin the top level versions captured with this bundle. Dependencies and upstream installers can still change: this is a reproducible skill snapshot, not a fully locked runtime environment. See upstream documentation for operating system requirements and removal instructions.

| Tool | Runtime installation | Next step |
| --- | --- | --- |
| Graphify | `uv tool install graphifyy==0.9.108` | The bundled Codex skill is already copied. Select `$graphify` and ask it to map the project. Upstream also offers `graphify install --project --platform codex`. |
| Headroom | `uv tool install --python 3.13 "headroom-ai[all]==0.44.0"` | Run `headroom wrap codex` in the app repository for a wrapped session. `$headroom` is the separate library integration skill. |
| Claude-Mem | `npx --yes claude-mem@15.18.3 install --ide codex --setup browser` | Complete upstream's browser setup and memory provider selection. Restart Codex as instructed. `$mem-search` retrieves memories once the integration is available. |
| OmniRoute | `npm install -g omniroute@3.8.54` | Run `omniroute`, connect a provider in its local dashboard, then use `$config-codex-cli` or upstream's `omniroute setup-codex` flow. |
| Task Observer | No separate runtime | Select `$task-observer`. Follow its `references/environments.md` for a persistent observation folder and optional activation instruction in `AGENTS.md`. Its runnable shell examples require Bash. |

Claude-Mem can retain session information and consume additional provider tokens. OmniRoute sends requests to providers you connect. Headroom changes the request path while wrapping Codex. Inspect upstream setup before combining proxies. The skill installation check does not exercise live provider calls or memory recording.

Install ECC separately using its [native Codex plugin instructions](https://github.com/affaan-m/ECC/tree/main/.codex-plugin). Autopilot uses workflows available in the host and records missing capabilities. The optional team board requires Node.js 22+ and Git; posting updates requires push access to the app repository.

## Start a hackathon session

For the lead, paste this into Codex in the app repository:

```text
Use $hackathon-autopilot and ECC to build our hackathon entry.
Challenge and rules: [link]
Deadline and time zone: [date/time/zone]
Team: [GitHub handles and integration lead]
Idea: [optional]
Deployment target: [optional]
Work through implementation, verified demo, and submission materials.
```

Autopilot maintains `docs/hackathon/STATE.md` with scope, assignments, assumptions, evidence, blockers, and the next action. It works within an active Codex session and available permissions. Event eligibility, accounts, deployment access, and submission depend on the event and your authorization.

Each teammate uses their own checkout or worktree and Codex session:

```text
Use $hackathon-autopilot in teammate mode. My team identity is [handle].
Read my assigned task and inbox, work in an isolated task branch,
then hand off the PR and test evidence to the integration lead.
```

The optional board records task ownership, inbox updates, and PR handoffs on a shared Git branch. Follow the [team guide](.agents/skills/hackathon-autopilot/references/team.md) for commands and the [usage guide](.agents/skills/hackathon-autopilot/references/usage.md) for operating defaults.

## Claude Code Setup in Codex

Select `$claude-automation-recommender` and explicitly ask for recommendations that fit your Codex environment. Its project analysis, recommendation structure, reusable skills, and MCP ideas are useful. Claude plugin commands, hook events, tool names, and `.claude/` subagent configuration need checking against your actual Codex client. Installing the skill does not make those Claude features available.

See [UPSTREAM.md](UPSTREAM.md) for compatibility notes. The original recommender is read only; applying a recommendation is a separate action.

## Layout, updates, and removal

```text
.agents/skills/hackathon-autopilot/  Coordinator and team board
vendor/                            Original skills, references, licenses
install.py                         Project installer and installed-file check
upstream-lock.json                 Source commits and bundled SHA-256 hashes
UPSTREAM.md                        Sources and compatibility notes
```

To update a snapshot, retrieve the intended upstream revision, replace its bundled files and license notices, update provenance and hashes, then check a fresh install before committing. Preserve original vendor text and keep Codex specific guidance explicit.

To remove an installed skill, delete its folder under the app's `.agents/skills/`. Removing skills does not stop separately installed runtimes or erase their databases and configuration; use upstream uninstall instructions for those.

Attribution belongs to the maintainers and contributors linked in [UPSTREAM.md](UPSTREAM.md), including Eoghan Henn and contributors for Task Observer (CC BY 4.0), Anthropic for Claude Code Setup, and Affaan Mustafa and contributors for ECC. Each bundled upstream directory carries its own license.
