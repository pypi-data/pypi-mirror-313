from __future__ import annotations

import sys
from dataclasses import dataclass
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING

from pyutilkit.timing import Stopwatch, Timing

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class ProcessOutput:
    stdout: bytes
    stderr: bytes
    pid: int
    returncode: int
    elapsed: Timing


def run_command(
    command: str | list[str],
    cwd: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> ProcessOutput:
    stdout = []
    stderr = []
    stopwatch = Stopwatch()
    with stopwatch:
        process = Popen(  # noqa: S603
            command, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env
        )

        for line in process.stdout or []:
            sys.stdout.buffer.write(line)  # type: ignore[misc]
            sys.stdout.flush()
            stdout.append(line)

        for line in process.stderr or []:
            sys.stderr.buffer.write(line)  # type: ignore[misc]
            sys.stderr.flush()
            stderr.append(line)

    with stopwatch:
        process.wait()

    return ProcessOutput(
        stdout=b"".join(stdout),
        stderr=b"".join(stderr),
        pid=process.pid,
        returncode=process.returncode,  # type: ignore[misc]
        elapsed=stopwatch.elapsed,
    )
