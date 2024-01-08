#!/bin/bash
if [[ -f /etc/wireguard/backup.zip ]]; then
  # Архив существует, удаляем его
  rm /etc/wireguard/backup.zip
fi
mv /app/wireguard.db /etc/wireguard/wireguard.db
zip -r /etc/wireguard/backup.zip /etc/wireguard
wg-quick down wg0
wg-quick up wg0
