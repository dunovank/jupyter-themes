import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='jupyterthemes',
    version='0.5.5',
    packages=['jupyterthemes'],
    include_package_data=True,
    package_data={'jupyterthemes': ['sandbox/*.js', 'layout/*.less', 'styles/*.less']},
    description='Select and install a Jupyter notebook theme',
    long_description=README,
    license='MIT',
    url='https://github.com/dunovank/jupyter-themes/',
    download_url='https://github.com/dunovank/jupyter-themes/tarball/0.2',
    author='dunovank',
    author_email='dunovank@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['lesscpy>=0.11.1'],
    keywords=['jupyter', 'ipython', 'notebook', 'themes', 'css'],
    entry_points={
        'console_scripts': [
            'jupyter-theme = jupyterthemes:main',
            'jt = jupyterthemes:main',
        ],
    }
)
