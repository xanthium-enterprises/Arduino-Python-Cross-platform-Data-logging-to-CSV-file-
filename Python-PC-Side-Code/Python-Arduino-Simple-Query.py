# Displays the Temperature values on Python Command line >>>

# Sends the $ character to the Arduino,
# Arduino sends back the temperature values from all the 4 sensors at atime
# The Python script uses a while loop to query the arduino continously
# Use CTRL + C to stop execution of the Script


import serial #PySerial needs to be installed in your system
import time   # for Time 

#COM 4 may change with system
SerialObj = serial.Serial('COM4',9600) # COMxx   format on Windows
                                        # /dev/ttyUSBx format on Linux
                                        #
                                        # Eg /dev/ttyUSB0
                                        # SerialObj = serial.Serial('/dev/ttyUSB0')

time.sleep(3)   # Only needed for Arduino,For AVR/PIC/MSP430 & other Micros not needed
                # opening the serial port from Python will reset the Arduino.
                # Both Arduino and Python code are sharing Com11 here.
                # 3 second delay allows the Arduino to settle down.
while 1:
    BytesWritten = SerialObj.write(b'$') #transmit $,to get temperture values from Arduino,
    time.sleep(0.10)
    ReceivedString = SerialObj.readline()       # Change to receive  mode to get the data from arduino,Arduino sends \n to terminate
    ReceivedString = str(ReceivedString,'utf-8')# Convert bytes to string of encoding utf8
    tempvalueslist = ReceivedString.split('-')  # Split the string into 4 values at '-'  
    print(f'AN1={tempvalueslist[0]} AN2={tempvalueslist[1]} AN3={tempvalueslist[2]} AN4={tempvalueslist[3]}')
    time.sleep(1) #change this delay to change sensing interval 

SerialObj.close()          # Close the port