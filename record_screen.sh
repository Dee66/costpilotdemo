#!/bin/bash

# Start virtual display
export DISPLAY=:99

# Start Xvfb
Xvfb :99 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 2

# Open Chrome with the page
google-chrome --no-sandbox --disable-dev-shm-usage --window-size=1920,1080 --app=http://localhost:8080 &

# Wait for Chrome to load
sleep 5

# Start recording with ffmpeg
ffmpeg -f x11grab -video_size 1920x1080 -i :99 -c:v libx264 -r 30 -t 9.5 ./video_assets/final/DemoTerminal_screen.mp4

# Kill background processes
pkill -f google-chrome
pkill -f Xvfb