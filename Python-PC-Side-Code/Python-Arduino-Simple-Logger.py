# Logs the Temperature values in a CSV file
# CSV file name generated from current time and date

# No Sinal Handler code for catching SIGINT interrupt


# Sends the $ character to the Arduino,
# Arduino sends back the temperature values from all the 4 sensors at atime
# The Python script uses a while loop to query the arduino continously

# logs No,Date,time  ,4 analog channels temp values
# Eg "10,22 April 2022,09:01:06,34.87,33.55,34.63,34.07"

# Use CTRL + C to stop execution of the Script


import serial #PySerial needs to be installed in your system
import time   # for Time 

# Generate file name using Current Date and Time

current_local_time = time.localtime() #Get Current date time
filename           = time.strftime("%d_%B_%Y_%Hh_%Mm_%Ss",current_local_time)# 24hour clock format
filename           = 'ard_'+ filename + '_daq_log.csv'
print(f'Created Log File -> {filename}')

#Create a csv File header

with open(filename,'w+') as csvFile:
    csvFile.write('No,Date,Time,AN1,AN2,AN3,AN4\n')
    
log_count = 1

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
    
    time.sleep(10) #change this delay to change sensing interval 

SerialObj.close()          # Close the port
