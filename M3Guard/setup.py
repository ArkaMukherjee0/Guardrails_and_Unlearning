from setuptools import setup, find_packages
import os

# Get the absolute path to the directory containing setup.py
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="m3guard",
    version="0.1.0",
    packages=find_packages(where=here),
    package_dir={'': '.'},
    install_requires=[
        'numpy',
        'pandas',
        'tqdm',
        'matplotlib',
        'seaborn',
        'sentence-transformers'
    ],
    python_requires='>=3.7'
)