from setuptools import setup, find_packages

setup(
    name="sparta-teams-notifications",
    version="1.0.4",
    description="Função de callback para integração entre airflow e teams",
    author="Henrique Gomes Nunes",
    author_email="henrique.gomes@sparta.com.br",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "apache-airflow",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
