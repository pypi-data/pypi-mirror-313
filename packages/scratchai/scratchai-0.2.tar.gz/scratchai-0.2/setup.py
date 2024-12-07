from setuptools import setup, find_packages

VERSION = '0.2'
DESCRIPTION = 'Python package for machine learning'
LONG_DESCRIPTION = 'Python package that provides some methods for mcahine learning and ai'

# Setting up
setup(
        name="scratchai", 
        version=VERSION,
        author="Mohamed Marghoub",
        author_email="<marghoubmohamed2@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'pandas', 'matplotlib'], # prerequisites

        keywords=['python', 'machine_learning', 'ai'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)