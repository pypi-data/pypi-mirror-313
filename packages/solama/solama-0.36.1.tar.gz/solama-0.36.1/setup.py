# -*- coding: utf-8 -*-
from setuptools import setup

long_des = open("README.md" ,"r",encoding="utf-8").read()
setup(

    name = 'solama',
    version = '0.36.1',
    description = 'Solana Python API',
    long_description = long_des,
    long_description_content_type="text/markdown",
    author="Huang",
    license="MIT",
    install_requires = [
        'construct-typing>=0.5.2,<0.6.0',
        'httpx>=0.23.0',
        'solders>=0.21.0,<0.22.0',
        'typing-extensions>=4.2.0',
        'websockets>=9.0,<12.0'
    ],

    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    
    packages = [
        'solana',
        'solana._layouts',
        'solana.rpc',
        'solana.rpc.providers',
        'solana.utils',
        'spl',
        'spl.memo',
        'spl.token'
    ],
  
    package_dir = {
        '': 'src',
        'spl': 'src/spl',
        'spl.memo': 'src/spl/memo',
        'spl.token': 'src/spl/token'
    },    
    package_data = {'': ['*']}

)
