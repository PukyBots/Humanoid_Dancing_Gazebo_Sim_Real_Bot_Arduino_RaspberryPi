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

# ==========================
# Main
# ==========================

print("Multi Servo Control Started")

# Initial Position
move_servos(90, 90, 70)
print("Initial Position Set")

time.sleep(2)

# Second Position
move_servos(70, 120, 150)
print("Second Position Set")

time.sleep(2)

# Back to Initial
move_servos(90, 90, 70)
print("Returned to Initial Position")

# Optional cleanup
# pca.deinit()