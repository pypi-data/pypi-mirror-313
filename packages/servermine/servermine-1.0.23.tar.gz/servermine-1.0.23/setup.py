
from setuptools import setup, find_packages
# autossh -M 0 -R servermine.serveo.net:443:localhost:9001 serveo.net
setup(
    name="servermine",
    version="1.0.23",
    packages=find_packages(),
    install_requires=['redis'],  # List your dependencies here
    description="Python library to connect to ServerMine services",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://www.servermine.io",  # GitHub repo or project page
    author="Thiago Magro",
    author_email="thiago.magro@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
