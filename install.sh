#!/usr/bin/env bash
# install.sh — Finance Skills plugin installer
#
# Usage:
#   ./install.sh --plugin <plugin-name> --target <path/to/project>
#   ./install.sh --plugin all --target <path/to/project>
#   ./install.sh --list
#
# The installer symlinks each skill directory from the chosen plugin(s) into
# <target>/.claude/skills/. The core plugin is always installed first.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

# Plugin dependencies come from each plugin's manifest
# (plugins/<name>/.claude-plugin/plugin.json). Returns a space-separated
# list; empty if the manifest is missing or unreadable.
plugin_deps() {
  local manifest="$PLUGINS_DIR/$1/.claude-plugin/plugin.json"
  if [[ -f "$manifest" ]]; then
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(' '.join(d.get('dependencies',[])))" "$manifest" 2>/dev/null || echo ""
  else
    echo ""
  fi
}

# The filesystem is the source of truth: every directory under plugins/ is a
# plugin. (bash 3.2 compatible — no mapfile.)
ALL_PLUGINS=()
for _p in "$PLUGINS_DIR"/*/; do
  [[ -d "$_p" ]] && ALL_PLUGINS+=("$(basename "$_p")")
done

# Track installed plugins to avoid duplicates (space-delimited list;
# bash 3.2 compatible — no associative arrays).
INSTALLED_PLUGINS=" "

usage() {
  cat <<EOF
Usage: $0 --plugin <plugin-name> --target <path>
       $0 --plugin all --target <path>
       $0 --list
       $0 --check

Options:
  --plugin <name>   Plugin to install (or "all" to install everything)
  --target <path>   Target project directory (must contain .claude/)
  --list            List available plugins and exit
  --check           Validate manifests, skill dirs, and CLAUDE.md counts
  --help            Show this help

Run '$0 --list' to see available plugins.
EOF
}

list_plugins() {
  echo "Available plugins:"
  echo ""
  for plugin in "${ALL_PLUGINS[@]}"; do
    manifest="$PLUGINS_DIR/$plugin/.claude-plugin/plugin.json"
    description=""
    if [[ -f "$manifest" ]]; then
      description=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('description',''))" "$manifest" 2>/dev/null || echo "")
    fi
    skill_count=$(ls "$PLUGINS_DIR/$plugin/skills/" 2>/dev/null | wc -l | tr -d ' ')
    echo "  $plugin ($skill_count skills)"
    echo "    $description"
    deps="$(plugin_deps "$plugin")"
    if [[ -n "$deps" ]]; then
      echo "    Dependencies: $deps"
    fi
    echo ""
  done
}

check_repo() {
  python3 - "$SCRIPT_DIR" <<'PYEOF'
import json, os, re, sys

root = sys.argv[1]
plugins_dir = os.path.join(root, "plugins")
errors = []

plugins = sorted(
    p for p in os.listdir(plugins_dir)
    if os.path.isdir(os.path.join(plugins_dir, p))
)
counts = {}

for p in plugins:
    skills_dir = os.path.join(plugins_dir, p, "skills")
    skills = sorted(
        s for s in os.listdir(skills_dir)
        if os.path.isdir(os.path.join(skills_dir, s))
    ) if os.path.isdir(skills_dir) else []
    counts[p] = len(skills)
    for s in skills:
        if not os.path.isfile(os.path.join(skills_dir, s, "SKILL.md")):
            errors.append(f"{p}/skills/{s}: missing SKILL.md")

    manifest_path = os.path.join(plugins_dir, p, ".claude-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        errors.append(f"{p}: missing .claude-plugin/plugin.json")
        continue
    try:
        manifest = json.load(open(manifest_path))
    except json.JSONDecodeError as e:
        errors.append(f"{p}: plugin.json is invalid JSON ({e})")
        continue
    if manifest.get("name") != p:
        errors.append(f"{p}: manifest name '{manifest.get('name')}' != directory name")
    for dep in manifest.get("dependencies", []):
        if dep not in plugins:
            errors.append(f"{p}: dependency '{dep}' is not a plugin directory")

marketplace_path = os.path.join(root, ".claude-plugin", "marketplace.json")
try:
    marketplace = json.load(open(marketplace_path))
    listed = sorted(pl.get("name", "") for pl in marketplace.get("plugins", []))
    if listed != plugins:
        errors.append(
            f"marketplace.json plugins {listed} != plugin directories {plugins}"
        )
except (OSError, json.JSONDecodeError) as e:
    errors.append(f".claude-plugin/marketplace.json unreadable: {e}")

claude_md = open(os.path.join(root, "CLAUDE.md")).read()
for name, claimed in re.findall(r"- \*\*([\w-]+)\*\* \((\d+) skills?\)", claude_md):
    if name in counts and counts[name] != int(claimed):
        errors.append(
            f"CLAUDE.md says {name} has {claimed} skills; directories have {counts[name]}"
        )
m = re.search(r"(\d+) skills across (\d+) plugin domains", claude_md)
if m:
    total, ndomains = int(m.group(1)), int(m.group(2))
    if total != sum(counts.values()):
        errors.append(
            f"CLAUDE.md total {total} != actual {sum(counts.values())}"
        )
    if ndomains != len(plugins):
        errors.append(f"CLAUDE.md says {ndomains} domains; found {len(plugins)}")

if errors:
    print("Check FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(
    f"Check passed: {len(plugins)} plugins, {sum(counts.values())} skills; "
    "manifests, skill dirs, and CLAUDE.md counts are consistent."
)
PYEOF
}

install_plugin() {
  local plugin="$1"
  local target="$2"
  local skills_dir="$target/.claude/skills"

  # Skip if already installed in this run
  case "$INSTALLED_PLUGINS" in
    *" $plugin "*) return 0 ;;
  esac

  # Validate plugin exists
  if [[ ! -d "$PLUGINS_DIR/$plugin" ]]; then
    echo "Error: Unknown plugin '$plugin'" >&2
    echo "Run '$0 --list' to see available plugins." >&2
    exit 1
  fi

  # Install dependencies first
  local deps
  deps="$(plugin_deps "$plugin")"
  for dep in $deps; do
    install_plugin "$dep" "$target"
  done

  echo "Installing plugin: $plugin"

  # Create target skills directory if needed
  mkdir -p "$skills_dir"

  # Symlink each skill directory
  local plugin_skills_dir="$PLUGINS_DIR/$plugin/skills"
  if [[ -d "$plugin_skills_dir" ]]; then
    local count=0
    for skill_dir in "$plugin_skills_dir"/*/; do
      if [[ -d "$skill_dir" ]]; then
        skill_name="$(basename "$skill_dir")"
        link_path="$skills_dir/$skill_name"
        if [[ -e "$link_path" || -L "$link_path" ]]; then
          echo "  Skipping $skill_name (already exists)"
        else
          ln -s "$skill_dir" "$link_path"
          echo "  Linked $skill_name"
          # NOT ((count++)): under `set -e`, ((count++)) returns the
          # pre-increment value, so the first increment (0) aborts the script.
          count=$((count + 1))
        fi
      fi
    done
    echo "  $count skill(s) installed from $plugin"
  else
    echo "  Warning: no skills directory found for plugin '$plugin'"
  fi

  INSTALLED_PLUGINS="$INSTALLED_PLUGINS$plugin "
}

# --- Parse arguments ---

PLUGIN=""
TARGET=""
CMD=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plugin)
      PLUGIN="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --list)
      CMD="list"
      shift
      ;;
    --check)
      CMD="check"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$CMD" == "list" ]]; then
  list_plugins
  exit 0
fi

if [[ "$CMD" == "check" ]]; then
  check_repo
  exit 0
fi

# Validate required arguments
if [[ -z "$PLUGIN" ]]; then
  echo "Error: --plugin is required" >&2
  usage >&2
  exit 1
fi

if [[ -z "$TARGET" ]]; then
  echo "Error: --target is required" >&2
  usage >&2
  exit 1
fi

# Validate target directory
if [[ ! -d "$TARGET" ]]; then
  echo "Error: Target directory does not exist: $TARGET" >&2
  exit 1
fi

# Install
if [[ "$PLUGIN" == "all" ]]; then
  echo "Installing all plugins into $TARGET/.claude/skills/"
  echo ""
  for p in "${ALL_PLUGINS[@]}"; do
    install_plugin "$p" "$TARGET"
  done
else
  echo "Installing plugin '$PLUGIN' into $TARGET/.claude/skills/"
  echo ""
  install_plugin "$PLUGIN" "$TARGET"
fi

echo ""
echo "Done. Skills are available at $TARGET/.claude/skills/"
