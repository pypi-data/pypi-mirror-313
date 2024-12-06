import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='api-test-2024-12-4',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/MiaoMiaoMeo/api-test',
    license='MIT',
    author='MiaoMiaoMeo',
    description='Just a simple api test',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    classifiers=[],
    python_requires='>=3.7'
)
