from setuptools import find_packages, setup

VERSION = "0.0.2"
DESCRIPTION = "An API for SourceStack"
LONG_DESCRIPTION = "A package that makes it easy to use the https://sourcestack.co/"

setup(
    name="sourcestack",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Kevin Sylvestre",
    author_email="kevin@ksylvest.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    keywords="sourcestack",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
