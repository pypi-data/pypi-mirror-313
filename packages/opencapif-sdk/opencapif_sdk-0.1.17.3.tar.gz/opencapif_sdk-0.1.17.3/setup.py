from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README_pipy.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="opencapif_sdk",
    version="0.1.17.3",
    author="JorgeEcheva, dgs-cgm",
    author_email="jorge.echevarriauribarri.practicas@telefonica.com, daniel.garciasanchez@telefonica.com",
    description=(
        "This repository develops a Python Software Development Kit(SDK) which focuses on "
        "connecting to OpenCAPIF (Common API Framework for 3GPP Northbound APIs) in a simple way, "
        "lowering integration complexity and allowing developers to focus on Network Applications (Network Apps) or services development."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="LICENSE",
    python_requires=">=3.9",
    keywords=[
        "pesp_capif_sdk", "capif", "sdk capif", "opencapif_sdk"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["opencapif_sdk", "opencapif_sdk.*"]),  # Ajusta según tus necesidades
    install_requires=[
        "requests==2.32.3",
        "PyYAML==6.0.1",
        "cryptography==38.0.4",
        "pyOpenSSL==22.1.0",
        "urllib3==2.2.2",
        "certifi==2024.7.4",
        "idna==3.7",
        "Flask==3.0.3",
        "Flask-JWT-Extended==4.6.0",
        "Jinja2==3.1.4",
        "MarkupSafe==2.1.5",
        "six==1.16.0",
        "typing-extensions>=4.8.0",
        "Werkzeug==3.0.4",
        "pytest==8.3.2",
        "flake8==3.9.2",
        "coverage==4.5.4",
        "mccabe==0.6.1",
        "pycodestyle==2.7.0",
        "pyflakes==2.3.1",
        "python-dateutil==2.9.0.post0",
        "jinja2-time==0.2.0",
        "text-unidecode==1.3",
        "binaryornot==0.4.4",
    ],
    url="https://github.com/Telefonica/pesp_capif_sdk",
)
