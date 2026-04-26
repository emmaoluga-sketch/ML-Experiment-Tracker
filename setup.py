from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ml-experiment-tracker",
    version="1.0.0",
    author="Emma Oluga",
    description="A lightweight MLOps tool for tracking machine learning experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emmaoluga-sketch/ml-experiment-tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
    ],
)
