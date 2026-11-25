#!/bin/bash
# Exercise: for each .h file in a directory, print its line count, then the total file count
# $( )          : capture command output
# awk '{print $1}' : first field (single quotes so bash doesn't expand $1)
# $(( ))        : integer math, returns result
# var=value     : assign (no $ on the left)

total=0
if [[ -e "$1" && -d "$1" ]]; then
  for f in "$1"/*.h; do
    lineCount=$(wc -l "$f" | awk '{print $1}')
    echo "$(basename "$f"): $lineCount"
    total=$(( total+1 ))
  done
fi
echo "Total: $total"
