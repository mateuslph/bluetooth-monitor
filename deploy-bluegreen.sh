#!/bin/bash

set -e

APP_DIR="/root/bluetooth"
NGINX_CONF="$APP_DIR/nginx/nginx.conf"

cd $APP_DIR

NEW_VERSION=$1

echo "Nova versão: $NEW_VERSION"

# Descobrir ativo atual
if grep -q "backend_blue" $NGINX_CONF; then
    ACTIVE="blue"
    TARGET="green"
else
    ACTIVE="green"
    TARGET="blue"
fi

echo "Ativo: $ACTIVE → Novo: $TARGET"

# Atualizar imagem
docker compose pull backend_$TARGET

# Subir novo container
docker compose up -d backend_$TARGET

echo "Aguardando subir..."
sleep 8

# Healthcheck
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health || true)

if [ "$STATUS" != "200" ]; then
    echo "Falha no novo deploy"
    exit 1
fi

echo "Novo container OK"

# Trocar Nginx
if [ "$TARGET" == "green" ]; then
    sed -i 's/backend_blue/backend_green/g' $NGINX_CONF
else
    sed -i 's/backend_green/backend_blue/g' $NGINX_CONF
fi

docker exec bt_nginx nginx -s reload

echo "Switch realizado!"

# Derrubar antigo
docker stop backend_$ACTIVE || true

echo "Antigo removido"

echo "Deploy sem downtime concluído!"