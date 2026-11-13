# KMA Hackathon Skills

A Codex hackathon coordinator built on [ECC's native Codex plugin](https://github.com/affaan-m/ECC/tree/main/.codex-plugin). Each teammate works in their own checkout or worktree. A shared Git branch records task ownership, inbox updates, and pull-request handoffs.

## Install

1. Install ECC once per teammate using the [upstream Codex instructions](https://github.com/affaan-m/ECC/tree/main/.codex-plugin).

   ```sh
   codex plugin marketplace add affaan-m/ECC
   codex plugin add ecc@ecc
   codex plugin list --json
   ```

2. Copy `.agents/skills/hackathon-autopilot/` from this repository into the same path in your **hackathon app repository** and commit it. Use Git and Node.js 22 or newer for the optional team board. Teammates who post updates need Git push access to the app repository.
3. Open your app repository in Codex and start one lead session. Each teammate starts their own Codex session from a separate clone or task worktree. Follow [Team coordination](.agents/skills/hackathon-autopilot/references/team.md).

## Start the lead session

```text
Use $hackathon-autopilot and ECC to build our hackathon entry.
Challenge and rules: [link]
Deadline and time zone: [date/time/zone]
Team: [GitHub handles and who's the integration lead]
Idea: [optional]
Deployment target: [optional]
Work autonomously through the verified demo and submission materials.
```

## Start a teammate session

```text
Use $hackathon-autopilot in teammate mode. My team identity is [handle].
Read my assigned task and inbox, work in an isolated task branch,
then hand off the PR and test evidence to the integration lead.
```

The [usage guide](.agents/skills/hackathon-autopilot/references/usage.md) covers Plus-plan defaults and the tools shown in the Instagram examples. ECC is loaded through its upstream plugin, so teammates get its full Codex package and upstream updates. Attribution goes to [ECC and its contributors](https://github.com/affaan-m/ECC).
