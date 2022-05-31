#!/bin/bash

ampy --baud 115200 --port /dev/ttyUSB${2} put ${1}
ampy --baud 115200 --port /dev/ttyUSB${2} ls
ampy --baud 115200 --port /dev/ttyUSB${2} reset

