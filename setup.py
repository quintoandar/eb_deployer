#!/usr/bin/env python
from setuptools import setup


setup(
    name='quintoandar_eb_deployer',
    description='Make your project publishes itself to AWS',
    version='1.12',
    author='Diego Queiroz',
    author_email='diego.queiroz@gmail.com',
    license='MIT',
    url='teste.com',
    long_description=open('README.rst').read(),
    packages=[
        'quintoandar_eb_deployer',
        'quintoandar_eb_deployer.management',
        'quintoandar_eb_deployer.management.commands',
        'quintoandar_eb_deployer.management.commands.aws'
    ],
    install_requires=[
        'Django',
        'python_magic'
    ],
    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ]
)
