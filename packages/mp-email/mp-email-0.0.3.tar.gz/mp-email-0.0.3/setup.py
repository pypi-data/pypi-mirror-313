
from setuptools import setup, find_packages


version = '0.0.3'
url = 'https://github.com/pmaigutyak/djmail'


setup(
    name='mp-email',
    version=version,
    description='Django mail app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
