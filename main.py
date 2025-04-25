# ------------------------------------------------------------------------------
# Doginator Project
# Copyright (c) 2025 Joel Goldwein
# All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
# ------------------------------------------------------------------------------
#
# This script auto-starts on Nicla Vision boot and launches the Doginator system.
# It initializes the dog detection and spray control logic defined in doginator_main.py.
# The system monitors zones for dog presence and triggers spraying based on behavior.
#
# ------------------------------------------------------------------------------

import doginator_main  # Main control logic

doginator_main.run()  # Start system at boot
