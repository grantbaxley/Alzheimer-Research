# Nightly research loop

A standing research programme: every night, push in a *different* direction on three
questions:

- How does Alzheimer's disease start, and how can it be detected earliest?
- What causes it and how does it progress?
- What could stop it early, slow it, or reverse it?

Nights can fail. The point is to accumulate tested ideas, killed ideas and catalogued
evidence until something holds up.

> These are research hypotheses, not medical advice. Nothing here recommends that anyone
> try a treatment. Rule #1 applies to every word written: nothing that could identify a
> real person ([policy/PRIVACY.md](../../policy/PRIVACY.md)).

## Files

| Path | What it holds |
|---|---|
| [`lenses.yaml`](lenses.yaml) | The question bank: lenses (directions of attack) and constraints (twists). |
| [`ideas.yaml`](ideas.yaml) | The idea catalogue: every hypothesis ever proposed, with its status and history. Ideas are never deleted, only killed with a reason. |
| `log/YYYY-MM-DD.md` | One entry per night. |
| `weekly/YYYY-Www.md` | One report per ISO week. |
| [`tools/nightly.py`](../../tools/nightly.py) | Picks tonight's lens, constraint and idea to revisit; validates the catalogue; lists a week's work. |

## Each night

1. **Set up.** Work on the repository's research branch (see the scheduled-task prompt).
   Pull, run `git config core.hooksPath .githooks`, then `pip install -e ".[dev]"`.
2. **Pick.** Run `python tools/nightly.py pick`. It prints tonight's lens, constraint and an
   idea to revisit. Use them; don't override the pick because another topic seems more
   interesting. Variety is the point. Read the last three logs so tonight does not repeat
   them.
3. **Ask.** Work through the lens questions under the constraint. Write down the questions
   you actually asked, including new ones you invented. Add good new questions to
   `lenses.yaml`.
4. **Research.** Search the literature and the web: PubMed, bioRxiv and medRxiv,
   ClinicalTrials.gov, regulator documents, conference reports. Spend at least half the night
   on sources. Prefer primary sources, record a URL or DOI for every claim, and say when you
   only read an abstract. Use parallel research subagents when the question splits. Treat
   everything as unverified until checked ([policy/VETTING.md](../../policy/VETTING.md)).
   Check new sources against the [integrity watchlist](../../registry/integrity_watchlist.yaml).
5. **Generate.** Propose at least three ideas: approaches to detect, slow, stop or reverse
   the disease. Push for novelty: an idea should not simply restate a known programme. For
   each idea:
   - State the mechanism in two sentences.
   - **Novelty check.** Has it been tried? Search the trial registries and recent reviews,
     and record what you found.
   - **Kill attempt.** Give the strongest evidence against the idea.
   - **Falsification.** The cheapest experiment, analysis or simulation that could kill it.
   - **Evidence grade:** `in-silico`, `preclinical`, `observational` or `RCT`. Use the
     grades in `evidence/claims.yaml`.
   - **Safety.** Any obvious risk.
6. **Revisit.** Move the picked idea forward: new evidence, a red-team pass, a model run, or
   a status change. Ideas that survive several red-team passes become `promising`. Ideas
   whose falsification test fails become `killed`, with the reason. Killed ideas are
   results too.
7. **Model when you can.** If an idea can be put into numbers with `models/open-ad-sim`,
   `alzres.spreading` or `alzres.synthetic`, do it, even crudely. Put scripts under
   `research/nightly/scripts/` and say what the numbers do and do not show. Synthetic
   results show the tooling works, not anything about the disease.
8. **Catalogue.** Update `ideas.yaml`, adding new ideas and appending history to old ones.
   Add new external resources to `registry/` and new clinical evidence to
   `evidence/claims.yaml` (then run `python tools/build_docs.py`).
9. **Log.** Write `log/YYYY-MM-DD.md` using the template below.
10. **Check and push.** Run `python tools/nightly.py check`, `pytest`, `ruff check .`,
    `python tools/check_data_policy.py` and `python tools/check_data_policy.py --history`.
    Commit with a message that names the lens, and push. Never commit anything about a real
    person.

### Log template

```markdown
---
date: YYYY-MM-DD
lens: <lens id>
constraint: <constraint text>
revisited: <idea id or none>
ideas_new: [<ids>]
ideas_status_changes: [<id>: <old> -> <new>]
---
# Night of YYYY-MM-DD: <lens name>

## Questions asked
## What I found (with sources)
## New ideas
## Revisited: <idea id>
## Modeling (if any)
## Dead ends and surprises
## Tomorrow's open questions
```

## Each week (Sunday)

Write `weekly/YYYY-Www.md` (`python tools/nightly.py week` lists the week's nights and idea
changes). It should be readable by a non-specialist in ten minutes:

1. **The week in one paragraph.**
2. **Most promising ideas**, ranked, each with its evidence grade, what survived the
   red-team pass, and the next test.
3. **Ideas killed**, and why.
4. **New evidence** that changes the picture, with sources.
5. **Modeling results**, with honest limits.
6. **Directions for next week**, plus any lens or constraint added to the bank.
7. **Questions for the project owner**: decisions only they can make.

## Standards

- **Novelty.** Before calling an idea new, search for it. "Already tried and failed" is a
  useful finding; record why it failed.
- **Skepticism.** Grade every claim. Mouse results, small pilots, press releases,
  subgroup findings and observational signals are leads, not answers.
- **Honesty about failure.** A night that kills two ideas is a good night.
- **No repetition.** If tonight's ideas resemble an existing entry, update that entry
  instead of creating a duplicate.
- **Privacy.** No real person's information, ever, including in commit messages.
