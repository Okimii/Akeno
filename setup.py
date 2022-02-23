from distutils.core import setup
import pathlib
import akeno

ROOT = pathlib.Path(__file__).parent
with open(ROOT / "README.md", "r", encoding="utf-8") as f:
    README = f.read()
VERSION = akeno.__init__.__version__

setup(
    name="Akeno",
    packages=["akeno"],
    version=VERSION,
    license="MIT",
    description="Module to interact with the twitter api",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Okimii",
    url="https://github.com/Okimii/Akenog",
    keywords=["twitter", "api"],
    project_urls={
        "Code": "https://github.com/Okimii/Akeno",
    },
    install_requires=[
        "aiohttp",
        "sphinx_book_theme",
        "furo",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)