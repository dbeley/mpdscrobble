with import <nixpkgs> { };
pkgs.mkShell {
  buildInputs = [
    python3
    python3Packages.pip
    pipenv

    python3Packages.mpd2
    python3Packages.pylast
    python3Packages.httpx
    python3Packages.twine
    python3Packages.pytest

    pre-commit
  ];

}
