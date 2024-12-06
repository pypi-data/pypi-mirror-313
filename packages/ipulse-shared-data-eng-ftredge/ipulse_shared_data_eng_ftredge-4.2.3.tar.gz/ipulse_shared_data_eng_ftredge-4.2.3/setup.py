# pylint: disable=import-error
from setuptools import setup, find_packages

setup(
    name='ipulse_shared_data_eng_ftredge',
    version='4.2.3',
    package_dir={'': 'src'},  # Specify the source directory
    packages=find_packages(where='src'),  # Look for packages in 'src'
    install_requires=[
        # List your dependencies here
        'python-dateutil~=2.8',
        'pytest~=7.1',
        'Cerberus~=1.3.5',
        'ipulse_shared_base_ftredge>=2.1.1',
        'google-cloud-bigquery~=3.20.0',
        'google-cloud-storage~=2.16.0',
        'google-cloud-pubsub>=2.19.0',
        'google-cloud-secret-manager~=2.18.3'
        
    ],
    author='Russlan Ramdowar',
    description='Shared Data Engineering functions for the Pulse platform project. Using AI for financial advisory and investment management.',
    url='https://github.com/TheFutureEdge/ipulse_shared_data_eng'
)
