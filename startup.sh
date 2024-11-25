#!/bin/bash

tmux kill-ses -t g8_pork
# 啟動tmux服務
tmux new-session -d -s g8_pork

tmux send-keys -t g8_pork "python3 main.py" C-m

tmux a -t g8_pork

# 結束腳本
exit 0