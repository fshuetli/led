#!/bin/bash
PIDS=$(ps -ef | grep "python.*server.p[y]" | awk '{print $2}')
kill $PIDS
