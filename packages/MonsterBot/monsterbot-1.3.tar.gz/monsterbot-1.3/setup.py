
from setuptools import setup, find_packages

setup(
    name="MonsterBot",
    version="1.3",  
    packages=find_packages(),
    install_requires=[                
        'requests>=2.0.0',       
    ],
    author="Your Name",
    description="A online chatbot module",
    long_description_content_type='text/markdown',
    url="https://github.com/7lMONSTERl7/networkpwner.git",
    classifiers=[      
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)