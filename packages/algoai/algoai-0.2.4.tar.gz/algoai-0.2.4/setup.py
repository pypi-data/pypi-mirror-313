from setuptools import setup, find_packages

setup(
    name='algoai',  
    version='0.2.4',
    packages=find_packages(),
    install_requires=[  
        'numpy',   
        'networkx', 
        'pgmpy',
        
    ],
    author='Leander',
    author_email='leander.antony2023@gmail.com',
    description='A collection of AI algorithms',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
