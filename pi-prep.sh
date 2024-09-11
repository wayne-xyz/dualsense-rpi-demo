#!/bin/bash
# Check USB devices and internet connection

# Function to check USB devices
check_usb() {
    echo "Checking connected USB devices..."
    lsusb
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

check_python() {
    echo "Checking Python version..."
    python3 --version
}

check_kernel() {
    echo "Checking kernel version..."
    uname -r
}

# add rule to let user access the PS5 controller without root
add_rule() {
    echo "Adding rule to let user access the PS5 controller without root..."
    sudo cp 70-ps5-controller.rules /etc/udev/rules.d
    sudo udevadm control --reload-rules
    sudo udevadm trigger
}

check_install_libhidapi() {
    echo "Checking if libhidapi is installed..."
    dpkg -l | grep libhidapi
    # if not installed, install it
    if [ $? -ne 0 ]; then
        echo "libhidapi is not installed. Installing..."
        sudo apt-get install libhidapi-dev
    fi
}


check_install_pydualsense() {
    echo "Checking if pydualsense is installed..."
    if ! dpkg -l | grep -q python3-pydualsense; then
        echo "pydualsense is not installed. Installing..."
        sudo apt update
        sudo apt install -y python3-pydualsense
    else
        echo "pydualsense is already installed."
    fi
}



# Execute all
check_usb
check_internet
check_python
check_kernel
add_rule
check_install_libhidapi
check_install_pydualsense
