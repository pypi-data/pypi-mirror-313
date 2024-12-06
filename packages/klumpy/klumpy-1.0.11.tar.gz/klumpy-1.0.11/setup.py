from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    description = fh.read()

setup(name="klumpy",
      version="1.0.11",
      packages=find_packages(),
      python_requires=">=3.6.0", 
      install_requires=["pycairo"],
      description="A package to evaluate genome assemblies and detect sequence motifs",
      long_description=description,
      long_description_content_type="text/markdown",
      author_email="gm33@illinois.edu",
      classifiers=["Programming Language :: Python :: 3","Operating System :: POSIX", "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
      author="Giovanni Madrigal <gm33@illinois.edu>, Bushra Fazal Minhas <bfazal2@illinois.edu>, Julian Catchen <jcatchen@illinois.edu>",
      scripts=["scripts/klumpy"])