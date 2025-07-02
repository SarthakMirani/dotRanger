#!/bin/bash

# dotRanger: Restore script for backed-up dotfiles
# Author: Sarthak Mirani

echo "🧬 dotRanger is restoring..."

SOURCE_DIR="$(dirname "$(realpath "$0")")/../dotfiles"
TARGET_DIR="$HOME"

echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"

