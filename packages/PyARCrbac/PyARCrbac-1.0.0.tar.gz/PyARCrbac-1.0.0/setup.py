from setuptools import setup, find_packages
import os
from pathlib import Path

here = os.path.abspath(os.path.dirname(__file__))
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '1.0.0'
DESCRIPTION = 'A Library that simplifies interaction with Azure / ARC Metadata services.'

# Setting up
setup(
    name="PyARCrbac",
    version=VERSION,
    author="ikbendion (dblonk)",
    author_email="<contact@ikbendion.nl>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    Homepage = "https://github.com/ikbendion/PyARCrbac",
    Issues = "https://github.com/ikbendion/PyARCrbac/issues", 
    readme = "README.MD",
    keywords=['python', 'azure', 'rbac', 'azurearc', 'authentication', 'azmanagement'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    project_urls={
        'Source': 'https://github.com/ikbendion/PyARCrbac',
    },
    license="MIT"
)
