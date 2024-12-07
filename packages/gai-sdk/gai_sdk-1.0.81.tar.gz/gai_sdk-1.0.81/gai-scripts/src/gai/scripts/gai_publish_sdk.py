import os
from rich.console import Console
console=Console()
from gai.scripts._scripts_utils import _publish_package
import subprocess

def publish_sdk(proj_path):
    try:
        console.print(f"[yellow] publishing from project path {proj_path}[/]")
        _publish_package(proj_path)
    except subprocess.CalledProcessError as e:
        print("An error occurred while publishing package:", e)