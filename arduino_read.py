'''Get data from arduino'''
import serial
from time import sleep

def weather_inside():
    '''Ask arduino for data'''
    weather = {}
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    sleep(2)
    ser.write("t".encode())
    weather['temp_in'] = float(ser.readline())
    ser.write("h".encode())
    weather['humidity_in'] = float(ser.readline())
    ser.write("p".encode())
    weather['pressure_in'] = int(ser.readline())/100
    return weather
