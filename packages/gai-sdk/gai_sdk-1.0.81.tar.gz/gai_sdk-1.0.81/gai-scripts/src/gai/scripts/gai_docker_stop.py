import os
from rich.console import Console
console=Console()
from gai.scripts._docker_utils import _docker_stop

def docker_stop(component):
    console.print(f"Stopping {component}...")
    _docker_stop(component_name=component)
    
