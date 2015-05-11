#! /usr/bin/python3

# Needs 12k as input!
# One signal at 12kHz is around 28000 "short int" long

import os
from time import sleep
from math import floor
import numpy as np

from db_sql import write_db
from arduino_read import weather_inside

def convert_data(data_block, rain_overflow):
    
    with open('rain_last.save', 'r') as f:
        rain_last = int(f.read())
    
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
            rain_temp = sum([
                             int(val)*16**(2-j) for j,val in 
                             enumerate(data_block[pos][7:10])
                           ])
            if rain_temp < rain_last:
                with open('rain_overflow.save', 'w') as f:
                    rain_overflow = rain_last * 0.51657 + rain_overflow
                    f.write(str(rain_overflow))
            with open('rain_last.save', 'w') as f:
                f.write(str(rain_temp))
            weather['rain'] = rain_temp * 0.51657 + rain_overflow
    
    write_db(weather)
    write_db(weather_inside())
    
def get_sample(rp):
    dt = np.dtype('i2')
    threshold = 13000
    response = rp.read(2**16)
    return ( abs( np.frombuffer(response, dtype=dt) ) 
             > threshold )

def main(rp):
    with open('rain_overflow.save', 'r') as f:
               rain_overflow = float(f.read())

    silence = 0
    pulse_len = 0
    packet = []
    block = []

    sample = get_sample(rp)
    if np.any(sample):
        # Make sure the signal is not cut off
        sample = np.append(sample, get_sample(rp))
        index = np.nonzero(sample == True)[0]
        # Cut signal
        sample = sample[index[0]:index[-1] + 1]
        # Add "silence" to mark the end of the signal
        sample = np.append(sample, np.array([False]*40))
        for val in sample:
            if val == True:
                silence = 0
                pulse_len += 1
            elif pulse_len > 0:
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
            else:
                silence += 1
        if len(block) == 6 or len(block) == 8:
            # Check for six blocks but rain?
            #print("Success: Block received")
            convert_data(block, rain_overflow)
            return True
        else:
            print("Error: Not all blocks received")
        
    return False

if __name__ == "__main__":
    rtl_pipe = "/tmp/rtl_fm-stream"
    try:
        os.mkfifo(rtl_pipe)
    except:
        pass
    open_rtl_fm = ("rtl_fm -M am -f 433.993M -s 12k 2>/dev/null > "
                    + "/tmp/rtl_fm-stream & ")
    os.system(open_rtl_fm)
    rp = open(rtl_pipe, 'rb')
    wait = False
    while True:
        if wait:
            os.system("killall rtl_fm")
            sleep(105)
            os.system(open_rtl_fm)
        wait = main(rp)
