import asyncio
import shlex
from typing import Optional

import typer
from typer import Typer

from .log import logger
from .starter import Runner, Service

cli = Typer()


@cli.command(
    help=(
        "Run multiple services at once. "
        "Set DEBUG environment variable to 1 for more verbose output when running."
    )
)
def main(
    backend: bool = typer.Option(
        default=False,
        help="Enable backend service",
    ),
    backend_cmd: str = typer.Option(
        default="poetry run invoke serve",
        help="Command to start backend service",
    ),
    backend_dir: str = typer.Option(
        default="backend",
        help="Working directory for the backend",
    ),
    backend_port: Optional[int] = typer.Option(
        default=None,
        help="Port number that backend is running at if port is used",
    ),
    backend_socket: str = typer.Option(
        default="/run/nginx/uvicorn.sock",
        help="UNIX socket path that backend is running at if socket is used",
    ),
    frontend: bool = typer.Option(
        default=False,
        help="Enable frontend service",
    ),
    frontend_port: Optional[int] = typer.Option(
        default=3000,
        help="Port number that frontend is running at",
    ),
    frontend_cmd: str = typer.Option(
        default="pnpm run start",
        help="Command to start frontend service",
    ),
    frontend_dir: str = typer.Option(
        default="frontend",
        help="Working directory for the frontend",
    ),
    nginx: bool = typer.Option(
        default=False,
        help="Enable nginx",
    ),
    nginx_cmd: str = typer.Option(
        default='nginx -g "daemon off;"',
        help="Command to start Nginx",
    ),
    service_wait_time: float = typer.Option(
        default=3.0,
        help="How long to wait for a service to be up an running (sec)",
    ),
    praga: bool = typer.Option(
        default=False,
        help="Enable praga",
    ),
    praga_cmd: str = typer.Option(
        default="praga --config=/etc/praga.yaml",
        help="Command to start praga",
    ),
    praga_port: Optional[int] = typer.Option(
        default=None,
        help="Port number that praga is running at if port is used",
    ),
    praga_socket: str = typer.Option(
        default="/run/nginx/praga.sock",
        help="UNIX socket path that praga is running at if socket is used",
    ),
):
    if not any([backend, frontend, nginx, praga]):
        logger.error("At least one service must be enabled")
        raise typer.Exit(1)

    backend_service = None
    if backend:
        backend_service = Service(
            cmd=shlex.split(backend_cmd),
            cwd=backend_dir,
            port=backend_port,
            socket=backend_socket,
            timeout=service_wait_time,
        )

    frontend_service = None
    if frontend:
        frontend_service = Service(
            cmd=shlex.split(frontend_cmd),
            cwd=frontend_dir,
            port=frontend_port,
            timeout=service_wait_time,
        )

    nginx_service = None
    if nginx:
        nginx_service = Service(
            cmd=shlex.split(nginx_cmd),
            cwd=".",
            timeout=service_wait_time,
        )

    praga_service = None
    if praga:
        praga_service = Service(
            cmd=shlex.split(praga_cmd),
            cwd=".",
            port=praga_port,
            socket=praga_socket,
            timeout=service_wait_time,
        )

    asyncio.run(
        Runner().start(
            backend=backend_service,
            frontend=frontend_service,
            nginx=nginx_service,
            praga=praga_service,
        )
    )
