# multi-start

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ioxiocom/multi-start/publish.yaml)](https://github.com/ioxiocom/multi-start/actions/workflows/publish.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/multi-start)](https://pypi.org/project/multi-start/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/multi-start)](https://pypi.org/project/multi-start/)
[![License: BSD 3-Clause](https://img.shields.io/pypi/l/multi-start)](https://opensource.org/license/bsd-3-clause/)

This tool aims to help running multiple services inside a single docker container.

Sometimes you might want to have backend, frontend and nginx (or a combination of those)
inside a single container. This tool may help with:

- Prepare final Nginx configs using
  [parse-template](https://github.com/cocreators-ee/parse-template)
- Wait until backend and frontend start responding before running Nginx
- Stop every process if one of them exits so the whole container stops gracefully

## Installation

```shell
pip install multi-start
```

## Usage

```
multi-start --help

Usage: multi-start [OPTIONS]

  Run multiple services at once. Set DEBUG environment variable to 1 for more
  verbose output when running.

Options:
  --backend / --no-backend        Enable backend service  [default: no-
                                  backend]
  --backend-cmd TEXT              Command to start backend service  [default:
                                  poetry run invoke serve]
  --backend-dir TEXT              Working directory for the backend  [default:
                                  backend]
  --backend-port INTEGER          Port number that backend is running at if
                                  port is used
  --backend-socket TEXT           UNIX socket path that backend is running at
                                  if socket is used  [default:
                                  /run/nginx/uvicorn.sock]
  --frontend / --no-frontend      Enable frontend service  [default: no-
                                  frontend]
  --frontend-port INTEGER         Port number that frontend is running at
                                  [default: 3000]
  --frontend-cmd TEXT             Command to start frontend service  [default:
                                  pnpm run start]
  --frontend-dir TEXT             Working directory for the frontend
                                  [default: frontend]
  --nginx / --no-nginx            Enable nginx  [default: no-nginx]
  --nginx-cmd TEXT                Command to start Nginx  [default: nginx -g
                                  "daemon off;"]
  --service-wait-time FLOAT       How long to wait for a service to be up an
                                  running (sec)  [default: 3.0]
```

## Development

Make sure you install [pre-commit](https://pre-commit.com/#install) and run:

```shell
pre-commit install
```

For testing you can use e.g.

```shell
poetry run multi-start \
  --backend \
  --backend-dir ../another-project/src \
  --backend-cmd "poetry run invoke dev" \
  --backend-port 8080
```
