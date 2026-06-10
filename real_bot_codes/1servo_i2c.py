import time
import board
import busio
from adafruit_pca9685 import PCA9685

# ==========================
# PCA9685 Setup
# ==========================

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 50

# Equivalent to Arduino values
SERVOMIN = 100
SERVOMAX = 500

print("Enter Servo Angle (0-180)")

while True:

    try:
        angle = int(input("Angle: "))

        angle = max(0, min(180, angle))

        pulse = int(
            SERVOMIN +
            (angle / 180.0) * (SERVOMAX - SERVOMIN)
        )

        # PCA9685 uses 16-bit values (0-65535)
        duty_cycle = int((pulse / 4096.0) * 65535)

        pca.channels[5].duty_cycle = duty_cycle

        print(f"Moved Servo to {angle} degrees")

    except ValueError:
        print("Enter a valid number")
    

for ch in range(16):
    pca.channels[ch].duty_cycle = 0