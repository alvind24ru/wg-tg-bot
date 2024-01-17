#!/bin/bash
rm /etc/wireguard/backup.zip
cp /app/wireguard.db /etc/wireguard/wireguard.db
cd /etc/wireguard
zip -r backup.zip .
rm /etc/wireguard/wireguard.db
wg-quick down wg0
wg-quick up wg0
