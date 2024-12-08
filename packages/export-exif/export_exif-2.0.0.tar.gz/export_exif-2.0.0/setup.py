from setuptools import setup, find_packages

setup(
    name="export-exif",
    version="2.0.0",
    packages=find_packages(),
    description="Une bibliothèque pour traiter des images avec EXIF",  # Courte description
    long_description=open("README.md", "r").read(),  # Description détaillée
    long_description_content_type="text/markdown",  # Type de contenu (Markdown)
    author="Fabrice Kopf",
    author_email="contact@fabricekopf.fr",
    url="https://github.com/Jean-LouisB/ExifRecup.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Version minimale de Python
    install_requires=[
        "exif",  # Dépendances (par exemple : exif)
        "pathlib",
    ],
)

