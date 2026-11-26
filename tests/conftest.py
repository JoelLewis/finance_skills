"""Shared helpers for the script test suite.

Skill scripts are standalone files, not an installed package, so tests load
them by path with ``load_script``.
"""

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

from hypothesis import HealthCheck, settings

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = sorted(REPO_ROOT.glob("plugins/*/skills/*/scripts/*.py"))

# "ci" runs 1,000 random cases per property; "dev" runs 100 for quick local runs.
settings.register_profile(
    "ci", max_examples=1000, deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.register_profile("dev", max_examples=100, deadline=None)
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "ci"))


def load_script(skill: str) -> ModuleType:
    """Import the script inside ``plugins/*/skills/<skill>/scripts/``."""
    matches = [p for p in SCRIPTS if p.parent.parent.name == skill]
    if len(matches) != 1:
        raise LookupError(f"expected one script for skill {skill!r}, found {matches}")
    path = matches[0]
    name = f"skill_{path.stem}"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
