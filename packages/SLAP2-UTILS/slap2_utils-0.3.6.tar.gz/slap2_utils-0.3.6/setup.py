
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt'), 'r') as f:
    required = f.read().splitlines()



setup(

    name='slap2_utils', 
    version='0.3.6',  

    
    description='Code to support using a SLAP2 Microscope',  

    url='https://github.com/Peter-Hogg/SLAP2_Utils',  

    
    author='Peter Hogg',  

    
    author_email='peter.hogg@ubc.ca',  
    
    classifiers=[ 
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Development Status :: 4 - Beta',


        'Intended Audience :: Researchers',

   
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],


    keywords='python two photon microscope', 

    
    packages=find_packages(exclude=['visual_stim', 'experiments', '*.test']), 
    entry_points={
        'console_scripts': [
            'pySLAP2Viewer=slap2_utils.dataviewer.cli:main',
        ],
    },

    install_requires=required,  


)
