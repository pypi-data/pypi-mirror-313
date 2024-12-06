import os
import httpx
from pydantic import BaseModel, model_serializer
from getpass import getpass
import codefast as cf

TARGET_PATH = "/opt/system_info_server/.env"
API_URL = "aHR0cHM6Ly93d3cudHRvby5sb2wvdnBzL2Vudgo="

class Env(BaseModel):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    @model_serializer
    def set_model(self):
        return f"SUPABASE_URL={self.SUPABASE_URL}\nSUPABASE_KEY={self.SUPABASE_KEY}"

def get_env():
    password = getpass("Input password(hint: p...7..): ")
    endpoint = cf.b64decode(API_URL)
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(endpoint, json={"password": password})
            js = resp.json()
            return Env(**js["env"])
    except httpx.HTTPStatusError as e:
        cf.error(f"Failed to get environment variables: {e}")
        exit(1)
    except KeyError as e:
        cf.error("Invalid password")
        exit(1)

def write_env(env: Env):
    os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
    try:
        with open(TARGET_PATH, "w") as f:
            f.write(env.model_dump())
    except PermissionError as e:
        cf.error("Permission denied to write to target path")
        exit(1)

def install_monitor(interface: str = "eth0", start_date: int = 23):
    cf.info(f"Installing monitor with interface {interface} and start date {start_date}")
    env = get_env()
    write_env(env)
    cmd = f'curl -L ttoo.lol/v.sh | bash -s -- --interface={interface} --start_date={start_date}'
    os.system(cmd)