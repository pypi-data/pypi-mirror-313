# raspi_tools/defaults.py

import os
import time

class BoardLED:
    LED_PATH = '/sys/class/leds/led0'

    @staticmethod
    def on():
        """Turn on the Raspberry Pi board LED."""
        with open(os.path.join(BoardLED.LED_PATH, 'brightness'), 'w') as f:
            f.write('1')

    @staticmethod
    def off():
        """Turn off the Raspberry Pi board LED."""
        with open(os.path.join(BoardLED.LED_PATH, 'brightness'), 'w') as f:
            f.write('0')

    @staticmethod
    def flash(times=5, interval=0.5):
        """Flash the Raspberry Pi board LED a specified number of times."""
        for _ in range(times):
            BoardLED.on()
            time.sleep(interval)
            BoardLED.off()
            time.sleep(interval)
