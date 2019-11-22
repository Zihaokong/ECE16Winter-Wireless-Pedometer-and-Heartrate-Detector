"""
Author: Ramsin Khoshabeh
Contact: ramsin@ucsd.edu
Date: 07 April 2019
Description: A wrapper for HM-10 BLE connection to handle 2-way communiation and handshake protocol.
"""

# Imports
import serial
from time import sleep
from time import time

class BLE:

    """ ================================================================================
    Constructor that sets up the BLE for the first time. It will only run
    :param serial_port: (str) the Serial port for the PC HM-10
    :param baudrate: (int) the baud rate to use to connect to the PC HM-10
    :param do_config: (bool) whether to initialize the PC HM-10 or not
    :return: None
    ================================================================================ """
    def __init__(self, serial_port, baudrate=9600, do_config=False):
        self._baudrate = baudrate
        self._serial_port = serial_port
        self._ser = serial.Serial(port=serial_port, baudrate=baudrate, timeout=1)
        self._peripheral_mac = None

        if do_config :
            self.write("AT")
            sleep(0.5)
            self.flush()

            commands = ["AT+IMME1", "AT+NOTI1", "AT+ROLE1", "AT+RESET"]
            print("Setting up the HM-10:")
            for command in commands :
                print("> " + command)
                self.write(command)
                sleep(0.5)
            print("Config completed successfully.")
        return

    """ ================================================================================
    Function to connect to the remote HM-10 using a 2-step BLE handshake protocol.
    While the connection is not confirmed, it will loop until 'max_tries' and:
        1) read everything in the buffer (using read_lines())
        2) check if connected: looking for "OK+CONNAOK+CONN" and not "CONNF" or "CONNE"
        3) check if confirmed: looking for "#"
        4) if not connected, writes a connection message (using self.write())
        5) if not confirmed, writes a "AT+NAME?" message (using self.write())
        6) if the loop exited and it wasn't confirmed, it raises an IOError
    :param peripheral_mac: MAC address of the remote HM-10 to connect with
    :param max_tries: maximum number of attempts before raising an IOError
    :return: nothing
    ================================================================================ """
    def connect(self, peripheral_mac, max_tries=20):
        print("start connect")
        self._peripheral_mac = peripheral_mac

        if self._ser is None or self._ser.closed:
            self._ser = serial.Serial(port=self._serial_port, baudrate=self._baudrate, timeout=1)

        # Always assume connected. Disconnect first and remove connection lost messages.
        print("Resetting connection.")
        self.write("AT")
        sleep(0.5)
        self.flush()
        x=0
        isConfirmed = False
        connected = False
        while isConfirmed is False and x<max_tries:
            string = self.read_lines()
            print(string)
            sleep(0.5)
            x+=1
            if "OK+CONNAOK+CONN" in string and "CONNF" not in string and "CONNE" not in string:
                connected = True
            if "#" in string:
                isConfirmed = True
                print("IS CONFIRMED",isConfirmed)
                return

            if connected == False:
                toWrite = "AT+CON"+self._peripheral_mac
                self.write(toWrite)
                sleep(0.5)
            if connected == True and isConfirmed == False:
                self.write("AT+NAME?")
        if isConfirmed == False:
            print("IO ERROR")
            raise IOError

        # 1. loop while not confirmed and we have not reached max_tries
        #   1.1. read the current hm10 buffer with self.read_lines()
        #       1.1.1. check if "OK+CONNAOK+CONN" is in the message but not "CONNF" or "CONNE"
        #           set connected to True if so
        #       1.1.2. check if "#" is in the message
        #           set confirmed to True if so
        #   1.2. if not connected
        #       1.2.1. try to connect with self._peripheral_mac
        #       1.2.2. sleep for half a second
        #   1.3. if not confirmed
        #       1.3.1. write "AT+NAME?" to the hm10
        #       1.3.2. sleep for half a second
        # 2. if not confirmed, raise an IOError because max_tries was reached


    """ ================================================================================
    Function to check if a connection was broken and tries to reconnect 'max_tries' 
    times. It will loop until 'max_tries' times and:
        1) look for 'OK+LOST' in the 'msg'
        2) call self.connect() if 'OK+LOST' was received
        3) call msg = self.read_lines() to see if 'OK+LOST' is still in the buffer
        4) If it reaches 'max_tries', it raises an IOError
    :param msg: the received message
    :param max_tries: maximum number of attempts before raising an IOError
    :return: nothing, but throws an IOError in case of failed connection
    ================================================================================ """
    def check_connection(self, msg, max_tries=10):
        x=0
        while "OK+LOST" in msg and x < max_tries:
            print("check connection!!!!!!!!!!!!")
            self.connect(self._peripheral_mac)
            msg = self.read_lines()
            x+=1


        if x>max_tries:
            print("IO error")
        # 1. loop while "OK+LOST" is in 'msg' and we have not reached max_tries
        #   1.1. try to connect by calling self.connect()
        #   1.2. read the entire buffer into 'msg'
        # 2. if attempts was >= max_tries, raise an IOError exception


    """ ================================================================================
    Function to read a single character from the BLE buffer
    :return: String containing data read from the BLE buffer (or empty string)
    ================================================================================ """
    def read(self):
        val = ""
        try:
            if (self._ser.in_waiting > 0):
                val = self._ser.read().decode('utf-8')
        except ValueError:
            print("Value Error：", val,"...")
            val = ""
        return val
        # 1. inside of a try-except block...
        #   1.1 check if there is anything in the hm10 buffer (hint: in_waiting)
        #       1.1.1. if there is, read a single byte and decode it (look at PySerial docs if you forgot)
        # 2. catch ValueError exceptions and print it to console
        # 3. Either return the byte (char) that was read or an empty string if an error happened


    """ ================================================================================
    Function to read the HM-10 buffer until the character 'eol' and tries to reconnect a
    lost connection. It repeatedly calls the self.read() function to read one character
    at a time. It will read until 'timeout' is reached if the termination is not found.
    Once the message is received, it calls self.check_connection() to make sure the
    message did not have an error in it and then returns the message.
    :param eol: character (single element string) containing delimiting character
    :param timeout: integer signifying how many seconds before it quits
    :return: String containing data read from the BLE buffer (or empty string)
    ================================================================================ """
    def read_line(self, eol='\n', timeout=1):
        assert len(eol) == 1, "Delimiting character must be a single element string."
        assert isinstance(eol, str), "Delimiting character must be a string."

        msg, c = '', ''
        t1 = time()
        while (c != eol) and (time() - t1 < timeout):
            msg += c
            c = self.read()

        #self.check_connection(msg)
        return msg

    """ ================================================================================
    Function to read the entire HM-10 buffer and tries to reconnect a lost connection.
    It repeatedly calls the self.read() function to read one character at a time.
    Once the message is received, it calls self.check_connection() to make sure the
    message did not have an error in it and then returns the message.
    :return: String containing data read from the BLE buffer (or empty string)
    ================================================================================ """
    def read_lines(self):
        msg = ''
        while self._ser.in_waiting:
            msg += self.read()
        self.check_connection(msg)
        return msg

    """ ================================================================================
    Function to write a message 'msg' to the PC HM-10. When not connected, these are
    commands to the module. When connected, it will be data sent over BLE.
    :return: nothing
    ================================================================================ """
    def write(self, msg):
        self._ser.write(msg.encode("utf-8"))
        return

    """ ================================================================================
    Function to clean both input and output buffers of the PC HM-10 module.
    :return: nothing
    ================================================================================ """
    def flush(self):
        self._ser.flushInput()
        self._ser.flushOutput()
        sleep(0.1)
        return

    """ ================================================================================
    Function to disconnect BLE, flush buffers, and close the Serial port
    :return: nothing
    ================================================================================ """
    def close(self):
        self.write("AT")
        sleep(0.5)
        self.flush()
        self._ser.close()
        return

