import click
import toml,subprocess
from rich.console import Console
console=Console()
import os,sys
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
workspace_folder = os.path.join(here, "..")

from devops_utils import (_get_version, 
                         _docker_build, 
                        _docker_push, 
                        _docker_stop,
                        _docker_idle,
                        _docker_ssh,
                        _publish_package,
                        _cmd)

@click.group()
def cli():
    """Example CLI for managing components."""
    pass

# VERSION ------------------------------------------------------------------------------------------------------------------------------------------------

# @cli.command()
# @click.argument('component')
# def get_version(component):

#     """Show the version of a specified component."""
#     pyproject_path = f"{workspace_folder}/{component}-svr/pyproject.toml"
#     try:
#         version=_get_version(pyproject_path=pyproject_path)
#         click.echo(f'Version of {component}: {version}')
#     except Exception as e:
#         click.echo(f"Error reading {component} version: {e}")
#         return None
    
# PACKAGE ------------------------------------------------------------------------------------------------------------------------------------------------

# @cli.command()
# @click.argument('env')
# @click.argument('proj_path')
# def publish_package(env, proj_path):
#     try:
#         _publish_package(env, proj_path)
#     except subprocess.CalledProcessError as e:
#         print("An error occurred while publishing package:", e)

# DOCKER_BUILD
# @cli.command()
# @click.argument('component')
# @click.option('--no-cache', is_flag=True, help='Build without cache.')
# def docker_build(component,no_cache):
#     pyproject_path = f"{workspace_folder}/{component}-svr/pyproject.toml"
#     version=_get_version(pyproject_path=pyproject_path)
#     _docker_build(
#         component_name=component, 
#         version=version,
#         dockercontext_path=f"{workspace_folder}/{component}-svr",
#         no_cache=no_cache)
#     print("Docker image built and tagged successfully.")

### DOCKER_PUSH
# @cli.command()
# @click.argument('component')
# def docker_push(component):
#     pyproject_path = f"{workspace_folder}/{component}-svr/pyproject.toml"
#     version = _get_version(pyproject_path=pyproject_path)
#     _docker_push(component,version)
#     print("Docker image pushed successfully.")

### DOCKER_RUN
# def _docker_run_ttt(component):
#     if component != "gai-ttt":
#         print("Wrong component found.")
#         return
#     cmd=f"""docker run -d \
#         -e DEFAULT_GENERATOR="ttt-exllamav2-mistral7b" \
#         -e SWAGGER_URL="/doc" \
#         -e SELF_TEST="true" \
#         --gpus all \
#         -v ~/.gai:/app/.gai \
#         -p 12031:12031 \
#         --name gai-ttt \
#         --network gai-sandbox \
#         kakkoii1337/gai-ttt:latest"""
#     _cmd(cmd)
def _docker_run_rag(component):
    if component != "gai-rag":
        print("Wrong component found.")
        return
    cmd=f"""docker run -d \
        -e DEFAULT_GENERATOR="rag-instructor-sentencepiece" \
        -e SWAGGER_URL="/doc" \
        -e DEVICE="cuda" \
        -e SELF_TEST="true" \
        --gpus all \
        -v ~/.gai:/app/.gai \
        -p 12036:12036 \
        --name gai-rag \
        --network gai-sandbox \
        kakkoii1337/gai-rag:latest"""
    _cmd(cmd)
def _docker_run_tti(component):
    if component != "gai-tti":
        print("Wrong component found.")
        return
    cmd=f"""docker run -d \
        -e CLI_ARGS="--listen --api --xformers --medvram" \
        --gpus all \
        -v ~/.gai/models/Stable-diffusion:/stable-diffusion-webui/models/Stable-diffusion \
        -v ~/.gai/models/VAE:/stable-diffusion-webui/models/VAE \
        -p 12035:12035 \
        --name gai-tti \
        --network gai-sandbox \
        kakkoii1337/gai-tti:latest"""
    _cmd(cmd)

def _docker_run_itt(component):
    if component != "gai-itt":
        print("Wrong component found.")
        return
    cmd=f"""docker run -d \
        -e DEFAULT_GENERATOR="itt-llava-v1.6-vicuna-7b" \
        -e SWAGGER_URL="/doc" \
        --gpus all \
        -v ~/.gai:/root/.gai \
        -p 12034:12034 \
        --name gai-itt \
        --network gai-sandbox \
        kakkoii1337/gai-itt:latest"""
    _cmd(cmd)
@cli.command()
@click.argument('component')
def docker_run(component):
    console.print(f"docker run [italic yellow]{component}[/]")
    if component == "gai-ttt":
        _docker_stop(component)
        _docker_run_ttt(component)
    elif component == "gai-rag":
        _docker_stop(component)
        _docker_run_rag(component)
    elif component == "gai-tti":
        _docker_stop(component)
        _docker_run_tti(component)
    elif component == "gai-itt":
        _docker_stop(component)
        _docker_run_itt(component)
    else:
        console.print(f"[red]Component not found. The script for {component} is not written yet.[/]")
        return
    print(f"Docker container {component} started.")


### DOCKER_STOP
@cli.command()
@click.argument('component')
def docker_stop(component):
    _docker_stop(component)

### DOCKER_IDLE
@cli.command()
@click.argument('component')
def docker_idle(component):
    _docker_idle(component)

### DOCKER_SSH
@cli.command()
@click.argument('component')
def docker_ssh(component):
    _docker_ssh(component)

if __name__ == '__main__':
    import os
    cli()
