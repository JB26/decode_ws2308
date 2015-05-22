#! /usr/bin/python3

# Needs 12k as input!
# One signal at 12kHz is around 28000 "short int" long

import os
from time import sleep
from math import floor
import numpy as np

import db_sql
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
    pos = []
    for i in range(0, alt):
        if health[i]:
            pos.append(i)
        elif health[i + alt]:
            pos.append(i + alt)
    for i in pos:
        if data_block[i][2] == '0' or data_block[i][2] == '4':
            weather['temp_out'] = (int(''.join(data_block[i][7:10]))-300)/10
        elif data_block[i][2] == '1' or data_block[i][2] == '5':
            weather['humidity_out'] = int(''.join(data_block[i][7:9]))
        elif data_block[i][2] == '3' or data_block[i][2] == '7':
            weather['wind_v'] = floor( sum([
                                            int(val)*16**(1-j) for j,val in 
                                            enumerate(data_block[i][7:9])
                                           ])*90/25
                                      )/10
            weather['wind_d'] = int(data_block[i][9]) * 22.5
        if data_block[i][2] == '2' or data_block[i][2] == '6':
            rain_temp = sum([
                             int(val)*16**(2-j) for j,val in 
                             enumerate(data_block[i][7:10])
                           ])
            if rain_temp < rain_last:
                with open('rain_overflow.save', 'w') as f:
                    rain_overflow = rain_last * 0.51657 + rain_overflow
                    f.write(str(rain_overflow))
            with open('rain_last.save', 'w') as f:
                f.write(str(rain_temp))
            weather['rain'] = rain_temp * 0.51657 + rain_overflow

    if len(weather) > 0:
        db_sql.write_db(weather)
    db_sql.write_db(weather_inside())
    
def get_sample(stream):
    dt = np.dtype('i2')
    threshold = 6000  # Weird it did work with 13000 but not anymore?
    x = []
    i = 0
    while len(x) == 0:
        sleep(5)
        response = stream.read(2**18)
        x = np.absolute( np.frombuffer(response, dtype=dt) )
        if len(x) == 0:
            i += 1
            if i > 5:
                return [ None, True ]
    error = False
    return [( x > threshold ), error]

def main(stream):
    with open('rain_overflow.save', 'r') as f:
               rain_overflow = float(f.read())

    silence = 0
    pulse_len = 0
    packet = []
    block = []

    sample = get_sample(stream)
    if sample[1]:
        print("Broken Pipe?")
        return True
    else:
        sample = sample[0]
    if np.any(sample):
        # Make sure the signal is not cut off
        sample = np.append(sample, get_sample(stream)[0])
        index = np.nonzero(sample == True)[0]
        # Cut signal
        sample = sample[index[0]:index[-1] + 1]
        # Add "silence" to mark the end of the signal
        sample = np.append(sample, np.array([False]*80))
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
                    print("Error: Pulse to long or to short")
                    return True
            elif silence > 60 and len(packet) > 0:
                if len(packet) == 52:
                    block.append(packet)
                    packet = []
                else:
                    print("Error: Not enough bits received")
                    return True
            else:
                silence += 1
        if len(block) == 6 or len(block) == 8:
            print("Success: Block received")
            convert_data(block, rain_overflow)
            return True
        else:
            print("Error: Not all blocks received")
            return True
    else:
        return False

if __name__ == "__main__":
    db_sql.init()
    tmp_file = "/tmp/rtl_fm-stream.tmp"
    open_rtl_fm = ("rtl_fm -M am -f 433.993M -g 50 -s 12k 2>/dev/null > "
                    + tmp_file + " & ")
    os.system("killall rtl_fm 2>/dev/null") # killall old instances
    os.system("killall -9 rtl_fm 2>/dev/null")
    os.system(open_rtl_fm)
    sleep(3)
    stream = open(tmp_file, 'rb')
    wait = False
    while True:
        if wait:
            os.system("killall rtl_fm 2>/dev/null")
            os.system("killall -9 rtl_fm 2>/dev/null")
            sleep(100)
            os.system(open_rtl_fm)
            sleep(3)
            start_up = False
            stream.seek(0, 0)
        wait = main(stream)
