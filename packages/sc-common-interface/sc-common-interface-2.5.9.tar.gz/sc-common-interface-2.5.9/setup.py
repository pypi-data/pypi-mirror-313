from setuptools import setup, find_packages

setup(
    name='sc-common-interface',
    version='2.5.9',
    description='SC贴文销售公用的接口',
    author='river',
    packages=find_packages(),
    install_requires=[
    "requests>=2.0.0",
    "jsonpath>=0.82",
             ],
)
