import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name="geopandas",
    version=versioneer.get_version(),
    description="Geographic pandas extensions",
    license="BSD",
    author="GeoPandas contributors",
    author_email="kjordahl@alum.mit.edu",
    url="http://geopandas.org",
    long_description=LONG_DESCRIPTION,
    packages=[
        "geopandas",
        "geopandas.io",
        "geopandas.tools",
        "geopandas.datasets",
        "geopandas.tests",
        "geopandas.tools.tests",
    ],
    package_data={"geopandas": data_files},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    cmdclass=versioneer.get_cmdclass(),
)