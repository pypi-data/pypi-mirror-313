from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
	log_description = fh.read()

setup(
	name="psswd_manager",
	version="0.1.1",
	packages=find_packages(),
	install_requires=[],
	author="Sammy-ulfh",
	description="A library to generate and manage passwords in your scripts.",
	long_description=log_description,
	long_description_content_type="text/markdown",
	url="https://github.com/sammy-ulfh/Python-packages",
)
