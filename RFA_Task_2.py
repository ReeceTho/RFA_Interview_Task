import time
import serial
import matplotlib.pyplot as plt
import random

#Write a Python script capable of visualising a 60 second snippet of acquired data. It's not
#necessary to have a live view of the incoming data.
#Provide a link to a public git repository, including a way to test the written software by
#emulating the serial data sent by the 4-20 mA to USB converter

port_name = 'COM3'                              #this was the name of my COM port for the USB
sample_time = 60                                #time limit on data gathering (seconds)
data = []
time_stamps = []
mode = 'emulate'                                #can be set to 'emulate' or 'read' 

if mode == 'read':
    ser = serial.Serial(port_name, timeout=1)       #sample from 'port_name' every 1 second  
    start_time = time.time()
    while time.time() - start_time < sample_time:   #starting a timer at t=0 until the length of sample_time
        reading = ser.readline()                    #gets a reading from the sensor
        reading.decode('UTF-8')                     #i assume sensor gives unicode 8
        reading.strip()
        reading = float(reading)  
        data.append(reading)
        time_stamps.append(time.time()-start_time)  #this marks the time elapsed when the reading is taken
        plt.title("Sampled real data")
    ser.close()

elif mode == 'emulate':
    for i in range(0, sample_time+1):
        rand_reading = random.uniform(4,20)             #in mA
        data.append(rand_reading)
        time_stamps.append(i)
        plt.title("Emulated data")

else:
    print("Invalid data aquisition mode")



plt.plot(time_stamps, data)
plt.xlabel("Time elapsed / s")
plt.ylabel("Sensor reading / mA")
plt.show()