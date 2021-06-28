from setuptools import setup

setup(
    name='listings',
    version='1.0.0',
    py_modules=['listings', 'resources'],
    install_requires=[
        'click',
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'listings = listings:cli',
        ],
    },
)
