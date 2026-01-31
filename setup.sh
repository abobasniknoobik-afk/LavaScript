#!/bin/bash
echo "Setting up LavaScript..."
chmod +x engine.py
echo "alias lava='python $(pwd)/engine.py'" >> ~/.bashrc
source ~/.bashrc
echo "LavaScript installed! Use 'lava file.ls' to run."
