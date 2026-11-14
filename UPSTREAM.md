# Upstream sources and Codex fit

Vendored files are unmodified upstream skill text, except Graphify's Codex-specific `skill-codex.md` is named `SKILL.md` for discovery. Licenses are beside each skill.

| Bundle | Upstream | Commit | Codex fit |
|---|---|---|---|
| graphify | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 52cb282 | Native Codex skill and references; install runtime with `uv tool install graphifyy==0.9.108`. |
| ecc | [affaan-m/ECC](https://github.com/affaan-m/ECC) | d2ef2680594f9a17526a6e1a2e18b3d242c5d17b | Version 2.2.3. Complete source in `vendor/ecc-source.zip`, exported directly with `git archive`; includes upstream marketplace and Codex manifests, skills, hooks, scripts, MCP config, assets, docs, tests, package manifests, and MIT license. Default setup extracts it and registers the native plugin from that local source. |
| headroom | [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 0368a87 | Native skill; upstream `headroom wrap codex` support. Requires Python 3.11+; see upstream README. |
| claude-mem | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 0c488b5 | Native Codex provider and plugin; follow upstream Codex provider setup (`npx claude-mem install --provider codex`). |
| omniroute | [cheaper-inference/OmniRoute](https://github.com/cheaper-inference/OmniRoute) | 82f60e5 | Native Codex config skill; upstream CLI supports Codex. Runtime: `npm install -g omniroute@3.8.54`. |
| task-observer | [rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all) | d61bc31 | Agent Skill text works in Codex; activate by invoking `$task-observer`. Claude `CLAUDE.md` setup does not transfer; Codex uses `AGENTS.md`. |
| claude-code-setup | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 893173f | Read-only recommender logic and project inspection apply. Claude-specific hooks, subagents, plugin commands, and MCP configuration need Codex equivalents; treat the original as guidance, not executable Codex setup. |

The installer preserves original skill content. It registers ECC in the active Codex home through native CLI commands; it does not install third-party runtime dependencies or authorize hooks. Check each upstream project for runtime requirements and provider terms before enabling it.

## Snapshot details

[upstream-lock.json](upstream-lock.json) records full commit IDs, original skill paths, source repository URLs, and SHA-256 hashes for every bundled upstream file. Graphify's NOTICE and MIT license for inherited components accompany its Apache license. Task Observer is attributed to Eoghan Henn and contributors under CC BY 4.0. File names are normalized for discovery; original skill text is retained.

ECC is archived to preserve its complete exported source and avoid exposing hundreds of duplicate skills in this toolkit's discovery paths. Its archive hash covers all contents, including original file modes. Extraction preserves executable modes on Unix. The installer checks all exported files against the installed cache, in addition to the enabled plugin/version registration. This verifies packaging and registration, not a live hook run, MCP launch, or model call. Upstream's native setup guide remains inside the archive at `.codex-plugin/README.md`.

## Applying Claude Code Setup recommendations

| Original feature | What applies in Codex |
| --- | --- |
| Project inspection | Examine manifests, dependencies, tests, CI, and project instructions to choose useful automations. |
| Skills | Copy portable Agent Skills into `.agents/skills/`; invoke the skill name in your Codex client. |
| MCP servers | Reuse the integration idea; register it through the actual Codex client's MCP configuration. Claude `.mcp.json` instructions are not a Codex configuration recipe. |
| Hooks | Reuse the workflow goal, such as formatting or checking code. Confirm the installed client's supported hook events and schema before configuring it; Claude hook JSON is client specific. |
| Subagents | Reuse roles and review criteria. Claude `.claude/agents/` files and tool names need mapping to capabilities exposed by the current Codex session. |
| Plugins | Use upstream Codex support when available. Claude `/plugin install` commands do not install into Codex. |

The recommender's original `tools` frontmatter names Claude tools. Treat that field as source metadata and use the host's actual tools. Its references remain preserved for inspection; they are not a promise of feature parity.
