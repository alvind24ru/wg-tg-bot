Данное решение предназначено для оперативного развертывания WireGuard на VPS сервере используя Docker-Compose и удобного управления сервером через Telegram-Бота.

Развертывание:
1. Установка git, docker и клонирование репозитория:
```copy
sudo apt-get update && apt-get install -y git docker && cd /root && git clone https://github.com/alvind24ru/wg-tg-bot.git

2. Заходим в файл .env и задаем токен бота (можно получить у @BotFather https://t.me/BotFather), порт работы VPN сервера и доменное имя сервера(опционально)

3. Запускаем docker контейнер:
```copy cd /root/wg-tg-bot && sudo docker-compose up -d
