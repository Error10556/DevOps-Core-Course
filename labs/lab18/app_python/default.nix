{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "devops-infoservice";
  version = "1.0.0";
  src = ./.;

  format = "other";

  propagatedBuildInputs = with pkgs.python3Packages; [
    flask
  ];

  nativeBuildInputs = [ pkgs.makeWrapper ];

  installPhase = ''
    mkdir -p $out/bin
    cp app.py $out/bin/devops-infoservice

    # Wrap with Python interpreter so it can execute
    wrapProgram $out/bin/devops-infoservice \
      --prefix PYTHONPATH : "$PYTHONPATH"
  '';
}
