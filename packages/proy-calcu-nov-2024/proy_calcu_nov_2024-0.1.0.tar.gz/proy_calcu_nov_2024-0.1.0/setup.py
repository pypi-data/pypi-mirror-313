from setuptools import setup, find_packages

setup(
    name="proy_calcu_nov_2024",  # Nombre del paquete en PyPI
    version="0.1.0",  # Versión inicial
    author="RASEC_2024",
    author_email="csanchezc.sdigitales@gmail.com",
    description="Una calculadora básica con funciones simples",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/mi_calculadora_basica",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "wheel",
        "twine"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
