#!/bin/bash

FILEDATE=$(date +%Y_%m_%d_%H_%M);
FILENAME="${HOME}/FanTest/log/${FILEDATE}_run_log.txt";  # filename is the date down to the minute for uniqueness

cd ~/FanTest/testing/GpuTest/ || exit;
# GpuTest *must* be run from this dir or /data is inaccessible to it and it defaults to running triangle

monitor() {
  stop=$(($1 + $(date +%s)));

  while [ $(date +%s) -lt $stop ]; do
    sleep 2 & (echo "DATE::$(date --iso-8601='seconds')" >> $FILENAME  && sensors >> $FILENAME) & wait;
    # write date and sensor info in background, immediately begin sleep to keep writes ~precisely on the 2s mark
  done;

  # TODO: Could add annotation like "echo "STRESSEND::$(date --iso-8601='seconds'" to get exact off-time of CPU stressor
}


runTest() {
  monitor 300;  # monitor without stressing for 5 minutes prior to every run

  monitor 2700 &
  stress-ng --cpu 6 -t 1800 &
  ./GpuTest /test=fur /width=1920 /height=1080 /fullscreen /msaa=8 /benchmark /benchmark_duration_ms=1800000 /no_scorebox /no_log_score &
  wait;

  # record time and date to file just prior to writing sensor info every 2s; totals to 900 measurements over 30min
    # annotate date row with "DATE::" for easy processing later
  # use stress-ng's blanket CPU stressor (explicityly 6 instances (one per core) and for 30 minutes
  # use the furmark test at full screen resolution, 8x anti-aliasing, for 30 minutes (180000ms), don't display or log
}


for ((i = 1; i < 4; i++)); do
  runTest;
done

monitor 300;  # monitor without stressing for 5 minutes after last run



