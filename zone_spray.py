# ------------------------------------------------------------------------------
# Doginator Project
# Copyright (c) 2025 Joel Goldwein
# All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
# ------------------------------------------------------------------------------

# spray function test with valve control
import time
import math
import pyb
import random

# --- USER CONFIGURABLE PARAMETERS ---
N_ITERATIONS = 1     # Number of outward + inward spiral cycles
SPIRAL_RADIUS = 5    # Spiral radius (degrees), recommended 2 - 10
JIGGLE_RANGE = 1.0   # Jiggle range in degrees
TURNS = 3            # Number of spiral turns per cycle
STEPS_PER_TURN = 72  # Smoothness of the spiral
DELAY = 0.03         # Delay between steps (seconds)

# --- Zone Selection (0 to 63) ---
ZONE_SELECTED = 7  # Example: Zone 8 (top-left, second row)

# --- Servo Angle Ranges ---
X_MIN = 60     # Minimum X servo angle
X_MAX = 120    # Maximum X servo angle
Z_MIN = 60     # Minimum Z servo angle
Z_MAX = 120    # Maximum Z servo angle

# --- Calculate X_CENTER and Z_CENTER from ZONE_SELECTED ---
GRID_SIZE = 8  # 8x8 grid
zone_row = ZONE_SELECTED // GRID_SIZE
zone_col = ZONE_SELECTED % GRID_SIZE

# Inverted Z-axis mapping (zone_row 0 = Z_MAX, zone_row 7 = Z_MIN)
Z_CENTER = Z_MAX - ((Z_MAX - Z_MIN) / (GRID_SIZE - 1)) * zone_row

# Inverted X-axis mapping (zone_col 0 = X_MAX, zone_col 7 = X_MIN)
X_CENTER = X_MAX - ((X_MAX - X_MIN) / (GRID_SIZE - 1)) * zone_col

print(f"Selected Zone: {ZONE_SELECTED} mapped to X: {X_CENTER:.2f}°, Z: {Z_CENTER:.2f}°")

# --- Buzzer Setup on A0 (PA0) --- (INACTIVE)
buzzer_pin = pyb.Pin(pyb.Pin.board.A0, pyb.Pin.OUT_PP)
buzzer_pin.low()  # Ensure buzzer is OFF initially

# --- PWM Setup for Servos (Updated to PA9 and PA10 using Timer 1) ---
# X-axis Servo on PA10 -> Timer 1, Channel 3
servo_pin_x = pyb.Pin.board.PA10
timer_x = pyb.Timer(1, freq=50)
ch_x = timer_x.channel(3, pyb.Timer.PWM, pin=servo_pin_x)

# Z-axis Servo on PA9 -> Timer 1, Channel 2
servo_pin_z = pyb.Pin.board.PA9
timer_z = pyb.Timer(1, freq=50)
ch_z = timer_z.channel(2, pyb.Timer.PWM, pin=servo_pin_z)

# --- Valve Control Setup ---
valve_pin = pyb.Pin(pyb.Pin.board.PB8, pyb.Pin.OUT_PP)
valve_pin.low()  # Ensure valve is initially closed

def buzzer_on():
    buzzer_pin.high()
    print("Buzzer ON (inactive)")

def buzzer_off():
    buzzer_pin.low()
    print("Buzzer OFF (inactive)")

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

# --- Valve Control Functions ---
def open_valve():
    valve_pin.high()
    print("Valve OPENED")

def close_valve():
    valve_pin.low()
    print("Valve CLOSED")

# --- Spiral Pattern with Jiggle ---
def spray_spiral(center_x, center_z, max_radius, turns, steps_per_turn, delay, inward=False, jiggle_range=1.0):
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
def spray(center_x=X_CENTER, center_z=Z_CENTER, iterations=N_ITERATIONS, max_radius=SPIRAL_RADIUS,
          turns=TURNS, steps_per_turn=STEPS_PER_TURN, delay=DELAY, jiggle_range=JIGGLE_RANGE):
    """
    Perform a jiggle spiral spray pattern using user-configurable parameters.
    """
    move_turret(center_x, center_z)
    time.sleep(1)

    open_valve()  # Start spraying

    for cycle in range(iterations):
        print(f"Cycle {cycle + 1} - OUTWARD Spiral")
        spray_spiral(center_x, center_z, max_radius, turns, steps_per_turn, delay, inward=False, jiggle_range=jiggle_range)

        print(f"Cycle {cycle + 1} - INWARD Spiral")
        spray_spiral(center_x, center_z, max_radius, turns, steps_per_turn, delay, inward=True, jiggle_range=jiggle_range)

    close_valve()  # Stop spraying

    move_turret(center_x, center_z)
    print(f"Returned to center X: {center_x:.2f}°, Z: {center_z:.2f}°")

# --- Execute Using User Parameters ---
if __name__ == "__main__":
    spray()  # Automatically uses the ZONE_SELECTED-mapped X_CENTER, Z_CENTER
