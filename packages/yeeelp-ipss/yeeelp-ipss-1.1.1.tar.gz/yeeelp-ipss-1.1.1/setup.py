from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.1'
DESCRIPTION = 'Dependency Confusion Attack'
LONG_DESCRIPTION = 'Python package demonstrating a dependency confusion vulnerability POC. The impact of this vulnerability is Remote Code Execution (RCE).'

# Setting up
setup(
    name="yeeelp-ipss",  # Package name
    version='1.1.1',  # Version number
    author="Mufasa",  # Replace with your actual name
    author_email="no1xjohnwick@gmail.com",  # Replace with your email
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],  # Removed 'discord'
    keywords=['dependency confusion', 'supply chain attack', 'RCE', 'vulnerability'],
)
