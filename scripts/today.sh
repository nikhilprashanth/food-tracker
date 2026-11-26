#!/bin/bash
LOG="$(dirname "$0")/../data/log.json"

if [ ! -f "$LOG" ]; then
  echo "No log yet."; exit 0
fi

jq -r --arg d "$(date +%F)" '
  def r: (. * 10 | round) / 10;
  [.[] | select(.date == $d)] as $e
  | "Totals for \($d) (\($e | length) entries)\n" +
    "Calories: \($e | map(.calories) | add // 0 | r)\n" +
    "Protein:  \($e | map(.protein)  | add // 0 | r) g\n" +
    "Carbs:    \($e | map(.carbs)    | add // 0 | r) g\n" +
    "Fat:      \($e | map(.fat)      | add // 0 | r) g"
' "$LOG"
