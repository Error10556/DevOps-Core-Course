# DevOps Info Service
## Overview

This app is an educational project that reports system information.

## Prerequisites

To successfully install this app, you will need the following programs:
- Python 3.11+
- pip

During installation, the following modules will be acquired automatically as app dependencies:
- Flask 3.1.0
- gunicorn

## Installation (Linux)

While in the same directory as this README file, execute the following:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

### With `gunicorn`

It is best to run Flask application through an external manager program, in this case, `gunicorn`:

```bash
gunicorn -b 127.0.0.1:5000 -e DEBUG=true app:app
```

The `DEBUG` flag allows the app to log web requests. Do not specify this flag to disable request logging:

```bash
gunicorn -b 127.0.0.1:5000 app:app
```

Note that environment variables `HOST` and `PORT` are ignored if the app is run with `gunicorn`.

### Directly

With request logging:

```bash
DEBUG=true python app.py
```

Without request logging:

```bash
python app.py
```

## API Endpoints

- `GET /` - Service and system information
- `GET /health` - Health check

## Configuration

| Name    | Default value | Meaning                                                                                       | `gunicorn` behavior |
| ---     | ---           | ---                                                                                           | ---                 |
| `HOST`  | `0.0.0.0`     | On which interface to accept connections. Set to `127.0.0.1` to disallow outside connections. | Ignored             |
| `PORT`  | 5000          | To which port to bind. When connecting to the server, specify this port.                      | Ignored             |
| `DEBUG` | `false`       | If `true`, log web requests to console.                                                       | Used                |

## Docker

To obtain the Docker image of this app, pull it from DockerHub or build it locally.

### Building locally

Execute something along the lines of:

```bash
cd app_python
docker build -t <image name> .
```

### Pulling from DockerHub

Execute this command:

```bash
docker pull timurusmanov/devops-infoservice
```

In the next section, refer to the image as `timurusmanov/devops-infoservice`.

### Running

Here is a template for the command you need to execute:

```bash
docker run <-it|-d> --name infoservice -p <127.0.0.1|0.0.0.0>:<port>:5000 <docker image>
```

- Choose `-it` if you want the program to output logs to your terminal and you want to be able to terminate the
  execution with a `Ctrl-C`. Choose `-d` if you want it to run in the background; in this case, terminate the program
  with `docker stop infoservice`.
- Choose `127.0.0.1` if you do **not** want to expose the API endpoints to the network. Choose `0.0.0.0` if you do.
- For the `port`, choose `80` for the default HTTP port, or any other value.
- The `docker image` is going to be whatever you tagged it as in the `docker build` command or
  `timurusmanov/devops-infoservice` if you pulled the image.
