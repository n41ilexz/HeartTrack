from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
import numpy as np
import time
import threading
from collections import deque
import RPi.GPIO as GPIO
import modules.global_variables as gv
RB_PIN = 13
LB_PIN = 6

def show_graph():
    try:
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        height = device.height

        BUFFER_LENGTH = 64
        X_SCALE = 2
        display_buffer = deque(maxlen=BUFFER_LENGTH)
        
        running = True


        def normalize(value, min_val, max_val, display_height):
            if max_val == min_val:
                return display_height // 2
            return int((value - min_val) / (max_val - min_val) * (display_height - 1))

        def update_display():
            nonlocal running
            while running:
                if len(display_buffer) < 5:
                    time.sleep(0.1)
                    continue
                current_min = min(display_buffer)
                current_max = max(display_buffer)
                if current_max - current_min < 1e-9:
                    current_max = current_min + 1e-9
                normalized = [normalize(v, current_min, current_max, height) for v in display_buffer]
                with canvas(device) as draw:
                    for i in range(1, len(normalized)):
                        x0 = (i-1) * X_SCALE
                        y0 = height - normalized[i-1]
                        x1 = i * X_SCALE
                        y1 = height - normalized[i]
                        draw.line((x0, y0, x1, y1), fill="white")
                    draw.text((5, 5), "ECG", fill="white")
                time.sleep(0.03)

        threading.Thread(target=update_display, daemon=True).start()
        while running:
            sample = gv.ECG_SIGNAL
            display_buffer.append(sample)
            time.sleep(0.01)
    except Exception:
        pass
graph = threading.Thread(target=show_graph, daemon=True)
graph.start()