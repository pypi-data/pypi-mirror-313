from setuptools import setup, find_packages

setup(
    name="vdntru",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.0"
    ],
    description="NTRU Encryption and Decryption using AES and RSA.",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
