# LitmusAI independent verification

This folder tests the released LitmusAI the way a stranger would. It installs the published package from PyPI, screens AI systems described in public sources, and compares each verdict with the answer the source itself gives. Anyone can repeat the run with one command.

> **Status:** blind re-test on 3 November 2026, litmus-screener 1.2.0, the same 175 cases, with the tester's answers to the new `influence` and `scope` questions. On the full screen: 49 of 51 expected prohibitions found, 2 flagged for review, none missed, and 9 of 113 permitted cases screened red. The findings, with the cause of every flag and false alarm and the cautions on this run, are in `REPORT.md`; the counts per point in `scorecard.md`. The first run (litmus-screener 1.1.2 and 1.1.3, 2 November 2026: 6 missed, 32 false alarms) is kept in `history/1.1.3/`.

LitmusAI is a screening aid. Neither the tool nor this test is a legal opinion, a conformity assessment or a certification.

## How the test is run

1. **Install like a stranger.** A fresh container with the released package from PyPI, pinned by version and hash in `requirements.lock`. Never from source.
2. **Use public subjects.** The cases come from the European Commission's worked examples in its Guidelines on prohibited AI practices (C(2025) 5052 final, 29 July 2025) and, for points (ba) and (bb), from the recitals of Regulation (EU) 2026/1744. Real products are not used as cases: no court or regulator has ruled one in breach of Article 5, so there is no outside answer to compare with.
3. **Write the expected answer first.** `SELECTION.md`, the case files and `expected.csv` are committed before any declaration is written or any screen is run. The git history shows the order.
4. **Write the inputs as a user would.** Each `declarations/<case_id>.yaml` is written from the case description and the template that `litmus init` produces, without reading LitmusAI's rules.
5. **One command.** `run.sh` gives the same result on any machine with Docker.
6. **Report honestly.** Misses, false alarms and limits are published with the results.

The cases, expected answers and declarations are written by a person or session that has not seen the ruleset. That separation is procedural: the PyPI package contains the ruleset, and the writer agrees not to open it.

## How verdicts are counted

LitmusAI answers red, amber (needs review) or clear for each Article 5 point. Each case has one target point and an expected label from its source. For each point the scorecard gives:

| Line | Meaning |
|---|---|
| Missed prohibitions | Expected red, got clear. The target is zero. |
| Flagged for review | Expected red, got amber. Counted apart from hits and misses. |
| False alarms | Expected clear, got red. |
| Over-caution | Expected clear, got amber. The ruleset prefers amber when a declaration is ambiguous, so some of this is by design. |
| Off-target reds | A point other than the case's target came back red. Each one is listed and reviewed. |

The full table of expected against actual labels is printed under these lines. The same descriptions are also run through the quick screen (`litmus screen --describe`) and scored separately, because the quick screen infers from keywords and says so.

Every report is also exported to SARIF and validated against the structure of the OASIS SARIF 2.1.0 schema (string formats such as URIs and dates are not checked); every case is screened twice and the two reports must match apart from `generated_at`; every `Art. 5(1)(x)` citation must name the point it sits under; and every recital cited must be one about that point (the map is in `harness.py`, read against the Regulation on 2 November 2026). The 1.1.2 package failed that last check on eleven rules, which 1.1.3 corrects.

## Run it yourself

With Docker:

```bash
git clone https://github.com/aiexponent/litmusai.git
cd litmusai
verification/run.sh
```

Without Docker (Python 3.11 or newer; everything is installed into a throwaway virtual environment under the output folder):

```bash
verification/run.sh --no-docker
```

Other options: `--out DIR` chooses where reports go (a new temporary folder by default), `--version X.Y.Z` tests another released version, and `--update` copies `results.csv` and `scorecard.md` back into this folder when publishing a new result. Nothing is written into the checkout without `--update`.

Exit codes: `0` the verdicts match the published `results.csv` (a change of confidence alone is reported, not a failure); `1` they differ, so the published result must be redone for this version; `2` a check failed (install, screen, SARIF, repeatability or citations).

The scorer's own tests need only the standard library:

```bash
python3 -m unittest discover -s verification/tests
```

## Files

| Path | What it is |
|---|---|
| `SELECTION.md` | The rule used to pick cases, written before any case |
| `cases/<case_id>.md` | Description, source location, expected label and reason (template: `cases/_TEMPLATE.md`) |
| `expected.csv` | `case_id,target_point,expected,source_ref` for every case |
| `declarations/<case_id>.yaml` | The `system.yaml` written for each case |
| `results.csv` | The published verdicts, one row per case, track and point |
| `scorecard.md` | The published scorecard |
| `REPORT.md` | The report: method, how amber counts, results per point, every miss and false alarm with its cause, limits |
| `retest-1.2.0/` | The re-test tester's own output (`results.csv`, `scorecard.md`) and notes, as committed |
| `history/1.1.3/` | The first run's report, results and scorecard (litmus-screener 1.1.2 and 1.1.3) |
| `run.sh`, `harness.py`, `score.py` | The one command, the runner and the scorer |
| `requirements.lock` | Pinned versions and hashes for the package under test and `jsonschema` |

## Sources and reuse

Case descriptions paraphrase European Commission documents, which the Commission licenses under CC BY 4.0 (© European Union). Each case names the document and page it comes from. The paraphrases are changes made by the authors of this folder; the Commission does not endorse them. The legal text is read on EUR-Lex on the day of each run, not from memory.
