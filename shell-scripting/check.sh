#!/bin/bash
# Exercise: classify a number as high (>100), medium (50-100), or low
# [[ ]] : string/file tests
# (( )) : integer math and comparison
# -z    : true if string is empty

if [[ -z "$1" ]]; then
  echo "Empty"
elif (( $1 >= 100)); then
  echo "High"
elif (( $1 >= 50 && $1 < 100 )); then
  echo "Medium"
else
  echo "low"
fi
