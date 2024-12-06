from setuptools import setup, find_packages

setup(
    name="nael-utils",
    version="0.1.1",
    description="Commonly useful utilities",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Nathanael",
    author_email="nael.nathanael71@gmail.com",
    url="https://github.com/Nael-Nathanael/nael-utils",
    packages=find_packages(),
    install_requires=[
        "langchain-core",
        "langchain-openai",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License (choose accordingly)
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum required Python version
)
