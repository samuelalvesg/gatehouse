#!/usr/bin/env bash
# Usage: ./install.sh <target-repo-dir> [--force] [--profile <name>] [--check]
#
# Without --profile: copies template/ (generic base for a new project).
# With --profile <name>: copies the layers listed in profiles/<name>/LAYERS, in
# order (later layers win), i.e. the exact agent/skill/plugin/MCP configuration
# of one example repo. See profiles/README.md.
#
# Existing files are skipped unless --force. Symlinks are preserved.
# --check copies nothing: it lists files that are missing or different in the
# target (and agents/skills in the target that the profile does not know) and
# exits 1 if there is any difference.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
target=""; force=""; profile=""; check=""
while [ $# -gt 0 ]; do
  case "$1" in
    --force) force="--force" ;;
    --check) check="1" ;;
    --profile) shift; profile="${1:?--profile needs a name}" ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) [ -z "$target" ] && target="$1" || { echo "unexpected argument: $1" >&2; exit 2; } ;;
  esac
  shift
done
[ -n "$target" ] || { echo "usage: install.sh <target-repo-dir> [--force] [--profile <name>] [--check]" >&2; exit 2; }
[ -d "$target" ] || { echo "target not found: $target" >&2; exit 1; }
target="$(cd "$target" && pwd)"

stage=""
cleanup() { [ -n "$stage" ] && rm -rf "$stage"; return 0; }
trap cleanup EXIT

if [ -n "$profile" ]; then
  layers_file="$here/profiles/$profile/LAYERS"
  [ -f "$layers_file" ] || { echo "unknown profile: $profile (see profiles/*/LAYERS)" >&2; exit 1; }
  stage="$(mktemp -d)"
  while read -r layer; do
    [ -z "$layer" ] && continue
    [ -d "$here/profiles/$layer/root" ] || { echo "missing layer: $layer" >&2; exit 1; }
    cp -a "$here/profiles/$layer/root/." "$stage/"
  done < "$layers_file"
  src="$stage"
else
  src="$here/template"
fi

if [ -n "$check" ]; then
  diffs=0
  cd "$src"
  while IFS= read -r p; do
    p="${p#./}"
    if [ -L "$p" ]; then
      [ -L "$target/$p" ] && [ "$(readlink "$p")" = "$(readlink "$target/$p")" ] || { echo "differs  $p (symlink)"; diffs=$((diffs+1)); }
    elif [ ! -e "$target/$p" ]; then
      echo "missing  $p"; diffs=$((diffs+1))
    elif ! cmp -s "$p" "$target/$p"; then
      echo "differs  $p"; diffs=$((diffs+1))
    fi
  done < <(find . \( -type f -o -type l \) | sort)
  if [ -n "$profile" ]; then
    for d in .claude/agents .claude/skills .agents/agents .agents/skills; do
      [ -d "$target/$d" ] && [ ! -L "$target/$d" ] || continue
      while IFS= read -r p; do
        p="${p#"$target"/}"
        [ -e "$p" ] || [ -L "$p" ] || { echo "unknown  $p (in the repo, not in the profile)"; diffs=$((diffs+1)); }
      done < <(find "$target/$d" \( -type f -o -type l \) -not -name SESSION_HANDOFF.md | sort)
    done
  fi
  echo "$diffs difference(s)"
  [ "$diffs" -eq 0 ]
  exit
fi

cd "$src"
# Regular files first, then symlinks (so a link never lands inside a not-yet-copied dir).
find . -type f | while read -r f; do
  dest="$target/${f#./}"
  if [ -e "$dest" ] && [ "$force" != "--force" ]; then
    echo "skip   $dest (exists)"; continue
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$f" "$dest"
  echo "copied $dest"
done

find . -type l | while read -r l; do
  dest="$target/${l#./}"
  link_target="$(readlink "$l")"
  if [ -L "$dest" ] || [ -e "$dest" ]; then
    if [ "$force" != "--force" ]; then
      echo "skip   $dest (exists)"; continue
    fi
    rm -rf "$dest"
  fi
  mkdir -p "$(dirname "$dest")"
  ln -s "$link_target" "$dest"
  echo "symlink $dest -> $link_target"
done

if [ -z "$profile" ]; then
  echo
  echo "Placeholders left to fill:"
  grep -rn '<[^>]*>' "$target/AGENTS.md" "$target/CLAUDE.md" "$target/.agents/agents/developer.md" "$target/.agents/skills/verify-delivery/SKILL.md" 2>/dev/null | grep -E '<(uma|pasta|tarefa|link|idioma|build|nome|Co-Author|Linguagem|Regras|Comandos)' | cut -c1-120 || true
fi
