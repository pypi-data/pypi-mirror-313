from setuptools import setup, find_packages

setup(
    name="catbench",
    version='0.1.18',
    author="JinukMoon",
    author_email="jumoon@snu.ac.kr",
    packages=find_packages(),
    description="CatBench: Benchmark of Graph Neural Networks for Adsorption Energy Predictions in Heterogeneous Catalysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JinukMoon/catbench",
    license="MIT",
    install_requires=[
        "ase>=3.22.1",
        "xlsxwriter>=3.2.0",
        "numpy==1.26",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="GNN benchmarking for catalysis",
    python_requires=">=3.8",
)