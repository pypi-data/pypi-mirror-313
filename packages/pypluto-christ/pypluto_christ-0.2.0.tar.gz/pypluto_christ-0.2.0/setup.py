from setuptools import setup, find_packages

setup(
    name='pypluto-christ',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],
    author='Shrey Jain',
    author_email='shrey.jain@mca.christuniversity.in',
    description='A library for controlling Pluto drones for the Christ University projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Drone-Club-ChristUniversity/plutoControlUpdated.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
