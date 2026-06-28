#!/usr/bin/env python3
"""Run local smoke checks without requiring manual PYTHONPATH setup.

This script locates the repository root from its own file path, so it can be
run from any current working directory:

    python path/to/repo/tools/local_smoke_check.py

It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SDK_PATH = REPO_ROOT / "sdk" / "python"


def run_step(name: str, command: list[str], env: dict[str, str] | None = None) -> None:
    print(f"\n== {name} ==", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=REPO_ROOT, env=env, check=True)


def python_env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    paths = [str(SDK_PATH)]
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def main() -> int:
    env = python_env()
    output_dir = Path(tempfile.gettempdir()) / "robot_controller_local_smoke"

    steps: list[tuple[str, list[str], dict[str, str] | None]] = [
        (
            "Python SDK unit tests",
            [sys.executable, "-m", "unittest", "discover", "-s", "sdk/python/tests"],
            env,
        ),
        (
            "Python SDK mock example",
            [sys.executable, "sdk/python/examples/mock_smoke_test.py"],
            env,
        ),
        (
            "Factory test mock",
            [
                sys.executable,
                "tools/factory_test.py",
                "--mock",
                "--order",
                "LOCAL-SMOKE",
                "--board-id",
                "MOCK-LOCAL",
                "--operator",
                "LocalSmoke",
                "--output-dir",
                str(output_dir),
            ],
            None,
        ),
    ]

    gcc = shutil.which("gcc")
    if gcc:
        steps.append(
            (
                "Firmware protocol compile check",
                [
                    gcc,
                    "-std=c99",
                    "-Wall",
                    "-Wextra",
                    "-pedantic",
                    "-I",
                    "firmware",
                    "-c",
                    "firmware/App/protocol.c",
                    "-o",
                    str(Path(tempfile.gettempdir()) / "robot_controller_protocol.o"),
                ],
                None,
            )
        )
    else:
        print("\n== Firmware protocol compile check ==", flush=True)
        print("SKIP: gcc not found on PATH", flush=True)

    for name, command, step_env in steps:
        run_step(name, command, step_env)

    print("\nLocal smoke checks completed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
