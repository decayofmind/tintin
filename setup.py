from setuptools import setup, find_packages
from pip.req import parse_requirements
from os.path import dirname, join

project_dir = dirname(__file__)
install_reqs = parse_requirements(join(project_dir, 'requirements.txt'))

setup(
    name='tintin',
    version='alpha',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    requires=['requests', 'simplejson', 'bencode']
)
