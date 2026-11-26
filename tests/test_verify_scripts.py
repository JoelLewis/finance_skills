"""Run every skill script in ``--verify`` mode and require exit code 0.

Each script's ``--verify`` mode checks its outputs against the worked
examples in its SKILL.md.
"""

import subprocess
import sys

import pytest

from conftest import REPO_ROOT, SCRIPTS


def test_scripts_found():
    assert SCRIPTS, "no skill scripts found under plugins/*/skills/*/scripts/"


@pytest.mark.parametrize(
    "script", SCRIPTS, ids=[p.parent.parent.name for p in SCRIPTS]
)
def test_verify_passes(script):
    result = subprocess.run(
        [sys.executable, str(script), "--verify"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, (
        f"{script.relative_to(REPO_ROOT)} --verify exited {result.returncode}\n"
        f"--- stdout (tail) ---\n{result.stdout[-3000:]}\n"
        f"--- stderr (tail) ---\n{result.stderr[-3000:]}"
    )
