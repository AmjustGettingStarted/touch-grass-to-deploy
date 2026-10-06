#!/usr/bin/env python3
"""
================================================================================
 Setup Script: Touch Grass to Deploy (Git Pre-Push Hook Installer)
================================================================================
 Installs the pre-push git hook into .git/hooks/pre-push.
 Cross-platform support for Windows (Git Bash/cmd/powershell), macOS, and Linux.
================================================================================
"""

import os
import sys
import stat
import argparse
from pathlib import Path

HOOK_CONTENT = """#!/bin/sh
# ==============================================================================
# Touch Grass to Deploy - Git Pre-Push Gatekeeper
# Dev Community x Hugging Face Hacktoberfest Challenge
# ==============================================================================
# This hook intercepts 'git push' and requires local vision proof of outdoor nature.
# ==============================================================================

# Locate repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
    REPO_ROOT="."
fi

VERIFY_SCRIPT="$REPO_ROOT/verify_grass.py"

if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "⚠️  Touch Grass hook: verify_grass.py not found at $VERIFY_SCRIPT. Skipping check."
    exit 0
fi

# Locate suitable Python binary (prioritize local virtualenvs)
PYTHON_BIN=""

if [ -f "$REPO_ROOT/.venv/bin/python" ]; then
    PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
elif [ -f "$REPO_ROOT/.venv/Scripts/python.exe" ]; then
    PYTHON_BIN="$REPO_ROOT/.venv/Scripts/python.exe"
elif [ -f "$REPO_ROOT/venv/bin/python" ]; then
    PYTHON_BIN="$REPO_ROOT/venv/bin/python"
elif [ -f "$REPO_ROOT/venv/Scripts/python.exe" ]; then
    PYTHON_BIN="$REPO_ROOT/venv/Scripts/python.exe"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
elif command -v py >/dev/null 2>&1; then
    PYTHON_BIN="py -3"
else
    echo "❌ Error: Python not found in PATH or virtual environment!"
    echo "Please ensure Python 3.9+ is installed to run the Touch Grass pre-push gatekeeper."
    exit 1
fi

# Run the verification script
"$PYTHON_BIN" "$VERIFY_SCRIPT"
VERIFY_EXIT=$?

if [ $VERIFY_EXIT -ne 0 ]; then
    echo ""
    echo "❌ git push aborted by Touch Grass gatekeeper."
    echo "💡 Touch grass, drop grass.jpg into the repo root, and try pushing again!"
    echo ""
    exit 1
fi

exit 0
"""

def install_hook(repo_root: Path):
    git_dir = repo_root / ".git"
    if not git_dir.is_dir():
        print(f"❌ Error: Not a git repository: {repo_root}")
        print("Please initialize git first using 'git init' or run this from a git repository.")
        sys.exit(1)

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_file = hooks_dir / "pre-push"

    # Normalize line endings to LF for portable bash execution
    clean_content = HOOK_CONTENT.replace("\r\n", "\n")

    with open(hook_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(clean_content)

    # Set executable permissions (chmod +x)
    current_mode = hook_file.stat().st_mode
    hook_file.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print("\n🌿 ================================================================")
    print("🌿  Touch Grass to Deploy: Hook successfully installed!")
    print("🌿 ================================================================")
    print(f"📍 Location: {hook_file}")
    print("\nEvery time you run `git push`, the gatekeeper will now inspect")
    print("for physical proof of nature before allowing code to deploy.\n")
    print("To test right now:")
    print("  python verify_grass.py")
    print("================================================================\n")

def uninstall_hook(repo_root: Path):
    hook_file = repo_root / ".git" / "hooks" / "pre-push"
    if hook_file.exists():
        hook_file.unlink()
        print(f"🗑️  Pre-push hook removed from {hook_file}.")
    else:
        print("ℹ️  No pre-push hook was found to uninstall.")

def main():
    parser = argparse.ArgumentParser(
        description="Install or uninstall Touch Grass Git Pre-Push Hook"
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall the pre-push hook",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent

    if args.uninstall:
        uninstall_hook(repo_root)
    else:
        install_hook(repo_root)

if __name__ == "__main__":
    main()
