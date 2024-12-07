# setup.py

from setuptools import setup, find_packages
# Read the contents of README.md
with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name='raspi_tools',
    version='1.0.5',
    description='A Python library for Raspberry Pi tools including GPS and board LED utilities.',
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    author='Elijah M',
    author_email='gichiam22@gmail.com',
    packages=find_packages(),
    install_requires=[
        'gps',
        'tinydb',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)
