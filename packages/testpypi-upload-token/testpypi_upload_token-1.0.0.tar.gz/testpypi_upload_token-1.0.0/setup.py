# setup.py

from setuptools import setup, find_packages

setup(
    name="testpypi_upload_token",                           # Package name
    version="1.0.0",                            # Package version
    packages=find_packages(),                   # Automatically discover the sub-packages
    install_requires=[],                        # Dependencies (if any)
    author="Vijay",                             # Your name
    author_email="vijayagopal.sb@gmail.com",    # Your email
    description="A simple math package",        # Short description
    long_description=open("README.md").read(), # Detailed decription from README
    long_description_content_type="text/markdown",
    url="http://github.com/",                       # Project URL  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",          # Minimum Python version
)

