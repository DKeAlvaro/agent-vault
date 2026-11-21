# Memory

<!-- Loaded by your agent at the start of every session. Keep it under 4 KB. Replace every <...>. -->

<Your name>, <what you do>, <where you are>.

## Hard rules
<!-- Only what every session in every project must obey. These are examples. -->
- Answer in <language>, short and direct.
- Act without asking, except for destructive or outward-facing actions.
- After changing a repo, commit when done.

## How memory works
Paths below are relative to `memory/` in this repo, cloned at `<path, e.g. ~/agent-vault>`.
1. Pick the area that matches the task, read its `README.md`, then open only the note it points at.
2. Before reading a note, check its size; over 10 KB, list its `## ` headings and read only the section you need.
   Logs (`log.md`, `*-log.md`) are history: grep them, never read them whole.
3. To save something, follow `SETUP.md`, then commit.

## Areas
- `example/` — a sample area: one note and its log. Replace it with your own.
