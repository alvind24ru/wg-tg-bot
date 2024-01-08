FROM ubuntu:latest

WORKDIR /app

COPY . /app

COPY ./wireguard /etc/wireguard

ENV DEBIAN_FRONTEND=noninteractive

ENV LANG C.UTF-8
# Установка зависимостей
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y wireguard iproute2 iptables zip unzip qrencode python3 python3-pip\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf \
    && pip install --no-cache-dir -r requirements.txt


#     && ip link add dev wg0 type wireguard \
#     && ip address add dev wg0 10.0.0.1/24 \
#     && wg-quick up wg0 \
#     && wg-quick down wg0 \
#     && wg-quick up wg0
#     #&& systemctl enable wg-quick@wg0 \
#     #&& systemctl start wg-quick@wg0 \

# RUN pip install --no-cache-dir -r requirements.txt

# Открытие порта 51820
EXPOSE 51822

# Команда по умолчанию для запуска вашего приложения
# CMD ["tail", "-f", "/dev/null"]
CMD ["python3", "main.py"]
