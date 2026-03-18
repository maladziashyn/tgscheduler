#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")
PROJ=$(basename $BASE_DIR)
WIN_MAIN="main"
WIN_GIT="git"

SOURCE_VENV="source "${BASE_DIR}"/venv/bin/activate"
COMBO="cd "${BASE_DIR}" && "${SOURCE_VENV}" && clear"

# Exit if tmux session already exists.
tmux has-session -t $PROJ 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Session already exists. Attaching..."
    tmux attach -t $PROJ
    exit 0
fi

# Start a new detached (-d) tmux session (-s) named BASENAME with main window.
tmux new-session -d -s $PROJ -n $WIN_MAIN
tmux send-keys -t $PROJ:$WIN_MAIN "$COMBO" C-m

tmux new-window -t $PROJ -n $WIN_GIT
tmux send-keys -t $PROJ:$WIN_GIT "cd "${BASE_DIR}" && clear" C-m
tmux send-keys -t $PROJ:$WIN_GIT "git status" C-m

# tmux select-window -t $WIN_MAIN

tmux attach-session -t $PROJ

exit 0

