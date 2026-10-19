"""The nightly research loop helper (tools/nightly.py)."""

import datetime as dt
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import nightly  # noqa: E402


def make_base(tmp_path):
    base = tmp_path / "nightly"
    (base / "log").mkdir(parents=True)
    shutil.copy(ROOT / "research" / "nightly" / "lenses.yaml", base / "lenses.yaml")
    (base / "ideas.yaml").write_text("ideas: []\n")
    return base


def write_log(base, date, lens, constraint):
    (base / "log" / f"{date}.md").write_text(
        f"---\ndate: {date}\nlens: {lens}\nconstraint: {constraint}\n---\n# Night\n"
    )


def test_repository_program_is_valid():
    assert nightly.check() == []


def test_pick_is_deterministic_and_rotates(tmp_path):
    base = make_base(tmp_path)
    d = dt.date(2026, 10, 20)
    first = nightly.pick(d, base)
    assert first == nightly.pick(d, base)
    write_log(base, "2026-10-20", first["lens"]["id"], first["constraint"])
    second = nightly.pick(d + dt.timedelta(days=1), base)
    assert second["lens"]["id"] != first["lens"]["id"]
    assert second["constraint"] != first["constraint"]


def test_every_lens_is_used_before_any_repeats(tmp_path):
    base = make_base(tmp_path)
    n = len(nightly.load_lenses(base)["lenses"])
    d = dt.date(2026, 11, 1)
    seen = []
    for k in range(n):
        p = nightly.pick(d + dt.timedelta(days=k), base)
        seen.append(p["lens"]["id"])
        write_log(base, (d + dt.timedelta(days=k)).isoformat(), p["lens"]["id"], p["constraint"])
    assert len(set(seen)) == n


def test_revisit_picks_the_most_neglected_open_idea(tmp_path):
    base = make_base(tmp_path)
    (base / "ideas.yaml").write_text(
        "ideas:\n"
        "  - {id: a, created: 2026-10-01, status: promising,"
        " history: [{date: 2026-10-15, note: x}]}\n"
        "  - {id: b, created: 2026-10-05, status: new}\n"
        "  - {id: c, created: 2026-09-01, status: killed, history: [{date: 2026-09-02, note: y}]}\n"
    )
    assert nightly.pick(dt.date(2026, 10, 20), base)["revisit"] == "b"


def test_check_catches_bad_entries(tmp_path):
    base = make_base(tmp_path)
    (base / "ideas.yaml").write_text(
        "ideas:\n  - {id: a, title: t, created: 2026-10-01, lens: nope, goal: cure, status: killed,"
        " mechanism: m, falsify: f}\n"
    )
    write_log(base, "2026-10-20", "inversion", "x")
    (base / "log" / "2026-10-20.md").rename(base / "log" / "2026-10-21.md")
    problems = " ".join(nightly.check(base))
    for expected in ("unknown lens", "goal must be", "killed ideas need", "does not match"):
        assert expected in problems
