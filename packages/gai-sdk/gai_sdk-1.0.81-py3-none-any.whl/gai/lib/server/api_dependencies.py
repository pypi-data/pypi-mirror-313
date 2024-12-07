from fastapi import FastAPI
import os
from dotenv import load_dotenv
load_dotenv()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
import asyncio
from gai.lib.common.utils import this_dir
from gai.lib.common.color import red, green

def get_app_version(pyproject_toml):
    import toml
    with open(pyproject_toml) as f:
        pyproject = toml.load(f)

    if not pyproject.get("project"):
        return pyproject["tool"]["poetry"]["version"]
    return pyproject["project"]["version"]

def get_sdk_version():
    import importlib.metadata
    try:
        version = importlib.metadata.version("gai-sdk")
        green(f"gai-sdk {version} is installed")
    except importlib.metadata.PackageNotFoundError:
        red("gai-sdk not installed.")
        raise

# This tells fastapi which path to host the swagger ui page.
def get_swagger_url():
    swagger_url=None
    if "SWAGGER_URL" in os.environ and os.environ["SWAGGER_URL"]:
        swagger_url=os.environ["SWAGGER_URL"]
        logger.info(f"swagger={swagger_url}")
    else:
        logger.info("swagger_url=disabled.")
    return swagger_url

def configure_cors(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware
    allowed_origins_str = "*"
    if "CORS_ALLOWED" in os.environ:
        allowed_origins_str = os.environ["CORS_ALLOWED"]    # from .env
    allowed_origins = allowed_origins_str.split(",")  # split the string into a list
    logger.info(f"allow_origins={allowed_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_semaphore():
    use_semaphore = os.getenv("USE_SEMAPHORE", "False").lower() == "true"
    semaphore = None
    if use_semaphore:
        logger.info("Using semaphore")
        import asyncio
        semaphore = asyncio.Semaphore(2)
    return semaphore

async def acquire_semaphore(semaphore):
    while semaphore:
        try:
            await asyncio.wait_for(semaphore.acquire(), timeout=0.1)
            break
        except asyncio.TimeoutError:
            logger.warn("_streaming: Server is busy")
            await asyncio.sleep(1)

def release_semaphore(semaphore):
    if semaphore:
        semaphore.release()
        logger.debug("_streaming: Server is available")
    