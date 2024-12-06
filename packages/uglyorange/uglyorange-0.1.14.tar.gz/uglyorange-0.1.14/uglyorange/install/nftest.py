import os

def nftest():
    os.system("docker run --rm --net=host lmc999/regioncheck")
