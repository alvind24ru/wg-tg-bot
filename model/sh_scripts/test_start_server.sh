#!/bin/bash
apt update -y && apt full-upgrade -y && apt install wireguard -y
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
wg-quick up wg0
systemctl enable wg-quick@wg0
wg-quick down wg0 && systemctl start wg-quick@wg0
