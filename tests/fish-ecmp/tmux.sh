#!/bin/sh
set -eu

# exe="python3.5 ../../router.pyc"
# exe="../../router.py"

exe="python3.5 ../../dccrip/router.pyc"
exe="../../dccrip/router.py"

for i in $(seq 1 6) ; do
    tmux split-window -v $exe "127.0.1.$i" 1 "$i.txt" &
    tmux select-layout even-vertical
done
