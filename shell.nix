with import <nixpkgs> { };
pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    python311Packages.pip

    python311Packages.mpd2
    python311Packages.pylast
    python311Packages.httpx
    python311Packages.twine

    pre-commit
  ];

}
