from setuptools import setup, find_packages

setup(
    name="wox-plugin",
    version="0.0.1",
    description="All Python plugins for Wox should use types in this package",
    author="Wox-launcher",
    author_email="",
    url="https://github.com/Wox-launcher/Wox",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)