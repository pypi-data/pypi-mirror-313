from setuptools import setup, find_packages

setup(
    name="hub77_manager",  # Agora sem o hífen
    version="0.1.2",
    author="Vinicius Moreira",
    author_email="vinicius@77indicadores.com.br",
    description="Facilitador para hub das automações e scraper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/77-Indicadores/modulo_hubdados",
    packages=find_packages(),  # Automaticamente encontra o pacote
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
