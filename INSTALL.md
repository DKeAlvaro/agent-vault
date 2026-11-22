# Setting up agent-vault for a user

You are an agent that was asked to set this vault up. Do these steps in order.

1. Make the user's private copy, cloned to a path that will stay, such as `~/agent-vault`:
   `gh repo create agent-vault --private --template DKeAlvaro/agent-vault --clone`. Without the GitHub CLI, clone
   this repository and point `origin` at a new private repository of the user's. Never fork it: a fork of a
   public repository is public, and the vault will hold personal notes.
2. In the clone, run `sh link.sh <file>`, where `<file>` is the global instructions file that you yourself load
   at the start of every session, for example `~/.claude/CLAUDE.md` (the default) or `~/.codex/AGENTS.md`. The
   script points that file at `memory/MEMORY.md` and installs `check.py` as the pre-commit hook. An existing
   file is moved to `<file>.bak-<time>`: copy what still applies from it into `memory/MEMORY.md`.
3. Ask the user who they are, which rules every session must follow, and which areas of their work the vault
   should cover. Write the answers into `memory/MEMORY.md`, replacing every `<...>`, and replace
   `memory/example/` with their areas. Do not invent any of it.
4. If you have a memory feature of your own, turn it off, or tell the user how to: the vault is the only memory.
5. Commit, push, and tell the user to start a new session.

From then on, `memory/MEMORY.md` tells you how to read and `memory/SETUP.md` how to write.
