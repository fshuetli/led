#!/bin/bash
PS=$(ps -ef | grep "python.*server.p[y]")
if [[ -n "$PS" ]]; then
  echo "Server is already running ($PS)"
else
  echo "Starting Server"
  python /home/pi/fishlight/server.py > serverlog.txt 2>&1 &
fi
