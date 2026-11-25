#!/bin/bash
# Exercise: classify a path as dir, empty file, executable, or file
# -z    : true if string is empty
# -e    : path exists
# -d    : is a directory
# -s    : exists and size > 0 (! -s = empty)
# -x    : executable by current user
# -f    : regular file

if [[ -z $1 ]]; then
  echo "Missing Path"
else
  if [[ -e $1 ]]; then
    if [[ -d $1 ]]; then
      echo "dir"
    elif [[ ! -s $1 ]]; then
      echo "empty file"
    elif [[ -x $1 ]]; then
      echo "executable"
    elif [[ -f $1 ]]; then
      echo "file"
    fi
  else
    echo "Invalid Path"
  fi
fi
