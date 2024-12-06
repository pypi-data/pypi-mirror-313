from setuptools import setup, find_packages

setup(
    name="listwizard",
    version="0.1.1",
    author="o_Frun",
    author_email="fran.cesljas@skole.hr",
    description="Python biblioteka za analiziranje i manipuliranje listama.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/listwizard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
