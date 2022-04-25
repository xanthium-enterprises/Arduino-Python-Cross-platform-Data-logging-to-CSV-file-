# Logs the Temperature values in a CSV file
# CSV file name generated from current time and date
# uses SIGINT signal to stop the script

# Sends the $ character to the Arduino,
# Arduino sends back the temperature values from all the 4 sensors at atime
# The Python script uses a while loop to query the arduino continously

# logs No,Date,time  ,4 analog channels temp values
# Eg "10,22 April 2022,09:01:06,34.87,33.55,34.63,34.07"

# Use CTRL + C to stop execution of the Script


import serial   # PySerial needs to be installed in your system
import time     # for Time
import signal   # Import signal module using the import keyword
import platform

log_count = 1
logging_interval_seconds = 1
Baudrate  = 9600
COMport   = 'COM4'


sentry = True # used to control the While loop querying the Arduino and writing to file

# Print Info about the Program
print('+----------------------------------------------------------------+')
print('|  Arduino Python Serial Port Data Logging to CSV file Software  |')
print('+----------------------------------------------------------------+')
print('| Requires Pyserial installed on your System                     |')
print('| use CTRL + C to exit from the software                         |')
print('| log file name created using date and time                      |')
print('| (c) www.xanthium.in                                            |')
print('+----------------------------------------------------------------+\n')

print('OS full name           -> ' + platform.system() + '-' + platform.release()) # Which OS,Which OS Version
print('Python Implementation  -> ' + platform.python_implementation() +' Version ' + platform.python_version()) # Which Python,Which Version

# Enter the Serial port number or Baud rate here
print('[Windows - COMxx or Linux - /dev/ttyUSBx]')
COMport = input('Enter Serial Port Number ->')
print('\nPort Selected ->',COMport.upper() )
print('Baud Rate     ->',Baudrate )

# Generate file name using Current Date and Time

current_local_time = time.localtime() #Get Current date time
filename           = time.strftime("%d_%B_%Y_%Hh_%Mm_%Ss",current_local_time)# 24hour clock format
filename           = 'ard_'+ filename + '_daq_log.csv'
print(f'\nCreated Log File -> {filename}')

print(f'\nLogging interval = {logging_interval_seconds} Seconds\n')

#Create a csv File header

with open(filename,'w+') as csvFile:
    csvFile.write('No,Date,Time,AN1,AN2,AN3,AN4\n')
    


#Open the Serial Port using Pyserial
SerialObj = serial.Serial(COMport,Baudrate) # COMxx   format on Windows
                                            # /dev/ttyUSBx format on Linux
                                            #
                                            # Eg /dev/ttyUSB0
                                            # SerialObj = serial.Serial('/dev/ttyUSB0')

print('3 sec Delay for Arduino Reset')
time.sleep(3)   # Only needed for Arduino,For AVR/PIC/MSP430 & other Micros not needed
                # opening the serial port from Python will reset the Arduino.
                # Both Arduino and Python code are sharing Com11 here.
                # 3 second delay allows the Arduino to settle down.

#Signal
# Create a Signal Handler for Signals.SIGINT:  CTRL + C 
def SignalHandler_SIGINT(SignalNumber,Frame):
    print ('CTR+C Pressed,Signal Caught')
    global sentry  # Global required since we want to modify sentry from inside the function
    sentry = False #Turn sentry into false so it exits the while loop
    print ('sentry = ',sentry)

signal.signal(signal.SIGINT,SignalHandler_SIGINT) #register the Signal Handler
    



# infinite loop that querie the arduino for data by sending $ character                
while sentry:
    #print(sentry) #debugging only
    BytesWritten = SerialObj.write(b'$') #transmit $,to get temperture values from Arduino,
    #print('$ transmitted to Arduino')
    time.sleep(0.10)
    ReceivedString = SerialObj.readline()       # Change to receive  mode to get the data from arduino,Arduino sends \n to terminate
    ReceivedString = str(ReceivedString,'utf-8')# Convert bytes to string of encoding utf8
    tempvalueslist = ReceivedString.split('-')  # Split the string into 4 values at '-'  
    #print(f'AN1={tempvalueslist[0]} AN2={tempvalueslist[1]} AN3={tempvalueslist[2]} AN4={tempvalueslist[3]}')
    
    seperator = ','
    
    log_time_date = time.localtime() #Get log date time from PC
    log_time = time.strftime("%H:%M:%S",log_time_date) #hh:mm:ss
    log_date = time.strftime("%d %B %Y",log_time_date) #dd MonthName Year
    #print(log_time)
    #print(log_date)
    
    # create a string to write into the file
    log_file_text1 = str(log_count) + seperator + log_date + seperator + log_time + seperator
    log_file_text2 = tempvalueslist[0] + seperator + tempvalueslist[1] + seperator +tempvalueslist[2]+ seperator+tempvalueslist[3]
    log_file_text3 =  log_file_text1 +  log_file_text2 + '\n'
    
    # write to file .csv
    with open(filename,'a') as LogFileObj:
        LogFileObj.write(log_file_text3)
        
    print(log_file_text3)
    log_count = log_count + 1 #increment no of logs taken
    
    time.sleep(logging_interval_seconds) #change logging_interval_seconds to change sensing interval 

#exit from the loop and close the Serial port when sentry = False
SerialObj.close()          # Close the port
print('Data logging Terminated')
print('====================================')