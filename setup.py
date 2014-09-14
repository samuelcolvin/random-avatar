#!/usr/bin/python
from setuptools import setup

description = "Set of random avatars with generator scripts."

setup(
    name='random_avatar',
    version='0.02',
    description=description,
    author='Samuel Colvin',
    license='MIT',
    author_email='S@muelColvin.com',
    url='https://github.com/samuelcolvin/random-avatar',
    packages=['random_avatar'],
    package_data={'random_avatar': ['random_data.json']},
    install_requires=['avatar-generator==0.0.13'],
)