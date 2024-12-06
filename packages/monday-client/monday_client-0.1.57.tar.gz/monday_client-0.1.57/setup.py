import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as read_me_file:
    long_description = read_me_file.read()

setup(
    name='monday-client',
    version='0.1.20',
    author='Dan Hollis',
    author_email='dh@leetsys.com',
    description='Python library for interacting with the monday.com API. Respects monday.com API rate limits and query complexity limits.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LeetCyberSecurity/monday-client',
    packages=find_packages(include=['monday', 'monday.*']),
    install_requires=[
        'aiohttp',
        'pydantic',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.11',
    license='GPLv3',
    project_urls={
        'Bug Reports': 'https://github.com/LeetCyberSecurity/monday-client/issues',
        'Source': 'https://github.com/LeetCyberSecurity/monday-client'
    },
)
