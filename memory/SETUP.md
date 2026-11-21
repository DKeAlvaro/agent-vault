# Write rules: read before saving anything

These notes are the only memory. If your harness has a memory feature of its own, do not use it.

```
MEMORY.md              always loaded: who the user is, hard rules, one line per area (4 KB)
<area>/README.md       one line per note: what it is, then "Open if:" triggers (2.5 KB)
<area>/<topic>.md      current state, rewritten when it changes (10 KB)
<area>/<topic>-log.md  history, append-only, any size (an area-wide log is log.md)
<area>/<sub>/          3+ notes on one thing: a subfolder with its own README.md, listed in the one above
```

- Save durable state only: decisions, current status, gotchas, preferences. When the user says "remember
  this", save it at once without asking. An answered question that changes nothing needs no write.
- A new topic is a new `<area>/<topic>.md` plus one line in its README:
  `` - `area/topic.md` — what it is, at most 16 words. Open if: concrete triggers. ``
  The line says when to open the note, never what it says. Add an area only if none fits, with its line in
  `MEMORY.md`.
- A note starts with an `updated: YYYY-MM-DD` line and holds current state in entries of at most 3 lines.
  Change it by rewriting what changed.
- Trim = log first. Before text leaves a note, append it verbatim to the area's log under a `## YYYY-MM-DD`
  heading. The hook fails a commit in which notes lose more lines than the logs gain.
- A note near 10 KB: move history to its log; if it is still big, move whole `## ` sections to a new note.
- One fact, one home: a value that can change lives in one note, and other notes point at it.
- Rules for every session go in the hard rules of `MEMORY.md`; rules for one project go in its note.
- Refer to files by their path from `memory/`, in backticks. `memory/` holds only `.md` files. No secrets
  anywhere in the repo.

Commit as `memory: <what changed>`. The pre-commit hook runs `check.py`: fix every FAIL, never use
`--no-verify`. `python3 drift.py` lists notes that point at paths or URLs that no longer exist.
