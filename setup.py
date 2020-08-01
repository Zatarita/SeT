import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Zatarita",
    version="0.0.1",
    author="Zatarita",
    author_email="richarda.mooreiii@gmail.com",
    description="Saber management toolset",
    long_description="do this eventually",
    long_description_content_type="text/markdown",
    url="https://github.com/Zatarita/SeT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
