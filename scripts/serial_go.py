#!/usr/bin/env python
#coding:utf-8
"""
  Author:  DreamTale --<dreamtalewind@gmail.com>
  Purpose: For serial read and wirte
  Created: 2016年11月07日
"""

import serial
import rospy
from std_msgs.msg import String

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
                        #print 'I get: ', recvBuff
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
def pub_serial_read():
    """publish the receive data from serial port"""
    pub = rospy.Publisher('serial_reader', String, queue_size=10)
    while not rospy.is_shutdown():
        recv=serial_read(useParse=True)
        if recv != '':
            rospy.loginfo(recv)
            pub.publish(recv)
        else:
            pass
    print 'Closing...'

#----------------------------------------------------------------------
def callback_serial_write(data):
    """callback the data from other nodes to send the data
         to the serial port"""
    serial_write(data.data)
    
    

#----------------------------------------------------------------------
if __name__ == '__main__':
    serial_configure();
    rospy.init_node('serialGo', anonymous=True)
    # Subscriber:
    rospy.Subscriber('serial_writer', String, callback_serial_write)
    pub_serial_read()
    rospy.spin()
    
