from setuptools import setup, find_packages

setup(
    name='file_organza',
    version='1.1.1',
    description='A Python package to organize files by type or date',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/asimsolehria/file_organza',
    packages=find_packages(),
    install_requires=[
        'pytest>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'organize-files=file_organizer.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
