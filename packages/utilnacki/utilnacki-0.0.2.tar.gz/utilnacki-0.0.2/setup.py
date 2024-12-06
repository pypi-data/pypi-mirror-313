from setuptools import find_packages, setup

setup(
    name="utilnacki",
    version="0.0.2",
    description="A package containing all non-project-specific helpers",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description="My long description",
    long_description_content_type="text/markdown",
    url="https://github.com/bernackimark/utilnacki",
    author="Bernacki",
    author_email="bernackimark@gmail.com",
    extras_require={"dev": "twine>=4.0.2"},
    python_requires=">=3.11",
)
