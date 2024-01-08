#!/bin/bash
file_path="/etc/wireguard/wg0.conf"
if [ -e "$file_path" ]; then
    wg-quick up wg0 && wg-quick up wg0 && wg-quick up wg0
else
    wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
    touch /etc/wireguard/wg0.conf
    echo "[Interface]
    Address = 10.0.0.1/24
    PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
    ListenPort = 51822
    PrivateKey = $(cat /etc/wireguard/privatekey)" > /etc/wireguard/wg0.conf
fi