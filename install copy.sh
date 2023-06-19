#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install selenium webdriver_manager

# Create config file
echo "Creating config file..."
cp config.ini.example config.ini

# Provide instructions for configuring the app
echo "Please configure the 'config.ini' file with your desired settings."

echo "Installation complete."