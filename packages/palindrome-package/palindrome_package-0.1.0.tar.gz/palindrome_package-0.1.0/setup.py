from setuptools import setup, find_packages

setup(
    name="palindrome_package",
    version="0.1.0",
    author="Dattasai",
    author_email="gadi.dattasai@gmail.com",
    description="A simple package for checking palindromic numbers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dattasai0612/Python_Practice",  # Replace with your project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
