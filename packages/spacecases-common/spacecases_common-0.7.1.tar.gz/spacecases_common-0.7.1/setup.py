from setuptools import setup, find_packages


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


def read_file(file):
    with open(file) as f:
        return f.read()


long_description = read_file("README.md")
version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name="spacecases-common",
    version=version,
    author="William Redding",
    author_email="williamdredding@proton.me",
    description="Common code shared across SpaceCases projects",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="GPL-3 license",
    packages=find_packages(),
    package_data={"spacecases_common": ["py.typed"]},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
