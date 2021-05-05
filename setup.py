import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hellofresh-interview",
    version="0.0.1",
    author="Mehrad Abdollahi",
    author_email="mhr.abdollahi@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehradabd/hellofresh-interview",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=[
        "pandas",
        "json",
        "re"
    ],
    python_requires=">3.7"
)
