{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  packages = with pkgs; [
    python3
    pre-commit
    ruff
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -e .
  '';
}
