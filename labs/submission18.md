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

