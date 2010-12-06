from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='redturtle.deletepolicy',
      version=version,
      description="Modified policy for deleting objects in Plone 3",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='delete policy permissions',
      author='RedTurtle Technology',
      author_email='info@redturtle.net',
      url='https://code.redturtle.it/svn/redturtle/redturtle.deletepolicy/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
