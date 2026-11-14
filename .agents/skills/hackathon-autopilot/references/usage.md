# Keep Codex usage manageable

- Default to one active Codex session per teammate. Delegate a bounded task only when it can run independently, such as checking a source, owning a distinct module, or reviewing a high-risk diff. Independent agents maintain their own context and can increase total token usage. [OpenAI multi-agent guidance](https://developers.openai.com/api/docs/guides/responses-multi-agent)
- Give workers the acceptance check, file paths, interface contract, and relevant decision excerpts. Reuse the task result through a PR link, changed paths, test result, and next action. Use a fresh task context or compact at a milestone if the client offers compaction. Preserve decisions and evidence in the checkpoint before doing so.
- Keep repository instructions short and load only the ECC skill you need. Search filenames and symbols first, open relevant ranges, and trim build output to the failing command and nearby lines. Keep source code readable. Avoid bringing generated files, dependency trees, and full logs into model context.
- Use the smallest available model or reasoning level that passes the task's acceptance check. Reserve stronger reasoning for architecture, integration failures, or high-risk review. Track actual usage in the Codex client and compare comparable tasks before adopting a proxy. No quota reduction is guaranteed.

## Patterns from the Instagram examples

| Pattern | Codex setup |
| --- | --- |
| Agent board and unread messages | Git-backed tasks, cursor-based inboxes, and PR handoffs |
| Headroom | Its [proxy docs](https://github.com/headroomlabs-ai/headroom/blob/main/docs/content/docs/proxy.mdx) document a Codex CLI wrapper. Benchmark separately if your environment supports it. Plus sign-in and quota savings are unverified for this package. |
| OmniRoute | Upstream documents [Codex CLI provider routing](https://github.com/cheaper-inference/OmniRoute/blob/main/docs/guides/CLI-INTEGRATIONS.md). External providers can have their own billing and data handling. The default workflow uses each teammate's normal Codex sign-in. |
| Claude-Mem | Original `mem-search` skill is bundled. Use upstream's native Codex runtime setup for recording and retrieval; continue to record shared task decisions in the repo checkpoint. |
| Claude Code Setup | Original read-only recommender is bundled. Apply the Codex compatibility mapping in the toolkit's `UPSTREAM.md`. |
| Task Observer | Original skill and references are bundled. Invoke `$task-observer` and follow its environment setup for a persistent observation log. |

Sources for the workflow ideas include the [agent board example](https://www.instagram.com/p/DfOLEP6v3AR/) and [tool roundup](https://www.instagram.com/p/Dbn6ElTvw_W/). The toolkit bundles the original upstream skills and complete pinned ECC source. Default setup registers ECC's native Codex plugin. The optional proxy and gateway require separate upstream runtime installation.
