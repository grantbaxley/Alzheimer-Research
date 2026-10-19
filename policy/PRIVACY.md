# Privacy policy: Rule #1

**Nothing that could identify a real person ever enters this repository.** Not in files,
file names, commit messages, branch names, pull requests, issues, reviews or CI logs, and
not "temporarily": git history is permanent and this repository is public.

This rule comes first because the project models a disease that affects real families,
and some contributors will run the models for someone they love.

## What counts as identifying

Treat all of these as off-limits, alone or in combination:

- **Direct identifiers:** names, initials, nicknames, signatures, photos, faces, voices,
  e-mail addresses, phone numbers, postal addresses, record or insurance numbers, device
  serials, account names.
- **People around a case:** relatives' names, care partners, clinicians, clinics,
  hospitals, care homes, trial sites.
- **Places and dates tied to a person:** town or street, dates of birth, visits, scans,
  diagnoses or death, and exact ages.
- **A person's measurements:** exact test values (a Centiloid to one decimal, a dated MMSE
  or CDR-SB score), scan readings, lab results, genotypes (e.g. a specific person's APOE),
  medication lists.
- **Documents and free text about a specific case:** clinic letters, reports, screenshots,
  case narratives, or an account of a relative's illness in a commit message or issue.
- **Indirect identification:** combinations that point to one person (age band + diagnosis
  + genotype + town), and model inputs or profiles built *around* one person's values.

Published research is different. Citations, author names and official findings (for
example a journal's retraction notice) are public scholarly record. Keep them factual and
sourced ([INTEGRITY.md](INTEGRITY.md)); they are not personal data in the sense of this rule.

## Working with a real person's information

Running a model for someone you know is allowed and can be valuable, **locally only**:

1. Get their consent, or their legal representative's.
2. Describe them as **ranges** wide enough to cover measurement error, never exact values
   (see `models/open-ad-sim/kit/HOW_TO_RUN_FOR_A_FAMILY_MEMBER.md`).
3. Keep inputs and outputs in a git-ignored folder (`patients/`, `private/` or `local/`).
   The privacy gate rejects these folders even if `.gitignore` is bypassed.
4. Do not paste their details into issues, pull requests, discussions or commit messages.
5. If you use an AI assistant with their details, use a private space you control, and do
   not let an agent write those details into this repository.

## The private denylist

Patterns cannot recognise every name. Each contributor who works with a real person's
information keeps a **denylist outside the repository**, one term per line:

```bash
mkdir -p ~/.config/alzheimer-research
${EDITOR:-nano} ~/.config/alzheimer-research/denylist.txt
```

List the person's names, initials and nicknames, relatives' and clinicians' names, clinics,
town and street, dates in every format you might write them, record numbers, and any exact
test values. Matching is whole-word and case-insensitive, and the gate never prints the
term it found. (`~/.config/open-ad-sim/denylist.txt` is read too, for older setups.)

Maintainers can add the same terms as the `PRIVACY_DENYLIST` repository secret
(Settings → Secrets and variables → Actions), so CI enforces them on every push without
the terms ever appearing in the repository or its logs.

## How the rule is enforced

| Layer | What runs | When |
|---|---|---|
| Local hooks: `git config core.hooksPath .githooks` (once per clone) | `pre-commit`: staged files and names; `commit-msg`: the message; `pre-push`: the whole history | before anything leaves your machine |
| CI ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) | tracked files, then every file version, path, commit message and author identity in history, with the denylist secret | every push and pull request |
| Review | [pull request checklist](../.github/pull_request_template.md) | every pull request |

The gate (`tools/check_data_policy.py`) blocks:

- denylisted terms, in content or file names;
- private folders, and files that look like a denylist;
- file types that carry personal or participant data: scans, recordings, photos and raster
  images, documents, spreadsheets and data tables, data dumps, databases, archives, mail,
  contact and calendar files, and keys;
- binary files, which cannot be scanned;
- e-mail addresses (except no-reply and reserved example domains), phone numbers, SSN-like
  numbers, dates of birth, record and patient numbers, street addresses, day/month/year
  dates, first-person references to a relative, cohort participant IDs, and credentials;
- commit author or committer addresses that are not no-reply addresses.

It never echoes what it found, because CI logs of a public repository are public.

**Commit identity.** Commit with a no-reply address. On GitHub, turn on *Settings → Emails →
Keep my email addresses private* and *Block command line pushes that expose my email*, and
use the `…@users.noreply.github.com` address in `git config user.email`.

**Exceptions** live in [`tools/privacy_allowlist.txt`](../tools/privacy_allowlist.txt) and
need a reason and review. A file path there may bypass only the file-type rule (e.g. a
generated figure). An exact historical file version (`blob:<id>`) may bypass only the
pattern rules, for reviewed false positives that are already public. A line may carry
`data-policy: allow` for a reviewed false positive. Nothing can bypass the denylist or the
private-folder rule, and no exception may ever cover information about a person.

**Limits.** No scanner recognises every quasi-identifier. The denylist, ranges-not-values
and review are what make the rule hold.

## If something slips through

Do not just delete it in a new commit: it stays in history and in GitHub's caches.

1. Stop pushing and tell the maintainers privately.
2. Rewrite history to remove it (e.g. `git filter-repo`), force-push every affected branch
   and tag, and ask everyone with a clone to re-clone.
3. Ask GitHub Support to purge cached views and pull-request references. GitHub documents
   this under *Removing sensitive data from a repository*.
4. If it involved cohort data, follow that cohort's DUA notification terms
   ([DATA_ACCESS.md](DATA_ACCESS.md)). If it involved a secret, rotate it.
5. Add the leaked terms to the denylist so the gate catches them from then on.
