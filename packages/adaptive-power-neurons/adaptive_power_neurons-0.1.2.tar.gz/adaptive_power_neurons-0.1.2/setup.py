from setuptools import setup, find_packages

# Read the contents of your README file to use as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adaptive_power_neurons", 
    version="0.1.2",  # Update version accordingly
    packages=find_packages(), 
    description="A machine learning model with adaptive power neurons for polynomial feature processing.",
    long_description=long_description,  # Ensure this is read correctly
    long_description_content_type="text/markdown",
    url="https://github.com/Dedeep007/adaptive-power-neurons", 
    author="Dedeep Vasireddy", 
    author_email="vasireddydedeep@gmail.com",  
    license="MIT",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.18.5", 
    ],
    python_requires='>=3.6',  # Python version requirement
)
