#!/bin/bash
LOG="$(dirname "$0")/../data/log.json"

if [ ! -f "$LOG" ]; then
  echo "No log yet."; exit 0
fi

jq -r '
  def r: (. * 10 | round) / 10;
  group_by(.date)[]
  | "\(.[0].date)  (\(length) entries)\n" +
    "  Calories: \(map(.calories) | add | r)\n" +
    "  Protein:  \(map(.protein)  | add | r) g\n" +
    "  Carbs:    \(map(.carbs)    | add | r) g\n" +
    "  Fat:      \(map(.fat)      | add | r) g\n"
' "$LOG"
