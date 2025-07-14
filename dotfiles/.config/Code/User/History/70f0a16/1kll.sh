#!/bin/bash

# dotRanger: Backup script for selected dotfiles
# Author: Sarthak Mirani

LOGFILE="$(dirname "$0")/../logs/dotranger.log"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [backup] $1" | tee -a "$LOGFILE"
}

DRY_RUN=flase

if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=true
  log "🧪 Dry-run mode activated. No files will actually be copied."
fi

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
    if [ "$DRY_RUN" = true ]; then
      rsync -a --dry-run "$SRC" "$TARGET_DIR"
      log "🧪 [Dry-run] Would back up: $file

    log "📁 Backed up: $file"
  else
    log "⚠️  $file not found — skipping."
  fi
done
