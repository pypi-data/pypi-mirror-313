from setuptools import setup, find_packages

PACKAGE = "mlscat"
NAME = PACKAGE
VERSION = __import__(PACKAGE).__version__



with open('./README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = ["h5py>=3.11.0",
                "matplotlib>=3.7.5",
                "numpy>=1.24.4",
                "scikit-learn>=1.3.2",
                "tqdm>=4.66.2",
                ]
setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "h5py>=3.11.0",
        "matplotlib>=3.7.5",
        "numpy>=1.24.4",
        "scikit-learn>=1.3.2",
        "tqdm>=4.66.2",
    ],
    author="i4mhmh",
    author_email='i4mhmh@outlook.com',
    description='A small cat help you enjoy your side channel attack journal!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i4mhmh/mlscat",
    python_requires = ">=3.8"
)