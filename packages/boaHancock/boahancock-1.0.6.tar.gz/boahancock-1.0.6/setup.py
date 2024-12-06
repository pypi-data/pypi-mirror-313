from setuptools import setup, find_packages

setup(
    name='boaHancock',
    version='1.0.6',
    author='Khoirul Anam',
    author_email='khoirulanaam4567@gmail.com',
    description='This is tools to make starter template python for create moduls or library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anammkh/boaHancock',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'boaHancock =boaHancock.generator:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['templates/*'],
    },
    install_requires=[
        'termcolor',
        'pyfiglet',
        'colorama',
    ],
    python_requires='>=3.6',
)

