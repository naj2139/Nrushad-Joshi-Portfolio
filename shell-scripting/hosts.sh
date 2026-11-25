#!/bin/bash
# Exercise: read a file line by line, skip empty and # lines, count the rest
# while IFS= read -r line : read a file line by line (keeps spaces and backslashes)
# done < "$1"             : feed the file into the loop
# -z $line                : empty line
# $line == "#"*           : starts with # (keep * unquoted so it acts as a glob)
# continue                : skip to the next iteration

total=0
if [[ -f "$1" ]]; then
  while IFS= read -r line; do
    if [[ -z $line || $line == "#"* ]]; then
      continue
    else
      echo $line
      total=$(( total+1 ))
    fi
  done < "$1"
fi
echo $total
