from setuptools import setup, find_packages

setup(
    name="ovsgui",
    version="1.0.0",
    author="ArsTech",
    author_email="arstechai@gmail.com",
    description="GUI for the Online Variables System (OVS)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/e500ky/ovsgui",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "customtkinter>=5.0.0",
        "firebase-admin>=6.0.0",
        "python-dotenv>=1.0.0",
    ],
)
