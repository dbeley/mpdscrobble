{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    pre-commit
  ];

  shellHook = ''
    if [ ! -d .venv ]; then
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -e . 2>/dev/null || true
  '';
}
