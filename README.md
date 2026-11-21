<p align="center"><img src=".github/logo.svg" width="88" alt="agent-vault"></p>
<h1 align="center">agent-vault</h1>
<p align="center">Memory for coding agents, kept as plain markdown in a git repository you own.</p>

Agents that load an instructions file at startup (Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`) get a
short index. The index names a folder for the task, the folder's `README.md` names a note, and the agent opens
that note. There is no database, server or embedding step: agents read files with the tools they already have.
Because the memory is your repository, it stays with you when you change model, harness or provider.

## How it works

```
memory/
  MEMORY.md          the index, loaded every session: who you are, standing rules, one line per area
  SETUP.md           the rules the agent follows when it saves something
  example/
    README.md        one line per note, with "Open if:" triggers
    commits.md       current state, rewritten when it changes
    commits-log.md   history, appended to, searched rather than read
check.py             pre-commit check
drift.py             lists notes that point at paths or URLs that no longer exist
link.sh              links MEMORY.md into your agent and installs the hook
```

To find something, an agent reads the index (already in context), one area README and one note.

## Quick start

1. Clone this repository to a path you will keep, such as `~/agent-vault`, and point `origin` at a new private
   repository of your own: it will hold personal notes.
2. Run `sh link.sh`. It links `memory/MEMORY.md` to `~/.claude/CLAUDE.md` (a symlink on Linux and macOS, a
   one-line `@` import on Windows under Git Bash) and installs `check.py` as the repository's pre-commit hook.
   An existing `CLAUDE.md` is moved to `CLAUDE.md.bak-<time>`; copy what you need from it into `MEMORY.md`.
3. Fill in the placeholders in `memory/MEMORY.md` and replace `memory/example/` with your own areas.
4. Start a session and ask the agent to remember something. It should update or add a note, list it in the
   area's README and commit. If the check fails, its output says what to fix.

Requires git and Python 3.7 or newer. Neither script needs to be executable.

## What the check enforces

`check.py` runs before every commit and blocks it if any of these fail:

- Size budgets: 4 KB for `MEMORY.md`, 2.5 KB for each `README.md`, 10 KB for each note. Logs (`log.md`,
  `*-log.md`) have no limit.
- Every note and folder is listed in the README one level up, with `MEMORY.md` as the top level. Logs are not
  listed.
- A README line describes its note in at most 16 words before "Open if:".
- Backticked paths that start with an area folder exist.
- In one commit, notes lose at most 3 lines more than the logs gain, so trimmed text goes to a log first.
- `memory/` holds only `.md` files, and none contains a string that looks like an API key or a private key.

`python3 drift.py` never blocks. It lists backticked absolute paths in notes that do not exist on this machine,
and URLs that return 404 or 410 or whose host does not resolve. `--no-urls` skips the network.

## Other agents

An agent is connected only through its instructions file. `sh link.sh ~/.codex/AGENTS.md` does for Codex what
step 2 does for Claude Code, and the same works for any agent that reads a markdown file at startup. Turn off
the agent's own memory feature, or facts end up in two places. On Windows the `@` import is resolved only by
Claude Code; for other agents, replace that line with one telling the agent to read the file first.

## License

MIT
