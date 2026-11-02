#!/usr/bin/env bash
# LitmusAI independent verification: one command.
#
#   verification/run.sh                 run in Docker with the pinned versions
#   verification/run.sh --no-docker     same, in a throwaway venv (needs Python 3.11+)
#   verification/run.sh --version X.Y.Z test another released version (no hash pins)
#   verification/run.sh --out DIR       where to write reports (default: a new temp dir)
#   verification/run.sh --update        copy results.csv and scorecard.md back into verification/
#
# Nothing is written into the checkout unless --update is given.
# Exit codes: 0 verdicts match the published results (or none are published yet),
#             1 verdicts differ from the published results.csv,
#             2 a check failed (install, screen, SARIF, repeatability, citations).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Official python image, mirrored on Amazon ECR Public; pinned by index digest.
IMAGE="public.ecr.aws/docker/library/python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159"

docker_mode=1
inside=0
update=0
force=0
version=""
out=""

while [ $# -gt 0 ]; do
  case "$1" in
    --no-docker) docker_mode=0 ;;
    --inside) inside=1 ;;
    --update) update=1 ;;
    --force) force=1 ;;
    --version) version="${2:-}"; shift ;;
    --out) out="${2:-}"; shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "Error: unknown option $1 (see --help)" >&2; exit 2 ;;
  esac
  shift
done

if [ -n "$version" ] && ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+((a|b|rc)[0-9]+)?$ ]]; then
  echo "Error: --version must look like 1.2.3, got '$version'" >&2
  exit 2
fi

if [ -z "$out" ]; then
  out="$(mktemp -d "${TMPDIR:-/tmp}/litmus-verification.XXXXXX")"
elif [ -e "$out" ] && [ -n "$(ls -A "$out" 2>/dev/null)" ] && [ "$force" -eq 0 ] && [ "$inside" -eq 0 ]; then
  echo "Error: $out is not empty; pass --force to reuse it" >&2
  exit 2
fi
mkdir -p "$out"
# An absolute path, so Docker bind-mounts the folder and never creates a named volume.
out="$(cd "$out" && pwd)"

run_checks() {
  # Build an isolated environment under $out, install, screen, score, compare.
  # Called as `run_checks || status=$?`, so set -e is off in here: check each step.
  python3 -m venv "$out/venv" || { echo "Error: could not create the venv" >&2; return 2; }
  if [ -n "$version" ]; then
    echo "Testing litmus-screener==$version (not hash-pinned; the lock pins the published version)."
    "$out/venv/bin/pip" install --quiet --no-cache-dir "litmus-screener==$version" "jsonschema==4.26.0" \
      || { echo "Error: install of litmus-screener==$version failed" >&2; return 2; }
  else
    "$out/venv/bin/pip" install --quiet --no-cache-dir --require-hashes -r "$HERE/requirements.lock" \
      || { echo "Error: install from requirements.lock failed" >&2; return 2; }
  fi
  local rc=0
  "$out/venv/bin/python" "$HERE/harness.py" --verification-dir "$HERE" --out "$out" \
    --litmus "$out/venv/bin/litmus" || rc=$?
  [ "$rc" -ne 0 ] && return "$rc"
  [ -f "$HERE/expected.csv" ] || return 0
  "$out/venv/bin/python" "$HERE/score.py" score --expected "$HERE/expected.csv" \
    --results "$out/results.csv" --out "$out" || return 2
  "$out/venv/bin/python" "$HERE/score.py" drift --committed "$HERE/results.csv" \
    --current "$out/results.csv" || return $?
}

status=0
if [ "$inside" -eq 1 ] || [ "$docker_mode" -eq 0 ]; then
  run_checks || status=$?
else
  command -v docker >/dev/null || { echo "Error: docker not found; use --no-docker" >&2; exit 2; }
  docker run --rm \
    --user "$(id -u):$(id -g)" -e HOME=/tmp -e PIP_DISABLE_PIP_VERSION_CHECK=1 \
    -v "$HERE:/verification:ro" -v "$out:/out" \
    "$IMAGE" bash /verification/run.sh --inside --out /out ${version:+--version "$version"} \
    || status=$?
fi

echo "Reports and scorecard: $out"
if [ "$update" -eq 1 ] && [ "$status" -ne 2 ] && [ -f "$out/results.csv" ]; then
  cp "$out/results.csv" "$HERE/results.csv"
  cp "$out/scorecard.md" "$HERE/scorecard.md"
  echo "Updated verification/results.csv and verification/scorecard.md"
  status=0
fi
exit "$status"
