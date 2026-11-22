#!/usr/bin/env bash
# Validates frontmatter of every agent/skill and that install.sh is idempotent.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
check() { # file, required keys...
  local f="$1"; shift
  [ "$(sed -n 1p "$f")" = "---" ] || { echo "no frontmatter: $f"; fail=1; return; }
  local fm; fm="$(awk 'NR>1 && /^---$/{exit} NR>1{print}' "$f")"
  for k in "$@"; do echo "$fm" | grep -q "^$k:" || { echo "missing $k: $f"; fail=1; }; done
}
# Every enabled plugin "name@marketplace" must name a marketplace declared in
# extraKnownMarketplaces, or a session that only reads the repo cannot install it.
check_settings() {
  python3 - "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
known = set(d.get("extraKnownMarketplaces", {}))
bad = [p for p in d.get("enabledPlugins", {}) if "@" not in p or p.split("@", 1)[1] not in known]
for p in bad: print(f"plugin without declared marketplace: {p} ({sys.argv[1]})")
sys.exit(1 if bad else 0)
PY
}
for f in "$root"/template/.claude/agents/*.md; do check "$f" name description tools model; done
for f in "$root"/template/.claude/skills/*/SKILL.md; do check "$f" name description; done
check_settings "$root/template/.claude/settings.json" || fail=1
neg="$(mktemp)"
echo '{"enabledPlugins": {"x@undeclared": true}}' > "$neg"
if check_settings "$neg" >/dev/null; then echo "check_settings accepted an undeclared marketplace"; fail=1; fi
rm -f "$neg"
[ -f "$root/template/.claude/skills/verify-delivery/SKILL.md" ] || { echo "missing skill verify-delivery"; fail=1; }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
"$root/install.sh" "$tmp" >/dev/null
echo "keep" > "$tmp/AGENTS.md"
"$root/install.sh" "$tmp" >/dev/null
[ "$(cat "$tmp/AGENTS.md")" = "keep" ] || { echo "install overwrote existing file"; fail=1; }
exit $fail
