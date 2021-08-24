import setuptools

with open("README.md") as f:
    long_description = f.read()

if __name__ == "__main__":
    setuptools.setup(
        name='propertylistings',
        version='0.1.9',
        author='Christopher Christofi',
        author_email='christopherlchristofi@outlook.com',
        license='GPL-3.0',
        description='Webscraping tool for archiving sales records on RightMove.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/christopher-christofi/listings',
        project_urls={
            "Bug Tracker": "https://github.com/christopher-christofi/listings/issues",
        },
        packages=setuptools.find_packages(),
        include_package_data=True,
        python_requires=">=3.0",
        install_requires=[
            'beautifulsoup4',
            'requests',
            'click',
        ],
        entry_points={
            'console_scripts': [
                'propertylistings = propertylistings.scripts.propertylistings:cli',
            ],
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
    )