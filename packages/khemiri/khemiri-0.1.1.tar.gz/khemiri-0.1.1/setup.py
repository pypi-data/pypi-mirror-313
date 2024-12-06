from setuptools import find_packages, setup

setup(
    name="khemiri",
    version="0.1.1",
    # description="An id generator that generated various types and lengths ids",
    package_dir={"": "assets"},
    packages=find_packages(where="assets"),
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/ArjanCodes/2023-package",
    author="khemiri",
    # author_email="khemiri@khemiri.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    # install_requires=["bson >= 0.5.10"],
    # extras_require={
    #     "dev": ["pytest>=7.0", "twine>=4.0.2"],
    # },
    python_requires=">=3.10",
)