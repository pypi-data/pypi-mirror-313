#!/bin/env python3
from pathlib import Path
import json
import sys,os
from openai import OpenAI
from rich.console import Console

console=Console()

from gai.lib.common.utils import this_dir
here = this_dir(__file__)

def app_dir():
    with open(Path("~/.gairc").expanduser(), "r") as file:
        rc=file.read()
        jsoned = json.loads(rc)
        return Path(jsoned["app_dir"]).expanduser()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Gai CLI Tool')
    parser.add_argument('command', choices=['init', 'pull', 'news', 'search','docker','chat','publish'], help='Command to run')
    parser.add_argument('-f', '--force', action='store_true', help='Force initialization')
    parser.add_argument('extra_args', nargs='*', help='Additional arguments for commands')
    parser.add_argument("--repo-name", default="kakkoii1337", help="Repository name for Docker image.")
    parser.add_argument("--image-name", help="Base name for Docker image, which is required.")
    parser.add_argument("--dockerfile-path", default="./Dockerfile", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--dockercontext-path", default=".", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--no-cache", action="store_true", help="Do not use cache when building the image.")

    args = parser.parse_args()

    if args.command == "init":
        from gai.scripts.gai_init import init
        print("Initializing...by force" if args.force else "Initializing...")
        init(force=args.force)
    elif args.command == "publish":
        if args.extra_args:
            if args.extra_args[0] == "sdk":
                from gai.scripts.gai_publish_sdk import publish_sdk
                publish_sdk(args.extra_args[1])
    elif args.command == "pull":
        if args.extra_args:
            from gai.scripts.gai_pull import pull
            pull(console, args.extra_args[0])
        else:
            console.print("[red]Model name not provided[/]")
    elif args.command == "docker":
        if args.extra_args:
            # gai docker up
            if args.extra_args[0] == "up":
                from gai.scripts.gai_docker_up import docker_up
                docker_up()
            # gai docker down
            elif args.extra_args[0] == "down":
                from gai.scripts.gai_docker_down import docker_down
                docker_down()
            # gai docker build (pyproject_path) [repo_name="kakkoii1337"] [image_name=None] [dockerfile_path"../Dockerfile"] [dockercontext_path=".."] [no_cache=False]
            # gai docker build (pyproject_path) (dockerfile_path) [image_name=None] [no_cache=False]
            elif args.extra_args[0] == "build":
                from gai.scripts.gai_docker_build import docker_build
                docker_build(
                    pyproject_path=args.extra_args[1],
                    repo_name=args.repo_name,
                    image_name=args.image_name,
                    dockerfile_path=args.dockerfile_path,
                    dockercontext_path=args.dockercontext_path,
                    no_cache=args.no_cache
                    )
            # gai docker build (pyproject_path)
            elif args.extra_args[0] == "push":
                from gai.scripts.gai_docker_push import docker_push
                docker_push(
                    pyproject_path=args.extra_args[1],
                    repo_name=args.repo_name,
                    image_name=args.image_name)
            elif args.extra_args[0] == "stop":
                from gai.scripts.gai_docker_stop import docker_stop
                docker_stop(
                    component=args.extra_args[1]
                    )
            else:
                console.print("[red]Invalid docker command[/]")
    elif args.command == "news":
        from gai.scripts.gai_news import news
        if args.extra_args:
            news(category=args.extra_args[0])
        else:
            news()
    elif args.command == "search":
        from gai.scripts.gai_search import search
        if args.extra_args:
            search(args.extra_args[0],5)
        else:
            console.print("[red]Search term not provided[/]")
    elif args.command == "chat":
        from gai.scripts.gai_chat import chat
        if args.extra_args:
            chat(args.extra_args[0])
        else:
            console.print("[red]Chat content not provided[/]")

if __name__ == "__main__":
    main()
