#!/bin/bash

echo "Clearing files"
sudo ./.env/bin/ampy -p /dev/ttyUSB0 rmdir /

FILES=esp/*

for f in $FILES
do
    echo "Uploading $f"
    sudo ./.env/bin/ampy -p /dev/ttyUSB0 put $f
done

echo "Done. Reset the device."
