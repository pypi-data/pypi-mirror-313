from setuptools import setup, find_packages

setup(
    name = "pyjuni",
    version = "1.5", 
    description = "Library for Junilab Products",
    author = "Junilab",
    author_email = "help@junilab.co.kr",
    url = "http://www.junilab.co.kr",
    packages = ['pyjuni', 
        ],
    install_requires = [
        'pyserial>=3.4',
        'pynput>=1.7.3',
        ],
)
