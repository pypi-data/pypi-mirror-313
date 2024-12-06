from setuptools import setup, find_packages

setup(
    name="desync_search",
    version="0.1.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for interfacing with the desync_search API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/desync_search",
    packages=find_packages(),
    install_requires=[
        "requests",  # Add any dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
