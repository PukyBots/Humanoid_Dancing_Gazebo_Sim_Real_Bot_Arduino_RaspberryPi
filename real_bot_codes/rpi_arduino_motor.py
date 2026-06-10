import serial
import time

# Change this if needed
PORT = '/dev/ttyUSB0'

# Open serial connection
arduino = serial.Serial(PORT, 9600, timeout=1)

time.sleep(2)   # wait for Nano reset

print("Controls:")
print("f = forward")
print("b = backward")
print("l = left")
print("r = right")
print("s = stop")
print("q = quit")

while True:

    cmd = input("Enter command: ").lower()

    if cmd in ['f', 'b', 'l', 'r', 's']:

        arduino.write(cmd.encode())

        print(f"Sent: {cmd}")

    elif cmd == 'q':

        arduino.write(b's')

        print("Exiting...")
        break

    else:
        print("Invalid command")

arduino.close()
