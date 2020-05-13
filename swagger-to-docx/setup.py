import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swagger-to-docx",
    version="1.0",
    author="Filippo Ferrazini",
    author_email="filippo.ferrazini@gmail.com",
    description="Swagger Converter to Microsoft Word (docx)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Filippo125/swagger-to-docx.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.6',
)