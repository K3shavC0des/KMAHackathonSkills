# KMA Hackathon Skills for Codex

A shared toolkit for building a hackathon entry with Codex: a hackathon coordinator, a Git based team board, and original upstream skills for understanding code, compressing context, remembering work, routing models, and improving workflows.

**Start here:** run the installer for your hackathon app repository, restart Codex, and use `$hackathon-autopilot`. Setup copies the project skills and installs ECC through its native Codex plugin interface. The other external tools have separate runtime setup described below.

## Why use this with Codex?

A prompt tells Codex what you want built. This toolkit gives the whole team a reusable workflow for planning, testing, and handing off work. Separate Codex sessions share task ownership, decisions, and test results through the app repository, so teammates can resume work without copying chat history or repeating instructions.

For example, a teammate working on frontend can ask whoever currently owns an API task for the response format on the shared Git board. That teammate can reply with the agreed fields and a PR link. Both keep working in their own checkouts or worktrees, and anyone integrating the changes can use the same information. Everyone can work across the project and choose responsibilities per task. Agents check the board during their work. Jira is optional.

Graphify can help Codex query a code map, and Headroom can compress large logs before they reach the model. These features require the runtime setup below. For a quick solo task, a regular prompt is often enough.

## Quick start

Each teammate can paste this entire prompt into their own Codex chat to set up their computer. The shared project is private, so Keshav must first grant each teammate GitHub collaborator access and they must accept the invitation. Codex may need their help with sign-in, installation approvals, or opening the final project folder.

```text
Set up my computer for our shared KMA hackathon project. Carry out the setup
through verification and resolve recoverable installation errors.

Download these two repositories into separate local Desktop folders:
  Toolkit: https://github.com/K3shavC0des/KMAHackathonSkills.git
  Project: https://github.com/K3shavC0des/KMAHackathonProject.git

Use folders named KMAHackathonSkills and KMAHackathonProject under MY account.
Detect my operating system, username, shell, and actual local paths. Use a
Desktop location outside OneDrive and the ChatGPT application folders. If my
Desktop is redirected to cloud storage, ask me to choose a local destination.
Request the host's filesystem permission when the destination requires it.

1. Check Git and GitHub authentication, then clone both repositories. The
   project is private. If access fails, tell me whether I need to sign in or
   accept a collaborator invitation. Use the service's normal sign-in flow.
   Keep credentials out of chat, repository files, and command output.
   If a destination already exists, inspect its origin and working tree.
   Reuse the matching checkout, preserve existing work, and update a clean
   checkout with git pull --ff-only. Resolve a conflicting destination with me.
   An empty project repository is expected before the team starts development.

2. Read the downloaded toolkit's README.md, UPSTREAM.md, install.py, and
   ecc_setup.py. Check the prerequisites and install missing prerequisites
   from their official source or a reputable package manager as permitted by
   this host. We need Git, Python 3.10+, Node.js 22+ for hooks and the team
   board, and a Codex CLI with native plugin support. Follow any required
   installation approvals and surface any sign-in step I must complete.

   If Python is unavailable but uv is installed, use this runner:
     uv run --python 3.12 python
   Otherwise check an actual Python interpreter such as py or python3.
   Verify that the interpreter runs before using it for installation.

   Locate the Codex CLI on my machine. Check PATH first, then the installed
   app or app-server executable paths for my operating system and account.
   Use its actual executable path with --codex if needed. Verify its version
   and plugin commands. Use the toolkit's documented compatibility requirements.

3. From the toolkit checkout, run its default installer for the absolute path
   of MY KMAHackathonProject checkout. For a working Python command, the flow is:
     python install.py --project "PROJECT_PATH" --codex "CODEX_EXECUTABLE"
     python install.py --project "PROJECT_PATH" --codex "CODEX_EXECUTABLE" --check
   Substitute real absolute paths and the Python runner established above.
   Quote paths for the detected shell. Check each exit status and fix failures
   before continuing. Use the default setup so it registers the bundled native
   ECC plugin and copies the seven project skills. Preserve edited installed
   skills and inspect differences before choosing an update. If an existing ECC
   marketplace points elsewhere, inspect it and explain any necessary source
   replacement before asking me to approve changes to that existing setup.

4. Confirm the project contains these installed skill folders:
     .agents/skills/hackathon-autopilot
     .agents/skills/graphify
     .agents/skills/headroom
     .agents/skills/claude-mem
     .agents/skills/omniroute
     .agents/skills/task-observer
     .agents/skills/claude-code-setup
   Confirm the pinned ECC plugin is enabled and its cache matches the bundled
   source using the installer's --check. Report actual results for each part.
   Read the team coordination guide inside hackathon-autopilot. Everyone can
   plan, build any part, assign or claim tasks, review, integrate, and verify.
   Temporary task ownership coordinates active file edits. Each teammate uses
   their own checkout, GitHub account, Codex session, and task branches.

5. Finish with my absolute project and toolkit paths, setup/check results,
   and the exact next steps to open KMAHackathonProject in Codex, restart or
   start a new session, review ECC's hook trust in /hooks, and use $configure-ecc.
   Keep the toolkit checkout available as ECC's local marketplace source.
   List the separate runtime setup still needed for Graphify, Headroom,
   Claude-Mem, and OmniRoute from the README. Leave provider selection and
   account connections for the team's tool-setup decisions.

Stop after setup and verification. Wait for our team to supply the challenge,
deadline, and agreed idea before planning or building the hackathon entry.
```

The prompt sets up the shared project skills and ECC. The separate tool runtimes and account connections are covered under [runtime installation](#install-the-original-tool-runtimes). The team can start working together using [these prompts](#start-a-hackathon-session) when ready.

## What is included

| Component | What it does | What is bundled |
| --- | --- | --- |
| **Hackathon Autopilot** | Turns a challenge, deadline, and rubric into tasks; maintains project state; coordinates teammates; guides implementation, verification, demo rehearsal, and submission preparation. | The coordinator skill, guides, and optional Node.js team board. Uses [ECC](https://github.com/affaan-m/ECC/tree/main/.codex-plugin) workflows when installed. |
| **ECC** | Supplies reusable workflows for planning, architecture, TDD, security, code review, verification, and more. | Complete upstream source exported at commit `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`, version **2.2.3**, with its MIT license. The installer registers its original native Codex plugin, including skills, hook scripts, MCP configuration, and assets. |
| **Graphify** | Builds knowledge graphs of code and documents to investigate architecture, relationships, and paths through a project. | Upstream's Codex specific skill and references. Graph generation requires the Graphify runtime. |
| **Headroom** | Compresses large tool results, logs, and other LLM context. Its CLI can wrap Codex through a local proxy. | Upstream's library integration skill. Installing this skill alone does not wrap Codex. |
| **Claude-Mem** | Records work across sessions and retrieves relevant memory. Its observer uses a configured AI provider. | Upstream's `mem-search` skill. Recording, the local worker, and Codex integration require its upstream installer. |
| **OmniRoute** | Runs a local gateway that routes requests to configured model providers, with routing and fallback options. | Upstream's `config-codex-cli` skill. The gateway and provider connections require separate setup. |
| **Task Observer** | Notices corrections and repeated workflows, records observations, and proposes improvements to skills for review. | The original skill and references. Read its environment instructions before choosing an observation folder or setting up automatic activation. |
| **Claude Code Setup** | Inspects a project and recommends useful automations. | Anthropic's original read-only recommender and references. Its Claude commands require interpretation for Codex. |

These are upstream skill snapshots, with their licenses retained. No replacement versions of the five requested tools were created. Exact source commits and bundled file hashes are in [upstream-lock.json](upstream-lock.json); [UPSTREAM.md](UPSTREAM.md) maps each snapshot to its source.

## Teammate installation

You need Git, Python 3.10 or newer, and the **Codex CLI with native plugin support** (ECC documents Codex 0.146.0 or newer; this setup was checked with 0.169.0). Node.js is needed to run ECC's hook commands; Node.js 22+ also supports the optional team board. On Windows, use `py` if that is your Python command; on macOS/Linux, use `python3` when needed.

```sh
git clone https://github.com/K3shavC0des/KMAHackathonSkills.git
cd KMAHackathonSkills
python install.py --project "/path/to/your/hackathon-app" --dry-run
python install.py --project "/path/to/your/hackathon-app"
python install.py --project "/path/to/your/hackathon-app" --check
```

The installer verifies bundled upstream files against their SHA-256 hashes, then copies seven skill folders into the target project's `.agents/skills/`, including Hackathon Autopilot. It preserves an existing folder with different contents and reports it; use `--force` only to intentionally replace that folder. Identical installs can be repeated.

It then unpacks the complete, pinned ECC source from `vendor/ecc-source.zip` into this toolkit checkout's ignored `.kma/ecc/<commit>/` directory and registers that directory using upstream's native flow:

```text
codex plugin marketplace add <absolute-path-to-extracted-ECC>
codex plugin add ecc@ecc
```

ECC is installed into the active Codex home, so each teammate runs setup once for their own Codex environment. Keep this toolkit checkout available as the local marketplace source. ECC's enabled state applies to sessions using that Codex home; it is not limited to the target app. `--check` verifies project skills, confirms the pinned ECC plugin is enabled, and compares every exported ECC file in its cache against the bundled archive.

Useful options:

| Option | Purpose |
| --- | --- |
| `--skills-only` | Copy or check the seven project skills without registering or checking ECC. The ECC source remains bundled. |
| `--codex "/path/to/codex"` | Use a Codex CLI executable that is not on PATH. |
| `--codex-home "/path/to/home"` | Install/check in an explicit Codex home; useful for an isolated verification. Otherwise setup respects `CODEX_HOME` or the CLI default. |
| `--dry-run` | Show the planned copies and ECC registration without writing files or running Codex. |

If an existing `ecc` marketplace points to another source, setup reports the mismatch rather than replacing that registration. Inspect it with `codex plugin marketplace list --json`. To intentionally switch to this bundle, run `codex plugin marketplace remove ecc` in the same Codex home and rerun setup. `--force` applies only to project skill copies.

Commit the installed folders in the **app repository** so teammates receive the same snapshots. Open or restart Codex in that app project. If discovery is unavailable in your client, explicitly ask it to read the relevant `SKILL.md`.

ECC registration updates Codex's plugin configuration and cache through its own CLI. Setup does not install npm/Python dependencies, services, or credentials. Skills are instructions for the agent; the other tools need the runtime setup below.

After setup, restart Codex, open `/hooks`, and review and trust ECC's hook definition before enabling it. Then select `$configure-ecc` for upstream's guided configuration. Native plugin registration does not automatically trust hooks. ECC also includes a Chrome DevTools MCP configuration; invoking it can download its pinned npm package.

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

ECC is already bundled and registered by the default installer. Its [included native setup guide](https://github.com/affaan-m/ECC/blob/d2ef2680594f9a17526a6e1a2e18b3d242c5d17b/.codex-plugin/README.md) explains hook runtime dependencies and cache recovery. Native registration does not run `npm ci`. If a hook reports a missing package, follow that guide for an explicit cache-local dependency install; rerun its cache checker against the actual active plugin directory. Autopilot uses workflows available in the host and records missing capabilities. Posting team board updates requires push access to the app repository.

## Start a hackathon session

Any teammate can paste this into Codex in the app repository.

```text
Use $hackathon-autopilot and ECC to build our hackathon entry.
Challenge and rules: [link]
Deadline and time zone: [date/time/zone]
Team: [all GitHub handles, with everyone able to work across the project]
Idea: [optional]
Deployment target: [optional]
Work through implementation, verified demo, and submission materials.
```

Autopilot maintains `docs/hackathon/STATE.md` with scope, assignments, assumptions, evidence, blockers, and the next action. It works within an active Codex session and available permissions. Event eligibility, accounts, deployment access, and submission depend on the event and your authorization.

Each teammate uses their own checkout or worktree and Codex session:

```text
Use $hackathon-autopilot in teammate mode. My team identity is [handle].
Read my assigned task and inbox, work in an isolated task branch,
Create or claim tasks, coordinate active edits, and post PRs and test evidence.
```

Everyone has the same workflow capabilities. Any teammate can create or assign tasks, claim queued work, update progress, integrate PRs, and verify the app. Responsibilities are chosen per task. Coordinate active edits with task ownership so shared files have one writer at a time. GitHub permissions still depend on each collaborator's repository access.

The optional board records task ownership, inbox updates, and PR handoffs on a shared Git branch. Follow the [team guide](.agents/skills/hackathon-autopilot/references/team.md) for commands and the [usage guide](.agents/skills/hackathon-autopilot/references/usage.md) for operating defaults.

## Claude Code Setup in Codex

Select `$claude-automation-recommender` and explicitly ask for recommendations that fit your Codex environment. Its project analysis, recommendation structure, reusable skills, and MCP ideas are useful. Claude plugin commands, hook events, tool names, and `.claude/` subagent configuration need checking against your actual Codex client. Installing the skill does not make those Claude features available.

See [UPSTREAM.md](UPSTREAM.md) for compatibility notes. The original recommender is read only; applying a recommendation is a separate action.

## Layout, updates, and removal

```text
.agents/skills/hackathon-autopilot/  Coordinator and team board
vendor/                            Original skills, references, licenses
vendor/ecc-source.zip               Complete pinned ECC source export (~39 MB)
vendor/ECC-LICENSE                  ECC's MIT license, also inside the archive
install.py + ecc_setup.py           Skill installation and native ECC setup/check
upstream-lock.json                 Source commits and bundled SHA-256 hashes
UPSTREAM.md                        Sources and compatibility notes
```

To update a snapshot, retrieve the intended upstream revision, replace its bundled files and license notices, update provenance and hashes, then check a fresh install before committing. For ECC, create a fresh `git archive --format=zip -9` export of the selected commit and update its commit, version, and archive hash in `upstream-lock.json`. Preserve original vendor text and keep Codex specific guidance explicit.

To remove an installed skill, delete its folder under the app's `.agents/skills/`. Removing skills does not stop separately installed runtimes or erase their databases and configuration; use upstream uninstall instructions for those.

To disable or remove ECC, use Codex's `/plugins` controls and inspect its marketplace registration before removing it. Once it is no longer used as a marketplace source, the extracted `.kma/ecc/` copy can be deleted. Updating the toolkit's Git checkout does not silently upgrade ECC in Codex; rerun setup to install and check the bundled version.

Attribution belongs to the maintainers and contributors linked in [UPSTREAM.md](UPSTREAM.md), including Eoghan Henn and contributors for Task Observer (CC BY 4.0), Anthropic for Claude Code Setup, and Affaan Mustafa and contributors for ECC ([MIT license](vendor/ECC-LICENSE), also retained inside the archive). Each bundled upstream skill directory carries its own license.

## Verification

Packaging and native ECC registration were checked on Windows with Python 3.12 and Codex CLI 0.169.0, using a separate app folder and isolated Codex home. To reproduce without touching your normal Codex home:

```sh
python install.py --project "/tmp/kma-test-app" --codex-home "/tmp/kma-test-codex-home"
python install.py --project "/tmp/kma-test-app" --codex-home "/tmp/kma-test-codex-home" --check
```

Use suitable absolute paths on Windows and `--codex` if the CLI is not on PATH. The check covers skill contents, the enabled ECC registration, and every archived file in the plugin cache. Live hooks, MCP servers, model requests, and a complete hackathon were not exercised by this packaging check.
