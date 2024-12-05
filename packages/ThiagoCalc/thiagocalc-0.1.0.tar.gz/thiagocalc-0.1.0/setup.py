from setuptools import setup, find_packages

setup(
    name="ThiagoCalc",
    version="0.1.0",
    author="Thiago",
    author_email="seu.email@example.com",
    description="Uma biblioteca incrível!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu_usuario/ThiagoCalc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
