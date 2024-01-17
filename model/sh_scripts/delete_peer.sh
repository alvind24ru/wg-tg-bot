#!/bin/bash
ip=$1
wg-quick down wg0
cd /etc/wireguard
# cat wg0.conf > vrem.conf
# rm wg0.conf
# sed -e "/$ip/{N;N;N;d;}" -e "${/^$ip$/d}" vrem.conf > wg0.conf
# rm vrem.conf


my_variable=$(grep -n "${ip}" wg0.conf | cut -d ':' -f 1)

sed -i "$(($my_variable-2)),$my_variable d" wg0.conf
rm -rf ./configs/$ip
wg-quick up wg0
