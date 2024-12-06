from .types import AbstractConfiger
import codefast as cf
import os

class SwapConfigurator(AbstractConfiger):
    def __init__(self, size: int):
        # size in GB
        self.size = size
        assert self.size > 0, "Swap size must be greater than 0"
        assert self.size <= 10, "Swap size must be less than 10 GB"

    def config(self):
        '''
        1. create swap file
        2. enable swap
        3. add swap to fstab
        '''
        os.system(
            f"fallocate -l {self.size}G /swapfile")
        os.system(f"mkswap /swapfile")
        os.system(f"chmod 600 /swapfile")
        os.system(f"swapon /swapfile")
        os.system(f"echo '/swapfile none swap sw 0 0' >> /etc/fstab")




def swap_config(size: int):
    SwapConfigurator(size).config()
