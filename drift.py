#!/usr/bin/env python3
"""Lists notes that point at things that no longer exist: backticked absolute paths, and URLs that
return 404/410 or whose host is unknown. It never blocks; run it now and then. --no-urls skips the network."""
import os, re, socket, sys, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

MEM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'memory')
PLACEHOLDER = re.compile(r'[<>{}*$|]|\.\.\.|example\.')
found, urls = [], {}
for folder, _, names in os.walk(MEM):
    for name in names:
        if not name.endswith('.md') or re.search(r'(^|-)log\.md$', name): continue
        note = os.path.relpath(os.path.join(folder, name), MEM).replace(os.sep, '/')
        with open(os.path.join(folder, name), encoding='utf-8', errors='replace') as f: text = f.read()
        for path in re.findall(r'`((?:~|/|[A-Za-z]:[/\\])[^`\n]+)`', text):
            if not PLACEHOLDER.search(path) and not os.path.exists(os.path.expanduser(path)):
                found.append(f'{note}: `{path}` does not exist')
        for url in re.findall(r'https?://[^\s`<>()"\']+', text):
            if not PLACEHOLDER.search(url): urls.setdefault(url.rstrip('.,;:'), set()).add(note)

def gone(url):  # auth walls, rate limits and timeouts do not count as gone
    try: urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'drift'}), timeout=10)
    except urllib.error.HTTPError as e: return e.code in (404, 410)
    except urllib.error.URLError as e: return getattr(e.reason, 'errno', None) == socket.EAI_NONAME
    except Exception: pass
    return False

if '--no-urls' not in sys.argv:
    with ThreadPoolExecutor(16) as pool:
        for url, dead in zip(urls, pool.map(gone, urls)):
            found += [f'{note}: {url} is gone' for note in sorted(urls[url]) if dead]
print('\n'.join(sorted(found)) or 'drift: nothing found')
