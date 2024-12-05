from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="solop",
    version="1.0.0",
    long_description=long_description,
    url="https://github.com/niallantony/SoloP",
    author="Niall Craven",
    classifiers=[
    "Topic :: File Formats :: JSON",
    "Topic :: Documentation",
    "Topic :: Software Development :: Documentation",
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    ],
    keywords=[
    "project management",
    "backlog",
    "progress",
    "task",
    "to do",
    "markdown"
    ],
    packages=find_packages(where='src'),
    python_requires=">=3.8",
    extras_require={
        "test":[
            "pytest",
            "pluggy"
        ]
    }
    entry_points={
        "console_scripts": [
            "solop=solop.cli:main"
        ]
    }
)