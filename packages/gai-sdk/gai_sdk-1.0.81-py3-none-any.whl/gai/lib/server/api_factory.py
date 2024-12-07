# FASTAPI
from fastapi import Depends, FastAPI
from gai.lib.server import api_dependencies

def create_app(pyproject_toml, category, gai_config):

    app=FastAPI(
        title="Gai Generators Service",
        description="""Gai Generators Service""",
        version=api_dependencies.get_app_version(pyproject_toml),
        docs_url=api_dependencies.get_swagger_url()
        )
    api_dependencies.configure_cors(app)

    # Event Handlers
    from gai.lib.server.api_event_handlers import get_startup_event, get_shutdown_event
    app.add_event_handler("startup", get_startup_event(app, category=category, pyproject_toml=pyproject_toml, gai_config=gai_config))
    app.add_event_handler("shutdown", get_shutdown_event(app))

    return app
