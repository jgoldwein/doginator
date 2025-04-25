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

# detects do and indicates grid where do is located

import sensor, time, ml, uos, gc
import pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.skip_frames(time=2000)

# Load model
try:
    net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64 * 1024)))
except Exception as e:
    raise Exception('Failed to load trained.tflite: ' + str(e))

# Load labels
try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load labels.txt: ' + str(e))

led = pyb.LED(2)
GRID_SIZE = 8
CELL_SIZE = 30

def classify_tile(tile_img):
    preds = net.predict([tile_img])[0].flatten().tolist()
    return list(zip(labels, preds))

def get_dog_centroid(img, global_conf):
    dog_grid = []
    for gy in range(GRID_SIZE):
        for gx in range(GRID_SIZE):
            x = gx * CELL_SIZE
            y = gy * CELL_SIZE
            sub = img.copy(roi=(x, y, CELL_SIZE, CELL_SIZE))
            preds = classify_tile(sub)
            dog_conf = 0
            for label, conf in preds:
                if label == "dog":
                    dog_conf = conf
                    break
            if dog_conf >= 0.4:  # lowered threshold
                dog_grid.append((gx, gy))

    if not dog_grid:
        if global_conf >= 0.6:
            return (4, 4)  # assume center
        return None

    avg_x = sum([g[0] for g in dog_grid]) / len(dog_grid)
    avg_y = sum([g[1] for g in dog_grid]) / len(dog_grid)
    return (avg_x, avg_y)

def describe_location(x, y):
    horizontal = "left" if x < 3 else "center" if x < 5 else "right"
    vertical = "top" if y < 3 else "center" if y < 5 else "bottom"
    return f"{vertical}-{horizontal}"

clock = time.clock()
while True:
    clock.tick()
    img = sensor.snapshot()
    preds = net.predict([img])[0].flatten().tolist()
    dog_conf = 0
    for i, label in enumerate(labels):
        if label == "dog":
            dog_conf = preds[i]
            break

    if dog_conf > 0.5:
        print("DOG DETECTED (conf = %.2f)" % dog_conf)
        led.on()
        grid_loc = get_dog_centroid(img, dog_conf)
        if grid_loc:
            print("DOG DETECTED in grid at:", describe_location(*grid_loc), "(grid coords: %.1f, %.1f)" % grid_loc)
        else:
            print("DOG DETECTED but no location in grid.")
    else:
        led.off()
        print("No dog detected.")
