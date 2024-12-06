from setuptools import setup, find_packages

setup(
    name="numpy__py_package",  
    version="0.1",
    description="A package for numerical operations using NumPy",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(), 
    install_requires=[
        "numpy>=1.21.0",  
    ],
)
