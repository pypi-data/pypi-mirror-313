import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="melpy",
    version="1.0.0.3",
    author="Lenny Malard",
    author_email="lennymalard@gmail.com",
    description="Melpy is a package made to learn machine learning and make its uses as simple as possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[                      
        "numpy>=1.18.0",
        "matplotlib>=3.2.0",
        "tqdm>=4.50.0"                                            
    ],                                             
    url="https://github.com/lennymalard/melpy-project",  
    packages=setuptools.find_packages(),
    classifiers=[                                 
        "Programming Language :: Python :: 3",   
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",  
        "Development Status :: 1 - Planning",
        "Natural Language :: French",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
)