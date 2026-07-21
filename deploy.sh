#!/usr/bin/env bash
# Script di deploy per hosting cPanel (giemme76.com/worklifebalancegm).
#
# Presuppone:
# - il repo clonato FUORI dalla document root pubblica, es. ~/apps/worklifebalancegm
# - il backend pubblicato via "Setup Python App" (Application URL: /worklifebalancegm/api)
# - Node.js/npm disponibili nel terminale cPanel
#
# Uso: eseguire da terminale cPanel dopo ogni `git pull`, dalla root del repo.
#
#   ./deploy.sh
#
# Personalizza le due variabili sotto in base al tuo account.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLIC_TARGET="$HOME/public_html/worklifebalancegm"   # cartella pubblica del frontend
API_BASE_URL="https://giemme76.com/worklifebalancegm/api"

echo "==> Build frontend"
cd "$REPO_DIR/frontend"
npm install --no-audit --no-fund
echo "VITE_API_BASE_URL=${API_BASE_URL}" > .env.production
npm run build

echo "==> Pubblica i file statici in ${PUBLIC_TARGET}"
mkdir -p "$PUBLIC_TARGET"
# Rimuove SOLO i file generati dalla build precedente (mai l'intera cartella:
# "${PUBLIC_TARGET}/api" contiene il routing verso Passenger creato da cPanel
# per il backend e non va mai toccato da qui).
rm -rf "${PUBLIC_TARGET:?}/assets" "${PUBLIC_TARGET:?}/index.html"
cp -r dist/* "$PUBLIC_TARGET"/

echo "==> Fatto."
echo "Ricorda di reinstallare le dipendenze Python se sono cambiate:"
echo "  cd $REPO_DIR/backend && pip install -r requirements.txt"
echo "e di fare Restart dell'app Python da cPanel > Setup Python App."
