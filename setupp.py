from setuptools import setup, find_packages

from pathlib import Path

# Read the contents of README.md



setup(
    name='argument_mining_framework',
    version='0.0.5',
    description='Argument Mining Framework (AMF) is a comprehensive toolkit designed to streamline and unify various argument mining modules into a single platform.',
    readme = "README.md",
    author='Debela',
    author_email='d.t.z.gemechu@dundee.ac.uk',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'transformers',
        'torch',
        'numpy'
        'xaif-eval==0.1.4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

