from setuptools import setup, find_packages

with open("README.md", "r") as file_readme:
    description = file_readme.read()

setup(
    name='psyLo',
    version='0.0.10',
    packages=find_packages(),
    install_requires=[],
    #entry_points={
        #"console_scripts": [
        #    "command_name = psyLo:finction_name",
        #    "testLib = psyLo:testLib"
        #],
    #},

    long_description=description,
    long_description_content_type="text/markdown",

    author="IshaanShinde"
)