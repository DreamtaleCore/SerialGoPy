#!/usr/bin/env python
#coding:utf-8
"""
  Author:  DreamTale --<dreamtalewind@gmail.com>
  Purpose: For serial read and wirte
  Created: 2016年11月07日
"""

import serial

serial_port = '/dev/ttyUSB0'
baud_rate = 9600
ser = serial.Serial()

#----------------------------------------------------------------------
def serial_configure():
    """to setup the serial"""
    global ser, serial_port, baud_rate
    ser = serial.Serial(port=serial_port, baudrate=baud_rate)

#----------------------------------------------------------------------
recvBuff = ''
startRecord = False
def serial_read(useParse=False, header='$', tail='#'):
    """read data from serial"""
    global ser, recvBuff, startRecord
    retData = ''
    if useParse:
        if ser.readable():
            while ser.inWaiting():
                c = ser.read(1)
                if c == header:
                    startRecord = True
                    recvBuff = ''
                elif c == tail:
                    startRecord = False
                    if recvBuff != '':
                        print 'I get: ', recvBuff
                        retData = recvBuff
                elif startRecord:
                    recvBuff += c
                else:
                    pass
        else:
            print 'The serial', ser.portstr, 'cannot be read.'
            pass
    else:
        if ser.readable():
            while ser.inWaiting():
                retData += ser.read(1)
        else:
            print 'The serial', ser.portstr, 'cannot be read.'
            pass        
    return retData

#----------------------------------------------------------------------
def serial_write(data):
    """write data to the serial port"""
    global ser
    if ser.writable():
        ser.write(data)
    else:
        print 'The serial', ser.portstr, 'cannot be written.'

#----------------------------------------------------------------------
if __name__ == '__main__':
    serial_configure();
    while True:
        #recv = serial_read(useParse=True)
        #if recv != '':
            #print 'After function: ', recv
        data = raw_input('Please input the angle: ')
        serial_write(data)
    