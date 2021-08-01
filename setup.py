from setuptools import setup, find_namespace_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements_dev.txt") as f:
    requirements_dev = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="trifle",
    version="0.1.0",
    description="Trifle Resolves Intricate Figures Layout Effortlessly",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_namespace_packages(exclude=("docs", "tests*")),
    include_package_data=True,
    url="https://github.com/vigji/trifle",
    author="Luigi Petrucco",
    author_email="luigi.petrucco@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
    ],
    zip_safe=False,
)
