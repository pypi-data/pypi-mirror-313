from setuptools import setup, find_packages

version = '1.0.0.dev9'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="certbot-beget-plugin",
    version=version,
    description="Beget DNS plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Medan-rfz",
    license="MIT License",
    url="https://github.com/Medan-rfz/certbot-beget-plugin",
    packages=find_packages(),
    install_requires=[
        "certbot",
    ],
    entry_points={
        "certbot.plugins": [
            "beget-plugin = certbot_beget_plugin.beget_plugin:Authenticator",
        ],
    },
)
