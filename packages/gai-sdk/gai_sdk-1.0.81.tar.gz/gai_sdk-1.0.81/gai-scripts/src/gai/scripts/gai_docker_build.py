import os
from rich.console import Console
console=Console()
from gai.scripts._docker_utils import _docker_build

def docker_build(
    pyproject_path,
    repo_name='kakkoii1337',
    image_name=None,                
    dockerfile_path=None, 
    dockercontext_path=None, 
    no_cache=False):

    _docker_build(
        pyproject_path=pyproject_path,
        repo_name=repo_name,
        image_name=image_name, 
        dockerfile_path=dockerfile_path,
        dockercontext_path=dockercontext_path,
        no_cache=no_cache)
