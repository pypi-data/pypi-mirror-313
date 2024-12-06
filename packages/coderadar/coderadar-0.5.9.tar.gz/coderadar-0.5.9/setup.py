from setuptools import setup, find_packages

setup(name='coderadar',
      version='0.5.9',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['coderadar=coderadar.__main__:main'],
          },
      package_data={
          # If any package contains *.txt or *.html files, include them:
          '': ['*.txt', '*.html'],
          # And if you specifically have files in mypackage/templates, you can be explicit:
          'coderadar.templates': ['*.html', '*.txt'],
      },
     )