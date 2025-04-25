# ------------------------------------------------------------------------------
# Doginator Project
# Copyright (c) 2025 Joel Goldwein
# All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
# ------------------------------------------------------------------------------
#
# This script provides the spray(zone) function used by the Doginator system.
# It converts zone numbers (0-63) to X/Z servo angles, moves the turret to the
# zone, opens the valve, performs a spray pattern, then closes the valve.
#
# ------------------------------------------------------------------------------

import time
import pyb

# --- Servo Angle Ranges ---
X_MIN = 60
X_MAX = 120
Z_MIN = 60
Z_MAX = 120
GRID_SIZE = 8  # 8x8 zones

# --- PWM Setup for Servos ---
servo_pin_x = pyb.Pin.board.PA10
timer_x = pyb.Timer(1, freq=50)
ch_x = timer_x.channel(3, pyb.Timer.PWM, pin=servo_pin_x)

servo_pin_z = pyb.Pin.board.PA9
timer_z = pyb.Timer(1, freq=50)
ch_z = timer_z.channel(2, pyb.Timer.PWM, pin=servo_pin_z)

# --- Valve Control ---
valve_pin = pyb.Pin(pyb.Pin.board.PB8, pyb.Pin.OUT_PP)
valve_pin.low()  # Ensure valve is off

# --- Servo Helpers ---
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
    print(f"Moved to X: {x_angle:.2f}°, Z: {z_angle:.2f}°")

# --- Valve Control ---
def open_valve():
    valve_pin.high()
    print("Valve OPENED")

def close_valve():
    valve_pin.low()
    print("Valve CLOSED")

# --- Convert zone number (0-63) to X/Z angles ---
def zone_to_angles(zone):
    row = zone // GRID_SIZE
    col = zone % GRID_SIZE

    # Inverted mapping if needed
    z_angle = Z_MAX - ((Z_MAX - Z_MIN) / (GRID_SIZE - 1)) * row
    x_angle = X_MAX - ((X_MAX - X_MIN) / (GRID_SIZE - 1)) * col

    return x_angle, z_angle

# --- Spray Function ---
def spray(zone):
    x_angle, z_angle = zone_to_angles(zone)
    print(f"Spraying zone {zone} -> X: {x_angle:.2f}, Z: {z_angle:.2f}")

    move_turret(x_angle, z_angle)
    time.sleep(1)  # Allow turret to settle

    open_valve()
    time.sleep(2)  # Spray duration (adjust as needed)
    close_valve()

    print(f"Completed spray for zone {zone}")
