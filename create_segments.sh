#!/bin/bash
set -e

FILTER="scale='min(iw,1920)':'min(ih,1080)':force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"

# Array of image duration
declare -A segments=(
    ["Hero.png"]="10"
    ["HeroStats.png"]="6"
    ["TerminalCommands.png"]="8"
    ["Findings.png"]="6"
    ["FindingOne.png"]="6"
    ["FindingTwo.png"]="5"
    ["CostTrendAnalysis.png"]="6"
    ["AutoFixSuggestions.png"]="6"
    ["InfrastructureImpact.png"]="7"
    ["Footer.png"]="6"
    ["ROICalculator.png"]="9"
)

for img in "${!segments[@]}"; do
    dur="${segments[$img]}"
    out="video_assets/final/video_segments/${img%.png}.mp4"
    echo "Creating $out with duration $dur"
    ffmpeg -y -loop 1 -i "video_assets/final/$img" -vf "$FILTER" -c:v libx264 -profile:v baseline -level 3.0 -t "$dur" -pix_fmt yuv420p -r 30 "$out"
done
