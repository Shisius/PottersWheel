#!/bin/bash

esptool.py --port /dev/ttyUSB${1} erase_flash

esptool.py --port /dev/ttyUSB${1} --baud 460800 write_flash --flash_size=detect 0 esp_upython.bin


