import os
from rich.console import Console
console=Console()
from gai.scripts._docker_utils import _docker_push

def docker_push(pyproject_path, 
                repo_name,
                image_name
                ):
    _docker_push(
        pyproject_path=pyproject_path,
        repo_name=repo_name,
        image_name=image_name)
    
