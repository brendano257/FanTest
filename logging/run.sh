#!/bin/bash

cd ~/FanTest/logging/data || exit

# TODO: Need filename that's useful/won't overwrite, do WITHOUT cd

watch -n 5 -p "date --iso-8601='seconds' >> file && sensors >> file" &
# write date in ISO8601

sleep 30;

# TODO: Sleep for appropriate time

kill -INT $(pidof watch)



