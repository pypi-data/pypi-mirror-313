from setuptools import setup, find_packages

setup(
    name="ablelabs",
    version="0.0.64",
    description="",
    author="sypark",
    author_email="sy.park@ablelabsinc.com",
    url="https://github.com/ABLE-Labs/ABLE-API",
    install_requires=[
        "et-xmlfile>=1.1.0",
        "future>=1.0.0",
        "iso8601>=2.1.0",
        "loguru>=0.7.2",
        "openpyxl>=3.1.5",
        "pyserial>=3.5",
        "PyYAML>=6.0.1",
    ],
    packages=find_packages(exclude=[]),
    keywords=["ablelabs"],
    python_requires=">=3.10",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
)
