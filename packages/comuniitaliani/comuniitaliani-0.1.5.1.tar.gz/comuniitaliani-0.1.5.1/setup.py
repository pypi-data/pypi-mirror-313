from setuptools import setup, find_packages

setup(
    name="comuniitaliani",
    version="0.1.5.1",
    description="Libreria Python per ottenere informazioni sui comuni italiani dal file ISTAT",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Andrea Carboni",
    author_email="andreacarboni@stepservizi.net",
    url="https://github.com/cvrboni/comuniitaliani",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "comuniitaliani": ["database/comuni.csv"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.0.0"
    ],
)
