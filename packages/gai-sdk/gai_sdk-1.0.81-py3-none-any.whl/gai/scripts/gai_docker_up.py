import os
import subprocess
from gai.lib.common.utils import get_packaged_docker_compose_path

def docker_up():
    try:
        docker_compose_path = get_packaged_docker_compose_path()
        print("docker-compose:",docker_compose_path)
        docker_command = f"docker-compose -f {docker_compose_path} up -d --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")