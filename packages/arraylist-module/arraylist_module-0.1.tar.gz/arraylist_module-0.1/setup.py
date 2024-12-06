from setuptools import setup, find_packages

setup(
    name="arraylist_module",  
    version="0.1",
    description="A package for numerical operations using NumPy",
    author="Deva",
    author_email="deva@gmail.com",
    packages=find_packages(), 
    install_requires=[
        "numpy>=1.21.0",  
    ],
)
