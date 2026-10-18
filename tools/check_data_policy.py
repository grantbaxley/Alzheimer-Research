#!/usr/bin/env python3
"""Block commits that could leak participant-level data (see policy/DATA_ACCESS.md).

Checks the given files (default: all git-tracked files) for:
  * imaging / single-cell / raw-data file types that must never be committed,
  * cohort participant identifier patterns (ADNI, OASIS),
  * files over the size limit.

    python tools/check_data_policy.py            # scan tracked files
    python tools/check_data_policy.py FILE ...   # scan specific files (pre-commit)

A line containing "data-policy: allow" is skipped; use it only for documentation
of the patterns themselves, and justify it in review.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOCKED_SUFFIXES = (
    ".nii",
    ".nii.gz",
    ".dcm",
    ".mgz",
    ".mgh",
    ".mnc",
    ".img",
    ".hdr",
    ".nrrd",
    ".ima",
    ".bval",
    ".bvec",
    ".edf",
    ".bdf",
    ".h5ad",
    ".loom",
    ".rds",
    ".sav",
    ".sas7bdat",
    ".dta",
    ".pkl",
    ".pickle",
)
# ADNI PTID (site_S_subject) and OASIS session/subject IDs.
ID_PATTERNS = {
    "ADNI participant ID": re.compile(r"\b\d{3}_S_\d{4}\b"),
    "OASIS subject ID": re.compile(r"\bOAS[1-4]_?\d{4}\b"),
}
MAX_BYTES = 5 * 1024 * 1024
ALLOW_MARKER = "data-policy: allow"


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True)
    return [Path(p) for p in out.stdout.decode().split("\0") if p]


def scan(paths: list[Path]) -> list[str]:
    problems = []
    for path in paths:
        name = path.name.lower()
        if name.endswith(BLOCKED_SUFFIXES):
            problems.append(f"{path}: blocked file type (imaging/raw/participant data)")
            continue
        if not path.is_file():
            continue
        size = path.stat().st_size
        if size > MAX_BYTES:
            problems.append(f"{path}: {size / 1e6:.1f} MB exceeds {MAX_BYTES / 1e6:.0f} MB limit")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if ALLOW_MARKER in line:
                continue
            for label, pattern in ID_PATTERNS.items():
                if pattern.search(line):
                    problems.append(f"{path}:{lineno}: looks like a {label}")
    return problems


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] if argv else tracked_files()
    problems = scan(paths)
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(
            f"\n{len(problems)} data-policy problem(s). See policy/DATA_ACCESS.md.", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
