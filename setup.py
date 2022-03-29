from setuptools import setup, find_packages
import os

version = '2.2.1.dev0'

setup(name='redturtle.deletepolicy',
      version=version,
      description="Modified policy for deleting objects in Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='delete policy permissions security',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/redturtle.deletepolicy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.monkeypatcher',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
