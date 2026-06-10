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

SERVOMIN = 100
SERVOMAX = 500

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

def clamp(value, low, high):
    return max(low, min(high, value))

def move_servos(angle1, angle5, angle9):

    # Constrain using calibrated positions
    angle1 = clamp(angle1, LS_UP, LS_DN)
    angle5 = clamp(angle5, RS_DOWN, RS_UP)
    angle9 = clamp(angle9, FACE_RIG, FACE_LF)

    pulse1 = angle_to_pulse(angle1)
    pulse5 = angle_to_pulse(angle5)
    pulse9 = angle_to_pulse(angle9)

    duty1 = pulse_to_duty_cycle(pulse1)
    duty5 = pulse_to_duty_cycle(pulse5)
    duty9 = pulse_to_duty_cycle(pulse9)

    pca.channels[1].duty_cycle = duty1
    pca.channels[5].duty_cycle = duty5
    pca.channels[9].duty_cycle = duty9

    print(
        f"LS={angle1}°, "
        f"RS={angle5}°, "
        f"FACE={angle9}°"
    )

LS_CEN = 90
LS_UP   = LS_CEN - 40
LS_DN  = LS_CEN + 40

# Servo 2 (Right Shoulder)
RS_CEN = 80
RS_UP   = RS_CEN + 50
RS_DOWN  = RS_CEN - 70

# Servo 3 (Head)
FACE_CEN = 95
FACE_LF   = FACE_CEN + 65
FACE_RIG  = FACE_CEN - 75

t1=1
t2=0.5
t3=2

# ==========================
# Main
# ==========================

print("Multi Servo Control Started")

# Initial Position: all hands down
move_servos(LS_DN, RS_DOWN, FACE_CEN)
print("Initial Position Set")

time.sleep(t3)

# First Position- Right hand center
move_servos(LS_DN, RS_CEN, FACE_CEN)
time.sleep(t1)

# Left and right hand center
move_servos(LS_CEN, RS_CEN, FACE_CEN)
time.sleep(t1)


# face left
move_servos(LS_CEN, RS_CEN, FACE_LF)
time.sleep(t2)

# face center
move_servos(LS_CEN, RS_CEN, FACE_CEN)
time.sleep(t2)

# face right
move_servos(LS_CEN, RS_CEN, FACE_RIG)
time.sleep(t2)

# face center
move_servos(LS_CEN, RS_CEN, FACE_CEN)
time.sleep(t2)

#..........................................
# Second Position- Right hand up
move_servos(LS_CEN, RS_UP, FACE_CEN)
time.sleep(1)

# Left and right hand up
move_servos(LS_UP, RS_UP, FACE_CEN)
time.sleep(1)

# face right
move_servos(LS_UP, RS_UP, FACE_RIG)
time.sleep(t2)

# face center
move_servos(LS_UP, RS_UP, FACE_CEN)
time.sleep(t2)

# face left
move_servos(LS_UP, RS_UP, FACE_LF)
time.sleep(t2)

# face center
move_servos(LS_UP, RS_UP, FACE_CEN)
time.sleep(t2)

#..........................................
# Third Position- move forward

arduino.write(b'f')
print(f"Sent: Forward")

time.sleep(2)

arduino.write(b's')
print(f"Sent: Stop")

time.sleep(0.2)

move_servos(LS_CEN, RS_CEN, FACE_CEN)
time.sleep(t1)

#..........................................
# Fourth Position- move left

arduino.write(b'r')
print(f"Sent: Left")
time.sleep(2.2)

arduino.write(b's')
print(f"Sent: Stop")
time.sleep(0.2)

move_servos(LS_CEN, RS_CEN, FACE_RIG)
time.sleep(t1)

arduino.write(b'f')
print(f"Sent: Forward")

time.sleep(2)

arduino.write(b's')
print(f"Sent: Stop")

time.sleep(0.2)


for ch in range(16):
    pca.channels[ch].duty_cycle = 0

print("All servos disabled")
