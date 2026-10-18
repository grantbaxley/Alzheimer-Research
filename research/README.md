# Research

This is where the project's own work lands, on top of the vetted foundation in
`registry/` and `src/alzres/`.

```
research/
├── intake/          # incoming work (e.g. the founder's project folder), not yet vetted
├── reproductions/   # one write-up per external resource we reproduce (policy/VETTING.md)
└── studies/         # our own analyses, each built on registry resources
```

## Bringing work in

Work moves in stages; nothing skips intake.

1. **Intake.** Copy the material into `research/intake/<topic>/` on a branch. Before
   committing, run `python tools/check_data_policy.py research/intake/<topic>/**/*`
   and remove any participant data, gated-cohort files or credentials. Add a short
   `README.md` listing what it is, where each part came from and what it depends on.
2. **Map dependencies.** Every external model, dataset or claim it relies on gets a
   registry record (or reuses one). Anything graded C is replaced or removed.
3. **Re-model.** Re-implement or re-run the core results with pinned versions, synthetic
   ground-truth checks, subject-level splits and baselines/nulls (the reproduction
   protocol in `policy/VETTING.md`). Reusable code moves into `src/alzres/` with tests.
4. **Promote.** Once a result passes, write it up under `research/studies/<topic>/`
   with its evidence grade and the registry IDs it rests on. Unvetted remnants stay in
   intake or are deleted.

## Write-up template

Each study or reproduction should state: question; data (and its access terms); registry
IDs used with pinned versions; methods; baselines and nulls; results with uncertainty;
what would falsify the result; limitations; and how to reproduce it.
