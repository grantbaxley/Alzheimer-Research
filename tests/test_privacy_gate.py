"""The privacy gate (tools/check_data_policy.py).

Example identifiers are assembled at runtime so that this file itself passes the gate.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_data_policy as gate  # noqa: E402

AT = "@"


def hits(text, deny=None):
    return gate.scan_text(text, deny, "f.md")


@pytest.mark.parametrize(
    "label, text",
    [
        ("e-mail address", "contact jane.doe" + AT + "mail.com"),
        ("phone number", "call (555) 123-" + "4567"),
        ("phone number", "call +44 " + "20 7946 0958"),
        ("SSN-like number", "ssn 123-45-" + "6789"),
        ("date of birth", "DO" + "B: 1950-03-02"),
        ("date of birth", "she was born" + " on 2 March 1950"),
        ("medical record or patient number", "MR" + "N: 00123456"),
        ("street address", "lives at 12 Oak" + "wood Road"),
        ("day/month/year date", "seen on 03/02/" + "2024"),
        ("first-person reference to a relative", "my " + "mother's Centiloid was 72"),
        ("ADNI participant ID", "123" + "_S_" + "4567"),
        ("OASIS subject ID", "OAS" + "3_0123"),
        ("credential or private key", "gh" + "p_" + "a" * 36),
    ],
)
def test_patterns_flag_identifiers_without_echoing_them(label, text):
    problems = hits(text)
    assert any(label in p for p in problems), problems
    assert text not in " ".join(problems)


@pytest.mark.parametrize(
    "text",
    [
        "Co-Authored-By: Claude <noreply" + AT + "anthropic.com>",
        "placeholder user" + AT + "example.org",
        "checked: 2026-10-18",
        "CDR-SB 0.5-2.5 over 76 weeks; z = +1.3 | -0.4 | +2.6",
        "Version 3.10.25; n = 1736 (552 high tau)",
        "a birthdate-based eligibility cutoff",
        "our partners at the consortium",
        "in amyloid-positive MCI, 58.1% were tau positive",
        "the family member's numbers stay on your computer",
        "CA1 synapses -18% (Scheff 2007)",
    ],
)
def test_patterns_ignore_ordinary_research_text(text):
    assert hits(text) == []


def test_allow_marker_skips_pattern_rules_on_that_line_only():
    text = "call (555) 123-" + "4567  <!-- data-policy: allow -->\ncall (555) 123-" + "4568"
    assert hits(text) == ["f.md:2: looks like a phone number"]


def test_denylist_is_whole_word_case_insensitive_and_never_echoed():
    deny = gate._denylist_regex(["Zebedee Quist", "73.2"])
    problems = hits("Notes for zebedee quist: centiloid 73.2", deny)
    assert problems == ["f.md: contains a denylisted term (not shown)"]
    assert hits("centiloid 73.25 and Zebedeequist", deny) == []


def test_denylist_cannot_be_bypassed_by_the_allow_marker():
    deny = gate._denylist_regex(["Zebedee"])
    assert hits("Zebedee <!-- data-policy: allow -->", deny)


def test_load_denylist_from_file_and_environment(tmp_path):
    f = tmp_path / "denylist.txt"
    f.write_text("# one term per line\nAlpha Beta\n\nx\n")
    terms = gate.load_denylist({"PRIVACY_DENYLIST": "Gamma\nDelta"}, files=[f])
    assert terms == ["Alpha Beta", "Delta", "Gamma"]  # single characters are ignored


@pytest.mark.parametrize(
    "path",
    [
        "models/open-ad-sim/patients/relative.yaml",
        "private/notes.md",
        "data/local/x.md",
        "docs/scan.nii.gz",
        "docs/photo.JPG",
        "docs/report.pdf",
        "data/table.csv",
        "bundle.zip",
        "voice/recording.m4a",
        "denylist.txt",
        ".env",
    ],
)
def test_risky_paths_are_blocked(path):
    assert gate.scan_path(path, None, set())


def test_allowlist_covers_file_types_but_never_private_directories():
    assert gate.scan_path("docs/figure.png", None, {"docs/figure.png"}) == []
    assert gate.scan_path("private/figure.png", None, {"private/figure.png"})


def test_file_names_are_scanned_too():
    deny = gate._denylist_regex(["Zebedee"])
    assert gate.scan_path("notes/zebedee-visit.md", deny, set())
    assert gate.scan_path("notes/jane" + AT + "mail.com.md", None, set())


def test_files_outside_the_repository_can_be_scanned(tmp_path):
    outside = tmp_path / "notes.md"
    outside.write_text("call (555) 123-" + "4567\n")
    problems = gate.scan_files([outside], None, set())
    assert problems and str(outside) in problems[0]


def test_binary_files_are_rejected():
    problems = gate.scan_blob("tools/blob.bin", b"\x00\x01", None, set())
    assert any("binary" in p for p in problems)


def test_history_exception_keeps_the_denylist():
    deny = gate._denylist_regex(["Zebedee"])
    data = ("Zebedee wrote to x" + AT + "mail.com").encode()
    problems = gate.scan_blob("notes.md", data, deny, {"blob:" + "a" * 12}, sha="a" * 40)
    assert any("denylisted" in p for p in problems)
    assert not any("e-mail" in p for p in problems)


def test_commit_messages_are_scanned_but_git_comments_are_not():
    msg = "Fix model\n\nCo-Authored-By: Claude <noreply" + AT + "anthropic.com>\n# my " + "mother\n"
    assert gate.scan_commit_message(msg, None) == []
    assert gate.scan_commit_message("Tested on my " + "father's scan", None)


def test_history_scan_finds_deleted_files_and_personal_author_emails(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = dict(
        os.environ,
        GIT_AUTHOR_NAME="A",
        GIT_AUTHOR_EMAIL="a" + AT + "mail.com",
        GIT_COMMITTER_NAME="A",
        GIT_COMMITTER_EMAIL="noreply" + AT + "github.com",
    )

    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)

    git("init", "-q")
    (repo / "notes.md").write_text("call (555) 123-" + "4567\n")
    git("add", "notes.md")
    git("commit", "-q", "-m", "add notes")
    git("rm", "-q", "notes.md")
    git("commit", "-q", "-m", "remove notes")
    monkeypatch.setattr(gate, "ROOT", repo)
    problems = gate.scan_history(None, set())
    assert any("phone number" in p for p in problems)  # deleted files stay in history
    assert any("author e-mail" in p for p in problems)
    assert not any("committer e-mail" in p for p in problems)


def test_git_hooks_are_executable_and_call_the_gate():
    for name in ("pre-commit", "commit-msg", "pre-push"):
        hook = ROOT / ".githooks" / name
        assert os.access(hook, os.X_OK), name
        assert "tools/check_data_policy.py" in hook.read_text()


def test_repository_passes_the_privacy_gate():
    assert gate.main([]) == 0


def test_repository_history_passes_the_privacy_gate():
    assert gate.main(["--history"]) == 0
