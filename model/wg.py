import subprocess


class WireGuard:
    def __init__(self): ...


    @staticmethod
    def get_config_text(username) -> str:
        # return 'config text'
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
        # print('peer added')
        subprocess.run([f'bash ./model/sh_scripts/add_new_peer.sh {username} {ip}'], shell=True)

    @staticmethod
    def restart():
        subprocess.run(['bash', './sh_scripts/restart_wg_server.sh'], shell=True)

    def delete_peer(self): ...


wg = WireGuard()
