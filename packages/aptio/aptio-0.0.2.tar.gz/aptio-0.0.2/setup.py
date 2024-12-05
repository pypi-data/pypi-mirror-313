from setuptools import setup, find_packages

description: str

with open("README.md", "r", encoding="utf-8") as fp:
    description = fp.read()

setup(
    name="aptio",
    version="0.0.2",
    author="Arye Zamir",
    author_email="arye.zamir@gmail.com",
    description="Aptio package manager.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/arye-zamir/aptio",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9, <4.0",
)
