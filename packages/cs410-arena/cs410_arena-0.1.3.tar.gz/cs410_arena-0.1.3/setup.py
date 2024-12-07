from setuptools import setup, find_packages

setup(
    name="cs410-arena",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3",
        "flask>=2.0.0",
        "requests>=2.25.1"
    ],
    author="John Wu",
    author_email="john_wu@brown.edu",
    description="A Go game arena for CS410 bot competitions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brown-cs-410/cs410-arena",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
