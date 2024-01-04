import subprocess


class WireGuard:
    def __init__(self): ...

    def get_config_file(self, path): ...

    @staticmethod
    def get_config_text(file_name) -> str:
        return 'config text'
        with open(f'./etc/wireguard/configs/{file_name}', 'r') as f:
            return f.read()

    @staticmethod
    def add_peer(username: str, ip: str) -> None:
        print('peer added')
        # subprocess.run((['bash', './sh_scripts/add_new_peer.sh', f'{username}', f'{ip}']), shell=True)

    @staticmethod
    def restart():
        subprocess.run(['bash', './sh_scripts/restart_wg_server.sh'], shell=True)

    def delete_peer(self): ...


wg = WireGuard()
