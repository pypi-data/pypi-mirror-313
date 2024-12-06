from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
  name = "deconomix",
  version = "1.0.0",
  author = "Malte Mensching-Buhr, Thomas Sterr, Nicole Seifert, Dennis Voelkl, Jana Tauschke, Austin Rayford, Helena U. Zacharias, Sushma Nagaraja Grellscheid, Tim Beissbarth,  Franziska Goertler, Michael Altenbuchinger",
  author_email = "michael.altenbuchinger@bioinf.med.uni-goettingen.de",
  description = "Provides methods for cellular composition, hidden background and gene regulation estimation of omics bulk mixtures.",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  packages = find_packages(),
  py_modules = [
    "methods",
    "utils"
  ],
  install_requires = [
    "torch>=2.5.0",
    "numpy>=1.23.0",
    "scikit-learn",
    "qpsolvers>=4.3.2",
    "qpsolvers[quadprog]",
    "qpsolvers[scs]",
    "qpsolvers[clarabel]",
    "matplotlib",
    "pandas>=2.2.2",
    "pyarrow",
    "seaborn",
    "scipy",
    "tqdm>=4.66.4",
    "ipywidgets"
  ]
  )
