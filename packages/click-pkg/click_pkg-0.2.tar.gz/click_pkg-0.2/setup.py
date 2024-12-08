import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

keywords = "click-shop-api, click, click-merchant, click-pkg, click-api, click-python-integration, click-integration, click-python, click-gateway, click-payment, click-payment-gateway, click-integration-python, click-api-client, click-django, click-rest-api" # noqa

setup(
    name='click-pkg',
    version='0.2',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages(),
    url='https://github.com/Muhammadali-Akbarov/click-pkg',
    keywords=keywords,
    install_requires=[
        'requests==2.*',
        "dataclasses==0.*;python_version<'3.7'",  # will only install on py3.6
        'djangorestframework==3.*'
      ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
