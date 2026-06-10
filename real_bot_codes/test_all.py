import time
import board
import busio
from adafruit_pca9685 import PCA9685
import serial

# Change this if needed
PORT = '/dev/ttyUSB0'
arduino = serial.Serial(PORT, 9600, timeout=1)
time.sleep(2)   # wait for Nano reset

# ==========================
# PCA9685 Setup
# ==========================

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 50

# ==========================
# Servo Parameters
# ==========================

SERVOMIN = 150
SERVOMAX = 600

# Servo angle limits
CH1_MIN = 10
CH1_MAX = 150

CH5_MIN = 20
CH5_MAX = 160

CH9_MIN = 0
CH9_MAX = 140

# ==========================
# Helper Functions
# ==========================

def angle_to_pulse(angle):
    return int(
        SERVOMIN +
        (angle / 180.0) * (SERVOMAX - SERVOMIN)
    )

def pulse_to_duty_cycle(pulse):
    return int((pulse / 4096.0) * 65535)

def move_servos(angle1, angle5, angle9):

    # Constrain angles
    angle1 = max(CH1_MIN, min(CH1_MAX, angle1))
    angle5 = max(CH5_MIN, min(CH5_MAX, angle5))
    angle9 = max(CH9_MIN, min(CH9_MAX, angle9))

    # Convert to PCA9685 pulse values
    pulse1 = angle_to_pulse(angle1)
    pulse5 = angle_to_pulse(angle5)
    pulse9 = angle_to_pulse(angle9)

    # Convert to 16-bit duty cycles
    duty1 = pulse_to_duty_cycle(pulse1)
    duty5 = pulse_to_duty_cycle(pulse5)
    duty9 = pulse_to_duty_cycle(pulse9)

    # Move servos
    pca.channels[1].duty_cycle = duty1
    pca.channels[5].duty_cycle = duty5
    pca.channels[9].duty_cycle = duty9

    print(
        f"CH1={angle1}°, "
        f"CH5={angle5}°, "
        f"CH9={angle9}°"
    )

# ==========================
# Main
# ==========================

print("Multi Servo Control Started")

# Initial Position
move_servos(90, 90, 90)
print("Initial Position Set")

time.sleep(2)

arduino.write(b'f')
print(f"Sent: Forward")

time.sleep(2)

arduino.write(b's')
print(f"Sent: Stop")

time.sleep(2)

# Second Position
move_servos(70, 120, 130)
print("Second Position Set")

time.sleep(2)

# Back to Initial
move_servos(90, 90, 90)
print("Returned to Initial Position")

# Optional cleanup
# pca.deinit()