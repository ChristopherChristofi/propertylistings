from setuptools import setup, find_packages

setup(
    name='listings',
    version='1.0.0',
    packages=find_packages(),
    include_packe_data=True,
    install_requires=[
        'click',
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'listings = listings.scripts.listings:cli',
        ],
    },
)
