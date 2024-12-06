from setuptools import setup, find_packages

setup(
    name='endetail_utilities',
    version='1.1.0',
    packages=find_packages(),

)
# python setup.py sdist bdist_wheel
# twine upload --repository-url http://localhost:8080/ dist/*