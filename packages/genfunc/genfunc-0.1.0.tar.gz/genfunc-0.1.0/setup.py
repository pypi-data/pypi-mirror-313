from setuptools import setup, find_packages

setup(
    name="genfunc",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv>=0.10.0",
    ],
    author="Argish",
    author_email="argish.official@gmail.com",
    description="A Python package for generating functions using LLMs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/argishh/genfunc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
