import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swapoc", # Replace with your own PyPI username(id)
    version="2.0.0",
    author="swapoc",
    author_email="boj.jerry@gmail.com",
    description="sample rce!!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)