import os
from setuptools import setup, find_packages


# Get long description from README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

# Get the requirements from requirements.txt
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='ViteRegistry',
    version='1.0.0',
    description='A free Python module to help you control your windows registry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vite License',
    author_email='admin@vitelicense.io',
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)