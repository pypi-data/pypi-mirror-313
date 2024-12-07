from setuptools import setup, find_packages

setup(
    name="mysqlmigratorpostgree",
    version="0.1.0",
    description="Libreria pensada para migrar datos a postgresql de manera versatil auto modulando simplificado el codigo",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="archenthusiastic",
    author_email="abuawadsantiago@gmail.com",
    url="https://github.com/archenthusiastic/mysql-migrator-postgreesql",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python", 
        "psycopg2",                
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
