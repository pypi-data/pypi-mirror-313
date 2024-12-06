from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easyprojectstructure",
    version="1.0.1",
    packages=find_packages(),
    author="Sergei Poluektov",
    author_email="seregatipich@outlook.com",
    description="A script to output the directory structure of a Python project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seregatipich/easyprojectstructure",
    entry_points={
        "console_scripts": [
            "getprojectstructure=easyprojectstructure.__main__:main",
            "easyprojectstructure=easyprojectstructure.__main__:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
