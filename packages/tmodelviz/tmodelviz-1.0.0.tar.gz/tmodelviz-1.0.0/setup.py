from setuptools import setup, find_packages

setup(
    name="tmodelviz",               # Package name
    version="1.0.0",                      # Version number
    description="Interactive visualization for Tellurium simulations",
    long_description=open("README.md").read(),  # Readme for PyPI description
    long_description_content_type="text/markdown",
    author="Shajesh Sharma",
    author_email="shajesh.sharma@colorado.edu",
    url="https://github.com/shajeshsharma/tmodelviz",  # Project URL
    packages=find_packages(),            # Automatically find package directories
    install_requires=[                   # Dependencies
        "tellurium",
        "matplotlib",
        "numpy",
        "ipywidgets"
    ],
    classifiers=[                        # Metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",             # Minimum Python version
)