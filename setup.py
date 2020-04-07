from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="maka",
    version="0.0.1",
    author="Gonza Huerta Canepa",
    author_email="gonzalo.huerta@uai.cl",
    description="A set of python classes to retrieve information from the Microsoft Academic Knowledge API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.4",
    install_requires=["requests"],
    url="https://github.com/gfhuertac/maka",
)
