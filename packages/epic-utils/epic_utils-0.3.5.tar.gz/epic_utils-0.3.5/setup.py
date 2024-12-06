from setuptools import setup, find_packages
setup(
name='epic-utils',
version='0.3.5',
author='Epic099',
author_email='',
description='Dependencies i regurlarly use',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
install_requires=[
    "requests",
    "numpy",
    "websockets"
]
)