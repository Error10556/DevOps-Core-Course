# Task 1

### Installation steps and verification output
On Arch Linux, I did what the Arch Wiki recommends:
```bash
# install
sudo pacman -S nix
# launch daemon
sudo systemctl enable --now nix-daemon.service
# add repo
nix-channel --add https://nixos.org/channels/nixpkgs-unstable
nix-channel --update
```
Verification:
```bash
nix --version
```
```text
nix (Nix) 2.34.7
```

### Your `default.nix` file with explanations of each field
The `default.nix` file was taken directly from the lab file, except I renamed the package (I called it
devops-infoservice throughout the course):
```nix
# use the installed packages
{ pkgs ? import <nixpkgs> {} }:

# build a python app
pkgs.python3Packages.buildPythonApplication {
# name
  pname = "devops-infoservice";
# version
  version = "1.0.0";
# source directory (default.nix is located in app_python)
  src = ./.;

# no setup.py
  format = "other";

# only need flask, gunicorn not needed to launch a dev server
  propagatedBuildInputs = with pkgs.python3Packages; [
    flask
  ];

# required to build
  nativeBuildInputs = [ pkgs.makeWrapper ];

# commands to install
  installPhase = ''
# create the 'bin' directory
    mkdir -p $out/bin
# python requires no compilation, so copy the script
    cp app.py $out/bin/devops-infoservice

# wrap with Python interpreter so it can execute
    wrapProgram $out/bin/devops-infoservice \
      --prefix PYTHONPATH : "$PYTHONPATH"
  '';
}
```

### Store path from multiple builds (prove they're identical)
Store path from the first build:
```text
/nix/store/4qqp6kfsd2jm0bg1x2bh3r686v4x074g-devops-infoservice-1.0.0
```

Store path from the second build:
```text
/nix/store/4qqp6kfsd2jm0bg1x2bh3r686v4x074g-devops-infoservice-1.0.0
```

They are identical, so the programs also are.

### Comparison table: `pip install` vs Nix derivation
| Aspect | Lab 1 (pip + venv) | Lab 18 (Nix) |
|--------|-------------------|--------------|
| Python version | System-dependent | Pinned in derivation |
| Dependency resolution | Runtime (`pip install`) | Build-time (pure) |
| Reproducibility | Approximate (with lockfiles) | Bit-for-bit identical |
| Portability | Requires same OS + Python | Works anywhere Nix runs |
| Binary cache | No | Yes (cache.nixos.org) |
| Isolation | Virtual environment | Sandboxed build |
| Store path | N/A | Content-addressable hash |


### Why does `requirements.txt` provide weaker guarantees than Nix?
It pins the listed packages' versions, but it does not specify the transitive dependencies' versions.

### Screenshots showing your Lab 1 app running from Nix-built version
![App in terminal](/labs/lab18/screenshots/task1-nix-running.png)

### Explanation of the Nix store path format and what each part means
```text
/nix/store/4qqp6kfsd2jm0bg1x2bh3r686v4x074g-devops-infoservice-1.0.0/
< storage> <         content hash         > <  package name  > <ver>
```
(`ver` = "version")

### **Reflection:** How would Nix have helped in Lab 1 if you had used it from the start?
I don't think Nix would have helped to complete Lab 1 because the main advantage, complete reproducibility, only starts
to show itself in the long term, when versions start to shift.

But if we consider the broader picture, Nix's versioning would definitely help to avoid potential confusion if I were
developing a real system monitoring service.

# Task 2

### Your `docker.nix` file with explanations of each field
```nix
# use installed packages
{ pkgs ? import <nixpkgs> {} }:

# use the devops-infoservice app how we defined it in default.nix, but inherit pkgs
let
  app = import ./default.nix { inherit pkgs; };
in
# build image
pkgs.dockerTools.buildLayeredImage {
# name of the image
  name = "devops-infoservice-nix";
# tag of the image
  tag = "1.0.0";

# what to include in the image
  contents = [ app ];

  config = {
# how to launch the image
    Cmd = [ "${app}/bin/devops-infoservice" ];
# info about exposed ports
    ExposedPorts = {
      "5000/tcp" = {};
    };
  };

  created = "1970-01-01T00:00:01Z";  # Reproducible timestamp
}
```

### Side-by-side comparison: Lab 2 Dockerfile vs Nix docker.nix
| Aspect | Lab 2 Traditional Dockerfile | Lab 18 Nix dockerTools |
|--------|------------------------------|------------------------|
| **Base images** | `python:3.13-slim` (changes over time) | No base image (pure derivations) |
| **Timestamps** | Different on each build | Fixed or deterministic |
| **Package installation** | `pip install` at build time | Nix store paths (immutable) |
| **Reproducibility** | ❌ Same Dockerfile → Different images | ✅ Same docker.nix → Identical images |
| **Caching** | Layer-based (breaks on timestamp) | Content-addressable (perfect caching) |
| **Image size** | ~150MB+ with full base image | ~50-80MB with minimal closure |
| **Portability** | Requires Docker | Requires Nix (then loads to Docker) |
| **Security** | Base image vulnerabilities | Minimal dependencies, easier auditing |

### SHA256 hash comparison proving Nix reproducibility
Docker:
```text
$ cd lab18/
$ docker build -t lab2-app:test1 ./app_python/
docker save lab2-app:test1 | sha256sum

sleep 2  # Wait a moment

docker build -t lab2-app:test2 ./app_python/
docker save lab2-app:test2 | sha256sum
[+] Building 0.6s (15/15) FINISHED                       docker:default
 => [internal] load build definition from Dockerfile               0.0s
 => => transferring dockerfile: 524B                               0.0s
 => [internal] load metadata for docker.io/library/python:3.13-al  0.0s
 => [internal] load .dockerignore                                  0.0s
 => => transferring context: 115B                                  0.0s
 => [ 1/10] FROM docker.io/library/python:3.13-alpine              0.0s
 => [internal] load build context                                  0.0s
 => => transferring context: 3.54kB                                0.0s
 => CACHED [ 2/10] RUN addgroup -S infoservice                     0.0s
 => CACHED [ 3/10] RUN adduser -S infoservice                      0.0s
 => CACHED [ 4/10] RUN mkdir /app /venv                            0.0s
 => CACHED [ 5/10] RUN chown infoservice:infoservice /venv /app    0.0s
 => CACHED [ 6/10] WORKDIR /app                                    0.0s
 => CACHED [ 7/10] RUN python -m venv /venv                        0.0s
 => CACHED [ 8/10] COPY --chown=infoservice:infoservice requireme  0.0s
 => CACHED [ 9/10] RUN pip install -r requirements.txt             0.0s
 => [10/10] COPY --chown=infoservice:infoservice app.py .          0.1s
 => exporting to image                                             0.4s
 => => exporting layers                                            0.4s
 => => writing image sha256:4353f5dc388c76983ca17789a5e9ea45be2f4  0.0s
 => => naming to docker.io/library/lab2-app:test1                  0.0s
27d6b2f9c92155d362e54ed6742ada0684c9a40f09ff77b6dc08454c6045a650  -
[+] Building 0.1s (15/15) FINISHED                       docker:default
 => [internal] load build definition from Dockerfile               0.0s
 => => transferring dockerfile: 524B                               0.0s
 => [internal] load metadata for docker.io/library/python:3.13-al  0.0s
 => [internal] load .dockerignore                                  0.0s
 => => transferring context: 115B                                  0.0s
 => [ 1/10] FROM docker.io/library/python:3.13-alpine              0.0s
 => [internal] load build context                                  0.0s
 => => transferring context: 63B                                   0.0s
 => CACHED [ 2/10] RUN addgroup -S infoservice                     0.0s
 => CACHED [ 3/10] RUN adduser -S infoservice                      0.0s
 => CACHED [ 4/10] RUN mkdir /app /venv                            0.0s
 => CACHED [ 5/10] RUN chown infoservice:infoservice /venv /app    0.0s
 => CACHED [ 6/10] WORKDIR /app                                    0.0s
 => CACHED [ 7/10] RUN python -m venv /venv                        0.0s
 => CACHED [ 8/10] COPY --chown=infoservice:infoservice requireme  0.0s
 => CACHED [ 9/10] RUN pip install -r requirements.txt             0.0s
 => CACHED [10/10] COPY --chown=infoservice:infoservice app.py .   0.0s
 => exporting to image                                             0.0s
 => => exporting layers                                            0.0s
 => => writing image sha256:4353f5dc388c76983ca17789a5e9ea45be2f4  0.0s
 => => naming to docker.io/library/lab2-app:test2                  0.0s
7d2bbcae8d570033e8fee5d3a475391aebe074362125b673306db84646dffbee  -
```

Nix:
```text
$ cd app_python/
$ rm $(readlink result)
rm: remove write-protected regular file '/nix/store/5xg4bxl4y3zsjay5vlj9
6xacwygbnb66-devops-infoservice-nix.tar.gz'? n
$ sudo !!
sudo rm $(readlink result)
[sudo] password for timur: 
$ nix-build docker.nix
<skipping>
Adding manifests...
Done.
/nix/store/c51sqj61v7rxnfmlhd7vz7z0c7ns2jk8-devops-infoservice-nix.tar.g
z
$ sha256sum result
1eee8cfcf1ab76e558eb3074a7491cddfc4c0010c25e4c23b3ab98491e9920ed  result
$ sudo rm $(readlink result)
$ nix-build docker.nix
<skipping>
Adding manifests...
Done.
/nix/store/c51sqj61v7rxnfmlhd7vz7z0c7ns2jk8-devops-infoservice-nix.tar.g
z
$ sha256sum result
1eee8cfcf1ab76e558eb3074a7491cddfc4c0010c25e4c23b3ab98491e9920ed  result
```

### Image size comparison table with analysis
| Metric | Lab 2 Dockerfile | Lab 18 Nix dockerTools |
|--------|------------------|------------------------|
| Image size | 62.6MB (with python:3.13-alpine) | 214MB |
| Reproducibility | ❌ Different hashes each build | ✅ Identical hashes |
| Build caching | Layer-based (timestamp-dependent) | Content-addressable |
| Base image dependency | Yes (python:3.13-alpine) | No base image needed |

### `docker history` output for both approaches
Old way, with `docker build`:
```text
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
d22d2731b38d   3 months ago   CMD ["-b" "0.0.0.0:5000" "-e" "DEBUG=true" "…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   ENTRYPOINT ["gunicorn"]                         0B        buildkit.dockerfile.v0
<missing>      3 months ago   EXPOSE [5000/tcp]                               0B        buildkit.dockerfile.v0
<missing>      3 months ago   COPY --chown=infoservice:infoservice app.py …   3.41kB    buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c pip install -r requirements.t…   7.12MB    buildkit.dockerfile.v0
<missing>      3 months ago   COPY --chown=infoservice:infoservice require…   30B       buildkit.dockerfile.v0
<missing>      3 months ago   ENV VIRTUAL_ENV=/venv                           0B        buildkit.dockerfile.v0
<missing>      3 months ago   ENV PATH=/venv/bin:/usr/local/bin:/usr/local…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c python -m venv /venv # buildk…   10.3MB    buildkit.dockerfile.v0
<missing>      3 months ago   USER infoservice                                0B        buildkit.dockerfile.v0
<missing>      3 months ago   WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c chown infoservice:infoservice…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c mkdir /app /venv # buildkit      0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c adduser -S infoservice # buil…   3.08kB    buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c addgroup -S infoservice # bui…   1.04kB    buildkit.dockerfile.v0
<missing>      3 months ago   CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c set -eux;  for src in idle3 p…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c set -eux;   apk add --no-cach…   35.8MB    buildkit.dockerfile.v0
<missing>      3 months ago   ENV PYTHON_SHA256=16ede7bb7cdbfa895d11b0642f…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   ENV PYTHON_VERSION=3.13.11                      0B        buildkit.dockerfile.v0
<missing>      3 months ago   ENV GPG_KEY=7169605F62C751356D054A26A821E680…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   RUN /bin/sh -c set -eux;  apk add --no-cache…   982kB     buildkit.dockerfile.v0
<missing>      3 months ago   ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      3 months ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      3 months ago   ADD alpine-minirootfs-3.23.3-x86_64.tar.gz /…   8.44MB    buildkit.dockerfile.v0
```

New way:
```text
IMAGE          CREATED   CREATED BY   SIZE      COMMENT
3ab9a20187e8   N/A                    0B        store paths: ['/nix/store/18ms6chkvk44j77r1n0p84sjbsjah3bi-devops-infoservice-nix-customisation-layer']
<missing>      N/A                    8.73kB    store paths: ['/nix/store/cd1zwi95li582658j89wpykjan9d24l9-devops-infoservice-1.0.0']
<missing>      N/A                    1.08MB    store paths: ['/nix/store/10hk7srr12wgp2hqm5lai0xxr69m76b7-python3.13-flask-3.1.2']
<missing>      N/A                    2.56MB    store paths: ['/nix/store/hmgasx01bmwlz4nr23gm13q9hnqkqw19-python3.13-werkzeug-3.1.6']
<missing>      N/A                    1.85MB    store paths: ['/nix/store/2kwicy8c1ab6zw8p1ps3nnn623b68dn0-python3.13-jinja2-3.1.6']
<missing>      N/A                    1.27MB    store paths: ['/nix/store/77p6rnrhbc14aaw7iwf6d7vxl89qa9kj-python3.13-click-8.3.1']
<missing>      N/A                    144kB     store paths: ['/nix/store/vxp23qrd7v308fr6g63cbai6lpxqm13j-python3.13-itsdangerous-2.2.0']
<missing>      N/A                    82.8kB    store paths: ['/nix/store/jpyvycfsc7gx267kaswq71dawa5ng0vq-python3.13-markupsafe-3.0.3']
<missing>      N/A                    73.9kB    store paths: ['/nix/store/8qn7dwv1rh0h80k7w0f9pa798y90vv2y-python3.13-blinker-1.9.0']
<missing>      N/A                    132MB     store paths: ['/nix/store/0r6k8xa2kgqyp3r4v2w7yrb80ma2iawm-python3-3.13.12']
<missing>      N/A                    10.3MB    store paths: ['/nix/store/si4q3zks5mn5jhzzyri9hhd3cv789vlm-gcc-15.2.0-lib']
<missing>      N/A                    9.3MB     store paths: ['/nix/store/wbyqkb1vpm41s4jb8pv0i9h4jv08xdrv-openssl-3.6.1']
<missing>      N/A                    5.86MB    store paths: ['/nix/store/5087xk8l09k90gddzw8y9b4yypyn23a5-sqlite-3.51.2']
<missing>      N/A                    505kB     store paths: ['/nix/store/47h2ny0j1xbz879a9s7s55fyv3zawr3r-readline-8.3p3']
<missing>      N/A                    3.28MB    store paths: ['/nix/store/2iaawa9vbqas51lgpn4cjnnfdv74x8fn-ncurses-6.6']
<missing>      N/A                    2.1MB     store paths: ['/nix/store/291rd5nk7hkhcpzbh7pxqiz75xikdll3-util-linux-minimal-2.42-lib']
<missing>      N/A                    1.85MB    store paths: ['/nix/store/i27rhb3nr65rkrwz36bchkwmav6ggsmn-bash-5.3p9']
<missing>      N/A                    843kB     store paths: ['/nix/store/hmslvsxvs2ijb7iw5krdckai2im6vp2y-xz-5.8.3']
<missing>      N/A                    448kB     store paths: ['/nix/store/rnaq5b0la7pcq6hyf86iy8ihazgcamg6-gdbm-1.26-lib']
<missing>      N/A                    307kB     store paths: ['/nix/store/pa6n8nrmgq8jswk2pkrl5qprcls1r0ch-expat-2.7.5']
<missing>      N/A                    224kB     store paths: ['/nix/store/yw0fl2v8g35w2dii8phnr0fjb9nr1b0b-mpdecimal-4.0.1']
<missing>      N/A                    131kB     store paths: ['/nix/store/ixhlv41i2wpl84xgjcks061dz4yssbg3-zlib-1.3.2']
<missing>      N/A                    87.6kB    store paths: ['/nix/store/2amncb4zvr32gm5d2i8m6gz29c02cn61-bzip2-1.0.8']
<missing>      N/A                    72.5kB    store paths: ['/nix/store/hyai3q7gvdfppw4ky7s2mvhxvfyp5bh7-libffi-3.5.2']
<missing>      N/A                    34.9MB    store paths: ['/nix/store/fjkx1l5cnskzrqacf08z7i8z17256w0j-glibc-2.42-61']
<missing>      N/A                    362kB     store paths: ['/nix/store/sgswwrxkhdlfskklqp4gsbi2cskfg07c-libidn2-2.3.8']
<missing>      N/A                    1.9MB     store paths: ['/nix/store/cxjmhdbpy3bk12jc6lwpmcvlas76a7zm-tzdata-2026a']
<missing>      N/A                    2.08MB    store paths: ['/nix/store/i4gg1f526vl5psg5nqniflj4v77vc1kd-libunistring-1.4.2']
<missing>      N/A                    197kB     store paths: ['/nix/store/wrxyd3k2f4bmh52pr5rpdjxxsm5r2qxm-gcc-15.2.0-libgcc']
<missing>      N/A                    197kB     store paths: ['/nix/store/xx0z77494lfxr8qjwpck246fry05n3nm-xgcc-15.2.0-libgcc']
<missing>      N/A                    121kB     store paths: ['/nix/store/0minj1ypl50k4zl85gsngfw0z0y9ddg0-util-linux-minimal-2.42']
<missing>      N/A                    118kB     store paths: ['/nix/store/b73wvf83q4cjwzz99pdanbl8qpfawr69-mailcap-2.1.54']
```

### Screenshots showing both containers running simultaneously
![Both](/labs/lab18/screenshots/task2-side-by-side.png)

### **Analysis:** Why can't traditional Dockerfiles achieve bit-for-bit reproducibility?
`docker build` embeds the build timestamp into the container itself, which causes unavoidable hash discrepancies.

### **Reflection:** If you could redo Lab 2 with Nix, what would you do differently?
If I could do that at the time, I would consider making a `docker.nix` file similar to the one in this lab and building
the docker image with Nix.

### Practical scenarios where Nix's reproducibility matters (CI/CD, security audits, rollbacks)
Reproducibility matters a lot in scenarios where we want to prevent malicious actors from replacing the released binary
with malware. For example, if builds are completely reproducible, we could check that a GitHub release is in fact built
from the source code in the repo (which can be reviewed).

In the rollback scenario, if we do not completely roll back some bad code change, we will immediately notice a different
hash in the package name.
