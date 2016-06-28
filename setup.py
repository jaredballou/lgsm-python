# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.join(os.getcwd(),"lgsm/modules"))

"""
# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "django"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break
"""

version = __import__('lgsmcore').get_version()

print "version is %s" % version
with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lgsmcore',
    version=version,
    description='Linux Game Server Manager for Steam-based games',
    long_description=readme,
    author='Jared Ballou',
    author_email='lgsm@jballou.com',
    url='https://github.com/jaredballou/lgsm-python',
    license=license,
    package_dir={'': 'lgsm/modules'},
    #packages=find_packages(exclude=('tests', 'docs', 'gamedata')),
    #py_modules=['lgsmcore', 'steam'],
    #packages=[''],
    scripts=['bin/lgsm'],
)

setup(
    name='steam',
    version=version,
    description='Linux Game Server Manager for Steam-based games',
    long_description=readme,
    author='Jared Ballou',
    author_email='lgsm@jballou.com',
    url='https://github.com/jaredballou/lgsm-python',
    license=license,
    package_dir={'': 'lgsm/modules'},
    #packages=find_packages(exclude=('tests', 'docs', 'gamedata')),
    #py_modules=['lgsmcore', 'steam'],
    #packages=[''],
    #scripts=['bin/lgsm'],
)
