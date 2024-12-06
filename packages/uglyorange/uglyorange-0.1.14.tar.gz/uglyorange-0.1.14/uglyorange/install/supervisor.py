import codefast as cf
import os
from .types import AbstractConfiger

DEFAULT_CONFIG = """[unix_http_server]
file=/tmp/supervisor.sock

[supervisord]
logfile=/tmp/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/tmp/supervisord.pid
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock

[include]
files = /etc/supervisor/conf.d/*.conf
"""


class SupervisorConfiger(AbstractConfiger):
    def __init__(self):
        self.config_dir = "/etc/supervisor"
        self.config_file = f"{self.config_dir}/supervisord.conf"

    def create_default_config(self):
        cf.shell(f"mkdir -p {self.config_dir}/conf.d", print_str=True)

        with open(self.config_file, "w") as f:
            f.write(DEFAULT_CONFIG)

        cf.shell('supervisord', print_str=True)

    def create_hello_world_config(self):
        supervisor_conf = """[program:hello_world]
command=bash -c 'while true; do echo "Hello World $(date)"; sleep 36000; done'
autostart=true
autorestart=true
"""
        with open(f"{self.config_dir}/conf.d/hello_world.conf", "w") as f:
            f.write(supervisor_conf)

    def config(self):
        self.create_default_config()
        self.create_hello_world_config()
        commands = [
            'supervisorctl reread',
            'supervisorctl update',
            'supervisorctl start hello_world'
        ]
        for command in commands:
            os.system(command)


def supervisor_config():
    SupervisorConfiger().config()
