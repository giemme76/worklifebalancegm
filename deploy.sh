#!/usr/bin/env bash
# Script di deploy per hosting cPanel.
#
# Default: smartworkingmanager.com alla radice del dominio (frontend E
# backend sullo stesso dominio, cookie di sessione same-site).
#
# Presuppone:
# - il repo clonato FUORI dalla document root pubblica, es. ~/apps/smartworkingmanager
# - il backend pubblicato via "Setup Python App" (Application URL: /api)
# - Node.js/npm disponibili nel terminale cPanel
#
# Uso: eseguire da terminale cPanel dopo ogni `git pull`, dalla root del repo.
#
#   ./deploy.sh
#
# Verifica PUBLIC_TARGET prima del primo deploy: deve essere la document root
# esatta assegnata da cPanel al dominio (cPanel > Domains > Document Root).
#
# Per rifare invece il vecchio deploy sotto giemme76.com/worklifebalancegm/
# (path dedicato, non radice), sovrascrivere le tre variabili:
#
#   PUBLIC_TARGET="$HOME/public_html/worklifebalancegm" \
#   API_BASE_URL="https://giemme76.com/worklifebalancegm/api" \
#   VITE_BASE_PATH="/worklifebalancegm/" \
#   ./deploy.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLIC_TARGET="${PUBLIC_TARGET:-$HOME/public_html}"   # cartella pubblica del frontend
API_BASE_URL="${API_BASE_URL:-https://smartworkingmanager.com/api}"
# vite.config.js legge VITE_BASE_PATH da process.env (variabile di shell),
# non da .env.production (quello alimenta solo import.meta.env lato client):
# va quindi esportata, non solo scritta su file.
export VITE_BASE_PATH="${VITE_BASE_PATH:-/}"

echo "==> Build frontend (base path: ${VITE_BASE_PATH}, API: ${API_BASE_URL})"
cd "$REPO_DIR/frontend"
npm install --no-audit --no-fund
echo "VITE_API_BASE_URL=${API_BASE_URL}" > .env.production
npm run build

echo "==> Pubblica i file statici in ${PUBLIC_TARGET}"
mkdir -p "$PUBLIC_TARGET"
# Rimuove SOLO i file generati dalla build precedente (mai l'intera cartella:
# "${PUBLIC_TARGET}/api" contiene il routing verso Passenger creato da cPanel
# per il backend e non va mai toccato da qui).
rm -rf "${PUBLIC_TARGET:?}/assets" "${PUBLIC_TARGET:?}/index.html" "${PUBLIC_TARGET:?}/og-image.png"
cp -r dist/* "$PUBLIC_TARGET"/

echo "==> Fatto."
echo "Ricorda di reinstallare le dipendenze Python se sono cambiate:"
echo "  cd $REPO_DIR/backend && pip install -r requirements.txt"
echo "e di fare Restart dell'app Python da cPanel > Setup Python App."
