from setuptools import setup

setup(
    name="github-ssh-setup",
    version="0.1",
    py_modules=["github_ssh_setup"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "github-ssh-setup=github_ssh_setup:main",
        ],
    },
)
