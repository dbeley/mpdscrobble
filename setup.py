import setuptools
import mpdscrobble

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpdscrobble",
    version=mpdscrobble.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="A simple Last.fm scrobbler for MPD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/mpdscrobble",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["mpdscrobble=mpdscrobble.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["httpx", "python-mpd2", "pylast"],
)
