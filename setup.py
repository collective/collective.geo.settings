from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.geo.settings',
      version=version,
      description="collective.geo settings",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://svn.plone.org/svn/collective/collective.geo.settings',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.geo.openlayers',
          'collective.geo.geopoint',
          'plone.app.z3cform',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
