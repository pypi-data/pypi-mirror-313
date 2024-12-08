import setuptools

with open('./Agently/requirements.txt') as f:
    origin_requirements = f.read().splitlines()

requirements = []
for requirement in origin_requirements:
    if not requirement.startswith("#"):
        requirements.append(requirement)

setuptools.setup(
    name = "Agently",
    version = "3.4.1.0",
    author = "Maplemx",
    author_email = "maplemx@gmail.com",
    description = "Agently, a framework to build applications based on language model powered intelligent agents.",
    long_description = "https://github.com/Maplemx/Agently",
    url = "https://github.com/Maplemx/Agently",
    license='Apache License, Version 2.0',
    packages = setuptools.find_packages(),
    package_data = {"": ["*.txt", "*.ini"]},
    install_requires= requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
