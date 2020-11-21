#!/usr/bin/env python3

import subprocess
import time

from gpiozero import OutputDevice


ON_THRESHOLD = 60  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 41  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 30  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.


def get_temp():
    """Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as handle:
        temp_str = handle.read().strip()
        try:
            return float(temp_str) / 1000 #convert milli celsius to celsius
        except (IndexError, ValueError):
            raise RuntimeError('Could not parse temperature output.')


if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()

        time.sleep(SLEEP_INTERVAL)
