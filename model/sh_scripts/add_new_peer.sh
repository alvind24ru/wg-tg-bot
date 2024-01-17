# Надо 2 аргумента, первый это название конфига, второй это ip адрес
NAME=$1
IP=$2
mkdir /etc/wireguard/configs
mkdir /etc/wireguard/configs/"$NAME"
wg genkey | tee /etc/wireguard/configs/"$NAME"/"${NAME}"_privatekey | wg pubkey | tee /etc/wireguard/configs/"$NAME"/"${NAME}"_publickey

EXTERNAL_IP=$(curl ifconfig.me)
PRIVATE=$(cat /etc/wireguard/configs/"$NAME"/"${NAME}"_privatekey)
PUBLIC=$(cat /etc/wireguard/configs/"$NAME"/"${NAME}"_publickey)
PUBLIC_SERVER=$(cat /etc/wireguard/publickey)
echo "
[Peer]
PublicKey = $PUBLIC
AllowedIPs = $IP/32" >> /etc/wireguard/wg0.conf

echo "
[Interface]
PrivateKey = $PRIVATE
Address = $IP/32
DNS = 8.8.8.8

[Peer]
PublicKey = $PUBLIC_SERVER
Endpoint = $EXTERNAL_IP:$VPN_PORT
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20" > /etc/wireguard/configs/"$NAME"/"$NAME".conf
wg-quick down wg0
wg-quick up wg0


qrencode -o /etc/wireguard/configs/"$NAME"/"${NAME}"-qr.png -t PNG < /etc/wireguard/configs/"$NAME"/"$NAME".conf
