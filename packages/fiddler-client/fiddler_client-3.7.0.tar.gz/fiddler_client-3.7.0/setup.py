from pathlib import Path

import setuptools

VERSION_FILE_PATH = Path(__file__).resolve().parent / 'fiddler' / 'VERSION'

with open(VERSION_FILE_PATH, encoding='utf-8') as f:
    version = f.read().strip()

with open('PUBLIC.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='fiddler-client',
    version=version,
    author='Fiddler Labs',
    description='Python client for Fiddler Platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://fiddler.ai',
    packages=setuptools.find_packages(),
    include_package_data=True,
    # As of pydantic>=1.10.17, the pydantic.v1 namespace can be used within V1.
    # This makes it easier to migrate to V2, which also supports the
    # pydantic.v1 namespace
    install_requires=[
        'pip>=21.0',
        'requests<3',
        'requests-toolbelt',
        'pandas>=1.2.5',
        'pydantic>=1.10.17',
        'deprecated==1.2.14',
        'tqdm',
        'simplejson>=3.17.0',
        'pyarrow>=7.0.0',
        'pyyaml',
        'typing-extensions>=4.6.0,<5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>3.8.0',
)
