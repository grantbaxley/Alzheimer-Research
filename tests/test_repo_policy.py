"""Repository-level checks: registry validity and generated docs (privacy: test_privacy_gate)."""

import subprocess
import sys
from pathlib import Path

from alzres.registry import load, validate, validate_record

ROOT = Path(__file__).resolve().parents[1]


def test_registry_is_valid():
    records = load(ROOT / "registry")
    assert len(records) > 50
    assert validate(records) == []


def test_a_grade_rejects_noncommercial_license():
    rec = {
        "id": "x",
        "name": "x",
        "url": "https://example.org",
        "kind": "model",
        "triage": "A",
        "license": {"spdx": "CC-BY-NC-4.0", "class": "non-commercial", "source": "license-file"},
        "reason": "x",
        "checked": __import__("datetime").date(2026, 1, 1),
    }
    assert any("reusable license" in e for e in validate_record(rec))


def test_status_claims_need_verification_pointer():
    rec = {
        "id": "x",
        "name": "x",
        "url": "https://example.org",
        "kind": "software",
        "triage": "B",
        "license": {"spdx": "MIT", "class": "permissive", "source": "license-file"},
        "reason": "x",
        "checked": __import__("datetime").date(2026, 1, 1),
        "our_status": "reproduced",
    }
    assert any("verification" in e for e in validate_record(rec))


def test_in_repo_urls_must_exist():
    rec = {
        "id": "x",
        "name": "x",
        "url": "docs/landscape-2026-10",
        "kind": "model",
        "triage": "B",
        "license": {"spdx": "MIT", "class": "permissive", "source": "license-file"},
        "reason": "x",
        "checked": __import__("datetime").date(2026, 1, 1),
    }
    assert validate_record(rec) == []
    for bad in ("models/does-not-exist", "../outside", "/etc/passwd", "http://insecure.org"):
        assert any("url" in e for e in validate_record(rec | {"url": bad})), bad


def test_generated_docs_are_fresh():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "build_docs.py"), "--check"], cwd=ROOT)
    assert r.returncode == 0, "run: python tools/build_docs.py"
