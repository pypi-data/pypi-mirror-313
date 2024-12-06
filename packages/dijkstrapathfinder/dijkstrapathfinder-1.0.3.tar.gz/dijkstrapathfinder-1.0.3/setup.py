from setuptools import setup, find_packages

setup(
    name='dijkstrapathfinder',
    version='1.0.3',
    description='A Python module to run algorithms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hariesh',
    author_email='hariesh28606@gmail.com',
    url='https://github.com/Hariesh28/AlgorithmVisualizer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your dependencies here, for example:
        'streamlit',
        'matplotlib',
        'networkx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
