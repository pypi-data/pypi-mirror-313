from setuptools import setup, find_packages

setup(
    name="zennewpy",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
	'requests',
	'tabulate', 
    ],
    author="Marco Mancini",
    author_email="marco.mancini@obspm.fr",
    description="Client to work with Zenodo API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zennewpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
