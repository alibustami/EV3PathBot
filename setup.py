"""This module contains the package information."""
from setuptools import setup

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name="EV3PathBOT",
    version="0.0.1",
    description="Control Lego Mindstorms EV3 robot, by drawing a path on an image",
    author=["Ali Albustami", "Waleed Abublan", "Hazem Albtoush"],
    author_email=["alialbustami@gmail.com", "waleedabublan@gmail.com", "hazem.albtoush@gmail.com"],
    python_requires=">=3.8",
    packages=["src"],
    install_requires=REQUIREMENTS,
    license="MIT",
    include_package_data=True,
)
