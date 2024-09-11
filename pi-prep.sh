#!/bin/bash
# Check USB devices and internet connection

# Function to check USB devices
check_usb() {
    echo "Checking connected USB devices..."
    lsusb
    echo "USB device list saved to usb_devices.txt"
    lsusb > usb_devices.txt
}

# Function to check internet connection
check_internet() {
    PING_TARGET="8.8.8.8"
    PING_COUNT=4
    echo "Checking internet connection by pinging $PING_TARGET..."
    if ping -c $PING_COUNT $PING_TARGET > /dev/null 2>&1; then
        echo "Internet connection is working."
    else
        echo "No internet connection detected."
    fi
}

# Execute both functions
check_usb
check_internet