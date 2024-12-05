from setuptools import setup, find_packages

setup(
    name="lance-image-converter",  # The package name
    version="0.1.0",               # Version of the package
    description="A package to convert image datasets to Lance format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vipul Maheshwari",                  
    author_email="vim.code.level@gmail.com",  
    url="https://github.com/lancedb/lance-deeplearning-recipes/tree/main/converters/lance-image-dataset-converter",
    packages=find_packages(),             # Automatically find all packages
    install_requires=[
        "pyarrow",                        # Required dependencies
        "pillow",                         
        "tqdm",
        "lance",
        "pandas",
        "lancedb"
    ],
    entry_points={                        # This defines the command-line entry point
        'console_scripts': [
            'convert-lance = converter.converter:main',  # This should point to your main function
        ],
    },
    classifiers=[                         # Helps classify the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Ensure Python version compatibility
)
