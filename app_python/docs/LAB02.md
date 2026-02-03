# Task 2 Documentation

```bash
docker push timurusmanov/devops-infoservice:1.0.0 
```
```text
The push refers to repository [docker.io/timurusmanov/devops-infoservice]
428e79dab196: Layer already exists 
2a7b67ba353c: Layer already exists 
5a2f163a57ac: Layer already exists 
a3d8a971987a: Layer already exists 
5f70bf18a086: Layer already exists 
043c867b6612: Layer already exists 
d5735eb4c1e6: Layer already exists 
c7b3bf7038e3: Layer already exists 
d51d80a9b06a: Layer already exists 
4a462158ec6c: Layer already exists 
9826379ec12d: Layer already exists 
f69ebdfdccef: Layer already exists 
989e799e6349: Layer already exists 
1.0.0: digest: sha256:bd6a94a3b845c6049a6ee88dec6765960a7969e2b30e42477e07c1f44cd1a2a1 size: 3028
```

Here is the pushed image: 
[hub.docker.com/repository/docker/timurusmanov/devops-infoservice](https://hub.docker.com/repository/docker/timurusmanov/devops-infoservice)

I used semantic versioning to add the version to the tag.

# Documentation

## Docker best practices applied

- Non-root container, because in this way a compromised continer would not be such a threat.
```dockerfile
RUN addgroup -S infoservice
RUN adduser -S infoservice
#...
USER infoservice
#...
```
- Layer caching (moving frequently changing COPY directives to the end), because that saves build time.
```dockerfile
# Setting up environment first (never changes)
RUN addgroup -S infoservice
RUN adduser -S infoservice
#...
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"
#...

# Dependenies next (they rarely change)
COPY --chown=infoservice:infoservice requirements.txt .
RUN pip install -r requirements.txt

# App code last (changes always)
COPY --chown=infoservice:infoservice app.py .
#...
```
- Using .dockerignore to reduce build context size and ensure nothing sensitive leaks into the image
```dockerignore
**/__pycache__
**/*.pyc
venv
docs
README.md
tests
.gitignore
.dockerignore
```
(did not specify `.git` here because it is not present in this directory)
- Never `COPY`ing directories, even with a .dockerignore, for additional control and security
```dockerfile
#...
COPY --chown=infoservice:infoservice requirements.txt .
#...
COPY --chown=infoservice:infoservice app.py .
#...
```
- Using a lightweight container to save system resources
```bash
docker image inspect python:3.13-slim python:3.13-alpine | jq '.[] | .Size'
```
Gives:
```text
117556646
45196349
```
So I used the Alpine-based image.

## Image Information & Decisions

I chose the `python:3.13-alpine` lightweight base image (see justification just above). The python version (3.13) was
chosen arbitrarily out of versions since 3.11.

Image size:
```bash
docker image inspect timurusmanov/devops-infoservice:latest | jq '.[0].Size'
```
Gave:
```text
62580512
```
Which is 63MB. Pretty good.

| Layer | Layer-generating command                                  | Explanation                                    |
|-------|-----------------------------------------------------------|------------------------------------------------|
| 1     | `FROM python:3.13-alpine`                                 | Base                                           |
| 2     | `RUN addgroup -S infoservice`                             | Modifies `/etc/group`                          |
| 3     | `RUN adduser -S infoservice`                              | Modifies `/etc/passwd`                         |
| 4     | `RUN mkdir /app /venv`                                    | Adds roots for the app and package environment |
| 5     | `RUN chown infoservice:infoservice /venv /app`            | Adds permissions                               |
| 6     | `RUN python -m venv /venv`                                | Populates `/venv`                              |
| 7     | `COPY --chown=infoservice:infoservice requirements.txt .` | `requirement.txt` appears                      |
| 8     | `RUN pip install -r requirements.txt`                     | Populates `/venv/{lib,bin}`                    |
| 9     | `COPY --chown=infoservice:infoservice app.py .`           | Populates `/app`                               |

To optimize, I tried to sequence several RUN commands into one, but with Alpine's shell, that is not always possible.
So I created `/app` and `/venv` in one RUN.

## Build & Run Process

Here is the output of the build command:
```bash
docker build --no-cache -t app_python . 2>log.txt
```
```text
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 524B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.13-alpine
#2 DONE 0.0s

#3 [internal] load .dockerignore
#3 transferring context: 115B done
#3 DONE 0.0s

#4 [ 1/10] FROM docker.io/library/python:3.13-alpine
#4 CACHED

#5 [internal] load build context
#5 transferring context: 63B done
#5 DONE 0.0s

#6 [ 2/10] RUN addgroup -S infoservice
#6 DONE 0.2s

#7 [ 3/10] RUN adduser -S infoservice
#7 DONE 0.3s

#8 [ 4/10] RUN mkdir /app /venv
#8 DONE 0.2s

#9 [ 5/10] RUN chown infoservice:infoservice /venv /app
#9 DONE 0.3s

#10 [ 6/10] WORKDIR /app
#10 DONE 0.0s

#11 [ 7/10] RUN python -m venv /venv
#11 DONE 5.8s

#12 [ 8/10] COPY --chown=infoservice:infoservice requirements.txt .
#12 DONE 0.1s

#13 [ 9/10] RUN pip install -r requirements.txt
#13 2.158 Collecting Flask==3.1.0 (from -r requirements.txt (line 1))
#13 2.592   Downloading flask-3.1.0-py3-none-any.whl.metadata (2.7 kB)
#13 2.816 Collecting gunicorn==24.0.0 (from -r requirements.txt (line 2))
#13 2.921   Downloading gunicorn-24.0.0-py3-none-any.whl.metadata (4.5 kB)
#13 3.154 Collecting Werkzeug>=3.1 (from Flask==3.1.0->-r requirements.txt (line 1))
#13 3.269   Downloading werkzeug-3.1.5-py3-none-any.whl.metadata (4.0 kB)
#13 3.456 Collecting Jinja2>=3.1.2 (from Flask==3.1.0->-r requirements.txt (line 1))
#13 3.614   Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
#13 3.775 Collecting itsdangerous>=2.2 (from Flask==3.1.0->-r requirements.txt (line 1))
#13 3.882   Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
#13 4.063 Collecting click>=8.1.3 (from Flask==3.1.0->-r requirements.txt (line 1))
#13 4.241   Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
#13 4.467 Collecting blinker>=1.9 (from Flask==3.1.0->-r requirements.txt (line 1))
#13 4.659   Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
#13 4.896 Collecting packaging (from gunicorn==24.0.0->-r requirements.txt (line 2))
#13 5.038   Downloading packaging-26.0-py3-none-any.whl.metadata (3.3 kB)
#13 5.491 Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->Flask==3.1.0->-r requirements.txt (line 1))
#13 5.703   Downloading markupsafe-3.0.3-cp313-cp313-musllinux_1_2_x86_64.whl.metadata (2.7 kB)
#13 5.914 Downloading flask-3.1.0-py3-none-any.whl (102 kB)
#13 6.436 Downloading gunicorn-24.0.0-py3-none-any.whl (110 kB)
#13 6.828 Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
#13 6.946 Downloading click-8.3.1-py3-none-any.whl (108 kB)
#13 7.270 Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
#13 7.401 Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
#13 7.880 Downloading markupsafe-3.0.3-cp313-cp313-musllinux_1_2_x86_64.whl (23 kB)
#13 8.053 Downloading werkzeug-3.1.5-py3-none-any.whl (225 kB)
#13 8.991 Downloading packaging-26.0-py3-none-any.whl (74 kB)
#13 9.342 Installing collected packages: packaging, MarkupSafe, itsdangerous, click, blinker, Werkzeug, Jinja2, gunicorn, Flask
#13 10.29 
#13 10.30 Successfully installed Flask-3.1.0 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.5 blinker-1.9.0 click-8.3.1 gunicorn-24.0.0 itsdangerous-2.2.0 packaging-26.0
#13 10.88 
#13 10.88 [notice] A new release of pip is available: 25.3 -> 26.0
#13 10.88 [notice] To update, run: pip install --upgrade pip
#13 DONE 11.0s

#14 [10/10] COPY --chown=infoservice:infoservice app.py .
#14 DONE 0.0s

#15 exporting to image
#15 exporting layers
#15 exporting layers 0.5s done
#15 writing image sha256:4cc4359b540ed65b2cec7a1ff75e345e4a809b0399039940cba7a295ae4f758c done
#15 naming to docker.io/library/app_python done
#15 DONE 0.5s
```

When the container is started and sent a request:
```bash
docker run -it -p 127.0.0.1:5000:5000 timurusmanov/devops-infoservice:latest
```
It outputs the following:
```text
[2026-02-03 17:00:46 +0000] [1] [INFO] Starting gunicorn 24.0.0
[2026-02-03 17:00:46 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2026-02-03 17:00:46 +0000] [1] [INFO] Using worker: sync
[2026-02-03 17:00:46 +0000] [7] [INFO] Booting worker with pid: 7
2026-02-03 17:00:46,993 - app - INFO - Application starting...
2026-02-03 17:00:53,509 - app - DEBUG - Request: GET /
```

Here is the output of `curl`:
```bash
curl localhost:5000
```
```json
{"endpoints":[{"description":"Service information","method":"GET","path":"/"},{"description":"Health check","method":"GET","path":"/health"}],"request":{"client_ip":"172.17.0.1","method":"GET","path":"/","user_agent":"curl/8.18.0"},"runtime":{"current_time":"2026-02-03T17:00:53.510+00:00","timezone":"UTC","uptime_human":"0 hours, 0 minutes","uptime_seconds":6},"service":{"description":"DevOps course info service","framework":"Flask","name":"devops-info-service","version":"1.0.0"},"system":{"architecture":"x86_64","cpu_count":16,"hostname":"cd9e6a6b50d2","platform":"Linux","platform_version":"#1 SMP PREEMPT_DYNAMIC Sat, 24 Jan 2026 00:47:39 +0000","python_version":"3.13.11"}}
```

Same request, but pretty-printed:
```bash
curl localhost:5000 | jq
```
```json
{
  "endpoints": [
    {
      "description": "Service information",
      "method": "GET",
      "path": "/"
    },
    {
      "description": "Health check",
      "method": "GET",
      "path": "/health"
    }
  ],
  "request": {
    "client_ip": "172.17.0.1",
    "method": "GET",
    "path": "/",
    "user_agent": "curl/8.18.0"
  },
  "runtime": {
    "current_time": "2026-02-03T17:07:36.813+00:00",
    "timezone": "UTC",
    "uptime_human": "0 hours, 0 minutes",
    "uptime_seconds": 5
  },
  "service": {
    "description": "DevOps course info service",
    "framework": "Flask",
    "name": "devops-info-service",
    "version": "1.0.0"
  },
  "system": {
    "architecture": "x86_64",
    "cpu_count": 16,
    "hostname": "1cabcbe9032c",
    "platform": "Linux",
    "platform_version": "#1 SMP PREEMPT_DYNAMIC Sat, 24 Jan 2026 00:47:39 +0000",
    "python_version": "3.13.11"
  }
}
```

Check it out: [hub.docker.com/repository/docker/timurusmanov/devops-infoservice](https://hub.docker.com/repository/docker/timurusmanov/devops-infoservice)

## Technical Analysis

### Why does your Dockerfile work the way it does?

Because this is how the image builder interprets it.

I have a vague idea of how the builder works, so I wrote the Dockerfile with that in mind.

No idea what you want from me.

### What would happen if you changed the layer order?

If I move user initialization to the end of the file, or the directory initialization after the directories are used,
or similar, then the image would not build.

If I change the order of layers listed in the **Image Information & Decisions** table, then the average build time would
increase.

Otherwise, nothing would really change.

### What security considerations did you implement?

- Non-root user
- `.dockerfile` ignoring some files

### How does .dockerignore improve your build?

- Increases build time by not sending irrelevant files to the build context
- Makes sure I do not accidentally include some irrelevant files in the image.

It does not hide any secrets at the moment.

## Challenges & Solutions

Issue: Alpine images do not support `useradd`, `groupadd`, and chaining other built-in commands.

Solution: the Internet suggested `adduser` and `addgroup`; I gave up trying to chain commands.

Learned: to use Alpine's `busybox`.
