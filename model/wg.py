import os
import subprocess
from model.db.db import db

class WireGuard:
    def __init__(self): ...

    @staticmethod
    def get_config_text(username) -> str:
        with open(f'/etc/wireguard/configs/{username}/{username}.conf', 'r') as f:
            return f.read()

    @staticmethod
    def get_config_file(username):
        with open(f'/etc/wireguard/configs/{username}/{username}.conf', 'rb') as f:
            return f.read()

    @staticmethod
    def get_config_qrcode(username):
        with open(f'/etc/wireguard/configs/{username}/{username}-qr.png', 'rb') as f:
            return f.read()

    @staticmethod
    def add_peer(username: str, ip: str) -> None:
        subprocess.run(
            [f'bash ./model/sh_scripts/add_new_peer.sh {username} {ip}'], shell=True)

    @staticmethod
    def restart():
        subprocess.run(
            ['bash', './sh_scripts/restart_wg_server.sh'], shell=True)

    @staticmethod
    def delete_peer(ip, username):
        subprocess.run(
            [f'bash ./model/sh_scripts/delete_peer.sh {ip} {username}'], shell=True)

    @staticmethod
    def start_wg_server():
        subprocess.run(
            ['bash /app/model/sh_scripts/start_server.sh'], shell=True)

    @staticmethod
    def create_backup():
        subprocess.run(['bash ./model/sh_scripts/backup.sh'], shell=True)

    @staticmethod
    def get_all_statistics():
        result = subprocess.run(['wg'], stdout=subprocess.PIPE, text=True)
        return result.stdout

    @staticmethod
    def get_statistics(ip: int):
        result = subprocess.run(
            [f'wg | grep {ip}/32 -A 2'], shell=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.split('\n')

    @staticmethod
    def restore_config(file_path):
        subprocess.run(
            [f'bash ./model/sh_scripts/restore.sh {file_path}'], shell=True)
        db.reload_session()


wg = WireGuard()
