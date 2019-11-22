import serial
from time import sleep        # sleep is like the delay function in Arduino

serial_port = "COM6"                # You need to put the correct port for the console cable (not Arduino!)

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
    write_BLE("AT",ser)
    sleep(0.1)
    print(read_BLE(ser))

    write_BLE("AT+IMME1",ser)
    sleep(0.1)
    print(read_BLE(ser))

    write_BLE("AT+NOTI1", ser)
    sleep(0.1)
    print(read_BLE(ser))

    write_BLE("AT+ROLE1", ser)
    sleep(0.1)
    print(read_BLE(ser))

    write_BLE("AT+RESET", ser)
    sleep(0.1)
    print(read_BLE(ser))


    #detects connection and then check if success, it exits the loop
    x=0
    while 1:
        write_BLE("AT+CON78DB2F16821E", ser)
        sleep(2)

        string = read_BLE(ser)
        print(string)


    write_BLE("Connected", ser)