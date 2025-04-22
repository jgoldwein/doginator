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

# Run this to check that the z-axis clearances and movements are unobstructed.  Do not pay attention to the actual stated angles.

import time
import pyb

# --- PWM Setup ---
# X-axis Servo on PB8 -> Timer 4, Channel 3
servo_pin_x = pyb.Pin.board.PB8
timer_x = pyb.Timer(4, freq=50)
ch_x = timer_x.channel(3, pyb.Timer.PWM, pin=servo_pin_x)

# Z-axis Servo on PB9 -> Timer 4, Channel 4
servo_pin_z = pyb.Pin.board.PB9
timer_z = pyb.Timer(4, freq=50)
ch_z = timer_z.channel(4, pyb.Timer.PWM, pin=servo_pin_z)

# --- Helper: Convert Angle to Pulse Width (µs) ---
def angle_to_us(angle):
    min_us = 1000  # ~1ms for 0°
    max_us = 2000  # ~2ms for 180°
    return int(min_us + (max_us - min_us) * angle / 180)

# --- Set Servo Positions ---
def set_x(angle):
    pulse = angle_to_us(angle)
    ch_x.pulse_width(pulse)
    print("X-axis set to", angle, "degrees | Pulse:", pulse)

def set_z(angle):
    pulse = angle_to_us(angle)
    ch_z.pulse_width(pulse)
    print("Z-axis set to", angle, "degrees | Pulse:", pulse)

# --- Initial Setup ---
print("Setting X-axis to 80° (fixed CENTER for DOGINATOR)...")
set_z(90)
time.sleep(1)
set_x(80)
time.sleep(1)

print("Sweeping Z-axis from 0° to 180°...")

# --- Sweep Z-axis ---
for z_angle in range(0, 180,5):
    set_z(z_angle)
    time.sleep(1)

print("Done. Returning to 90°")
set_z(90)
