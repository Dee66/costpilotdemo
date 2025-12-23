#!/bin/bash
# Regenerate video segments from PNG screenshots or trim existing MP4s

REPO_ROOT="$(pwd)"
FINAL_DIR="$REPO_ROOT/video_assets/final"
SEGMENTS_DIR="$FINAL_DIR/video_segments"

mkdir -p "$SEGMENTS_DIR"

# Function to create or trim segment
create_segment() {
    local input_file="$1"
    local output_file="$2"
    local duration="$3"

    if [ -f "$input_file" ]; then
        echo "Processing $input_file to $output_file (duration: ${duration}s)"
        if [[ "$input_file" == *.png ]]; then
            # Convert PNG to MP4 with duration
            ffmpeg -y -loop 1 -i "$input_file" \
                -vf "scale='min(iw,1920)':'min(ih,1080)':force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
                -c:v libx264 -profile:v baseline -level 3.0 -t "$duration" -pix_fmt yuv420p -r 30 \
                "$output_file"
        elif [[ "$input_file" == *.mp4 ]]; then
            # Get current duration
            current_duration=$(ffprobe -v quiet -print_format json -show_format "$input_file" | grep -o '"duration": "[^"]*"' | cut -d'"' -f4 | cut -d'.' -f1)
            if [[ "$current_duration" != "$duration" ]]; then
                # Trim to temp file then move
                temp_file="${output_file}.tmp.mp4"
                ffmpeg -y -i "$input_file" -t "$duration" -c copy "$temp_file" && mv "$temp_file" "$output_file"
            else
                echo "Duration already matches, skipping trim for $input_file"
            fi
        fi
    else
        echo "Warning: $input_file not found, skipping"
    fi
}

# Parse input_images.txt and process each file with its duration
IMG_LIST="$REPO_ROOT/video_assets/input_images.txt"

current_file=""
while IFS= read -r line; do
    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')  # trim
    if [[ $line == file\ * ]]; then
        current_file=$(echo "$line" | sed "s/file '//;s/'$//")
        duration="6.0"  # default
    elif [[ $line == duration\ * ]]; then
        duration=$(echo "$line" | cut -d' ' -f2)
        # Now process the file
        input_file="$REPO_ROOT/$current_file"
        if [[ "$current_file" == *.png ]]; then
            base_name=$(basename "$current_file" .png)
            output_file="$SEGMENTS_DIR/${base_name}.mp4"
        else
            output_file="$input_file"  # trim in place for MP4
        fi
        create_segment "$input_file" "$output_file" "$duration"
        current_file=""
    fi
done < "$IMG_LIST"

# Process any remaining file with default duration (only PNGs)
if [[ -n "$current_file" ]]; then
    input_file="$REPO_ROOT/$current_file"
    if [[ "$current_file" == *.png ]]; then
        base_name=$(basename "$current_file" .png)
        output_file="$SEGMENTS_DIR/${base_name}.mp4"
        create_segment "$input_file" "$output_file" "6.0"
    fi
fi

echo "All segments processed. Run ./video_assets/make_video.sh to rebuild the video."