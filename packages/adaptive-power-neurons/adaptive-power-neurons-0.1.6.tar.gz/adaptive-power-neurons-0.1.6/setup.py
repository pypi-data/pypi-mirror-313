from setuptools import setup, find_packages

setup(
    name="adaptive-power-neurons", 
    version="0.1.6", 
    packages=find_packages(),
    description="A machine learning model with adaptive power neurons for polynomial feature processing.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dedeep007/adaptive-power-neurons",
    author="Dedeep Vasireddy", 
    author_email="vasireddydedeep@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.18.5",
    ],
    python_requires='>=3.6',
)
