import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SecuriPy",
    version="3.0.2",
    author="Anupam Kanoongo",
    author_email="programmer.tiak@gmail.com",
    description="Encrypter and Decrypter of all types of human-readable file formats and much more Using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/SecuriPy",
    project_urls={
        "Our Website": "https://anupam1707.github.io/",
        "Our YT Handle": "https://youtube.com/@developer.anupam"
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["SecuriPy"],
    python_requires=">=3.6"
)