import os
import subprocess
from gai.lib.common.utils import get_packaged_docker_compose_path

def docker_down():
    try:
        docker_compose_path = get_packaged_docker_compose_path()
        print("docker-compose:",docker_compose_path)
        docker_command = f"docker-compose -f {docker_compose_path} down -v --remove-orphans"
        result=subprocess.run(docker_command, shell=True, check=True, capture_output=True)
        # Print stdout and stderr for debugging
        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())
        print("Containers and associated resources have been forcefully shut down and removed.")        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")