#!/usr/bin/env bash
# Sample the RAM and CPU of one Android app over adb, one line per interval, as CSV.
# Use it to investigate "app not responding" (ANR) or memory growth while you reproduce a bug.
#
# Usage: scripts/monitor/monitor_android.sh <package> [interval_seconds] [samples]
# Example: scripts/monitor/monitor_android.sh com.example.app 2 60 > run.csv
#
# Needs adb on the PATH and one device connected. Not verified in CI: no device there.
set -euo pipefail

package="${1:?usage: monitor_android.sh <package> [interval] [samples]}"
interval="${2:-2}"
samples="${3:-60}"

command -v adb >/dev/null || { echo "NOT VERIFIED: adb not found" >&2; exit 2; }

echo "time,pss_kb,cpu_percent"
for ((i = 0; i < samples; i++)); do
  now="$(date -u +%H:%M:%S)"
  pss="$(adb shell dumpsys meminfo "$package" 2>/dev/null | awk '/TOTAL PSS:/ {print $3; exit}')"
  cpu="$(adb shell top -b -n 1 2>/dev/null | awk -v p="$package" '$0 ~ p {gsub("%","",$9); print $9; exit}')"
  echo "$now,${pss:-},${cpu:-}"
  sleep "$interval"
done
