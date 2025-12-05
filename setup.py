# Arquivo: setup.py
from setuptools import setup, find_packages

setup(
    name="ds_flow",
    version="1.0.0",
    description="Uma biblioteca fluente para Data Science ágil criada por wSanice.",
    author="Wantruil Sanice",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "openpyxl>=3.1.0",
        "scikit-learn>=1.2.0"
    ],
    python_requires=">=3.8",
)
