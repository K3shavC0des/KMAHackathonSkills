---
name: hackathon-autopilot
description: Run a hackathon project autonomously with Codex and ECC, from challenge selection through implementation, testing, demo rehearsal, and submission preparation. Use when asked to build a hackathon entry, coordinate coding agents, finish a time-limited prototype, or resume a hackathon with minimal supervision.
---

# Hackathon Autopilot for Codex

Own the requested outcome through completion. Use ECC's installed research, planning, implementation, review, and verification workflows. Apply this skill's hackathon scheduling and coordination to those workflows. Follow the host's instructions, permissions, and the team's explicit choices.

## Start with one brief

Read the repository instructions, existing code, event brief, rubric, deadline with timezone, submission requirements, and available integrations. Reuse answers already provided. Ask one bundled question only for missing information that prevents useful progress. Continue independent work while waiting.

Infer reversible choices and record them. If no idea is supplied, compare up to three feasible concepts against the actual rubric, choose the strongest, and proceed. If event rules are inaccessible, record that gap and build a provisional prototype without claiming eligibility. Check restrictions on AI assistance, pre-existing code, data, team size, licenses, and submission format against the supplied official rules.

Default to the existing stack and available services. For a new project, choose the simplest stack that supports the core demonstration. Use zero new paid resources unless the user supplies a spending limit. Treat a missing deadline as a request for the smallest complete prototype, and ask for the deadline while starting the work.

## Establish durable state

Keep one concise `docs/hackathon/STATE.md` in the project, or use its existing equivalent. Record the goal, source links, deadline/timezone, acceptance criteria, chosen approach, assumptions, authorized external actions, resource limits, current branch, task owners, blockers, last verified results, and next action. Keep credentials out of this file.

Create a short task table with task, owner, dependencies, files, acceptance check, and status. Distinguish queued, working, blocked, review, and verified. Update it after integration, a scope change, a material failure, and before ending a session. On resume, compare the state with the actual working tree and rerun only checks invalidated by changes. Preserve teammates' work.

## Route to ECC

Discover the actual installed skill names and available agent tools before invoking them. Load only the workflow needed for the next task. Use the current Codex tools for delegation and skill invocation. ECC documents may contain Claude slash commands or tool names, which require mapping to the host's available capabilities.

| Work | ECC foundation |
| --- | --- |
| Find reusable implementations and verify APIs | search-first, available research skills |
| Choose scope, architecture, dependencies, acceptance checks | planner and architect guidance |
| Implement features and reproduce bugs | tdd-workflow, relevant language and framework skills |
| Integrate the app and exercise user journeys | e2e-testing, api-design, frontend/backend patterns |
| Inspect correctness and sensitive code | code-reviewer and security-review guidance |
| Repair build failures | build-error-resolver guidance |
| Verify delivery | verification-loop |
| Preserve context and resume | strategic-compact and available session workflows |

Read the installed ECC instructions before relying on their requirements. Preserve existing project quality gates. Use actual project commands and the detected shell and package manager. If ECC or a named agent is unavailable, continue using the available Codex tools and the workflow below, recording the missing capability. Never claim a tool ran when only its instructions were read.

## Plan around the demonstration

Define one end-to-end user journey that proves the project's value. Link every required feature to a rubric item or that journey. Separate essentials from optional work and set observable acceptance checks.

Allocate the remaining time approximately as 10% discovery and planning, 55% implementation, 20% integration and verification, and 15% demo and submission preparation. Adjust to the actual event and existing progress. Establish a working vertical slice early. Verify the riskiest API, dataset, hardware, or model integration before investing in polish.

At 25% of the time remaining, freeze optional features. At 10%, focus on regressions, launch reliability, and the demo. Never remove a mandatory requirement silently. If it becomes infeasible, report the impact and the smallest viable alternative.

## Coordinate agents and teammates

Use Codex subagents for independent work when available and allowed. Start with one active session per teammate. Delegate only independent work when it saves time, with up to two implementers or one targeted reviewer per session. Use the [usage guide](references/usage.md) when setting a session budget. Stay within the session's limits. Every teammate can plan, implement any part of the application, assign tasks, review, integrate, and verify work. Choose responsibilities per task as the team needs them.

Give each worker a concrete goal, input paths, interface contract, owned files or isolated branch/worktree, acceptance checks, deadline, and required report. Request changed paths, commands run, results, unresolved issues, and integration instructions. Anyone can change dependency manifests, lockfiles, schemas, and shared state after coordinating ownership of that task. Use one active writer per shared file. Do dependent tasks sequentially.

For multiple human teammates running Codex, follow [team coordination](references/team.md). Use the bundled board when the team has a shared writable Git origin. Every teammate session reads the board and inbox, creates or claims suitable tasks, coordinates its active paths, and posts PRs and verification evidence. Anyone can update the checkpoint or integrate work after claiming the relevant paths. Read current task ownership before editing and announce handoffs. Bring changes together in small increments and verify the combined application. A task reaches verified only after its behavior works in the integrated app. A worker's completion message alone is insufficient.

If agent tools are unavailable, perform the same roles sequentially. State that fallback accurately. Ask for user decisions only when they are material and cannot be inferred from the brief or existing authorization.

## Execute until the outcome works

Repeat the following loop while work remains and the run budget permits.

1. Select the highest-value unblocked task on the critical path.
2. Inspect existing code and use ECC research to choose reuse, extension, or implementation.
3. Make the smallest complete change through the normal application entry points.
4. Run the relevant checks, fix failures, and integrate the result.
5. Update the task state and select the next task without asking whether to continue.

Check dependency, service, and runtime availability before relying on them. Use timeouts for external requests and bounded retries for transient errors. After two materially different unsuccessful fixes for the same blocker, change the approach, reduce optional scope, or isolate the dependency. Continue other tasks and surface a precise blocker when user input is necessary.

Use explicit sample fixtures for an offline demo when helpful. Label sample or simulated results in the interface and pitch. Keep live and fixture execution distinct. For AI features, evaluate a small representative input set, handle empty or malformed outputs, bound latency and cost, and show failure states. For NASA or other scientific data, preserve dataset provenance, units, timestamps, and uncertainty.

Use existing authorization for specified pushes, deployment targets, or submissions. When an external action is outside that scope, finish the local work and prepare the exact action for approval. Respect host-required approvals. This skill does not expand permissions or authorize spending, credential changes, or public disclosure of private data.

## Verify the deliverable

Run ECC's verification loop with the project's real build, type, lint, and test commands. Capture exit status and concise evidence. Mark unavailable or inapplicable checks explicitly. Review the actual changed files for regressions, secrets, input handling, authorization, and external-service failures relevant to the app.

Run the core user journey through the real interface. Check empty input, failed requests, refresh, and a clean launch with documented setup. For a website, inspect the principal screen at desktop and mobile sizes. Confirm links and buttons lead to working behavior. A passing build alone does not prove the demo works.

If deployment is authorized and available, deploy, open the deployed URL, and rerun the core journey there. Record local and deployed verification separately. Keep a reliable local launch path and known demo inputs. Never claim successful deployment or submission without observed evidence.

## Prepare the handoff

Create or update the project's setup instructions, environment-variable names without secret values, demo steps, submission text, and short pitch. Include the problem, intended user, working solution, technical approach, required data and sponsor tools, limitations, and credits. Fit the actual event's limits. Rehearse the demo against the running app and prepare a fallback sequence if the network fails.

Finish only when the required journey is verified and the requested deliverables exist, or when a concrete blocker prevents further useful work. Report the working entry point, what was verified, remaining limitations, and any precise action the user must take. Preserve the next action in state if runtime, context, or tool limits end the session. A skill requires an active Codex session and available tools to execute.
