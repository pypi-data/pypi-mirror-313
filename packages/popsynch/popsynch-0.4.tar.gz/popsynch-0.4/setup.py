from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text()

setup(
name='popsynch',
version='0.4',
author='Francis C. Motta',
author_email='fmotta@fau.edu',
description='A pure Python package for computing the synchrony of population distributions in compact metric spaces.',
license='MIT',
keywords='Synchrony, Synchronization, Frechet Variance, Wasserstein Distance, Optimal Transport',
url = "https://gitlab.com/biochron/popsynch",
download_url = "https://gitlab.com/biochron/popsynch/-/archive/1.0.0/popsynch-1.0.tar.gz",
packages=find_packages(include=['popsynch', 'popsynch.*']),
long_description=long_description,
long_description_content_type="text/markdown",
install_requires=['scipy>=1.12', 'numpy>=1.26.3'],
extras_require={
        'notebooks': ['matplotlib>=3.8.2', 'pandas>=2.2', 'jupyter>=1.0.0']},
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
"Development Status :: 4 - Beta"
],
python_requires='>=3.12',
)