from setuptools import setup, find_packages

setup(
    name='model_ELISA',  
    version='0.1.2',  
    packages=find_packages(),  
    install_requires=['numpy', 'matplotlib', 'tellurium'],  # List of dependencies if any
    description='A GUI to simulate the direct ELISA model',  
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    author='Kelsey Leong',
    author_email='kml5gb@uw.edu',
    url='https://github.com/kml5gb/model_ELISA',
    classifiers=[  # Helps people find your package based on categories
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
