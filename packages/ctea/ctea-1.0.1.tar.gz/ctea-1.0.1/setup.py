from setuptools import setup, Extension
import os

extension = Extension('ctea', ['ctea.c'])

setup(
    name="ctea",
    version="1.0.1",
    author='wood',
    author_email='miraclerinwood@gmail.com',
    url='https://github.com/Rin-Wood/ctea',
    description="TEA Decryption",
    long_description=open('README.md', 'rb').read().decode('utf8'),
	long_description_content_type='text/markdown',
    license="BSD",
    keywords="ctea",
    ext_modules=[extension],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires=">=3.6",
)
