# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a curated collection of Claude Code subagent definitions — specialized AI assistants for specific development tasks. Subagents are markdown files with YAML frontmatter that Claude Code can load and invoke. The repository doubles as a Claude Code plugin **marketplace**: each category directory is published as an installable plugin via `.claude-plugin/marketplace.json`.

There is no build system, test runner, or package manifest. Contributions are plain markdown edits plus metadata updates.

## Repository Structure

```
.
├── .claude-plugin/
│   └── marketplace.json            # Top-level plugin marketplace manifest
├── .github/workflows/
│   └── enforce-plugin-version-bump.yml  # CI: requires plugin.json version bumps on .md changes
├── categories/
│   ├── 01-core-development/        # 11 agents: backend, frontend, fullstack, mobile, API, etc.
│   ├── 02-language-specialists/    # 29 agents: TypeScript, Python, Go, Rust, Java, etc.
│   ├── 03-infrastructure/          # 16 agents: DevOps, cloud, Kubernetes, SRE
│   ├── 04-quality-security/        # 15 agents: testing, security audit, code review
│   ├── 05-data-ai/                 # 13 agents: ML, data engineering, LLM
│   ├── 06-developer-experience/    # 14 agents: tooling, docs, DX
│   ├── 07-specialized-domains/     # 12 agents: blockchain, IoT, fintech, gaming
│   ├── 08-business-product/        # 12 agents: product, business analysis
│   ├── 09-meta-orchestration/      # 10 agents: multi-agent coordination
│   └── 10-research-analysis/       # 8 agents: research, analysis
│       └── <each category>/
│           ├── .claude-plugin/plugin.json  # Plugin manifest (name, version, agent list)
│           ├── README.md                   # Category overview + Quick Selection Guide
│           └── <agent-name>.md             # Individual subagent definitions
├── tools/
│   └── subagent-catalog/           # Claude Code slash-command skill to browse/fetch agents
├── install-agents.sh               # Interactive installer (local or global, from disk or GitHub)
├── README.md                       # Main catalog README with agent index
└── CONTRIBUTING.md                 # Contribution guide
```

Agent counts above reflect the current state; update them if you add or remove agents.

## Subagent File Format

Each subagent is a markdown file with YAML frontmatter:

```yaml
---
name: agent-name
description: When this agent should be invoked (used by Claude Code for auto-selection)
tools: Read, Write, Edit, Bash, Glob, Grep  # Comma-separated tool permissions
model: sonnet                                # Optional: sonnet | opus | haiku
---

You are a [role description]...

[Agent-specific checklists, patterns, guidelines]

## Communication Protocol
[Inter-agent communication specs]

## Development Workflow
[Structured implementation phases]
```

The filename must match `name` in the frontmatter (e.g. `api-designer.md` ↔ `name: api-designer`).

### Tool Assignment by Role Type

- **Read-only** (reviewers, auditors): `Read, Grep, Glob`
- **Research** (analysts): `Read, Grep, Glob, WebFetch, WebSearch`
- **Code writers** (developers): `Read, Write, Edit, Bash, Glob, Grep`
- **Documentation**: `Read, Write, Edit, Glob, Grep, WebFetch, WebSearch`

## Plugin / Marketplace Model

Each `categories/<N>-<name>/` directory is a standalone Claude Code plugin.

- **`categories/<category>/.claude-plugin/plugin.json`** declares the plugin name, `version` (semver), description, and the list of agent `.md` files it ships.
- **`.claude-plugin/marketplace.json`** at the repo root is the marketplace manifest. It lists every category plugin along with its `version`, keywords, and category.

The plugin `name` and `version` in `categories/<category>/.claude-plugin/plugin.json` **must** match the corresponding entry in `.claude-plugin/marketplace.json`. CI enforces this (see below).

## Versioning Requirements (IMPORTANT)

When you modify *any* `*.md` file inside `categories/<category>/`, you MUST:

1. Bump the `version` field in `categories/<category>/.claude-plugin/plugin.json` (semver).
2. Update the matching plugin entry's `version` in `.claude-plugin/marketplace.json` to the same value.

If you add a new agent, also add its relative path (e.g. `"./new-agent.md"`) to the `agents` array in `plugin.json`.

The `.github/workflows/enforce-plugin-version-bump.yml` GitHub Action blocks PRs that change markdown under a category without bumping that category's plugin version, and blocks PRs where the category `plugin.json` version and `marketplace.json` version are out of sync.

## Contributing a New Subagent

When adding a new agent, update all of the following:

1. **Create the agent file** at `categories/<N>-<category>/<agent-name>.md` using the template above.
2. **Main `README.md`** — Add a link in the appropriate category section, alphabetical order. Format:
   `- [**agent-name**](categories/<N>-<category>/<agent-name>.md) - Brief description`
3. **Category `README.md`** (e.g. `categories/02-language-specialists/README.md`) — Add a detailed description under "Available Subagents", update the "Quick Selection Guide" table, and the "Common Technology Stacks" section if applicable.
4. **`categories/<category>/.claude-plugin/plugin.json`** — Append `"./agent-name.md"` to `agents` and bump `version`.
5. **`.claude-plugin/marketplace.json`** — Bump the matching plugin entry's `version` to match.

For edits to an existing agent, steps 4 and 5 (version bumps) are still required; step 2/3 updates depend on whether the agent's description or positioning changed.

## Tools

The `tools/` directory hosts Claude Code slash-command skills that enhance catalog discovery. Currently:

- **`tools/subagent-catalog/`** — Installed to `~/.claude/commands/subagent-catalog/`. Provides `/subagent-catalog:search`, `:fetch`, `:list`, and `:invalidate` for browsing and pulling agent definitions from GitHub with 12h caching.

When adding a new tool: create a folder under `tools/`, include a `README.md`, one `.md` file per command with YAML frontmatter, and any helper scripts. Add it to the "Tools" section of the main `README.md`.

## Installation Scripts

- **`install-agents.sh`** — Interactive bash installer that copies agents to either `~/.claude/agents/` (global) or `./.claude/agents/` (local), sourcing from either the local `categories/` tree or the GitHub API. The GitHub-backed mode is wired to `VoltAgent/awesome-claude-code-subagents` (see `GITHUB_API_BASE` in the script) — keep that in sync if the canonical repository URL changes.

## Subagent Storage in Claude Code

| Type    | Path                 | Scope                 |
|---------|----------------------|-----------------------|
| Project | `.claude/agents/`    | Current project only  |
| Global  | `~/.claude/agents/`  | All projects          |

Project subagents take precedence over global ones with the same name.

## Conventions & Gotchas

- Keep agent lists in both main and category READMEs in **alphabetical order**.
- Do **not** edit `.claude/` in this repo — it is gitignored and reserved for local Claude Code state.
- Most agents use `model: sonnet`; only set `model: opus` / `haiku` when there is a specific reason.
- There is no linter or test suite — verify your agent loads in Claude Code before submitting.
- License is MIT; contributions are accepted "as is" without security auditing.
