# Resource registry

One YAML record per external resource the project uses, evaluates or warns against.
Records are grouped by layer (one file per layer). `python -m alzres.registry validate`
checks them, CI runs it, and `tools/build_docs.py` renders them into
[`awesome/README.md`](../awesome/README.md).

## Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Unique, kebab-case. |
| `name`, `url` | yes | `url` must be https. |
| `kind` | yes | `software`, `model`, `dataset`, `benchmark`, `knowledge-base`, `platform`, `research-claim`. |
| `triage` | yes | `A` / `B` / `C`; see [policy/VETTING.md](../policy/VETTING.md). |
| `license` | yes | `{spdx, class, source}`. `class`: permissive, weak-copyleft, copyleft, network-copyleft, non-commercial, data-terms, none, unconfirmed. `source`: license-file, api-metadata, docs, secondary, unconfirmed, n/a. |
| `reason` | yes | One line: why this grade. |
| `checked` | yes | Date the facts in the record were last checked. |
| `access` | datasets | `open`, `account`, `application`, `controlled`, `enclave`, `closed`. |
| `our_status` | no | Defaults to `not-started`; anything we claim to have run needs `verification`. |
| `verification` | conditional | Test, report or PR that backs `our_status`. |
| `peer_reviewed`, `independent_replication` | no | `yes`, `partial`, `no`, `unknown`. |
| `maintained`, `pinned` | no | Activity observed; exact upstream commit we use. |
| `red_flags`, `to_verify`, `sources` | no | Lists. |

## Provenance of the initial records

The first 89 records were written from the six scout notes in
[`docs/landscape-2026-10/notes/`](../docs/landscape-2026-10/notes/). On 2026-10-18 every
GitHub URL was confirmed to exist with `git ls-remote`, and the LICENSE files of 16 repos
were read directly (`source: license-file`). That check:

- resolved Clinica's license conflict (MIT, so it moved to A);
- confirmed `ucl-pond/network_spreading_models` exists (MIT);
- found no LICENSE file in the BioFINDER SIR tau model (moved to C);
- confirmed GPL-3.0 for kde_ebm and pyebm and AGPL-3.0 for nmed2024.

Everything else is desk research, not verification by this project.
