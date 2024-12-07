"""Support executing the CLI by doing `python -m composio`."""
from __future__ import annotations

from composio.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
