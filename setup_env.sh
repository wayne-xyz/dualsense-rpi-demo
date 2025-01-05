#!/bin/bash

# Install system dependencies
brew install hidapi libusb libarchive

# Get Homebrew prefix
BREW_PREFIX=$(brew --prefix)

# Create necessary directories
sudo mkdir -p /usr/local/lib

# Create symbolic links
sudo ln -sf ${BREW_PREFIX}/lib/libarchive.dylib /usr/local/lib/libarchive.20.dylib
sudo ln -sf ${BREW_PREFIX}/lib/libhidapi.dylib /usr/local/lib/libhidapi.dylib

# Set environment variables
export LDFLAGS="-L${BREW_PREFIX}/lib"
export CPPFLAGS="-I${BREW_PREFIX}/include"
export HIDAPI_LIBRARY_PATH="${BREW_PREFIX}/lib/libhidapi.dylib"
export DYLD_LIBRARY_PATH="${BREW_PREFIX}/lib:/usr/local/lib:$DYLD_LIBRARY_PATH"

# Install conda packages first
conda install -y -c conda-forge cython
conda install -y -c conda-forge libusb
conda install -y -c conda-forge libarchive

# Then install pip packages
pip install -r requirements.txt 