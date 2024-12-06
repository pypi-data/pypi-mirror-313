'''Module to run Code Radar.'''

from __future__ import absolute_import

import sys
import os

from .report import Report

from .pylint import runPylint
from .pytest import runPytest
# from .flake8 import runFlake8
# from .gitlab import Gitlab
  

class CodeRadar(object):
    """
    Class to analyze and report on the quality of code in a given package.
    """
    def __init__(self, package_name):
        """
        Initialize CodeRadar with the package name.
        """
        self._package_name = package_name

    
    def analyze(self):
        """
        Initialize CodeRadar with the package name.
        """
        runPytest(self._package_name)
        runPylint(self._package_name)
        
    def report(self):
        """
        Summarize the code quality of the package.
        """
        myReport = Report()
        myReport.summarizeCodeQuality(self._package_name)
        
    

def main():
    """
    Main function to run CodeRadar from commandline.
    """
    if len(sys.argv) < 2:
        print("Please provide a package name as a command line argument.")
        sys.exit(1)

    package_name = os.path.relpath(sys.argv[1])
    cr = CodeRadar(package_name)
    cr.analyze()
    cr.report()
    
    
# if __name__ == '__main__':
#     main()
    
