#!/bin/bash

# dotRanger: Git Sync script
# Author: Sarthak Mirani

PROJECT_DIR="$(dirname "$(realpath "$0")")/.."
cd "$PROJECT_DIR" || exit 1

LOGFILE="$PROJECT_DIR/logs/dotranger.log"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [sync] $1" | tee -a "$LOGFILE"
}

if [[ "$1" == "--push" ]]; then
  log "🚀 Pushing dotfiles to remote Git repo..."
  git add .
  git commit -m "🔄 dotRanger sync: $(date '+%Y-%m-%d %H:%M:%S')" || log "ℹ️ Nothing to commit."
  git push && log "✅ Sync complete."
  exit 0
fi

if [[ "$1" == "--pull" ]]; then
  log "📥 Pulling latest dotfiles from remote Git repo..."
  git pull && log "✅ Sync complete."
  exit 0
fi

log "❌ Invalid sync option. Use --push or --pull."
exit 1