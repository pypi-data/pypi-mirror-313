from setuptools import setup, find_packages

setup(
    name="cognidb",
    version="0.2.5",
    packages=find_packages(),
    install_requires=[
        "openai",
        "psycopg2",
        "mysql-connector-python",
        "sqlparse",
    ],
    entry_points={
        "console_scripts": [
            "cognidb=cognidb.__main__:main",
        ],
    },
    author="Rishabh Kumar",
    author_email="rishabh.vaaiv@gmail.com",
    description="A tool for generating SQL queries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/boxed-dev/cognidb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
