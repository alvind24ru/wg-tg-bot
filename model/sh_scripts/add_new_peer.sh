# Надо 2 аргумента, первый это название конфига, второй это ip адрес
NAME=$1
IP=$2
mkdir /etc/wireguard/configs
mkdir /etc/wireguard/configs/"$NAME"
wg genkey | tee /etc/wireguard/configs/"$NAME"/"${NAME}"_privatekey | wg pubkey | tee /etc/wireguard/configs/"$NAME"/"${NAME}"_publickey

PRIVATE=$(cat /etc/wireguard/configs/"$NAME"/"${NAME}"_privatekey)
PUBLIC=$(cat /etc/wireguard/configs/"$NAME"/"${NAME}"_publickey)
echo "[Peer]
PublicKey = $PUBLIC
AllowedIPs = ${IP}/32" >> /etc/wireguard/wg0.conf

echo "[Interface]
PrivateKey = $PRIVATE
Address = ${IP}/32
DNS = 8.8.8.8

[Peer]
PublicKey = /r0IPyXJLSgcxfsdyYFBZJlLmnOYBQ0OslqU6ucmbBM=
Endpoint = 31.172.70.114:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20" > /etc/wireguard/configs/"$NAME"/"$NAME".conf

qrencode -o /etc/wireguard/configs/"$NAME"/"${NAME}"-qr.png -t PNG < /etc/wireguard/configs/"$NAME"/"$NAME".conf
