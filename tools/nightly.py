#!/usr/bin/env python3
"""Helper for the nightly research loop (research/nightly/PROGRAM.md).

    python tools/nightly.py pick  [--date YYYY-MM-DD]   # lens, constraint, idea to revisit
    python tools/nightly.py check                       # validate lenses, ideas and log headers
    python tools/nightly.py week  [--date YYYY-MM-DD]   # nights and idea changes in that ISO week

The pick is deterministic for a date: the least recently used lens (ties broken by a
date-seeded draw), a constraint not used in the last 10 nights, and the open idea that has
gone longest without attention.
"""

from __future__ import annotations

import argparse
import datetime as dt
import random
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NIGHTLY = ROOT / "research" / "nightly"
STATUSES = {"new", "investigating", "promising", "parked", "killed", "tested"}
GOALS = {"detect", "slow", "stop", "reverse", "understand"}
EVIDENCE = {"in-silico", "preclinical", "observational", "RCT", "none"}
IDEA_REQUIRED = ("id", "title", "created", "lens", "goal", "status", "mechanism", "falsify")
OPEN = {"new", "investigating", "promising"}
CONSTRAINT_MEMORY = 10


def load_lenses(base: Path = NIGHTLY) -> dict:
    return yaml.safe_load((base / "lenses.yaml").read_text())


def load_ideas(base: Path = NIGHTLY) -> list[dict]:
    return yaml.safe_load((base / "ideas.yaml").read_text()).get("ideas") or []


def read_logs(base: Path = NIGHTLY) -> list[dict]:
    """Front matter of every nightly log, oldest first."""
    logs = []
    for path in sorted((base / "log").glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
        meta = yaml.safe_load(m.group(1)) if m else {}
        meta = meta or {}
        meta["_path"] = path
        logs.append(meta)
    return logs


def _as_date(value) -> dt.date:
    return value if isinstance(value, dt.date) else dt.date.fromisoformat(str(value))


def pick(date: dt.date, base: Path = NIGHTLY) -> dict:
    lenses = load_lenses(base)
    logs = [m for m in read_logs(base) if "date" in m and _as_date(m["date"]) < date]
    rng = random.Random(date.toordinal())

    last_used = {}
    for i, m in enumerate(logs):
        last_used[m.get("lens")] = i
    order = sorted(lenses["lenses"], key=lambda lens: (last_used.get(lens["id"], -1), rng.random()))
    lens = order[0]

    recent = {m.get("constraint") for m in logs[-CONSTRAINT_MEMORY:]}
    pool = [c for c in lenses["constraints"] if c not in recent] or lenses["constraints"]
    constraint = rng.choice(pool)

    def last_touch(idea):
        dates = [_as_date(h["date"]) for h in idea.get("history") or [] if "date" in h]
        return max(dates, default=_as_date(idea["created"]))

    open_ideas = [i for i in load_ideas(base) if i.get("status") in OPEN]
    revisit = min(open_ideas, key=lambda i: (last_touch(i), i["id"]), default=None)
    return {
        "date": date.isoformat(),
        "lens": lens,
        "constraint": constraint,
        "revisit": revisit["id"] if revisit else None,
    }


def check(base: Path = NIGHTLY) -> list[str]:
    problems = []
    lenses = load_lenses(base)
    lens_ids = [lens["id"] for lens in lenses["lenses"]]
    if len(set(lens_ids)) != len(lens_ids):
        problems.append("lenses.yaml: duplicate lens id")
    for lens in lenses["lenses"]:
        if not lens.get("questions"):
            problems.append(f"lenses.yaml: {lens['id']} has no questions")
    ideas = load_ideas(base)
    ids = [i.get("id") for i in ideas]
    if len(set(ids)) != len(ids):
        problems.append("ideas.yaml: duplicate idea id")
    for idea in ideas:
        where = f"ideas.yaml:{idea.get('id', '?')}"
        problems += [f"{where}: missing {k}" for k in IDEA_REQUIRED if not idea.get(k)]
        if idea.get("status") not in STATUSES:
            problems.append(f"{where}: status must be one of {sorted(STATUSES)}")
        if idea.get("goal") not in GOALS:
            problems.append(f"{where}: goal must be one of {sorted(GOALS)}")
        if idea.get("evidence", "none") not in EVIDENCE:
            problems.append(f"{where}: evidence must be one of {sorted(EVIDENCE)}")
        if idea.get("lens") not in lens_ids:
            problems.append(f"{where}: unknown lens {idea.get('lens')}")
        if idea.get("status") == "killed" and not idea.get("history"):
            problems.append(f"{where}: killed ideas need a history entry saying why")
    for meta in read_logs(base):
        name = meta["_path"].name
        for key in ("date", "lens", "constraint"):
            if key not in meta:
                problems.append(f"log/{name}: front matter missing {key}")
        if meta.get("lens") and meta["lens"] not in lens_ids:
            problems.append(f"log/{name}: unknown lens {meta['lens']}")
        if "date" in meta and f"{_as_date(meta['date']).isoformat()}.md" != name:
            problems.append(f"log/{name}: file name does not match its date")
    return problems


def week(date: dt.date, base: Path = NIGHTLY) -> dict:
    year, wk, _ = date.isocalendar()
    nights = [
        m for m in read_logs(base)
        if "date" in m and _as_date(m["date"]).isocalendar()[:2] == (year, wk)
    ]  # fmt: skip
    changed = []
    for idea in load_ideas(base):
        dates = [_as_date(idea["created"])] + [
            _as_date(h["date"]) for h in idea.get("history") or []
        ]
        if any(d.isocalendar()[:2] == (year, wk) for d in dates):
            changed.append(f"{idea['id']} ({idea['status']})")
    return {
        "week": f"{year}-W{wk:02d}",
        "nights": [m["_path"].name for m in nights],
        "ideas": changed,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["pick", "check", "week"])
    ap.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    args = ap.parse_args(argv)
    if args.command == "check":
        problems = check()
        print("\n".join(problems) or "nightly: OK")
        return 1 if problems else 0
    if args.command == "week":
        w = week(args.date)
        print(f"{w['week']}\nnights: {', '.join(w['nights']) or 'none'}")
        print(f"ideas created or updated: {', '.join(w['ideas']) or 'none'}")
        return 0
    p = pick(args.date)
    print(f"date: {p['date']}\nlens: {p['lens']['id']} - {p['lens']['name']}")
    print(f"constraint: {p['constraint']}\nrevisit: {p['revisit'] or 'none'}\nquestions:")
    for q in p["lens"]["questions"]:
        print(f"  - {q}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
