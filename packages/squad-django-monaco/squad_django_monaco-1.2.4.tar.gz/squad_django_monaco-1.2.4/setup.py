import os
from setuptools import setup, find_packages

README = open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
).read()

setup(
    name="squad-django-monaco",
    version="1.2.4",
    packages=["monaco"],
    description="Monaco editor widgets in the Django Admin",
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    author="Ayush Shanker",
    keywords=[
        "monaco",
    ],
    platforms=["OS Independent"],
    license="MIT",
    install_requires=[
        "Django<=5.2",
    ],
)
