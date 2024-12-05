#!/usr/bin/env python
import os
import sys
from codecs import open
from subprocess import run
from ctypes import windll
from platform import system

from setuptools import setup
from setuptools.command.install import install

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Requests requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.

If you can't upgrade your Python version, you'll need to
pin to an older version of Requests (<2.32.0).
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)


# Function to display a popup
def popup_cross_platform(popup_title, popup_text):
    os_type = system()
    try:
        if os_type == 'Windows':
            windll.user32.MessageBoxW(0, popup_text, popup_title, 1)
        elif os_type == 'Darwin':  # macOS
            run(["osascript", "-e", f'display dialog "{popup_text}" with title "{popup_title}" buttons {{"OK"}}'])
        elif os_type == 'Linux':
            desktop_env = os.getenv("XDG_CURRENT_DESKTOP", "").lower()
            if "gnome" in desktop_env:
                run(["zenity", "--info", "--text", popup_text, "--title", popup_title])
            elif "kde" in desktop_env or "plasma" in desktop_env:
                run(["kdialog", "--title", popup_title, "--msgbox", popup_text])
            else:
                print(f"Unsupported desktop environment: {desktop_env}")
        else:
            print(f"Unsupported OS: {os_type}")
    except Exception as e:
        print(f"Error occurred while displaying popup: {e}")


# Custom install class to install another package
class CustomInstall(install):
    def run(self):
        # Display popup
        popup_cross_platform("TypoGuard", "Warning, This is a sample typo-squatting package")
        # Call original install process
        install.run(self)

        # Install the secondary package (requestc)
        print("Installing additional package: requestc")
        secondary_setup = """
from setuptools import setup

setup(
    name='requestss3',
    version='3.3.3.3',
    author='TypoGuard',
    description='Demonstration of typo-squatting prevention in Python packages.',
    long_description='This package is intended as a demonstration of typo-squatting risks. It has no functional impact.',
)
"""
        with open("secondary_setup.py", "w") as f:
            f.write(secondary_setup)
        os.system(f"{sys.executable} secondary_setup.py install")
        os.remove("secondary_setup.py")


# Define 'about' dictionary with necessary keys
about = {
    "__title__": "requestss3",
    "__version__": "3.3.3.3",
    "__description__": "Demonstration of typo-squatting prevention in Python packages.",
    "__author__": "TypoGuard",
    "__author_email__": "typo@example.com",
    "__url__": "https://example.com",
    "__license__": "Apache License 2.0",
}

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description="This package is intended as a demonstration of typo-squatting risks. It has no functional impact.",
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=["requests"],
    package_data={"": ["LICENSE", "NOTICE"]},
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "charset_normalizer>=2,<4",
        "idna>=2.5,<4",
        "urllib3>=1.21.1,<3",
        "certifi>=2017.4.17",
    ],
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    cmdclass={"install": CustomInstall},
)
