# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_fanstatic',
    'waitress',
    'rebecca.fanstatic',
    'js.bootstrap',
    'pyzmq',
    'couchdbkit',
    'pyramid_beaker',
    'rpdb',
    ]

setup(name='cyplp.timelapse_commander',
      version='0.1',
      description='cyplp.timelapse_commander',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author=u'Cyprien Le Pannérer',
      author_email='cyplp@free.fr',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      namespace_packages=['cyplp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="cyplptimelapse_commander",
      entry_points = """\
      [paste.app_factory]
      main = cyplp.timelapse_commander:main
      """,
      )

