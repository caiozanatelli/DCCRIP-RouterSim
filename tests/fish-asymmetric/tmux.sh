#!/bin/sh
set -eu

exe="python3.5 ../../router.pyc"
exe="../../router.py"

for i in $(seq 1 6) ; do
    tmux split-pane -v $exe --addr "127.0.1.$i" --startup-commands "$i.txt" &
    tmux select-layout even-vertical
done
