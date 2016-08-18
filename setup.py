import os
from glob import glob
from setuptools import setup
import numpy as np
README = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README) as rdme:
    longdescr = ''
    i = 0
    for line in rdme:
        if i>=28:
            longdescr += line
        i+=1

pkgname = 'jupyterthemes'
datafiles = {pkgname: ['sandbox/*.js', 'layout/*.less', 'layout/*.css', 'styles/*.less', 'styles/compiled/*.css']}
fontfams = ['monospace', 'sans-serif', 'serif']
fsubdirs = [os.path.join(pkgname,'fonts', subdir) for subdir in fontfams]
fontsdata = np.hstack([['/'.join(f.split('/')[1:]) for f in glob(os.path.join(fsub, '*', '*'))] for fsub in fsubdirs]).tolist()
datafiles[pkgname].extend(fontsdata)

setup(
    name='jupyterthemes',
    version='0.11.1',
    packages=['jupyterthemes'],
    include_package_data=True,
    package_data = datafiles,
    description='Select and install a Jupyter notebook theme',
    long_description=longdescr,
    license='MIT',
    url='https://github.com/dunovank/jupyter-themes/',
    download_url='https://github.com/dunovank/jupyter-themes/tarball/v0.11.1',
    author='dunovank',
    author_email='dunovank@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['jupyter', 'jupyter_core', 'numpy', 'lesscpy>=0.11.1'],
    keywords=['jupyter', 'ipython', 'notebook', 'themes', 'css'],
    entry_points={
        'console_scripts': [
            'jupyter-theme = jupyterthemes:main',
            'jt = jupyterthemes:main',
        ],
    }
)
