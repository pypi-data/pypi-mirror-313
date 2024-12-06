import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arlas_cli",
    entry_points={'console_scripts': ['arlas_cli=arlas.cli.cli:main']},
    version="26.2.3",
    author="Gisaïa",
    description="ARLAS Command line for ARLAS Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    py_modules=["arlas.cli.cli", "arlas.cli.collections", "arlas.cli.index", "arlas.cli.settings", "arlas.cli.variables", "arlas.cli.service", "arlas.cli.model_infering", "arlas.cli.configurations", "arlas.cli.persist", "arlas.cli.iam", "arlas.cli.user", "arlas.cli.org", "arlas.cli.arlas_cloud"],
    package_dir={'': 'src'},
    install_requires=[
        "click==8.1.7",
        "typer==0.9.0",
        "python-dateutil==2.8.2",
        "envyaml==1.10.211231",
        "PyJWT==2.8.0",
        "attrs==23.2.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "prettytable==3.9.0",
        "pydantic==2.5.3",
        "alive-progress==3.1.5",
        "shapely==2.0.2",
        "python-dateutil==2.8.2",
        "geojson==3.1.0",
        "numpy==1.26.4"
    ]
)
