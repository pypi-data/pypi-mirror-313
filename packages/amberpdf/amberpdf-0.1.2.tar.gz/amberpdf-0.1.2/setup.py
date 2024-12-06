from setuptools import setup, find_packages

setup(
    name="amberpdf",
    version="0.1.2",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyMuPDF>=1.18.0",
        "boto3>=1.26.0",
        "pandas"
    ],
    author="Paulo Suclly",
    author_email="paulo.suclly@pucp.edu.pe",
    description="Librería que procesa un PDF mixto (texto e imágenes/tablas) y extrae el contenido en orden",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amberpdf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
