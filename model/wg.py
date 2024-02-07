import os
import subprocess
from model.db.db import db

class WireGuard:
    def __init__(self): ...

    @staticmethod
    def get_config_text(ip) -> str:
        with open(f'/etc/wireguard/configs/{ip}/{ip}.conf', 'r') as f:
            return f.read()

    @staticmethod
    def get_config_file(ip):
        with open(f'/etc/wireguard/configs/{ip}/{ip}.conf', 'rb') as f:
            return f.read()

    @staticmethod
    def get_config_qrcode(ip):
        with open(f'/etc/wireguard/configs/{ip}/{ip}-qr.png', 'rb') as f:
            return f.read()

    @staticmethod
    def add_peer(ip: str) -> None:
        subprocess.run(
            [f'bash /app/model/sh_scripts/add_new_peer.sh {ip} $DOMAIN'], shell=True)

    @staticmethod
    def restart():
        subprocess.run(
            ['bash /app/model/sh_scripts/restart_wg_server.sh'], shell=True)

    @staticmethod
    def delete_peer(ip):
        subprocess.run(
            [f'bash /app/model/sh_scripts/delete_peer.sh {ip}'], shell=True)

    @staticmethod
    def start_wg_server():
        subprocess.run(
            ['bash /app/model/sh_scripts/start_server.sh'], shell=True)

    @staticmethod
    def create_backup():
        subprocess.run(['bash /app/model/sh_scripts/backup.sh'], shell=True)

    @staticmethod
    def get_all_statistics():
        result = subprocess.run(['wg'], stdout=subprocess.PIPE, text=True)
        return result.stdout

    @staticmethod
    def get_statistics(ip: int) -> list:
        result = subprocess.run(
            [f'wg | grep {ip}/32 -A 2'], shell=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.split('/n')

    @staticmethod
    def restore_config(file_path):
        subprocess.run(
            [f'bash /app/model/sh_scripts/restore.sh {file_path}'], shell=True)
        db.reload_session()


def main():
wg = WireGuard()
