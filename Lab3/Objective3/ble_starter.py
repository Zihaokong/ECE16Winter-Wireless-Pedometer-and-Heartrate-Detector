import serial
from time import sleep        # sleep is like the delay function in Arduino

serial_port = "COM5"                # You need to put the correct port for the console cable (not Arduino!)

# Read from serial ser and return the string that was read
def read_BLE(ser):
    if (ser.in_waiting > 0):
        string = ser.readline(ser.in_waiting).decode('utf-8')
        print(string)
        return string
    return ""


# Write the string, command, to serial ser; return nothing
def write_BLE(command, ser):
    ser.write(command.encode("utf-8"))


# Open the serial port and when successful, execute the code that follows
with serial.Serial(port=serial_port, baudrate=9600, timeout=1) as ser:
    write_BLE("AT+NAMEKZH",ser)
    sleep(0.1)
    string = read_BLE(ser)
    write_BLE("AT+NAME?",ser)
    sleep(0.1)
    string = read_BLE(ser)
