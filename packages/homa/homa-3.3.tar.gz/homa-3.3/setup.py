from setuptools import setup
from setuptools import find_packages

with open("README.md") as fh:
    description = fh.read()

setup(
    name="homa",
    maintainer="Taha Shieenavaz",
    maintainer_email="tahashieenavaz@gmail.com",
    version=3.3,
    packages=find_packages(),
    install_requires=["torchvision", "torch"],
    long_description=description,
    long_description_content_type="text/markdown",
)
