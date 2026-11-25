# Shell Scripting

Bash scripts showing my shell scripting knowledge: conditionals, file tests, loops, reading files line by line, and text processing (awk, sort, uniq).

| Script | Covers |
|---|---|
| check.sh | if / elif / else, `[[ ]]`, `(( ))` |
| filecheck.sh | file tests: `-e -d -f -s -x` |
| sweep.sh | `for` over files, `$( )`, awk, counters |
| hosts.sh | `while read`, skipping blank/comment lines |
| jobs.sh | arrays, `sort \| uniq -c \| sort -nr` |

Sample inputs are in `data/`. Example: `./jobs.sh data/jobs.log`
