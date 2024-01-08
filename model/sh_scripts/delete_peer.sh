#!/bin/bash
ip=$1
name=$2
my_variable=$(grep -n "10.0.0.${ip}" /etc/wireguard/wg0.conf | cut -d ':' -f 1)
sed -i "$(($my_variable-2)),$my_variable d" /etc/wireguard/wg0.conf
rm -rf /etc/wireguard/"$(name)"
wg-quick down wg0 && wg-quick up wg0
