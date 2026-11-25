# Shell Scripting

Bash scripts showing my shell scripting knowledge: conditionals, file tests, loops, reading files line by line, and text processing (awk, sort, uniq).

Shell scripting is the glue of HPC work: Slurm job scripts, benchmark sweeps, parsing results from output files, cluster health checks, and log analysis all run on it.

| Script | Covers |
|---|---|
| check.sh | if / elif / else, `[[ ]]`, `(( ))` |
| filecheck.sh | file tests: `-e -d -f -s -x` |
| sweep.sh | `for` over files, `$( )`, awk, counters |
| hosts.sh | `while read`, skipping blank/comment lines |
| jobs.sh | arrays, `sort \| uniq -c \| sort -nr` |

Sample inputs are in `data/`. Example: `./jobs.sh data/jobs.log`

## AI Usage

I used AI as a tutor to learn and review shell scripting concepts. The scripts are my own work.
