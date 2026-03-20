#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")
PROJ="tg_rcv"   # tmux session name
WIN_MAIN="rcv_main"
SOURCE_VENV="source "${BASE_DIR}"/venv/bin/activate"
COMBO="cd "${BASE_DIR}" && "${SOURCE_VENV}" && clear"

# Exit if tmux session already exists.
tmux has-session -t $PROJ 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Session already exists. Attaching..."
    tmux attach -t $PROJ
    exit 0
fi

# Start a new detached -d session -s named PROJ.
tmux new-session -d -s $PROJ -n $WIN_MAIN
tmux send-keys -t $PROJ:$WIN_MAIN "$COMBO" C-m
tmux send-keys -t $PROJ:$WIN_MAIN "python receiver.py" C-m

# tmux attach-session -t $PROJ
exit 0

