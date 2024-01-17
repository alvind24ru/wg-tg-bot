#!/bin/bash
BACKUP_FILE=$1
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Архив $BACKUP_FILE не найден."
  exit 1
fi
echo "Начало"
wg-quick down wg0 && echo "VPN отключен"
rm -rf /etc/wireguard/ && echo "Содержимое wireguard удалено"
#pkill -f "python" && echo "бот убит"
rm /app/wireguard.db && echo "удалена старая БД"
mkdir /etc/wireguard && echo "создана директория wireguard"
cd /etc/wireguard && echo "зашел в директорию"
unzip "$BACKUP_FILE" && echo "распаковка завершена"
rm "$BACKUP_FILE" && echo "удален архив"
mv /etc/wireguard/wireguard.db /app/wireguard.db && echo "бд перенесена в /app" && rm /etc/wireguard/wireguard.db
wg-quick up wg0 && echo "wg запущен"
#pkill -f /app/main.py && echo "бот перезапущен"
