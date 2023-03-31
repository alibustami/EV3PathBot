"""This module contains the package information."""
from setuptools import setup

REQUIREMENTS = []

DEV_REQUIREMENTS = [
    "pre-commit",
    "black",
    "flake8",
    "flake8-docstrings",
    "isort",
    "pep8-naming",
]

TEST_PACKAGES = [
    "pytest",
    "pytest-cov",
]

setup(
    name="EV3PathBOT",
    version="0.0.1",
    description="Control Lego Mindstorms EV3 robot, by drawing a path on an image",
    author=["Ali Albustami", "Waleed Abublan", "Hazem Albtoush"],
    author_email=["alialbustami@gmail.com", "waleedabublan@gmail.com", "hazem.albtoush@gmail.com"],
    python_requires="==3.8.13",
    packages=["src"],
    install_requires=REQUIREMENTS + DEV_REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS + TEST_PACKAGES,
        "test": TEST_PACKAGES,
    },
    license="MIT",
    include_package_data=True,
)
