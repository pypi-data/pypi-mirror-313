from setuptools import setup

with open('/Users/benjamin/Projects/CRBM/astecmanagerelease/requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name = "AstecManager",
    version = "0.2.27",
    author = "Benjamin GALLEAN",
    author_email = "benjamin.gallean@crbm.cnrs.fr",
    description = "This package creates a management system to run the ASTEC algorithms for developmental biology live "
                  "imaging. ",
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url = "https://gite.lirmm.fr/bgallean/astecmanagerelease",
    project_urls = {
        "Bug Tracker": "https://gite.lirmm.fr/bgallean/astecmanagerelease/-/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["AstecManager","AstecManager.libs","AstecManager.atlas","AstecManager.libs.ImageHandling",],
    include_package_data = True,
    install_requires=required
)
