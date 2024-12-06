# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setuptools.setup(
    name='pilot-platform-common',
    version='2.7.0',
    author='Indoc Systems',
    author_email='etaylor@indocresearch.org',
    description='Generates entity ID and connects with Vault (secret engine) to retrieve credentials',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'python-dotenv>=0.19.1',
        'httpx>=0.23.0,<0.27.0',
        'redis>=4.5.0,<5.0.0',
        'aioboto3==9.6.0',
        'xmltodict==0.13.0',
        'minio==7.1.8',
        'python-json-logger==2.0.2',
        'pyjwt==2.6.0',
        'starlette>=0.37.2,<0.38.0',
        'requests>=2.26.0,<2.32.0',
        'cryptography==39.0.0',
        'pydantic>=2.7.1,<3.0.0',
    ],
    include_package_data=True,
    package_data={
        '': ['*.crt'],
    },
)
