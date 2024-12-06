from setuptools import setup, find_packages

setup(
    name='Game_generation_utils',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'opensimplex',
        'numpy',
        'matplotlib',
        'plotly',
        'pandas',
        'nbformat',
    ],
    entry_points={
        'console_scripts': [
            # Add your command line scripts here
        ],
    },
    author='Luis Miguel Trinidad Salvador',
    author_email='your.email@example.com',
    description='A 2D terrain generation utility',
    url='https://github.com/LuisMiguelTrinidad/2d-terrain-Gen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)