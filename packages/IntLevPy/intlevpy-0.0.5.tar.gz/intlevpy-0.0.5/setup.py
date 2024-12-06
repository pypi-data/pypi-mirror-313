from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

try:
    with open("authors.rst", "r") as authors_file:
        long_description += "\n\n" + authors_file.read()
except FileNotFoundError:
    long_description += "\n\nFor a detailed list of contributors, visit: [Contributors Page](https://intlevpy.readthedocs.io/en/latest/authors.html#contributors)."


setup(
    name="IntLevPy",
    version="0.0.5",
    author="Shailendra Bhandari",
    author_email="shailendra.bhandari@oslomet.no",
    description="A Python toolkit for simulating intermittent processes and Levy flights.",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url="https://github.com/shailendrabhandari/IntLevy-Processes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
