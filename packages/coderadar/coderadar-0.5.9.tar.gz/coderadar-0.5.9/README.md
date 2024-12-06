# CodeRadar

Identifying the highest threats to your code quality by analyzing code metrics of your project using pytest and pylint.

**Status:**  Beta (runs, but certainly has bugs)\
**Authors:** Carsten König

## Purpose

In order to quickly see where an existing project needs refactoring, an overview of the worst code smells is needed. This package therefore summarizes these in a very brief report, that should guide you directly to the places in your software where an improvement would have the highest impact when you want to improve code quality.

CodeRadar investigates the results from Pytest and Pylint and summarizes the most important findings in a report with actionable hints that are prioritized for the best return on investment regarding your time: fixing the locations pointed out by CodeRadar will improve your code quality the most. If you fix one after the other, you will be able to improve your code step by step, with the highest impact fixes first. In order to give you feeling of progress, changes of the code quality are also indicated in the code quality report.

When run under Python 2.7 (yes, there is still legacy code out there that needs to be ported to Python 3), CodeRadar also points out Python 2/3 compatibility issues (but here in no specific order, as all of them need to be addressed). 

The code quality report is available in HTML and TXT format - the latter is printed on the console when you run CodeRadar. Here is an example of the console output for a previous version of CodeRadar:

```
Code Quality Report
coderadar
--------------------------------------------------
Pytest:
  Number of tests: 31 (+24)
           errors: 0 (+0)
  Test coverage: 42% (+26%)

--------------------------------------------------
Pylint Score:   4.20/10 (+0.36)
  Missing docstrings:             21 (+21)

  Needs Refactoring:
    Too complex:                  0 (+0) (max cyclomatic complexity=0 (+0))
                                    :  (line )
    Function too long (LoC/func): 1 (+1) (max LoC/func=60 (+60))
                                    report.py: Report._fillTemplate (line 194)
    Duplicate code:               0 block(s) (+0)
                                    0 lines in 0 modules:
                                    

  Obsolete code:
    Unused imports:             0 (+0)
                                  
                                  0 imports: 
    Unused variables:           0 (+0)
                                  
                                  0 variables: 
    Unused arguments:           1 (+0)
                                  report.py
                                  1 arguments: 'Report.getReportTemplate(coverage)' (l:105)
    Unreachable code:           0 (+0)
                                  
                                  0 block(s): 

--------------------------------------------------
```

And here is an image of the same code quality report in HTML format:
![CodeRadar HTML code quality report](https://gitlab.com/ck2go/coderadar/-/raw/main/docs/code_quality_report_html.png)

## Installation

```bash
pip install coderadar
```

## How to use
In order to analyze your sourcecode, go to your project root folder and run

```bash
coderadar <path-to-source>
```
This will run pytest, pylint and flake8 to get the metrics that will be analyzed.

The following artifacts will be created:

- ``coverage.xml``
- ``coverage.txt``
- ``pylint.json``
- ``pylint.txt``
- ``code_quality_report.html``
- ``code_quality_report.txt``
- 
If you run `coderadar` under Python 2.7, the following artifacts will be created additionally, in order to assess Python 3 compatibility:
- ``pylint_py3.json`` 
- ``pylint_py3.txt``

If you place these artifacts in a folder called `last_run`, located in the directory where you run the command, the results of the last run are automatically compared to the current run.

## How to contribute

No, CodeRadar itself, although developed in a (partially) test-driven manner, and being all about code quality, is also not a perfect piece of code (ironic, isn't it?). Feel free to suggest new features, report bugs or even contribute code. I would be happy to see this project grow and improve with your help. 

## License
[GNU GPLv3 License](https://choosealicense.com/licenses/gpl-3.0/)

## Author
**Carsten König**

- [GitLab](https://gitlab.com/ck2go "Carsten König")
- [GitHub](https://github.com/ck2go "Carsten König")
- [LinkedIn](https://www.linkedin.com/in/ck2go/ "Carsten König")
- [Website](https://www.carsten-koenig.de "Carsten König")