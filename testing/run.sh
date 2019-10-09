#!/bin/bash

cd ~/FanTest/testing/GpuTest/ || exit;
# GpuTest *must* be run from this dir or /data is inaccessible to it and it defaults to running triangle

stress-ng --cpu 6 -t 30m &
./GpuTest /test=fur /width=1920 /height=1080 /fullscreen /msaa=8 /benchmark /benchmark_duration_ms=180000 /no_scorebox /no_log_score;
# use the furmark test at full screen resolution, 8x anti-aliasing, for 30 minutes (180000ms), don't display or log

wait;