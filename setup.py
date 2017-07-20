import os
from glob import glob
from setuptools import setup
from itertools import chain

major = 0
minor = 17
patch = 0

version = '.'.join([str(v) for v in [major, minor, patch]])
url = 'https://github.com/dunovank/jupyter-themes'
download_url = '/'.join([url, 'tarball', 'v' + version])

# get readme content after screenshots for pypi site
README = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README) as read_me:
    longdescr = ''
    startReading = False
    for line in read_me:
        if "Travis" in line.strip():
            startReading = True
        if "Monospace Fonts" in line.strip():
            break
        if startReading:
            longdescr += line

pkgname = 'jupyterthemes'
datafiles = {pkgname: ['sandbox/*.js', 'layout/*.less', 'layout/*.css',
                       'styles/*.less', 'styles/compiled/*.css']}

# recursively point to all included font directories
fontfams = ['monospace', 'sans-serif', 'serif']
fsubdirs = [os.path.join(pkgname, 'fonts', subdir) for subdir in fontfams]
fontsdata = chain.from_iterable([['/'.join(f.split('/')[1:])
                                  for f in glob(os.path.join(fsub, '*', '*'))]
                                 for fsub in fsubdirs])

datafiles[pkgname].extend(fontsdata)

# required dependencies
install_requires = ['ipython<6.0', 'jupyter_core', 'lesscpy', 'matplotlib']

setup(
    name='jupyterthemes',
    version=version,
    packages=['jupyterthemes'],
    include_package_data=True,
    package_data=datafiles,
    description='Select and install a Jupyter notebook theme',
    long_description=longdescr,
    license='MIT',
    url=url,
    download_url=download_url,
    author='dunovank',
    author_email='dunovank@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=install_requires,
    keywords=['jupyter', 'python', 'ipython', 'notebook', 'theme', 'less', 'css'],
    entry_points={
        'console_scripts': [
            'jupyter-theme = jupyterthemes:main',
            'jt = jupyterthemes:main',
        ],
    })
