#!/bin/bash
# Exercise: count jobs per status from a log, sorted by count
# read -r -a line          : split each line into an array
# ${line[2]}               : 3rd field (index from 0)
# done < file | sort ...   : pipe the whole loop's output
# sort | uniq -c | sort -nr : count + rank

if [[ -f "$1" ]]; then
  while read -r -a line; do
    echo ${line[2]}
  done < "$1" | sort | uniq -c | sort -nr
fi
