from setuptools import setup
from pygyat import VERSION_NUMBER

with open("README.md", "r") as fh:
    long_description = fh.read()

# Install python package, scripts and manual pages
setup(name="pygyat",
      version=VERSION_NUMBER,
      author="Shamith Pasula",
      author_email="shamith09@berkeley.edu",
      license="MIT",
      description="Python with rizz",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/shamith09/pygyat",
      scripts=["scripts/gyat2py", "scripts/pygyat", "scripts/py2gyat"],
      data_files=[("man/man1", ["etc/pygyat.1", "etc/py2gyat.1", "etc/gyat2py.1"])],
      packages=["pygyat"],
      zip_safe=False)