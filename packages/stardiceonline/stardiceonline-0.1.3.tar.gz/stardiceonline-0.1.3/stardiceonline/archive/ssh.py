import ssh_agent_setup
import subprocess
from stardiceonline.tools.config import config
import socket

def is_tunnel_alive(port):
    try:
        # Try to connect to the tunnel's local port
        with socket.create_connection(("localhost", port), timeout=2) as sock:
            pass
        return True
    except (socket.error, socket.timeout):
        return False  # Tunnel is not responding, might be down


def ssh_command(command):
    ssh_agent_setup.setup()
    if not config['ssh.proxy']:
        return subprocess.check_output(['ssh', f'{config["ssh.user"]}@{config["ssh.host"]}'] + command)
    else:
        return subprocess.check_output(['ssh', '-J', f'{config["ssh.proxyuser"]}@{config["ssh.proxy"]}', f'{config["ssh.user"]}@{config["ssh.host"]}'] + command)

def rsync(source, dest):
    ssh_agent_setup.setup()
    if not config['ssh.proxy']:
        return subprocess.check_call(['rsync', '-av', f'{config["ssh.user"]}@{config["ssh.host"]}:{source}', f'{dest}'])
    else:
        return subprocess.check_call(['rsync', '-av', '-e', f'ssh -J {config["ssh.proxyuser"]}@{config["ssh.proxy"]}', f'{config["ssh.user"]}@{config["ssh.host"]}:{source}', f'{dest}'])

def ssh_tunnel(port, target):
    ssh_agent_setup.setup()
    if not is_tunnel_alive(port):
        print("Tunnel seems to be down. Attempting to restart...")
        # Terminate existing tunnel process if any (this might need more sophisticated PID management)
        subprocess.call(['pkill', '-f', f'ssh.*-L{port}:{target}:{port}'])
        if not config['ssh.proxy']:
            return subprocess.check_call(['ssh', f'{config["ssh.user"]}@{config["ssh.host"]}', f'-L{port}:{target}:{port}', '-N', '-f'])
        else:
            return subprocess.check_call(['ssh', '-J', f'{config["ssh.proxyuser"]}@{config["ssh.proxy"]}', f'{config["ssh.user"]}@{config["ssh.host"]}', f'-L{port}:{target}:{port}', '-N', '-f'])
    
if __name__ == '__main__':
    #print(ssh_command(['ls', '/data/stardiceot1']))
    print(ssh_tunnel(9009))
