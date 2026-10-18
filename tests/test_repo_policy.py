"""Repository-level checks: registry validity, data-policy scanner, generated docs."""

import subprocess
import sys
from pathlib import Path

from alzres.registry import load, validate, validate_record

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_data_policy  # noqa: E402


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


def test_scanner_flags_ids_and_imaging(tmp_path):
    adni_like = "123" + "_S_" + "4567"  # built at runtime so this file passes the scan
    (tmp_path / "rows.csv").write_text(f"subject,mmse\n{adni_like},28\n")
    (tmp_path / "scan.nii.gz").write_bytes(b"\0")
    (tmp_path / "ok.md").write_text("Nothing to see here.\n")
    problems = check_data_policy.scan(sorted(tmp_path.iterdir()))
    assert len(problems) == 2
    assert any("ADNI" in p for p in problems)
    assert any("blocked file type" in p for p in problems)


def test_tracked_files_pass_data_policy():
    files = check_data_policy.tracked_files()
    assert check_data_policy.scan(files) == []


def test_generated_docs_are_fresh():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "build_docs.py"), "--check"], cwd=ROOT)
    assert r.returncode == 0, "run: python tools/build_docs.py"
