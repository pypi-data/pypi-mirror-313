from setuptools import setup, find_packages

setup(
    name="StreamlinedCryptography",
    version="1.0.0",
    description="A high-level cryptography library for symmetric and asymmetric operations.",
    long_description=open("./StreamlinedCryptography/README.md").read(),
    long_description_content_type="text/markdown",
    author="Preston Coley",
    author_email="prestoncoley0920@proton.me",
    url="https://github.com/HaZeShade/StreamlinedCryptography",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "cryptography>=42.0.7",
    ],
)
