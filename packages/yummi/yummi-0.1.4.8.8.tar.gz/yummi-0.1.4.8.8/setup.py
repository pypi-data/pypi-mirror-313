from setuptools import setup, find_packages

setup(
    name="yummi",
    version="0.1.4.8.8",
    packages=find_packages(where="."),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
