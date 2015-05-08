#!/bin/bash
while :
do
  rtl_fm -M am -f 433.993M -s 12k 2>/dev/null | python3 ./stream.py
  sleep 110
done
