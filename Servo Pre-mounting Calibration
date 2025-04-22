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

# Sets the X and Z servos to 90 degrees for use prior to mounting to the mounting bracket.

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

# --- Helper: Standard 90° Pulse Width ---
def set_servo_to_90(ch):
    duty_90 = 1500  # Standard 90° = 1.5ms = 1500µs
    ch.pulse_width(duty_90)

# --- Center Both Servos ---
print("Centering both servos to 90° (1500µs pulse)...")
set_servo_to_90(ch_x)
set_servo_to_90(ch_z)

print("Servos centered. Please re-mount manually.")
# Hold for inspection
while True:
    time.sleep(1)
