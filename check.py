#!/usr/bin/env python3
"""Pre-commit check for memory/, installed as a git hook by link.sh. Prints every FAIL, exits 1 if any.
The rules it enforces are written for the agent in memory/SETUP.md."""
import os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_MAX, README_MAX, NOTE_MAX, WORDS_MAX, SLACK = 4000, 2500, 10000, 16, 3
SECRET = re.compile(r'sk-[\w-]{20,}|gh[pousr]_\w{30,}|github_pat_\w{20,}|AKIA[0-9A-Z]{16}|AIza[\w-]{35}'
                    r'|xox[abp]-[\w-]{10,}|BEGIN [A-Z ]*PRIVATE KEY')

def git(*args):
    return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, encoding='utf-8').stdout
def mem(path): return os.path.join(ROOT, 'memory', path)
def read(path):
    with open(mem(path), encoding='utf-8', errors='replace') as f: return f.read()
def is_log(path): return re.search(r'(^|/|-)log\.md$', path)  # history: never listed, never read whole
def is_note(path): return '/' in path and not is_log(path) and os.path.basename(path) != 'README.md'

listed = git('ls-files', '-z', '--cached', '--others', '--exclude-standard', 'memory').split('\0')
files = [f[7:] for f in listed if f and os.path.isfile(os.path.join(ROOT, f))]
areas = {f.split('/')[0] for f in files if '/' in f}
fails = []
for f in files:
    if not f.endswith('.md'):
        fails.append(f'{f}: memory/ holds only .md files'); continue
    text, folder, size = read(f), os.path.dirname(f), os.path.getsize(mem(f))
    if SECRET.search(text): fails.append(f'{f}: looks like it holds a secret')
    limit = INDEX_MAX if f == 'MEMORY.md' else README_MAX if f.endswith('README.md') else is_note(f) and NOTE_MAX
    if limit and size > limit: fails.append(f'{f} is {size} B, over its {limit} B budget')
    if f != 'MEMORY.md' and not is_log(f):  # listed in the index one level up: README.md, or MEMORY.md at the top
        index, name = (os.path.dirname(folder), folder + '/') if f.endswith('README.md') else (folder, f)
        index = index + '/README.md' if index else 'MEMORY.md'
        if not os.path.isfile(mem(index)): fails.append(f'{os.path.dirname(index)}/ has no README.md')
        elif f'`{name}`' not in read(index): fails.append(f'{index} has no line for `{name}`')
    if f.endswith('README.md'):
        for name, desc in re.findall(r'^- `([^`]+)` [-—–] (.*)', text, re.M):
            if len(desc.split('Open if:')[0].split()) > WORDS_MAX:
                fails.append(f'{f}: the line for `{name}` takes over {WORDS_MAX} words before "Open if:"')
    if not is_log(f):
        for path in re.findall(r'`([^`\s<>*{}]+/[^`\s<>*{}]*)`', text):
            if path.split('/')[0] in areas and not os.path.exists(mem(path)):
                fails.append(f'{f} points at `{path}`, which does not exist')

lost = 0  # lines the staged commit removes from notes, net, minus the lines it adds to logs
for row in filter(None, git('diff', '--cached', '--numstat', '--no-renames', '-z', '--', 'memory').split('\0')):
    added, deleted, path = row.split('\t')
    path = path[7:]
    if added != '-' and (is_note(path) or is_log(path)):
        lost += (int(deleted) if is_note(path) else 0) - int(added)
if lost > SLACK: fails.append(f'notes lost {lost} more lines than the logs gained: log removed text first')

for msg in dict.fromkeys(fails): print('FAIL: ' + msg)
print('memory check: ' + ('FAIL' if fails else 'ok'))
raise SystemExit(1 if fails else 0)
