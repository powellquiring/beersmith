from setuptools import setup, find_packages

setup(
    name='beersmith',
    version='0.1.0',
    license='apache',
    description='beersmith xml dumper',

    author='Powell Quiring',
    author_email='powellquiring@gmail.com',
    url='https://powellquiring.com',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['click'],

    entry_points={
        'console_scripts': [
            'beersmith = beersmith.cli:cli',
        ]
    },
)

