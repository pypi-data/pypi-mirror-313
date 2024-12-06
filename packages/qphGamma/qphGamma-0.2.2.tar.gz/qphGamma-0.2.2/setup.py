from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qphGamma",  # name of package dir below module
    version="0.2.02",
    author="Brian Robinson",
    author_email="b.p.robinson102@gmail.com",
    description="A package for finding quasiparticle and quasihole scattering rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brobinson10296/qphGamma",
    download_url="https://github.com/brobinson10296/qphGamma/archive/main.zip",
    keywords=[
        "first principles",
        "VASP",
        "Fermi gas",
        "Fermi liquid",
        "e-e scattering",
    ],
    packages=find_packages(where="./src"),
    package_dir={"": "src"},
    install_requires=["numpy", "pandas", "scipy", "py4vasp", "plasmapy"],
)
