from setuptools import setup, find_packages

setup(
    name="aptio",
    version="0.0.1",
    author="Arye Zamir",
    author_email="arye.zamir@gmail.com",
    description="Aptio package manager.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arye-zamir/aptio",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
