import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyPhasesRecordloader",
    version="v0.7.2"[1:],
    author="Franz Ehrlich",
    author_email="fehrlichd@gmail.com",
    description="Adds a record loaders to the pyPhases package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tud.ibmt.public/pyphases/pyphasesrecordloader/",
    packages=setuptools.find_packages(),
    package_data={"": ["*.yaml"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyPhases", "numpy", "tqdm", "pandas"],
    python_requires=">=3.5",
)
