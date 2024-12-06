import os
import re
import setuptools

NAME             = "oatk"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "contact@christophe.vg"
DESCRIPTION      = "A collection of useful functions for dealing with OAuth"
LICENSE          = "MIT"
KEYWORDS         = "oauth human"
URL              = "https://github.com/christophevg/" + NAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Topic :: Security :: Cryptography",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.8",
  "Development Status :: 4 - Beta",
  
]
INSTALL_REQUIRES = [
  "pyjwt",
  "cryptography",
  "python-dotenv",
  "fire",
  "authlib",
  "flask",
  "flask_cors",
  "flask_restful",
  "pymongo",
  "requests",
  
]
ENTRY_POINTS = {
  "console_scripts" : [
    "oatk=oatk.__main__:cli",
    
  ]
}
SCRIPTS = [
  
]

HERE = os.path.dirname(__file__)

def read(file):
  with open(os.path.join(HERE, file), "r") as fh:
    return fh.read()

VERSION = re.search(
  r'__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
  setuptools.setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages(),
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
    scripts=SCRIPTS,
    include_package_data=True    
  )
