from pathlib import Path

from setuptools import find_packages, setup

with Path("requirements.txt").open() as f:
    requirements = f.read()
requirements = requirements.splitlines()

with Path("README.md").open(encoding="utf-8") as f:
    readme = f.read()
readme = "\n".join(readme.split("\n")[2:])

with Path("src/bluequbit/version.py").open() as f:
    Version = f.read()

Version = Version.rstrip()
Version = Version[15:-1]

setup(
    name="bluequbit",
    version=Version,
    description="Python SDK to BlueQubit app",
    license="Apache 2.0",
    author="BlueQubit",
    author_email="hovnatan@bluequbit.io",
    url="https://app.bluequbit.io",
    project_urls={
        "Documentation": "https://app.bluequbit.io/sdk-docs",
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    entry_points={
        "pennylane.plugins": [
            "bluequbit.cpu = bluequbit.pennylane_plugin:BluequbitCPU",
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
)
