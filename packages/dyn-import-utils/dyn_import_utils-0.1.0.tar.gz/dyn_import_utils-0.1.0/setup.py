from setuptools import setup, find_packages

setup(
    name="dyn_import_utils",
    version="0.1.0",
    description="A simple package for dynamic imports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="",  
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

