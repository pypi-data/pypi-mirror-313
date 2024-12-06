#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup config for installing the package."""

from setuptools import setup

oc_version = '5.18.1'

desc = open('README.md').read()
try:
    changelog = open('CHANGELOG').read()
    desc += '\n\n'
    desc += "## CHANGELOG: "
    desc += '\n```\n'
    desc += changelog
    desc += '\n```\n'
except FileNotFoundError:
    try:
        from owega.changelog import OwegaChangelog as oc
        changelog = oc.log
        desc += '\n\n'
        desc += "## CHANGELOG: "
        desc += '\n```\n'
        desc += changelog
        desc += '\n```\n'
    except ModuleNotFoundError:
        pass

requirements = [
    'openai>=1.45.0',
    'prompt_toolkit>=3.0',
    'requests>=2.0',
    'beautifulsoup4>=4.0',
    'lxml>=4.0',
    'json5>=0.9.0',
    'python-editor>=1.0.4',
    'setuptools>=60.0',
]

setup(
    name='owega',
    version=oc_version,
    description="A command-line interface for conversing with AI APIs (OpenAI, anthropic, ...)",
    long_description=desc,
    long_description_content_type='text/markdown',
    author="darkgeem",
    author_email="darkgeem@pyrokinesis.fr",
    url="https://git.pyrokinesis.fr/darkgeem/owega",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: Freely Distributable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: File Formats :: JSON',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    packages=[
        'owega',
        'owega.changelog',
        'owega.config',
        'owega.OwegaFun',
        'owega.conversation',
        'owega.OweHandlers',
        'owega.OwegaSession',
    ],
    entry_points={
        'console_scripts': [
            'owega = owega.owega:main',
        ]
    },
    install_requires=requirements,
    license="DGPL-1.0",
    license_files=["LICEN[CS]E*"],
    project_urls={
        'Source': 'https://git.pyrokinesis.fr/darkgeem/owega',
        'Support': 'https://discord.gg/KdRmyRrA48',
    },
    package_data={
        '': [
            'CHANGELOG',
            'VERSION',
        ]
    },
    include_package_data=True,
)
