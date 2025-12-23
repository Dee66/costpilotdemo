#!/bin/bash
# Build the complete video: regenerate segments and concatenate

echo "Regenerating video segments..."
./regenerate_segments.sh

echo "Building final video..."
./video_assets/make_video.sh

echo "Video build complete!"