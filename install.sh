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

# Plugin dependency map (space-separated list of deps per plugin)
declare -A PLUGIN_DEPS
PLUGIN_DEPS["core"]=""
PLUGIN_DEPS["wealth-management"]="core"
PLUGIN_DEPS["compliance"]="core"
PLUGIN_DEPS["advisory-practice"]="core wealth-management"
PLUGIN_DEPS["trading-operations"]="core"
PLUGIN_DEPS["client-operations"]="core"
PLUGIN_DEPS["data-integration"]="core"

ALL_PLUGINS=(core wealth-management compliance advisory-practice trading-operations client-operations data-integration)

# Track installed plugins to avoid duplicates
declare -A INSTALLED_PLUGINS

usage() {
  cat <<EOF
Usage: $0 --plugin <plugin-name> --target <path>
       $0 --plugin all --target <path>
       $0 --list

Options:
  --plugin <name>   Plugin to install (or "all" to install everything)
  --target <path>   Target project directory (must contain .claude/)
  --list            List available plugins and exit
  --help            Show this help

Available plugins:
  core               Mathematical foundations (always installed)
  wealth-management  Investment knowledge, portfolio construction, personal finance
  compliance         US securities regulatory guidance
  advisory-practice  Advisor-facing systems and workflows
  trading-operations Order lifecycle, execution, settlement
  client-operations  Account lifecycle and servicing
  data-integration   Reference data and integration patterns
EOF
}

list_plugins() {
  local marketplace="$SCRIPT_DIR/marketplace.json"
  echo "Available plugins:"
  echo ""
  if [[ -f "$marketplace" ]]; then
    python3 - "$marketplace" <<'PYEOF'
import json, sys

with open(sys.argv[1]) as f:
    catalog = json.load(f)

for plugin in catalog.get("plugins", []):
    name = plugin.get("name", "")
    description = plugin.get("description", "")
    skill_count = plugin.get("skillCount", len(plugin.get("skills", [])))
    deps = plugin.get("dependencies", [])
    print(f"  {name} ({skill_count} skills)")
    print(f"    {description}")
    if deps:
        print(f"    Dependencies: {' '.join(deps)}")
    print()
PYEOF
  else
    # Fallback: read individual plugin.json files
    for plugin in "${ALL_PLUGINS[@]}"; do
      manifest="$PLUGINS_DIR/$plugin/plugin.json"
      if [[ -f "$manifest" ]]; then
        description=$(python3 -c "import json,sys; d=json.load(open('$manifest')); print(d.get('description',''))" 2>/dev/null || echo "")
        skill_count=$(ls "$PLUGINS_DIR/$plugin/skills/" 2>/dev/null | wc -l | tr -d ' ')
        echo "  $plugin ($skill_count skills)"
        echo "    $description"
        deps="${PLUGIN_DEPS[$plugin]:-}"
        if [[ -n "$deps" ]]; then
          echo "    Dependencies: $deps"
        fi
        echo ""
      fi
    done
  fi
}

install_plugin() {
  local plugin="$1"
  local target="$2"
  local skills_dir="$target/.claude/skills"

  # Skip if already installed in this run
  if [[ -n "${INSTALLED_PLUGINS[$plugin]+_}" ]]; then
    return 0
  fi

  # Validate plugin exists
  if [[ ! -d "$PLUGINS_DIR/$plugin" ]]; then
    echo "Error: Unknown plugin '$plugin'" >&2
    echo "Run '$0 --list' to see available plugins." >&2
    exit 1
  fi

  # Install dependencies first
  local deps="${PLUGIN_DEPS[$plugin]:-}"
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
          ((count++))
        fi
      fi
    done
    echo "  $count skill(s) installed from $plugin"
  else
    echo "  Warning: no skills directory found for plugin '$plugin'"
  fi

  INSTALLED_PLUGINS[$plugin]=1
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
