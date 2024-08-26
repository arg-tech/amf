from setuptools import setup, find_packages

setup(
    name='Argument Mining Framework (AMF)',
    version='0.0.1',
    description='Argument Mining Framework (AMF) is a comprehensive toolkit designed to streamline and unify various argument mining modules into a single platform.',
    author='Debela',
    author_email='d.t.z.gemechu@dundee.ac.uk',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'transformers',
        'torch',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


