# ------------------------------------------------------------------------------
# Doginator Project
# Copyright (c) 2025 Joel Goldwein
# All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
#
# You may share this file with attribution, but you may not use it for commercial purposes,
# modify it, or distribute modified versions without express permission.
# ------------------------------------------------------------------------------

# Run this to check that the x-axis clearances and movements are unobstructed.  Do not pay attention to the actual stated angles.

import time
import pyb

# --- Setup X-axis Servo PWM ---
servo_pin_x = pyb.Pin.board.PB8  # X-axis servo on PB8
timer_x = pyb.Timer(4, freq=50)
ch_x = timer_x.channel(3, pyb.Timer.PWM, pin=servo_pin_x)

# --- Calibrated Range ---
min_us = 700
center_us = 1500
max_us = 2500

# --- Helper: Convert Calibrated Angle (0°-180°) to Pulse Width ---
def angle_to_us(angle):
    return int(min_us + (max_us - min_us) * angle / 180)

# --- Set X-axis Servo to Angle ---
def set_x(angle):
    pulse = angle_to_us(angle)
    ch_x.pulse_width(pulse)
    print("X-axis set to", angle, "degrees | Pulse:", pulse, "µs")

# --- Move to Center and Sweep ---
print("Setting X-axis to calibrated center (90°)...")
set_x(90)
time.sleep(2)

print("Sweeping X-axis from 10° to 170° (Calibrated)...")
for x_angle in range(170, 9, -10):
    set_x(x_angle)
    time.sleep(1.5)

print("Back to calibrated center (90°)...")
set_x(90)
