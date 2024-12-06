from setuptools import setup, find_packages, find_namespace_packages
from seeq.data_lab_env_mgr._version import __version__

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = parse_requirements('requirements.txt')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='seeq-data-lab-env-mgr',
    version=__version__,
    install_requires=requirements,
    python_requires='>=3.8',
    packages=find_namespace_packages(include=['seeq.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Seeq Corporation',
    author_email='support@seeq.com',
    description='Data Lab Environment Manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/seeq12/seeq-data-lab-env-mgr'
)
