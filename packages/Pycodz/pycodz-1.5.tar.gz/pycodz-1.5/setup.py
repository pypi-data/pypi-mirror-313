import setuptools

with open("README.md", "r" , encoding="utf-8") as fh:
    lng_description = fh.read()
setuptools.setup(
    name = "Pycodz",
    version = "1.5",
    author=  "AlEx",
    author_email="alexcrow221@gmail.com",
    long_description_content_type="text/markdown",
    description = "- simple library with python",
    long_description=lng_description,
    python_requires=">=3.6",
    url="https://github.com/A-X-1/test-lib",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)