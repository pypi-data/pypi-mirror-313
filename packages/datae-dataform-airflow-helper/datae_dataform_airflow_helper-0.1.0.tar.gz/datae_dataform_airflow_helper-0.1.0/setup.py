from setuptools import setup, find_packages
setup(
name='datae_dataform_airflow_helper',
version='0.1.0',
author='DATAE',
description='Airflow helper creating datafrom tasks.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)