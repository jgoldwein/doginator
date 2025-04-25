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

import socket
import network
import time

# Wi-Fi Connection (already verified)
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect("ssid", "password")

while not nic.isconnected():
    time.sleep(1)
    print("Connecting...")

print("Connected!", nic.ifconfig())

# Start TCP Server (Telnet-like)
addr = socket.getaddrinfo('0.0.0.0', 23)[0][-1]  # Telnet port 23
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Telnet-like server listening on:', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    cl.send(b"Welcome to Nicla Vision\r\n")
    cl.send(b"Type 'spray <zone>', 'stop', or 'exit'\r\n")
    while True:
        try:
            data = cl.recv(64)
            if not data:
                break
            try:
                cmd = data.decode('utf-8').strip()  # Use 'utf-8' with error handling
            except UnicodeError:
                cl.send(b"Unicode decode error. Try again.\r\n")
                continue

            print(f"Received: {cmd}")
            if cmd.startswith('spray'):
                try:
                    _, zone = cmd.split()
                    zone = int(zone)
                    cl.send(f"Spraying zone {zone}\r\n".encode())
                    # call spray(zone) here
                except:
                    cl.send(b"Invalid spray command. Use: spray <zone>\r\n")
            elif cmd == 'stop':
                cl.send(b"Stopping spray\r\n")
                # call stop_spray() here
            elif cmd == 'exit':
                cl.send(b"Goodbye\r\n")
                break
            else:
                cl.send(b"Unknown command\r\n")
        except Exception as e:
            cl.send(b"Error occurred.\r\n")
            print(f"Error: {e}")
            break
    cl.close()
    print("Client disconnected")
