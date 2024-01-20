FROM ubuntu:latest

WORKDIR /app

COPY . /app

# COPY ./wireguard /etc/wireguard

ENV DEBIAN_FRONTEND=noninteractive

ENV LANG C.UTF-8
ENV VPN_PORT=${VPN_PORT}
ENV DOMAIN=${DOMAIN}
ENV API_TOKEN=${API_TOKEN}
# Установка зависимостей
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y wireguard iproute2 iptables zip unzip qrencode python3 python3-pip curl\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf \
    && pip install --no-cache-dir -r requirements.txt



EXPOSE ${VPN_PORT}

# Команда по умолчанию для запуска вашего приложения
# CMD ["tail", "-f", "/dev/null"]
CMD ["python3", "main.py"]
