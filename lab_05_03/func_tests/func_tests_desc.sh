#!/bin/bash

dir="results"
ind=1
desc="$(jq -r '.[] | select(.name=="test_'$ind'") | .desc' func_tests/func_tests.json)"
while [ -n "$desc" ]
do
    echo "$desc" > "$dir/test_$ind.txt"
    ind=$((ind + 1))
    desc="$(jq -r '.[] | select(.name=="test_'$ind'") | .desc' func_tests/func_tests.json)"
done
