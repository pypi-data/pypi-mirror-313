
from setuptools import find_packages, setup

setup(
    name='milea-base',
    version='0.5.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-celery-results>=2.5.1', 'django-celery-beat>=2.5.0', 'django-countries>=7.5.1', 'django-currentuser>=0.7.0', 'django-environ>=0.11.2', 'django-object-actions>=4.2.0', 'django>=5.0.2', 'djangorestframework>=3.14.0', 'pillow>=10.2.0', 'pymysql>=1.1.0', 'requests>=2.31.0', 'milea-users>=0.2', 'milea_notify>=0.2', 'milea_licence>=0.1'],
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    description='Milea Framework - Milea Base Module',
    license='MIT',
)
