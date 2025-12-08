#!/usr/bin/env bash
set -euo pipefail

# Usage: run from repo root:
#   ./video_assets/make_video.sh
#
# Produces: video_assets/launch-video/costpilot_launch.mp4
# Reads:    video_assets/input_images.txt
# Audio:    video_assets/audio/voiceover.mp3

REPO_ROOT="$(pwd)"
SCRIPT_DIR="$REPO_ROOT/video_assets"
IMG_LIST="$SCRIPT_DIR/input_images.txt"
AUDIO_FILE="$SCRIPT_DIR/audio/voiceover.mp3"
OUTPUT_DIR="$SCRIPT_DIR/launch-video"
OUTPUT_FILE="$OUTPUT_DIR/costpilot_launch.mp4"
TMP_CONCAT="$(mktemp --tmpdir="$SCRIPT_DIR" ffconcat.XXXX.txt)"

trap 'rm -f "$TMP_CONCAT"' EXIT

TARGET_W=1920
TARGET_H=1080

mkdir -p "$OUTPUT_DIR"

# Sanity checks
if [ ! -f "$IMG_LIST" ]; then
  echo "ERROR: input images list not found: $IMG_LIST"
  exit 1
fi
if [ ! -f "$AUDIO_FILE" ]; then
  echo "ERROR: audio file not found: $AUDIO_FILE"
  exit 1
fi

# Build an absolute ffmpeg concat file.
# Accepts lines like:
#   file 'video_assets/final/Hero.png'
#   duration 11
# or absolute paths.
# The ffconcat file will contain absolute paths.

# Track last 'file' we wrote and whether last non-empty line was a duration
last_file=""
last_was_duration="no"

# Clean tmp concat
: > "$TMP_CONCAT"

while IFS= read -r rawline || [ -n "$rawline" ]; do
  line="${rawline#"${rawline%%[![:space:]]*}"}"  # ltrim
  line="${line%"${line##*[![:space:]]}"}"        # rtrim

  # empty line -> passthrough
  if [ -z "$line" ]; then
    printf "\n" >> "$TMP_CONCAT"
    continue
  fi

  # If line starts with file (case sensitive)
  case "$line" in
    file\ *)
      # get the path part after 'file '
      path_part="${line#file }"
      # strip surrounding single or double quotes if present
      if [ "${path_part:0:1}" = "'" ] && [ "${path_part: -1}" = "'" ]; then
        path_inner="${path_part:1:${#path_part}-2}"
      elif [ "${path_part:0:1}" = "\"" ] && [ "${path_part: -1}" = "\"" ]; then
        path_inner="${path_part:1:${#path_part}-2}"
      else
        path_inner="$path_part"
      fi

      # If it's an absolute path, use it. Otherwise treat it relative to repo root.
      if [ "${path_inner:0:1}" = "/" ]; then
        abs_path="$path_inner"
      else
        abs_path="$REPO_ROOT/$path_inner"
      fi

      # Normalize repeated slashes (simple)
      abs_path="$(echo "$abs_path" | sed -E 's:/+:/:g')"

      if [ ! -f "$abs_path" ]; then
        echo "ERROR: referenced image missing -> $abs_path"
        echo "Check your video_assets/input_images.txt entries (they should point to files under video_assets/final/ or absolute paths)."
        rm -f "$TMP_CONCAT"
        exit 2
      fi

      printf "file '%s'\n" "$abs_path" >> "$TMP_CONCAT"
      last_file="$abs_path"
      last_was_duration="no"
      ;;
    duration\ *)
      # pass through duration lines unchanged
      printf "%s\n" "$line" >> "$TMP_CONCAT"
      last_was_duration="yes"
      ;;
    # pass through other possible ffconcat directives such as ffconcat-version
    ffconcat-version*|inpoint*|outpoint*)
      printf "%s\n" "$line" >> "$TMP_CONCAT"
      last_was_duration="no"
      ;;
    *)
      # Unknown line; pass through to avoid dropping useful directives.
      printf "%s\n" "$line" >> "$TMP_CONCAT"
      last_was_duration="no"
      ;;
  esac
done < "$IMG_LIST"

# If file ended with a duration, ffmpeg concat expects last file repeated once.
if [ "$last_was_duration" = "yes" ] && [ -n "$last_file" ]; then
  printf "file '%s'\n" "$last_file" >> "$TMP_CONCAT"
fi

# Final verification: ensure concat file has at least one file entry
if ! grep -q "^file " "$TMP_CONCAT"; then
  echo "ERROR: No 'file' entries found in constructed concat list ($TMP_CONCAT)."
  rm -f "$TMP_CONCAT"
  exit 3
fi

# Build video:
# - scale images to fit into TARGET_W x TARGET_H while preserving aspect
# - pad to exact TARGET_WxTARGET_H (centered)
# - ensure even dimensions for x264 by outputting fixed even canvas (1920x1080)
FILTER="scale='min(iw,${TARGET_W})':'min(ih,${TARGET_H})':force_original_aspect_ratio=decrease,pad=${TARGET_W}:${TARGET_H}:(ow-iw)/2:(oh-ih)/2"

echo "Rendering video to $OUTPUT_FILE ..."
ffmpeg -v warning -y \
  -f concat -safe 0 -i "$TMP_CONCAT" \
  -i "$AUDIO_FILE" \
  -vf "$FILTER" \
  -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 192k \
  -shortest \
  "$OUTPUT_FILE"

echo "DONE: $OUTPUT_FILE"
