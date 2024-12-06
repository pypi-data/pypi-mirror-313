from setuptools import setup, find_packages

setup(
    name='lumtina',
    version='0.2.7',
    packages=find_packages(),
    description='Lumtina is a Python package for various utilities.',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='Simo',
    author_email='cardellasimone10@gmail.com',
    url='https://github.com/sonosimooo/Lumtina',  
    install_requires=[
        'colorama'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
