import time
import serial
import matplotlib.pyplot as plt
import random
import csv
import sys

#Write a Python script capable of visualising a 60 second snippet of acquired data. It's not
#necessary to have a live view of the incoming data.
#Provide a link to a public git repository, including a way to test the written software by
#emulating the serial data sent by the 4-20 mA to USB converter

#variables (change for your circumstance)
sample_time = 60                                #time limit on data gathering (seconds)
data = []
time_stamps = []

#basic 
print("1 - Data reading from USB bus")
print("2 - Emulate")
mode = -0
while mode != 1 and mode != 2:
    mode = int(input("Select mode number:   "))
    if mode != 1 and mode != 2:
        print("Enter valid mode number!\n")
if mode == 1:
    mode = 'emulate'
elif mode == 2:
    mode = 'read'
    port_name = input("Enter serial port:    ")

r_shunt = 100                                   #this is the resistance of the shunt in ohms

if mode == 'read':
    try:
        ser = serial.Serial(port_name, timeout=1)       #sample from 'port_name' every 1 second  
    except:
        print("Cannot read serial!")
        sys.exit(1)                                 #ends the program
    start_time = time.time()
    while time.time() - start_time < sample_time:   #starting a timer at t=0 until the length of sample_time
        voltage = ser.readline()                    #gets a reading from the sensor
        voltage = voltage.decode('UTF-8')          #i assume sensor gives unicode 8
        voltage = voltage.strip()
        voltage = float(voltage)
        current = (voltage / r_shunt) * 1000    #readings from the MCU are in voltage, i need to convert back to current
                                                #also, i'm converting the current to mA
        data.append(current)
        time_stamps.append(time.time()-start_time)  #this marks the time elapsed when the reading is taken
        fuel_percent = (current - 4) / 16 * 100     
        #i don't use this, but you can easily just add a new list called plot this instead of current. 
    ser.close()
    plt.title("Sampled real data")

elif mode == 'emulate':         #emulation branch
    for i in range(0, sample_time+1):
        rand_reading = random.uniform(4,20)             #in mA
        data.append(rand_reading)
        time_stamps.append(i)
    plt.title("Emulated data")

else:
    print("Invalid data aquisition mode")


#this is the simple graphical plotting of the data gathered
plt.plot(time_stamps, data)
plt.xlabel("Time elapsed / s")
plt.ylabel("Sensor reading / mA")
plt.fill_between(time_stamps, 0, 4, color='black', alpha = 0.3, label='Fault region (<4mA)')        #highlights <4mA fault
plt.legend()

plt.savefig(f"{mode}.pdf", format='pdf')
plt.show()

#this part is for creating a csv file of the data from the test
with open("data_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time / s", "Current / mA"])
    writer.writerows(zip(time_stamps, data))

