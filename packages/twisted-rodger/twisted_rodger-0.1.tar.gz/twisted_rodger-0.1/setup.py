from setuptools import setup, find_packages

setup(
    name='twisted_rodger',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rodger = twisted_rodger.rodger:main',
        ],
    },
    install_requires=[],
)
