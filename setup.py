from setuptools import setup, find_packages

setup(
    name='argumentminingnlp',
    version='0.1',
    description='A library for argument mining using state-of-the-art NLP models.',
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


