#!/bin/bash

DATE=$(date +%Y_%m_%d_%H_%M);
FILENAME="${HOME}/FanTest/log/${DATE}_run_log.txt";

cd ~/FanTest/testing/GpuTest/ || exit;
# GpuTest *must* be run from this dir or /data is inaccessible to it and it defaults to running triangle

stress-ng --cpu 6 -t 1m &
./GpuTest /test=fur /width=1920 /height=1080 /fullscreen /msaa=8 /benchmark /benchmark_duration_ms=60000 /no_scorebox /no_log_score &
watch -n 5 -p "echo DATE::$(date --iso-8601='seconds') >> ${FILENAME} && sensors >> ${FILENAME}";
# use the furmark test at full screen resolution, 8x anti-aliasing, for 30 minutes (180000ms), don't display or log

sleep 60;

kill -INT $(pidof watch);

wait;