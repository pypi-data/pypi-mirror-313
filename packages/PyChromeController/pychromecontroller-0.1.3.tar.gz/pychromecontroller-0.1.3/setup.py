from setuptools import setup, find_packages

setup(
    name="PyChromeController",  # Name des Packages
    version="0.1.3",  # Versionsnummer
    description="A Python package to control Chrome browser actions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Format der README
    author="Michael Christian Dörflinger",
    author_email="michaeldoerflinger93@gamil.com",
    license="MIT",
    url="https://github.com/Michdo93/PyChromeController",  # GitHub-Link
    packages=find_packages(),  # Findet alle Packages (inkl. __init__.py)
    install_requires=open("requirements.txt").read().splitlines(),  # Abhängigkeiten
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Mindest-Python-Version
)
