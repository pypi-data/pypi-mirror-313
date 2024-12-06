from setuptools import setup, find_packages

# TEST PYPI TOKEN
# pypi-AgENdGVzdC5weXBpLm9yZwIkNzQ3ZDk5NWItZmZlNS00NGQ5LTk1YjMtZDk4ODZmMmE5YmZkAAIqWzMsImUwNmZmNmE5LWFhNjgtNGY3ZS05MGE2LTMyZjZhYjZhMTUwNSJdAAAGIJmRQzoTbPzDUkpxzH9uqX3M1KYw9V0dBxWCk6Pxu9TP
# PYPI TOKEN
# pypi-AgEIcHlwaS5vcmcCJDcyMjZiODcxLTExNGQtNDZjZC05MjY0LTQ0ZmE4OGQ3MjQ5MQACKlszLCI5NTE5NDA1Yi04YjYwLTQwZDYtYTUxNi00ZWRhNDdmOWFmMjIiXQAABiBBU6Hokm40O1uf_zRGl_xok37g-RV-HGtEOUQvCTy5Dg


setup(
    name="geogeometry",
    version="0.0.2",
    description="A Python geometrical library made for geotechnical engineering.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jorge Martinez",
    author_email="jmartinez@gmintec.com",
    license="MIT",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)