from setuptools import setup, find_packages

setup(
    name="nmtextprocessor1",  # Name of your package
    version="0.1.0",  # Initial version
    author="Nidhi Mahandru",  # Your name
    author_email="nidhimahendru@gmail.com",  # Your email
    description="A text processing library for various NLP tasks",  # Short description
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",  # Format of the long description
    #url="https://github.com/yourusername/nmtextprocessor",  # Project homepage URL
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[  # External dependencies
        
    ],
    classifiers=[  # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version required
    
)