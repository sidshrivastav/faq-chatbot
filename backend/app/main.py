"""FastAPI application entrypoint for the FAQ Knowledge Assistant."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the FastAPI application.

    Feature routers are added in later tasks. This setup task only provides a
    compilable application shell.
    """
    app = FastAPI(title="Configurable FAQ Knowledge Assistant")
    return app


app = create_app()
