#!/bin/sh
# Usage: sh link.sh [instructions-file]
# Links memory/MEMORY.md into an agent's instructions file (default ~/.claude/CLAUDE.md) and installs
# check.py as this repo's pre-commit hook. An existing instructions file is moved to <file>.bak-<time>.
set -e
cd "$(dirname "$0")"
SRC="$(pwd)/memory/MEMORY.md"
TARGET="${1:-$HOME/.claude/CLAUDE.md}"
case "$(uname -s)" in # Windows: symlinks need admin rights, so write a one-line @import instead
	MINGW* | MSYS* | CYGWIN*) IMPORT="@$(cygpath -m "$SRC")" NOW=$(cat "$TARGET" 2>/dev/null || true) ;;
	*) IMPORT='' NOW=$(readlink "$TARGET" 2>/dev/null || true) ;;
esac
if [ "$NOW" != "${IMPORT:-$SRC}" ]; then
	mkdir -p "$(dirname "$TARGET")"
	if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
		BAK="$TARGET.bak-$(date +%Y%m%d%H%M%S)" && mv "$TARGET" "$BAK" && echo "moved the existing file to $BAK"
	fi
	if [ -n "$IMPORT" ]; then echo "$IMPORT" >"$TARGET"; else ln -s "$SRC" "$TARGET"; fi
fi
echo "linked $TARGET -> ${IMPORT:-$SRC}"

for PY in python3 python; do
	"$PY" -c 'import sys; assert sys.version_info >= (3, 7)' 2>/dev/null && break || PY=
done
[ -n "$PY" ] || { echo "Python 3.7+ not found: pre-commit check not installed" >&2; exit 1; }
HOOKS="$(git rev-parse --git-dir)/hooks"
mkdir -p "$HOOKS"
printf '#!/bin/sh\nexec %s check.py\n' "$PY" >"$HOOKS/pre-commit"
chmod +x "$HOOKS/pre-commit"
echo "installed $HOOKS/pre-commit ($PY check.py)"
