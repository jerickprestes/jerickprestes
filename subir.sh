#!/usr/bin/env bash
# Sobe as alterações do site para o GitHub.
# Uso:  ./subir.sh "mensagem do commit"      (a mensagem é opcional)
set -e
cd "$(dirname "$0")"

MSG="${1:-Atualiza site $(date '+%d/%m/%Y %H:%M')}"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

git add -A
if git diff --cached --quiet; then
  echo "Nada para subir: nenhuma alteração desde o último commit."
  exit 0
fi

git commit -m "$MSG"
git push origin "$BRANCH"
echo "Pronto: alterações enviadas para a branch '$BRANCH'."
