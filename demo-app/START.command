#!/bin/bash
# When launched from Finder, PATH may not include node/npm — fix it
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
[ -s "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh"
if ! command -v npm &>/dev/null; then
  echo "npm not found. Run this from Terminal instead:"
  echo "  cd $(dirname "$0")"
  echo "  npm run dev"
  echo ""
  read -p "Press Enter to close."
  exit 1
fi

cd "$(dirname "$0")"
echo "Starting Dragonfruit demo..."
echo "Browser will open in a few seconds. Keep this window open."
echo ""

# Open browser after delay (in background); run server in foreground so it stays alive
( sleep 6 && open "http://localhost:3000" ) &
npm run dev
