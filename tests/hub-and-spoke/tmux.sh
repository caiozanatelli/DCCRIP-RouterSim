#!/bin/sh
set -eu

exe="python3.5 ../../router.pyc"
exe="../../router.py"

tmux split-pane -v $exe --addr 127.0.1.10 --startup-commands hub.txt &

for i in $(seq 1 5) ; do
    tmux split-pane -v $exe --addr "127.0.1.$i" --startup-commands spoke.txt &
    tmux select-layout even-vertical
done
