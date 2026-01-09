"""Setup script for counting objects task data generator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements = []
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="counting-objects-task-generator",
    version="1.0.0",
    description="Data generator for counting objects reasoning tasks for VMEvalKit",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="VMEvalKit Contributors",
    url="https://github.com/vm-dataset/O-33_counting_object_data-generator",
    packages=find_packages(include=["core", "core.*", "src", "src.*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
