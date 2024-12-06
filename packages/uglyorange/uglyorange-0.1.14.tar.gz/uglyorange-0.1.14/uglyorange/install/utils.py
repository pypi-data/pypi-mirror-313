

def is_sudo_required():
    try:
        result = subprocess.run(["sudo", "-n", "true"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False
