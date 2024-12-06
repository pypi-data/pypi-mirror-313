from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="musicas_cristianas",
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    author="Eric Hernan Ortiz Lozano",
    description="Paquete para obtener datos de canciones cristianas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url= "https://www.youtube.com"

)