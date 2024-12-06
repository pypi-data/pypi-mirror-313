import os


def endlessh_config():
    # docker run -d --name endlessh -p 22:22 signalout/endlessh
    os.system("docker run -d --name endlessh -p 22:22 signalout/endlessh")
