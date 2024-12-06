from setuptools import setup, find_packages

VERSION = '1.2.5'
DESCRIPTION = 'Loads data.'
LONG_DESCRIPTION = 'Loads simulation data.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="joecomp", 
        version=VERSION,
        author="Joe Williams",
        author_email="joepw1@hotmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        # download_url='https://github.com/AstroWilliams/chemcomp-plotter/archive/refs/tags/v_0.3.8.tar.gz',
        packages=find_packages(),
        install_requires=['tables', 'numpy', 'matplotlib', 'astropy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Scientific/Engineering :: Astronomy",
            # "Operating System :: Microsoft :: Windows",
        ]
)