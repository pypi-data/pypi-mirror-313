from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
	log_description = fh.read()

setup(
	name="hack4u_sammy-ulfh",
	version="0.1.1",
	packages=find_packages(),
	install_requires=[],
	author="Sammy-ulfh",
	description="Una biblioteca para consultar cursos de hack4u.",
	long_description=log_description,
	long_description_content_type="text/markdown",
	url="https://hack4u.io",
)
