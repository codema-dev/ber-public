from setuptools import setup
import versioneer

requirements = [
    "dask",
    "pyarrow",
    "pandas",
    "requests",
    "tqdm",
]

dev_requires = ["black"]
test_requires = ["pytest", "pytest-cov"]
extras = {
    "all": requirements + test_requires + dev_requires,
    "dev": test_requires + dev_requires,
}

setup(
    name="ber_public",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A Python toolkit for the SEAI's BER public dataset ",
    license="MIT",
    author="Rowan Molony",
    author_email="rowan.molony@codema.ie",
    url="https://github.com/rdmolony/ber-public",
    packages=["ber_public"],
    entry_points={"console_scripts": ["ber_public=ber_public.cli:cli"]},
    install_requires=requirements,
    extras_require=extras,
    keywords="ber_public",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
