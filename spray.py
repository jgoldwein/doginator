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

# spray function test sans valve control

import time
import math
import pyb
import random

# --- USER CONFIGURABLE PARAMETERS ---
X_CENTER = 90        # X-axis center position (0-180 degrees)
Z_CENTER = 90        # Z-axis center position (0-180 degrees)
N_ITERATIONS = 3     # Number of outward + inward spiral cycles
SPIRAL_RADIUS = 5    # Spiral radius (degrees), recommended 2 - 10

# --- PWM Setup for Servos ---
# X-axis Servo on PB8 -> Timer 4, Channel 3
servo_pin_x = pyb.Pin.board.PB8
timer_x = pyb.Timer(4, freq=50)
ch_x = timer_x.channel(3, pyb.Timer.PWM, pin=servo_pin_x)

# Z-axis Servo on PB9 -> Timer 4, Channel 4
servo_pin_z = pyb.Pin.board.PB9
timer_z = pyb.Timer(4, freq=50)
ch_z = timer_z.channel(4, pyb.Timer.PWM, pin=servo_pin_z)

# --- Servo Control Helper Functions ---
def angle_to_us(angle):
    min_us = 700
    max_us = 2500
    us = min_us + (max_us - min_us) * (angle / 180.0)
    return int(us)

def move_servo(channel, angle):
    us = angle_to_us(angle)
    channel.pulse_width(us)

def move_turret(x_angle, z_angle):
    move_servo(ch_x, x_angle)
    move_servo(ch_z, z_angle)
    print(f"Moved turret to X: {x_angle:.2f}°, Z: {z_angle:.2f}°")

# --- Spiral Pattern with Jiggle ---
def spray_spiral(center_x, center_z, max_radius=5, turns=3, steps_per_turn=72, delay=0.03, inward=False, jiggle_range=1.0):
    total_steps = turns * steps_per_turn
    radius_increment = max_radius / total_steps

    step_range = range(total_steps)
    if inward:
        step_range = reversed(step_range)

    for i in step_range:
        angle = 2 * math.pi * i / steps_per_turn
        radius = radius_increment * i

        x_offset = radius * math.cos(angle)
        z_offset = radius * math.sin(angle)

        jiggle_x = random.uniform(-jiggle_range, jiggle_range)
        jiggle_z = random.uniform(-jiggle_range, jiggle_range)

        target_x = center_x + x_offset + jiggle_x
        target_z = center_z + z_offset + jiggle_z

        target_x = max(0, min(180, target_x))
        target_z = max(0, min(180, target_z))

        move_turret(target_x, target_z)
        time.sleep(delay)

# --- Main Spray Function ---
def spray(center_x=90, center_z=90, iterations=2, max_radius=5, turns=3, steps_per_turn=72, delay=0.03, jiggle_range=1.0):
    move_turret(center_x, center_z)
    time.sleep(1)

    for cycle in range(iterations):
        print(f"Cycle {cycle + 1} - OUTWARD Spiral")
        spray_spiral(center_x, center_z, max_radius, turns, steps_per_turn, delay, inward=False, jiggle_range=jiggle_range)

        print(f"Cycle {cycle + 1} - INWARD Spiral")
        spray_spiral(center_x, center_z, max_radius, turns, steps_per_turn, delay, inward=True, jiggle_range=jiggle_range)

    move_turret(center_x, center_z)
    print(f"Returned to center X: {center_x:.2f}°, Z: {center_z:.2f}°")

# --- Execute with Top Parameters ---
if __name__ == "__main__":
    spray(center_x=X_CENTER, center_z=Z_CENTER, iterations=N_ITERATIONS, max_radius=SPIRAL_RADIUS)
