from setuptools import find_packages, setup

VERSION = "0.0.5"
DESCRIPTION = "A python package for using the https://sourcestack.co/ API."

with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()
    LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

setup(
    name="sourcestack",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
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
