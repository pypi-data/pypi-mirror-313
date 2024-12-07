from setuptools import setup, find_packages

setup(
    name="NashUtils", 
    version="0.1.0", 
    description="This package contains Utlitiy tools for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohammed Althaf",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",  # Repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your dependencies here, e.g.,
        # "numpy>=1.19.0",
    ],
)
