#!/bin/bash

# dotRanger: Restore script for backed-up dotfiles
# Author: Sarthak Mirani

LOGFILE="$(dirname "$0")/../logs/dotranger.log"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [restore] $1" | tee -a "$LOGFILE"
}

DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=true
  log "🧪 Dry-run mode activated. No files will actually be restored."
fi

if [[ "$1" == "--list" ]]; then
  log "📄 Listing available dotfiles to restore:"
  echo

  DOTFILES_DIR="$(dirname "$(realpath "$0")")/../dotfiles"

  if [ -d "$DOTFILES_DIR" ]; then
    for f in "$DOTFILES_DIR"/.*; do
      # Skip . and ..
      [[ "$(basename "$f")" == "." || "$(basename "$f")" == ".." ]] && continue
      echo "• $(basename "$f")"
    done
  else
    log "❌ Dotfiles directory not found."
  fi

  exit 0
fi




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
    if [ "$DRY_RUN" = true ]; then
      rsync -a --dry-run "$SRC" "$TARGET_DIR"
      log "🧪 [Dry-run] Would restore: $file"
    else
      rsync -a "$SRC" "$TARGET_DIR"
      log "📁 Restored: $file"
    fi
  else
    log "⚠️  Backup for $file not found — skipping."
  fi
done
