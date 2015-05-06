#! /usr/bin/python3

# Needs 12k as input!

import struct
import sys
from math import floor
from db_sql import write_db

def convert_data(data_block):
    
    weather = {}

    health = [True]*len(data_block)
    # Convert 4 bits each to an int -> 52 bits to 13 int
    for i, data in enumerate(data_block):
        data = [ int(''.join(data[j:j+4]), 2) 
                          for j in range(0,52,4) ]
        data_block[i] = [ str(j) for j in data ]
        if sum(data) % 2 != 0:
             health[i] = False
        # Checksum
        if sum(data[-1:]) & 15 != data[-1]:
            health[i] = False
        # Reverse bit check
        if 15-data[7] != data[10] or 15-data[8] != data[11]:
            health[i] = False

    # convert data
    
    print(data_block)
    alt = int(len(data_block)/2)
    pos = False
    for i in range(0, alt):
        if health[i]:
            pos = i
        elif health[i + alt]:
            pos = i + alt
        if pos == 0 or pos == alt:
            weather['temp_out'] = (int(''.join(data_block[pos][7:10]))-300)/10
        if pos == 1 or pos == alt + 1:
            weather['humidity_out'] = int(''.join(data_block[pos][7:9]))
        if pos == alt - 1 or pos == alt * 2:
            weather['wind_v'] = floor( sum([
                                            int(val)*16**(1-j) for j,val in 
                                            enumerate(data_block[pos][7:9])
                                           ])*90/25
                                      )/10
            weather['wind_d'] = int(data_block[pos][9]) * 22.5
        if alt == 4 and (pos == 2 or pos == alt + 2):
            weather['rain'] = int(''.join(data_block[pos][7:10]))
    
    write_db(weather)

silence = 0
pulse_len = 0
packet = []
block = []
receive = False
while True:
    sample = struct.unpack("h", sys.stdin.buffer.read(2))[0]
    if abs(sample) > 17000:
        receive = True
        silence = 0
        pulse_len += 1
    elif receive:
        if pulse_len > 0:
            if pulse_len < 6 and pulse_len > 2:
                packet.append('1')
                pulse_len = 0
            elif pulse_len < 20 and pulse_len > 14:
                packet.append('0')
                pulse_len = 0
            else:
                pulse_len = 0
                print("Error: Pulse to long or to short")
        elif silence > 30 and len(packet) > 0:
            if len(packet) == 52:
                block.append(packet)
                packet = []
            else:
                print("Error: Not enough bits received")
                packet = []
        elif silence > 2000:
            if len(block) == 6 or len(block) == 8:
                print("Success: Block received")
                convert_data(block)
            else:
                print("Error: Not all blocks received")
            receive = False
            block = []
            silence = 0
        else:
            silence += 1
