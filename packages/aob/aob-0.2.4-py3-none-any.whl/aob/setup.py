from setuptools import setup

setup(
    name="aob",
    entry_points={
        "console_scripts": [
            "aob=aob.main:app",
        ],
        "distutils.commands": [
            "post_install=aob.entry:show_welcome",
        ],
    },
)