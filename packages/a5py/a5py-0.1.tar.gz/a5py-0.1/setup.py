import configparser
import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        # create_ini_from_dict(config_data, config_path)
        super().run()

setup(
    name="a5py",
    version="1.0",
    packages=find_packages(),
    description='a5 hydrometeorologic database management system',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Juan F. Bianchi',
    author_email='jbianchi@ina.gob.ar',
    url='https://github.com/jbianchi81/a5_client',
    cmdclass={
        "install": CustomInstallCommand,
    },
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "gdal==3.8.4",
        "numpy",
        "psycopg2",
        "sqlalchemy",
        "geoalchemy2",
        "rasterio",
        "shapely"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'a5py=a5py.a5py_cli:main',
            'a5py_config=a5py.config:run',
        ],
    },
)

