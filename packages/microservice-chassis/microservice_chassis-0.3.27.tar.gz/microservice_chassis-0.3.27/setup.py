from setuptools import setup, find_packages

setup(
    name="microservice_chassis",
    version="0.3.27",
    packages=find_packages(),
    install_requires=[
        "PyJWT",        # Dependencias que tu librería necesita
        "SQLAlchemy",
    ],
    author="Microservice chassis",
    description="Chassis para microserviccdios en Python",
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/microservice_chassis",
)