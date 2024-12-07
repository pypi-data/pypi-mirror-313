from setuptools import setup, find_packages

setup(
    name="hub77-manager",  # Nome do pacote no PyPI
    version="0.1.1",            # Versão inicial
    author="Vinicius Moreira",
    author_email="vinicius@77indicadores.com.br",
    description="Facilitador para hub das automações e scraper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/77-Indicadores/modulo_hubdados",  # Substitua pelo link do repositório
    packages=find_packages(),  # Automaticamente encontra os pacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.0.0",
    ],
)
