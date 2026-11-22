<p align="center"><img src=".github/logo.svg" width="88" alt="agent-vault"></p>
<h1 align="center">agent-vault</h1>
<p align="center">Memory for coding agents, kept as plain markdown in a git repository you own.</p>

Coding agents read an instructions file at the start of every session. agent-vault puts a short index there, so
your agent always knows what it has written down about you and where to find it. The notes are markdown files in
your own repository, so they stay with you when you change model, harness or provider.

## Quick start

Tell your agent:

> Make a private copy of https://github.com/DKeAlvaro/agent-vault and set it up for me.

It asks who you are and which rules it should always follow, and from then on it keeps the notes itself. You need
git and Python 3.7 or newer.

## How it works

```
memory/
  MEMORY.md          the index, loaded every session: who you are, rules, areas
  SETUP.md           the rules the agent follows when it saves something
  example/
    README.md        one line per note, with "Open if:" triggers
    commits.md       current state, rewritten when it changes
    commits-log.md   history, appended to, searched rather than read
check.py             runs on every commit and rejects notes that break the format
drift.py             lists notes that point at paths or URLs that are gone
link.sh              links MEMORY.md into your agent and installs the check
INSTALL.md           the setup steps your agent follows
```

To find something, the agent reads the index, one folder's README and one note. To save something, it writes or
updates a note and commits. There is no database, server or embedding step: git keeps the history, markdown holds
the notes, and a script enforces the format.

## License

MIT
