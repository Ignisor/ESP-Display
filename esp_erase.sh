#!/bin/bash

sudo ./.env/bin/esptool.py --port /dev/ttyUSB0 erase_flash
read -p "Replug adapter or reset the board and press enter to continue..."
sudo ./.env/bin/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 $1
