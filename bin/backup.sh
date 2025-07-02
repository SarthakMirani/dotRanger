#!/bin/bash

# dotRanger: Backup script for selected dotfiles
# Author: Sarthak Mirani

echo "📦 dotRanger is starting..."

SOURCE_DIR="$HOME"
TARGET_DIR="$(dirname "$(realpath "$0")")/../dotfiles"

# List of dotfiles to back up
dotfiles=(
  ".bash_logout"
  ".config"
  ".gtkrc-2.0"
  ".icons"
  ".local"
  ".profile"
  ".themes"
)

for file in "${dotfiles[@]}"; do
  SRC="$SOURCE_DIR/$file"
  DEST="$TARGET_DIR/$file"

  if [ -e "$SRC" ]; then
    rsync -a "$SRC" "$TARGET_DIR"
    echo "📁 Backed up: $file"
  else
    echo "⚠️  $file not found — skipping."
  fi
done
