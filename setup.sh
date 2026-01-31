#!/bin/bash
echo "Installing LavaScript..."
chmod +x engine.py
echo "alias lava='python $(pwd)/engine.py'" >> ~/.bashrc
source ~/.bashrc
echo "Ready! Type 'lava main.ls' to run."
