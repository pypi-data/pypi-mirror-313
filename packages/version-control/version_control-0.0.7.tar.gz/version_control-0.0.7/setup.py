import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='version-control',
    version='0.0.7',
    packages=find_packages(exclude=["example", "*tests*"]),
    install_requires=[
        'Django>=2.2.10',
    ],
    include_package_data=True,
    license='MIT',
    description='Django Version Control',
    long_description=README,
    long_description_content_type="text/x-rst",
    url='https://github.com/kuter/django-version-control',
    author='kuter',
    author_email='contact@devktr.pl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
