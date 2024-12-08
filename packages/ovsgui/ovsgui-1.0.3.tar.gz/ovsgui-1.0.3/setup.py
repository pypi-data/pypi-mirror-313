from setuptools import setup, find_packages

setup(
    name="ovsgui",
    version="1.0.3",
    author="ArsTech",
    packages=find_packages(),
    author_email="arstechai@gmail.com",
    description="Online Variable System GUI - A GUI for managing online variables through Firebase",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/e500ky/ovsgui",  # Buraya GitHub linkinizi ekleyin
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
    entry_points={
        'console_scripts': [
            'ovsgui = ovsgui.__init__:main',  # terminalde 'ovsgui' komutuyla başlatacak
        ],
    },
)
