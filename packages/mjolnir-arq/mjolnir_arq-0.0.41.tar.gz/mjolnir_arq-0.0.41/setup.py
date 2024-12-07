# setup.py

from setuptools import setup, find_packages

setup(
    name="mjolnir_arq",
    version="0.0.41",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marlon Andres Leon Leon",
    author_email="dandresleon64@gmail.com",
    url="https://github.com/dandres10/mjolnir_arq",
    packages=find_packages(),
    include_package_data=True,  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyfiglet==1.0.2",
        "termcolor==2.4.0",
        "inquirerpy==0.3.4",
        "fastapi==0.112.0",
        "sqlalchemy==2.0.36",
    ],
    entry_points={
        "console_scripts": [
            "mj=mjolnir_arq.module:main",
        ],
    },
)
