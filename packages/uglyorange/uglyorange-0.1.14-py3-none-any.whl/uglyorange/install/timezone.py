import os
import codefast as cf
from .types import AbstractConfiger

class TimezoneConfigurator(AbstractConfiger):
    def __init__(self, timezone: str = "Asia/Shanghai"):
        self.timezone = timezone

    def config(self):
        """Configure system timezone and time synchronization"""
        try:
            # Enable and start timesyncd
            commands = [
                "systemctl enable systemd-timesyncd",
                "systemctl start systemd-timesyncd",
                f"timedatectl set-timezone {self.timezone}",
                "timedatectl set-ntp true"
            ]

            for cmd in commands:
                cf.info(f"Executing: {cmd}")
                os.system(cmd)

            # Verify the configuration
            os.system("timedatectl status")
            return True
        except Exception as e:
            cf.error(f"Failed to configure timezone: {e}")
            return False

def timezone_config(timezone: str = "Asia/Shanghai"):
    return TimezoneConfigurator(timezone).config()