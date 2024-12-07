from setuptools import setup, find_packages
import os
import platform

# Helper function to handle long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Determine if Graphviz is installed for pygraphviz
graphviz_dependency = "pygraphviz>=1.7"

# Check platform and environment
if platform.system() == "Windows":
    graphviz_path = os.environ.get("GRAPHVIZ_PATH", r"C:\Program Files\Graphviz")
    if not os.path.exists(graphviz_path):
        graphviz_dependency += "; extra_requires_graphviz"  # Warn user to install manually

setup(
    name="signalpathwaysimulator",  
    version="0.1.0",                
    description="A signal pathway simulator package for SBML-based models.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Wenhui Xie",
    author_email="whxie@uw.edu",
    url="https://github.com/whxie123/SignalPathwaySimulator.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "sympy>=1.9",
        "matplotlib>=3.4.0",
        "pygraphviz>=1.7",
        "python-libsbml>=5.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "signalpathwaysimulator=signalpathwaysimulator.main:main",
        ],
    },
)

