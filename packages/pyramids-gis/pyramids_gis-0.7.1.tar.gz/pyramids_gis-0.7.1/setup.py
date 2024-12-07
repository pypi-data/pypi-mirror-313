from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [line.strip() for line in open("requirements.txt").readlines()]
requirements_dev = [line.strip() for line in open("requirements-dev.txt").readlines()]
requirements_all = [
    line.strip() for line in open("requirements-optional-packages.txt").readlines()
]

setup(
    name="pyramids-gis",
    version="0.7.1",
    description="GIS utility package",
    author="Mostafa Farrag",
    author_email="moah.farag@gmail.com",
    url="https://github.com/Serapieum-of-alex/pyramids",
    keywords=["GIS", "gdal"],
    long_description=readme + "\n\n" + history,
    repository="https://github.com/MAfarrag/pyramids",
    documentation="https://pyramids-gis.readthedocs.io/",
    long_description_content_type="text/markdown",
    license="GNU General Public License v3",
    zip_safe=False,
    packages=find_packages(include=["pyramids", "pyramids.*"]),
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "viz": ["cleopatra>=0.4.0"],
        "all": requirements_all,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
    package_data={"": ["gdal_drivers.yaml", "ogr_drivers.yaml", "config.yaml"]},
)
