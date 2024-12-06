from setuptools import setup, find_packages
import os 

def get_version():
    version = os.getenv('PACKAGE_VERSION', None)
    if version:
        return version
    else:
        raise ValueError('PACKAGE_VERSION environment variable not set.')

DESCRIPTION = 'Zero-TOTP Database Model'
LONG_DESCRIPTION = 'The database shared model used accross the zero-totp project.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="zero_totp_db_model", 
        version=get_version(),
        author="Seaweedbrain",
        author_email="developer@zero-totp.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['Zero-TOTP', 'database'],
)