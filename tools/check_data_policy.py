#!/usr/bin/env python3
"""Privacy and data-policy gate: keep identifying information and participant data out of the repo.

Rule #1 (policy/PRIVACY.md): nothing that could identify a real person ever enters this
repository: not in files, file names, commit messages or history. Cohort participant data
never enters either (policy/DATA_ACCESS.md).

    python tools/check_data_policy.py                  # every tracked file (CI)
    python tools/check_data_policy.py FILE ...         # specific files (pre-commit framework)
    python tools/check_data_policy.py --staged         # staged content (.githooks/pre-commit)
    python tools/check_data_policy.py --commit-msg F   # a commit message (.githooks/commit-msg)
    python tools/check_data_policy.py --history        # every blob, path, message and author

Checks:
  1. A private denylist of terms that must never appear (names, initials, places, clinicians,
     dates, exact test values). It lives OUTSIDE the repository, in
     ~/.config/alzheimer-research/denylist.txt (or the older ~/.config/open-ad-sim/denylist.txt)
     and/or the PRIVACY_DENYLIST environment variable / CI secret, one term per line.
     Matching is whole-word and case-insensitive.
  2. Private paths (patients/, private/, local/, ...) and files that look like a denylist.
  3. File types that carry personal or participant data (scans, recordings, photos, documents,
     spreadsheets, data dumps, archives, mail/contact/calendar files, keys), and any binary
     file, since it cannot be scanned.
  4. Identifier patterns: e-mail addresses, phone numbers, SSN-like numbers, dates of birth,
     record numbers, street addresses, day/month/year dates, first-person references to a
     relative, cohort participant IDs, and credentials.

Output never echoes the matched text, because CI logs of a public repository are public.

Exceptions: a reviewed path may be listed in tools/privacy_allowlist.txt (file-type and binary
rules only), and a line may carry the marker "data-policy: allow" (pattern rules only). The
denylist and private-path rules cannot be bypassed.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Iterator
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_FILE = ROOT / "tools" / "privacy_allowlist.txt"
DENYLIST_FILES = (
    Path("~/.config/alzheimer-research/denylist.txt").expanduser(),
    Path("~/.config/open-ad-sim/denylist.txt").expanduser(),
)
ALLOW_MARKER = "data-policy: allow"
MAX_BYTES = 5 * 1024 * 1024

PRIVATE_DIRS = {"patients", "patient", "private", "local", "phi", "pii", "personal"}
BLOCKED_NAMES = {".env", "id_rsa", "id_ed25519", "id_ecdsa"}
BLOCKED_TYPES = {
    "medical image or scan": (
        ".nii", ".nii.gz", ".dcm", ".dicom", ".mgz", ".mgh", ".mnc", ".img", ".hdr",
        ".nrrd", ".ima", ".bval", ".bvec", ".par", ".rec",
    ),
    "physiological recording": (
        ".edf", ".bdf", ".set", ".fdt", ".fif", ".vhdr", ".vmrk", ".eeg", ".cnt", ".gdf", ".xdf",
    ),
    "audio or video": (
        ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma",
        ".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp",
    ),
    "photo or raster image": (
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".heif", ".webp",
        ".dng", ".raw", ".cr2", ".nef", ".arw",
    ),
    "document": (
        ".pdf", ".doc", ".docx", ".odt", ".rtf", ".pages", ".ppt", ".pptx", ".key", ".odp", ".epub",
    ),
    "spreadsheet or data table": (
        ".csv", ".tsv", ".xls", ".xlsx", ".xlsm", ".ods", ".numbers",
        ".parquet", ".feather", ".arrow", ".orc", ".avro",
    ),
    "statistical or array data": (
        ".sav", ".sas7bdat", ".xpt", ".dta", ".rds", ".rdata", ".rda", ".mat", ".npy", ".npz",
        ".h5", ".hdf5", ".h5ad", ".loom", ".zarr", ".pkl", ".pickle", ".joblib",
    ),
    "database": (".db", ".sqlite", ".sqlite3", ".mdb", ".accdb", ".dbf"),
    "archive (contents cannot be scanned)": (
        ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".zst",
    ),
    "mail, contact or calendar file": (".eml", ".msg", ".mbox", ".pst", ".vcf", ".ics"),
    "key or certificate": (".pem", ".p12", ".pfx", ".jks", ".keystore", ".asc", ".gpg"),
}  # fmt: skip

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
ALLOWED_EMAILS = {"noreply@anthropic.com", "noreply@github.com"}
ALLOWED_EMAIL_DOMAINS = ("users.noreply.github.com", "example.com", "example.org", "example.net")
_MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?"
_RELATIVE = (
    r"(?:mom|mum|mother|dad|father|parents?|grand(?:mother|father|ma|pa|parents?)|wife|"
    r"husband|spouse|aunt|uncle|sister|brother|son|daughter|relatives?|family\s+members?|"
    r"in-laws?|mother-in-law|father-in-law)"
)
PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "phone number",
        re.compile(
            r"(?<![\w.+])(?:\+\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\w.])"
            r"|(?<![\w.])\+\d{1,3}[\s.-]?\d{1,4}(?:[\s.-]\d{2,4}){2,4}(?![\w.])"
        ),
    ),
    ("SSN-like number", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    (
        "date of birth",
        re.compile(
            r"\b(?:DOB|D\.O\.B\.?|date\s+of\s+birth|birth\s?date|birthday)\b\s*[:=]?\s*\(?\d"
            rf"|\bborn\s+(?:on\s+|in\s+)?(?:\d|{_MONTH}\s+\d)",
            re.I,
        ),
    ),
    (
        "medical record or patient number",
        re.compile(
            r"\b(?:MRN|medical\s+record(?:\s+(?:number|no\.?))?|patient\s+(?:id|number|no\.?)|"
            r"hospital\s+(?:number|no\.?)|NHS\s+(?:number|no\.?)|chart\s+(?:number|no\.?))"
            r"\s*[:#=]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{3,}",
            re.I,
        ),
    ),
    (
        "street address",
        re.compile(
            r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s+){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|"
            r"Dr|Court|Ct|Boulevard|Blvd|Way|Place|Pl|Terrace|Close|Crescent)\b"
        ),
    ),
    ("day/month/year date", re.compile(r"\b\d{1,2}[/.]\d{1,2}[/.](?:19|20)\d{2}\b")),
    (
        "first-person reference to a relative",
        re.compile(rf"\b(?:my|our)\s+(?:(?:late|dear|beloved)\s+)?{_RELATIVE}\b", re.I),
    ),
    ("ADNI participant ID", re.compile(r"\b\d{3}_S_\d{4}\b")),
    ("OASIS subject ID", re.compile(r"\bOAS[1-4]_?\d{4}\b")),
    (
        "credential or private key",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{36,}\b|"
            r"\bAKIA[0-9A-Z]{16}\b|\bsk-[A-Za-z0-9_-]{20,}|\bxox[abprs]-[A-Za-z0-9-]{10,}"
        ),
    ),
]
ALLOWED_IDENTITY_DOMAINS = ("users.noreply.github.com",)


# ---------------------------------------------------------------- configuration


def load_denylist(environ=os.environ, files: Iterable[Path] = DENYLIST_FILES) -> list[str]:
    terms: list[str] = []
    sources = [p.read_text(encoding="utf-8") for p in files if p.is_file()]
    sources.append(environ.get("PRIVACY_DENYLIST", ""))
    for text in sources:
        for line in text.splitlines():
            term = line.strip()
            if term and not term.startswith("#") and len(term) >= 2:
                terms.append(term)
    return sorted(set(terms), key=str.lower)


def load_allowlist(path: Path = ALLOWLIST_FILE) -> set[str]:
    if not path.is_file():
        return set()
    entries = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip()
        if entry:
            entries.add(entry)
    return entries


def _denylist_regex(terms: list[str]) -> re.Pattern | None:
    if not terms:
        return None
    alts = "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True))
    return re.compile(rf"(?<!\w)(?:{alts})(?!\w)", re.I)


# ---------------------------------------------------------------- checks


def _email_allowed(address: str) -> bool:
    address = address.lower()
    domain = address.rsplit("@", 1)[-1]
    return address in ALLOWED_EMAILS or domain.endswith(ALLOWED_EMAIL_DOMAINS)


def scan_text(text: str, deny: re.Pattern | None, where: str) -> list[str]:
    """Pattern and denylist checks on a block of text. Never returns the matched text."""
    problems = []
    if deny is not None and deny.search(text):
        problems.append(f"{where}: contains a denylisted term (not shown)")
    for lineno, line in enumerate(text.splitlines(), 1):
        if ALLOW_MARKER in line:
            continue
        if any(not _email_allowed(m.group(0)) for m in EMAIL.finditer(line)):
            problems.append(f"{where}:{lineno}: looks like an e-mail address")
        for label, pattern in PATTERNS:
            if pattern.search(line):
                problems.append(f"{where}:{lineno}: looks like a {label}")
    return problems


def scan_path(path: str, deny: re.Pattern | None, allow: set[str]) -> list[str]:
    problems = []
    parts = [p.lower() for p in PurePosixPath(path).parts]
    name = parts[-1] if parts else ""
    if any(p in PRIVATE_DIRS for p in parts[:-1]):
        problems.append(f"{path}: private directory; personal data never goes in the repository")
    if name.startswith("denylist") or name.endswith((".denylist", "_denylist.txt")):
        problems.append(f"{path}: the privacy denylist must stay outside the repository")
    if name in BLOCKED_NAMES:
        problems.append(f"{path}: blocked file (environment or key file)")
    if path not in allow:
        for label, suffixes in BLOCKED_TYPES.items():
            if name.endswith(suffixes):
                problems.append(f"{path}: blocked file type ({label})")
                break
    problems += [p.replace(f"{path}:1:", f"{path}: file name") for p in scan_text(path, deny, path)]
    return problems


def _blob_allowed(sha: str | None, allow: set[str]) -> bool:
    """History exceptions are reviewed entries "blob:<sha prefix of 12+ hex digits>"."""
    if not sha:
        return False
    return any(e.startswith("blob:") and len(e) >= 17 and sha.startswith(e[5:]) for e in allow)


def scan_blob(
    path: str, data: bytes, deny: re.Pattern | None, allow: set[str], sha: str | None = None
) -> list[str]:
    problems = scan_path(path, deny, allow)
    if len(data) > MAX_BYTES:
        mb = len(data) / 1e6
        return problems + [f"{path}: {mb:.1f} MB exceeds the {MAX_BYTES // 2**20} MB limit"]
    if b"\0" in data[:8192]:
        text = None
    else:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
    if text is None:
        if path not in allow and not _blob_allowed(sha, allow):
            problems.append(f"{path}: binary file cannot be scanned; not allowed")
        return problems
    if _blob_allowed(sha, allow):
        # A reviewed historical false positive: only the denylist still applies.
        return problems + [p for p in scan_text(text, deny, path) if "denylisted" in p]
    return problems + scan_text(text, deny, path)


def scan_commit_message(text: str, deny: re.Pattern | None, where: str = "commit message") -> list:
    body = "\n".join(line for line in text.splitlines() if not line.startswith("#"))
    return scan_text(body, deny, where)


def _identity_allowed(email: str) -> bool:
    email = email.lower()
    return email in ALLOWED_EMAILS or email.endswith(ALLOWED_IDENTITY_DOMAINS)


# ---------------------------------------------------------------- git plumbing


def _git(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True, input=input_bytes
    ).stdout


def tracked_files() -> list[Path]:
    return [Path(p) for p in _git("ls-files", "-z").decode().split("\0") if p]


def staged_blobs() -> Iterator[tuple[str, bytes]]:
    names = _git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR").decode()
    for name in filter(None, names.split("\0")):
        yield name, _git("show", f":{name}")


def history_blobs() -> Iterator[tuple[str, str, bytes]]:
    """Every blob reachable from any ref, once, with one of the paths it was committed under."""
    listing = _git("rev-list", "--objects", "--all").decode().splitlines()
    pairs = [line.split(" ", 1) for line in listing if " " in line]
    if not pairs:
        return
    query = ("\n".join(sha for sha, _ in pairs) + "\n").encode()
    kinds = _git("cat-file", "--batch-check=%(objectname) %(objecttype)", input_bytes=query)
    blob_shas = {line.split()[0] for line in kinds.decode().splitlines() if line.endswith(" blob")}
    for sha, path in pairs:
        if sha in blob_shas:
            yield sha, path, _git("cat-file", "blob", sha)


def history_paths() -> set[str]:
    """Every path that ever existed in any commit (rev-list names each blob only once)."""
    out = _git("log", "--all", "--name-only", "-z", "--format=").decode()
    return {p.strip("\n") for p in out.split("\0") if p.strip("\n")}


def history_commits() -> Iterator[tuple[str, str, str, str]]:
    fmt = "%H%x00%ae%x00%ce%x00%B%x1e"
    for record in _git("log", "--all", f"--format={fmt}").decode().split("\x1e"):
        record = record.lstrip("\n")
        if record:
            sha, author, committer, body = record.split("\0", 3)
            yield sha, author, committer, body


# ---------------------------------------------------------------- entry point


def _display_path(p: Path) -> str:
    """Repository-relative path when possible; files outside the repository keep their own."""
    if p.is_absolute():
        try:
            return p.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return p.as_posix()
    return p.as_posix()


def scan_files(paths: Iterable[Path], deny, allow) -> list[str]:
    problems = []
    for p in paths:
        rel = _display_path(p)
        if p.is_file():
            problems += scan_blob(rel, p.read_bytes(), deny, allow)
        else:
            problems += scan_path(rel, deny, allow)
    return problems


def scan_history(deny, allow) -> list[str]:
    problems = []
    for sha, path, data in history_blobs():
        found = scan_blob(path, data, deny, allow, sha=sha)
        problems += [f"history (blob {sha[:12]}): {p}" for p in found]
    for path in history_paths():
        problems += [f"history: {p}" for p in scan_path(path, deny, allow)]
    for sha, author, committer, body in history_commits():
        short = sha[:9]
        if not _identity_allowed(author):
            problems.append(f"commit {short}: author e-mail is not a no-reply address")
        if not _identity_allowed(committer):
            problems.append(f"commit {short}: committer e-mail is not a no-reply address")
        problems += scan_commit_message(body, deny, f"commit {short} message")
    return sorted(set(problems))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true", help="scan staged content")
    mode.add_argument("--commit-msg", metavar="FILE", help="scan a commit message file")
    mode.add_argument("--history", action="store_true", help="scan the whole git history")
    ap.add_argument("files", nargs="*", type=Path)
    args = ap.parse_args(argv)

    terms = load_denylist()
    deny, allow = _denylist_regex(terms), load_allowlist()
    if args.commit_msg:
        problems = scan_commit_message(Path(args.commit_msg).read_text(encoding="utf-8"), deny)
    elif args.staged:
        problems = [p for name, data in staged_blobs() for p in scan_blob(name, data, deny, allow)]
    elif args.history:
        problems = scan_history(deny, allow)
    else:
        problems = scan_files(args.files or tracked_files(), deny, allow)

    if not terms:
        print(
            "note: no private denylist configured (see policy/PRIVACY.md); pattern checks ran.",
            file=sys.stderr,
        )
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(
            f"\n{len(problems)} privacy/data-policy problem(s). Nothing that could identify a real "
            "person, and no participant data, may enter this repository. See policy/PRIVACY.md.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
