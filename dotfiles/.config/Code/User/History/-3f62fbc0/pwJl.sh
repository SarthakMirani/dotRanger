#!/bin/bash

# dotRanger: Restore script for backed-up dotfiles
# Author: Sarthak Mirani

LOGFILE="$(dirname "$0")/../logs/dotranger.log"

echo "🧬 dotRanger is restoring..."

SOURCE_DIR="$(dirname "$(realpath "$0")")/../dotfiles"
TARGET_DIR="$HOME"

echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"

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
    echo "🔄 Restored: $file"
  else
    echo "⚠️  Backup for $file not found — skipping."
  fi
done
