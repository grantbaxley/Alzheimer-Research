"""Provenance registry: every external resource the project uses or evaluates.

Each ``registry/*.yaml`` file holds a ``resources`` list. A record states what
the resource is, its triage grade from the landscape review (A build on,
B vet first, C avoid), how its license was established, and how far *this
project* has verified it. Nothing is trusted because it is in the registry;
``our_status`` says what we have actually checked.

Usage:
    python -m alzres.registry validate [registry_dir]
    python -m alzres.registry summary [registry_dir]
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

TRIAGE = {"A", "B", "C"}
KINDS = {
    "software",
    "model",
    "dataset",
    "benchmark",
    "knowledge-base",
    "platform",
    "research-claim",
}
LICENSE_CLASSES = {
    "permissive",
    "weak-copyleft",
    "copyleft",
    "network-copyleft",
    "non-commercial",
    "data-terms",
    "none",
    "unconfirmed",
}
LICENSE_SOURCES = {"license-file", "api-metadata", "docs", "secondary", "unconfirmed", "n/a"}
OUR_STATUS = {"not-started", "smoke-tested", "reproducing", "reproduced", "failed", "rejected"}
ACCESS = {"open", "account", "application", "controlled", "enclave", "closed"}
EVIDENCE = {"yes", "partial", "no", "unknown"}
REQUIRED = ("id", "name", "url", "kind", "triage", "license", "reason", "checked")
# A-grade items must be reusable by an open project.
A_ALLOWED_LICENSES = {"permissive", "weak-copyleft", "copyleft", "data-terms"}
DEFAULT_DIR = Path(__file__).resolve().parents[2] / "registry"


@dataclass
class Record:
    data: dict
    path: Path

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)


def load(registry_dir: Path | str = DEFAULT_DIR) -> list[Record]:
    records = []
    for path in sorted(Path(registry_dir).glob("*.yaml")):
        doc = yaml.safe_load(path.read_text()) or {}
        for item in doc.get("resources", []):
            records.append(Record(item, path))
    return records


def validate_record(r: dict) -> list[str]:
    errs = [f"missing '{k}'" for k in REQUIRED if k not in r]
    if errs:
        return errs
    if r["triage"] not in TRIAGE:
        errs.append(f"triage must be one of {sorted(TRIAGE)}")
    if r["kind"] not in KINDS:
        errs.append(f"kind must be one of {sorted(KINDS)}")
    lic = r["license"]
    if not isinstance(lic, dict) or not {"spdx", "class", "source"} <= lic.keys():
        errs.append("license needs spdx, class and source")
    else:
        if lic["class"] not in LICENSE_CLASSES:
            errs.append(f"license.class must be one of {sorted(LICENSE_CLASSES)}")
        if lic["source"] not in LICENSE_SOURCES:
            errs.append(f"license.source must be one of {sorted(LICENSE_SOURCES)}")
        if r["triage"] == "A" and lic["class"] not in A_ALLOWED_LICENSES:
            errs.append("triage A requires a reusable license class")
    status = r.get("our_status", "not-started")
    if status not in OUR_STATUS:
        errs.append(f"our_status must be one of {sorted(OUR_STATUS)}")
    if status in {"reproduced", "failed", "smoke-tested"} and not r.get("verification"):
        errs.append(f"our_status '{status}' needs a 'verification' pointer (test, report or PR)")
    if r["kind"] == "dataset" and r.get("access") not in ACCESS:
        errs.append(f"datasets need access in {sorted(ACCESS)}")
    for key in ("peer_reviewed", "independent_replication"):
        if key in r and r[key] not in EVIDENCE:
            errs.append(f"{key} must be one of {sorted(EVIDENCE)}")
    if r["triage"] == "A" and r.get("peer_reviewed") == "no":
        errs.append("triage A cannot have peer_reviewed: no")
    checked = r["checked"]
    if not isinstance(checked, dt.date):
        errs.append("checked must be an ISO date (YYYY-MM-DD)")
    if not str(r["url"]).startswith("https://"):
        errs.append("url must be https")
    return errs


def validate(records: list[Record]) -> list[str]:
    problems = []
    ids = Counter(r.get("id") for r in records)
    for dup, n in ids.items():
        if n > 1:
            problems.append(f"duplicate id '{dup}' ({n} records)")
    for rec in records:
        for e in validate_record(rec.data):
            problems.append(f"{rec.path.name}:{rec.get('id', '?')}: {e}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="alzres-registry")
    parser.add_argument("command", choices=["validate", "summary"])
    parser.add_argument("registry_dir", nargs="?", default=str(DEFAULT_DIR))
    args = parser.parse_args(argv)
    records = load(args.registry_dir)
    if args.command == "validate":
        problems = validate(records)
        for p in problems:
            print(p, file=sys.stderr)
        print(f"{len(records)} records, {len(problems)} problem(s)")
        return 1 if problems else 0
    by = Counter((r.get("triage"), r.get("our_status", "not-started")) for r in records)
    for (triage, status), n in sorted(by.items()):
        print(f"{triage}  {status:<13} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
