"""
Setup configuration for BlenderUpdater package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
version = {}
with open(os.path.join("blender_updater", "__init__.py")) as fp:
    for line in fp:
        if line.startswith("__version__"):
            exec(line, version)
            break

setup(
    name="blender-updater",
    version=version.get("__version__", "1.0.0"),
    author="ThunderFly-aerospace",
    description="Update mesh models in Blender while preserving properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThunderFly-aerospace/BlenderUpdater",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # bpy is provided by Blender, so we don't list it here
    ],
    entry_points={
        "console_scripts": [
            "blender-updater=blender_updater.cli:main",
        ],
    },
    include_package_data=True,
)
