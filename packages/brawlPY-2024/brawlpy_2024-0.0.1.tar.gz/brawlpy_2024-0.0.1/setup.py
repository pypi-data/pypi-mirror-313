from setuptools import setup, find_packages

setup(
    name="brawlPY-2024", 
    version="0.0.1",
    author="gusejuice",
    description="Library for accessing data from Brawl Stars API",
    long_description=open("README.md").read(),
    url="https://github.com/gusejuice/brawlPY",
    packages=find_packages(),
    install_requires=["requests", 
                      "python-dotenv"],
    keywords=["python","API","Brawl Stars"],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)