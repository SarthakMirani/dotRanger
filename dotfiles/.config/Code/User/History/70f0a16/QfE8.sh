#!/bin/bash

# dotRanger: Backup script for selected dotfiles
# Author: Sarthak Mirani

LOGFILE="$(dirname "$0")/../logs/dotranger.log"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [backup] $1" | tee -a "$LOGFILE"
}

# Load ignore list
IGNORE_FILE="$(dirname "$0")/../.dotrangerignore"
ignored=()

if [ -f "$IGNORE_FILE" ]; then
  while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    ignored+=("$line")
  done < "$IGNORE_FILE"
fi

DRY_RUN=false

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
  # Skip ignored files
  for ignore in "${ignored[@]}"; do
    if [[ "$file" == "$ignore" ]]; then
      log "🚫 Ignored: $file"
      continue 2
    fi
  done
  
  SRC="$SOURCE_DIR/$file"
  DEST="$TARGET_DIR/$file"

  if [ -e "$SRC" ]; then
    if [ "$DRY_RUN" = true ]; then
      rsync -a --dry-run "$SRC" "$TARGET_DIR"
      log "🧪 [Dry-run] Would back up: $file"
    else
      rsync -a "$SRC" "$TARGET_DIR"
      log "📁 Backed up: $file"
    fi
  else
    log "⚠️  $file not found — skipping."
  fi
done
