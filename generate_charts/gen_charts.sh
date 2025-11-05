#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="/opt/src/generate_charts"
DEST="${OUT_DIR:-/tmp}"

if [ ! -d "$CHART_DIR" ]; then
  echo "[charts] ERROR: chart dir not found: $CHART_DIR"
  exit 1
fi

mkdir -p "$DEST"
MARKER="$(mktemp)"; touch "$MARKER"

cd "$CHART_DIR"

SCRIPTS=(
  "benchmark_ours.py"
  "benchmark_ours_sender_set.py"
  "compare_different_sender_sets.py"
  "compare_increasing_senders.py"
)

for s in "${SCRIPTS[@]}"; do
  if [ -f "$s" ]; then
    echo "[charts] Running: $s"
    python3 "$s"
  else
    echo "[charts] WARN: missing script: $CHART_DIR/$s"
  fi
done

echo "[charts] Collecting new figures into $DEST"
find "$CHART_DIR" -type f \
  \( -iname '*.pdf' -o -iname '*.png' -o -iname '*.svg' \) \
  -newer "$MARKER" -print -exec cp -f {} "$DEST"/ \;
echo ""
echo "[charts] Done. Figures are in: $DEST and ~/artifact_output folders."
