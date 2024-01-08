#!/bin/bash
BACKUP_FILE=$1
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Архив $BACKUP_FILE не найден."
  exit 1
fi
rm -rf /etc/wireguard/
rm /app/wireguard.db
cd /etc/wireguard || exit 1
unzip -j "$BACKUP_FILE"
mv ./wireguard.db /app/wireguard.db
wg-quick down wg0 && wg-quick up wg0

