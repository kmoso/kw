import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RealEstate-Real-Kmoso", # Replace with your own username
    version="0.0.1",
    author="Carlos Morlan",
    author_email="kmosog@gmail.com",
    description="Package to test AWS Lambda functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmoso/kw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)