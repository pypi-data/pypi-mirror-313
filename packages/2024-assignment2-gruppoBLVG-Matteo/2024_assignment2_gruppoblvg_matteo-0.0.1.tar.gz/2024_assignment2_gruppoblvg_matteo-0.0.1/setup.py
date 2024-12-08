from setuptools import setup, find_packages

setup(
    name="2024_assignment2_gruppo_BLVG",  
    version="0.1",  
    packages=find_packages(),  
    install_requires=[],  
    extras_require={
        "test": ["pytest", "tox", "ruff"],  
    },
)
