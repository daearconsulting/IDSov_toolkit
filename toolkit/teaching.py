"""Shared setup for the notebook teaching series."""

import os
from pathlib import Path

from toolkit.sovereignty import SovereigntyContext


def load_context(root, config_path=None):
    """Explicit argument > IDSOV_CONFIG > nation.yaml > labeled teaching example.

    A selected invalid/missing config raises; never fall back silently.
    Relative explicit/environment paths are resolved from the repository root.
    """
    root = Path(root)
    selected = config_path or os.environ.get("IDSOV_CONFIG")
    if selected:
        path = Path(selected)
        if not path.is_absolute():
            path = root / path
    else:
        path = root/"config/nation.yaml"
        if not path.exists():
            path = root / "config/teaching_example.yaml"
    return SovereigntyContext.from_config(path)


def output_directory(root, ctx):
    """Keep generated teaching material separate from working project outputs."""
    path = Path(root)/"outputs"/("teaching" if ctx.config.teaching else "project")
    path.mkdir(parents=True, exist_ok=True)
    return path
