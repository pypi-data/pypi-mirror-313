import asyncio
import os
import signal
import sys
from asyncio.subprocess import Process
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import httpx

from .log import logger


@dataclass
class Service:
    cmd: List[str]
    cwd: str
    timeout: float
    socket: Optional[str] = None
    port: Optional[int] = None


async def run(
    cmd: List[str],
    cwd: Optional[str] = None,
    pipe_output=False,
    extra_env: Optional[dict] = None,
) -> Process:
    """
    Run a process
    :param cmd: Command to run
    :param cwd: Working directory
    :param pipe_output: Whether to pipe the output or print it on screen instead
    :param extra_env: Extra environment variables
    :return: Process
    """
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE if pipe_output else sys.stdout,
        stderr=asyncio.subprocess.PIPE if pipe_output else sys.stderr,
        cwd=cwd,
        env=env,
    )

    return proc


async def run_and_wait(
    cmd: List[str], cwd: Optional[str] = None, extra_env: Optional[dict] = None
):
    proc = await run(cmd, cwd, extra_env=extra_env)
    code = await proc.wait()
    if code != 0:
        raise RuntimeError(f"{cmd} failed with code {code}")


async def get_output(cmd: List[str], cwd: Optional[str] = None) -> bytes:
    """
    Run command and get its stdout if completed successfully
    :param cmd: Command to run
    :param cwd: Working directory
    :return: Bytes from stdout
    """
    proc = await run(cmd, cwd, pipe_output=True)
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd} failed with code {proc.returncode}")
    return out


async def stop_process(proc: Process, timeout: float = 3.0) -> None:
    """
    Try to stop the process gracefully, otherwise killing it
    :param proc: Process to stop
    :param timeout: How long to wait for a graceful stop
    """
    if proc.returncode is not None:
        return
    proc.terminate()
    await asyncio.wait_for(proc.wait(), timeout=timeout)
    if proc.returncode is not None:
        return
    else:
        proc.kill()


async def setup_nginx() -> None:
    """
    Prepare Nginx.
    Optionally setup HTTP Basic Auth, if environment variables are provided.
    Process Nginx templates to build actual configuration files.
    """
    if user := os.environ.get("HTTP_BASIC_AUTH_USER"):
        pwd = os.environ["HTTP_BASIC_AUTH_PASSWORD"]
        await run_and_wait(["htpasswd", "-b", "-c", "/run/nginx/.htpasswd", user, pwd])
        if not os.environ.get("HTTP_BASIC_AUTH_REALM"):
            os.environ["HTTP_BASIC_AUTH_REALM"] = "Private area"

    for f in ["/etc/nginx/conf.d/default.conf", "/etc/nginx/dataspace-headers.conf"]:
        path = Path(f)
        if path.exists():
            final_config = await get_output(["parse-template", f])
            path.write_bytes(final_config)
            logger.info(f"{f} is generated")

            if os.environ.get("NGINX_DEBUG"):
                logger.info(f"=== {f} ===")
                logger.info(path.read_text("utf8") + "\n")


async def start_service(svc: Service, extra_env: Optional[dict] = None) -> Process:
    """
    Start a service.
    :param svc: Service to run
    :param extra_env: Extra environment variables
    :return: Process
    """
    logger.debug(f"Starting service: {svc.cmd}")
    return await run(svc.cmd, cwd=svc.cwd, extra_env=extra_env)


async def wait_for_service(svc: Service, timeout: float, name: str):
    """
    Wait until a service and up and listening for either a port or socket.
    Port takes precedence over a socket if both defined.
    :param svc: Service to wait for
    :param timeout: How long to wait in seconds
    :param name: How to describe the service in exceptions
    """
    if not svc.socket and not svc.port:
        raise RuntimeError("Either socket or port should be defined")

    if svc.port:
        url = f"http://localhost:{svc.port}"
        transport = httpx.AsyncHTTPTransport()
    else:
        url = "http://localhost"
        transport = httpx.AsyncHTTPTransport(uds=svc.socket)

    async with httpx.AsyncClient(transport=transport) as client:
        wait_step = 0.3
        max_attempts = int(timeout / wait_step)
        for _ in range(max_attempts):
            try:
                await client.get(url, timeout=timeout)
            except (
                httpx.NetworkError,
                httpx.TimeoutException,
                httpx.HTTPStatusError,
            ) as e:
                logger.debug(f"Caught {type(e).__name__} from {url}")
                await asyncio.sleep(wait_step)
            else:
                logger.debug(f"Connection established: {url}")
                break
        else:
            raise TimeoutError(
                f"{name.capitalize()} service is not responding, aborting..."
            )


class Runner:
    def __init__(self):
        self._stop = asyncio.Event()

    def stop(self, *args):
        self._stop.set()

    async def start(
        self,
        backend: Optional[Service],
        frontend: Optional[Service],
        nginx: Optional[Service],
        praga: Optional[Service],
    ):
        # Handle Ctrl+C gracefully by stopping all running services
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.add_signal_handler(signal.SIGTERM, self.stop)

        prerequisites = []
        procs = []

        if backend:
            procs.append(await start_service(backend))
            prerequisites.append(wait_for_service(backend, backend.timeout, "backend"))

        if frontend:
            frontend_svc = await start_service(
                frontend, extra_env={"PORT": str(frontend.port)}
            )
            procs.append(frontend_svc)
            prerequisites.append(
                wait_for_service(frontend, frontend.timeout, "frontend")
            )

        if praga:
            procs.append(await start_service(praga))
            prerequisites.append(wait_for_service(praga, praga.timeout, "praga"))

        if nginx:
            prerequisites.append(setup_nginx())

        try:
            await asyncio.gather(*prerequisites)
        except TimeoutError as e:
            logger.error(str(e))
            return

        if nginx:
            procs.append(await start_service(nginx))

        try:
            tasks = [asyncio.create_task(p.wait()) for p in procs]
            tasks.append(asyncio.create_task(self._stop.wait()))
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        finally:
            logger.info("Shutting down all processes")
            await asyncio.gather(
                *[asyncio.create_task(stop_process(proc)) for proc in procs]
            )
