# Notes on the blind re-test of litmus-screener 1.2.0

Run on 2026-11-03 with `verification/run.sh --no-docker --version 1.2.0 --out /tmp/retest`. Exit code 1: verdicts differ from the published results.csv, as expected.

## Declarations

No mistakes found after the run. No declaration was changed after a verdict was seen.

## Things a reader should know

- After the answers were written and checked, but before commit 1, the tester saw the message of the release commit for 1.2.0 in `git log`. It summarises the release. The answers were already final and were not changed.
- Four cases are about a private person using an image tool (ba-04, ba-05, bb-04, bb-05). `scope.role` has no value for a person acting for non-professional purposes, so these use `deployer`, with a comment.
- Six cases use `provider_only` (ba-01 to ba-03, bb-01 to bb-03, h-01). Only h-01 says the provider does not use the system. For the others this is an assumption, noted in a comment.
- Cases outside points (a) and (b) answer `influence` with `not_answered`, except `significant_harm_likely` where the case states or leaves open a harm.
