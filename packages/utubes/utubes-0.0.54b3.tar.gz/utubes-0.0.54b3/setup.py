from Utubes import appname, version, install, classis
from setuptools import setup, find_packages
with open("README.md", "r") as o:
    description = o.read()

setup(
    name=appname,
    license='MIT',
    version=version,
    description='ㅤ',
    classifiers=classis,
    python_requires='~=3.10',
    packages=find_packages(),
    install_requires=install,
    long_description=description,
    url='https://github.com/Monisha',
    keywords=['python', 'youtube', 'extension'],
    long_description_content_type="text/markdown")
