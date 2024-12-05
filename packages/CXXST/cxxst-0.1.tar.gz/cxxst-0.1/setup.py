from setuptools import setup, find_packages

setup(
    name='CXXST',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_package_exec = CXXST.main:main',  # Entry point to execute the main function
        ],
    },
    install_requires=[],  # Add dependencies if required
)
