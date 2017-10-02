#/bin/bash

ps | grep client.py | awk '{print $2}' | xargs kill -9
ps | grep 'client.sh' | awk '{print $2}' | xargs kill -9
ps | grep server.py | awk '{print $2}' | xargs kill -9
ps | grep 'start.sh' | awk '{print $2}' | xargs kill -9
