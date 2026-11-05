{
  pkgs ? import <nixpkgs> { },
}:

# Everything the project needs comes from nix, including the runtime
# dependencies: entering the shell never builds or installs the package itself.
# The package is importable from the repository root, so `python -m mpdscrobble`
# and `python -m pytest` work as-is. Install the project (pip, systemd unit, ...)
# only when you actually need it.
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (
      ps: with ps; [
        httpx
        pylast
        python-mpd2
        pytest
      ]
    ))
    pkgs.pre-commit
    pkgs.ruff
  ];

  shellHook = ''
    mpdscrobble() { python -m mpdscrobble "$@"; }
  '';
}
