import os


def trojan_config(domain: str, password: str):
    cmd = f'curl -L ttoo.lol/trojan.sh | bash -s -- -domain {domain} -password {password}'
    print(cmd)
    os.system(cmd)
