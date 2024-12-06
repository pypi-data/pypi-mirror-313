from setuptools import setup, find_packages

setup(
    name="cast-planet-api",
    version="0.1.3",
    author="Center for Advanced Spatial Technologies",
    author_email="cast@uark.edu",
    description="A package for searching and retrieving imagery via the Planet REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://castuofa.github.io/cast-planet-api",
    packages=find_packages(),
    install_requires=[
        "pydantic", "pydantic-settings", "pydantic-geojson",
        "requests", "tqdm", "geopandas", "pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)