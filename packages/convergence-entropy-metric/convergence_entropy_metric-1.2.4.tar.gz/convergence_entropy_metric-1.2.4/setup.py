from setuptools import setup, find_packages

import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="convergence_entropy_metric",
    author='ZP Rosen',
    version="1.2.4",
    setup_requires=install_requires,
    install_requires=install_requires,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
