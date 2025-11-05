#!/usr/bin/env bash
# NDSS-ELSA test runner
# Runs each module inside the 'ndss-elsa' image with clear messages and completed/fail summary.

set -uo pipefail

IMAGE="${IMAGE:-ndss-elsa}"

# Figure out whether we need sudo for docker
DOCKER_BIN="${DOCKER_BIN:-docker}"
if $DOCKER_BIN info >/dev/null 2>&1; then
  SUDO=""
else
  SUDO="sudo"
  if ! $SUDO $DOCKER_BIN info >/dev/null 2>&1; then
    echo "ERROR: Cannot talk to Docker. Is the daemon running?"; exit 1
  fi
fi

# Pretty colors when connected to a TTY
if [ -t 1 ]; then
  GREEN=$'\e[32m'; RED=$'\e[31m'; YELLOW=$'\e[33m'; BLUE=$'\e[34m'; BOLD=$'\e[1m'; RESET=$'\e[0m'
else
  GREEN=""; RED=""; YELLOW=""; BLUE=""; BOLD=""; RESET=""
fi

# Use -it only when in a TTY so non-interactive CI doesn't hang
IT_FLAG="-i"
if [ -t 1 ]; then IT_FLAG="-it"; fi

# Preflight: image present?
if ! $SUDO $DOCKER_BIN image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "ERROR: Docker image '$IMAGE' not found. Build first:  docker build -t $IMAGE ."
  exit 1
fi

pass=0; fail=0; skip=0
START_TS=$(date +%s)

log() { printf "%s\n" "$*"; }
hr()  { printf "%s\n" "---------------------------------------------------------------------"; }

have_bin() {
  local bin="$1"
  $SUDO $DOCKER_BIN run --rm "$IMAGE" bash -lc "test -x $bin" >/dev/null 2>&1
}

run_test() {
  local title="$1"; shift
  local bin="$1"; shift

  hr
  log "${BOLD}${BLUE}▶ ${title}${RESET}"
  if ! have_bin "$bin"; then
    log "${YELLOW}SKIP${RESET}: $bin not found in image '$IMAGE'"
    skip=$((skip+1))
    return 0
  fi

  local start=$(date +%s)
  if $SUDO $DOCKER_BIN run --rm $IT_FLAG "$IMAGE" "$bin" "$@"; then
    local dur=$(( $(date +%s) - start ))
    log "${GREEN}PASS${RESET}: ${title} (${dur}s)"
    pass=$((pass+1))
  else
    local dur=$(( $(date +%s) - start ))
    log "${RED}FAIL${RESET}: ${title} (${dur}s)"
    fail=$((fail+1))
  fi
}

# Show what's inside /opt for quick sanity
hr
log "${BOLD}Binaries present in /opt:${RESET}"
$SUDO $DOCKER_BIN run --rm "$IMAGE" bash -lc 'ls -l /opt | grep -E "(^|- )main" || true'
log

# Dockerfile creates a /data symlink pointing to the repo’s data.
# Use absolute /data paths (no need for -w /opt/src/build).

run_test \
  "Testing the protocol for VLDP (Vehicle Loan Default Prediction) dataset" \
  /opt/main_psmt \
  -DBPath /data/VLDP/ -DBName VLDP -isSim 1 -isCompact 1 -numChunks 4 -itemLen 1 -scalingModSize 44

run_test \
  "Testing the PEPSI's OpenFHE implementation (bitlen=89, HW=32, unencrypted)" \
  /opt/main_pepsi \
  -bitlen 89 -HW 32 -isEncrypted 0


run_test \
  "Testing the Cong et. al.'s OpenFHE implementation (16 parties, 28-bit items, unencrypted)" \
  /opt/main_apsi \
  -numParties 16 -numItems 20 -isEncrypted 0  

run_test \
  "Testing the logistic regression model on breast cancer dataset" \
  /opt/main_logreg

run_test \
  "Testing the hashing module" \
  /opt/main_hash

run_test \
  "Testing slotwise windowing (delta=20, kappa=5)" \
  /opt/main 20 5

run_test \
  "Testing VAF + wDEP on 10-bit domain (no slotwise windowing)" \
  /opt/main_vaf 6.75 2.59 158.54 2 8 0 22 1


hr
TOTAL=$((pass+fail+skip))
ELAPSED=$(( $(date +%s) - START_TS ))
log "${BOLD}Summary:${RESET} ${GREEN}${pass} completed${RESET}, ${RED}${fail} failed${RESET}, ${YELLOW}${skip} skipped${RESET}  (total ${TOTAL}, ${ELAPSED}s)"
hr

# Exit nonzero if anything failed
[ "$fail" -eq 0 ] || exit 1
