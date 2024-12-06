'''Module containing PyLint functionality.'''
import json
import os.path
import sys
from collections import Counter

from ._functions import executeShell


def _runPylintPy2(package_name):
    """
    Run PyLint for Python 2. Creates pylint.txt and pylint.json report files.

    Parameters
    ----------
    package_name: str
        Name of the package to run PyLint on.

    Returns
    -------
    None
    """
    # unfortunately, pylint does not support json and text output at the same
    # time in Python 2, so we have to run each test twice
    # 2 for normal tests, 2 for Python 3 compatibility (--py3k) tests
    cmd = ['pylint',
           '-ry',
           '--load-plugins=pylint.extensions.mccabe',
           '--output-format=text',
           '--ignore=tests',
           '--persistent=n',
           './%s/' % package_name
           ]
    executeShell(cmd, print_output=True, save_output_as='pylint.txt')

    cmd = ['pylint',
           '-ry',
           '--load-plugins=pylint.extensions.mccabe',
           '--output-format=json',
           '--ignore=tests',
           '--persistent=n',
           './%s/' % package_name
           ]
    executeShell(cmd, print_output=False, save_output_as='pylint.json')

    cmd = ['pylint',
           '-ry',
           '--py3k',
           '--load-plugins=pylint.extensions.mccabe',
           '--output-format=text',
           '--ignore=tests',
           '--persistent=n',
           './%s/' % package_name
           ]
    executeShell(cmd, print_output=True, save_output_as='pylint_py3.txt')

    cmd = ['pylint',
           '-ry',
           '--py3k',
           '--load-plugins=pylint.extensions.mccabe',
           '--output-format=json',
           '--ignore=tests',
           '--persistent=n',
           './%s/' % package_name
           ]
    executeShell(cmd, print_output=False, save_output_as='pylint_py3.json')
    
    
def _runPylintPy3(package_name):
    """
    Run PyLint for Python 3. Creates pylint.txt and pylint.json report files.

    Parameters
    ----------
    package_name: str
        Name of the package to run PyLint on.

    Returns
    -------
    None
    """
    cmd = ['pylint',
           '-ry',
           '--load-plugins=pylint.extensions.mccabe',
           '--output-format=json:pylint.json,text:pylint.txt',
           '--ignore=tests',
           './%s/' % package_name
           ]
    executeShell(cmd)


def runPylint(package_name):
    """
    Run PyLint for the given package.

    Parameters
    ----------
    package_name: str
        Name of the package to run PyLint on.

    Returns
    -------
    None
    """
    print('Running PyLint...')
    if sys.version_info.major == 2:
        _runPylintPy2(package_name)
    else:
        _runPylintPy3(package_name)


class PylintReport(object):
    """
    Class to analyze and report on the PyLint report that is loaded from file.
    """
    def __init__(self, txt=None, json=None):
        if txt is None:
            txt = 'pylint.txt'
        if json is None:
            json = 'pylint.json'
            
        self._txt = txt
        self._json = json
        self._report = self._loadJsonReport(self._json)

        self._txt3 = None
        self._json3 = None
        self._report3 = None

        if sys.version_info.major == 2:
            self._txt3 = self._txt.split('.')[0] + '_py3.txt'
            self._json3 = self._json.split('.')[0] + '_py3.json'
            if os.path.exists(self._json3):
                self._report3 = self._loadJsonReport(self._json3)

    def hasPython23Report(self):
        return self._report3 is not None

    def getTxtUrl(self):
        """
        Get the URL of the text report.

        Returns
        -------
        str
            URL of the text report.
        """
        return self._txt
    
    def _loadJsonReport(self, jsonfile):
        """
        Load the PyLint JSON report from file.

        Returns
        -------
        dict
            JSON report.
        """
        # For Python 3.x compatibility where JSONDecodeError is defined
        if sys.version_info.major == 2:
            # For Python 2.7, where JSONDecodeError does not exist
            JSONDecodeError = ValueError
        else:
            JSONDecodeError = json.decoder.JSONDecodeError

        try:
            res = json.load(open(jsonfile))
        except JSONDecodeError:
            if os.path.getsize(jsonfile) == 0:
                raise RuntimeError("File '%s' is empty!" % self._json)
            else:
                raise RuntimeError("Can't decode JSON in file '%s'!" % self._json)
        return res
        
    def getScore(self):
        """
        Get the PyLint score.

        Returns
        -------
        str
            PyLint score.
        """
        with open(self._txt) as f:
            lines = f.readlines()
        
        for line in lines:
            if 'Your code has been rated' in line:
                score = line[line.find(' at ')+3:line.find('/')]
        return score
    
    def getMissingDocstrings(self):
        """
        Get the number of missing docstrings.

        Returns
        -------
        int
            Number of missing docstrings.
        """
        if sys.version_info.major == 2:
            no_docstring = 'C0111'
            msg_ids = [no_docstring]
        else:
            no_module_docstring = 'C0114'
            no_class_docstring = 'C0115'
            no_function_docstring = 'C0116'
            msg_ids = [no_module_docstring, no_class_docstring, no_function_docstring]
        
        no_docstrings = [msg for msg in self._report if msg['message-id'] in msg_ids]
        num_missing_docstrings = len(no_docstrings)
        return num_missing_docstrings
    
    def getTooComplex(self):
        """
        Get the information on too complex code.

        Returns
        -------
        set(int, int, str, str, str)
            Number of too complex code, maximum complexity, file with too complex code, object with too complex code, line with too complex code.
        """
        too_complex = 'R1260'
        msg_ids = [too_complex]
        
        too_complex = [msg for msg in self._report if msg['message-id'] in msg_ids]
        num_too_complex = len(too_complex)
        
        if num_too_complex > 0:
            max_too_complex = max([int(msg['message'][msg['message'].rfind(' ')+1:]) for msg in too_complex])
            msg = [msg
                   for msg in too_complex
                   if max_too_complex == int(msg['message'][msg['message'].rfind(' ')+1:])][0]
            too_complex_file = msg['path'][msg['path'].find('/')+1:]
            too_complex_line = msg['line']
            too_complex_obj = msg['obj']
        else:
            max_too_complex = 0
            too_complex_file = ''
            too_complex_obj = ''
            too_complex_line = ''
            
        return num_too_complex, max_too_complex, too_complex_file, too_complex_obj, too_complex_line
    
    def getTooManyStatements(self):
        """
        Get the information on too many statements.

        Returns
        -------
        set(int, int, str, str, str)
            Number of too many statements, maximum number of statements, file with too many statements, object with too many statements, line with too many statements.
        """
        too_many_satements = 'R0915'
        msg_ids = [too_many_satements]
        
        too_many_satements = [msg for msg in self._report if msg['message-id'] in msg_ids]
        num_too_many_satements = len(too_many_satements)
        
        if num_too_many_satements > 0:
            max_too_many_satements = max([int(msg['message'][msg['message'].rfind('(')+1:msg['message'].rfind('/')]) for msg in too_many_satements])
            msg = [msg
                   for msg in too_many_satements
                   if max_too_many_satements == int(msg['message'][msg['message'].rfind('(')+1:msg['message'].rfind('/')])][0]
            too_many_statements_file = msg['path'][msg['path'].find('/')+1:]
            too_many_statements_obj = msg['obj']
            too_many_statements_line = msg['line']
        else:
            max_too_many_satements = 0
            too_many_statements_file = ''
            too_many_statements_obj = ''
            too_many_statements_line = ''
            
        return num_too_many_satements, max_too_many_satements, too_many_statements_file, too_many_statements_obj, too_many_statements_line
    
    def getUnusedImports(self):
        """
        Get the information on unused imports.

        Returns
        -------
        set(int, str, int, list)
            Number of unused imports, file with unused imports, number of unused imports, list of unused imports.
        """
        unused_import = 'W0611'
        msg_ids = [unused_import]
        
        unused_import = [msg['path'] 
                         for msg in self._report 
                         if msg['message-id'] in msg_ids]
        num_unused_import = len(unused_import)
        
        if num_unused_import > 0:
            unused_import_path, unused_import_num = Counter(unused_import).most_common()[0]
            unused_import_file = unused_import_path[unused_import_path.find('/')+1:]
            
            unused_import_messages = [msg['message'] 
                                      for msg in self._report 
                                      if msg['message-id'] in msg_ids and 
                                      msg['path'] == unused_import_path]
            
            unused_import_items = []
            for msg in unused_import_messages:
                if msg[:13] == 'Unused import':
                    item = msg[14:]
                elif ' imported from' in msg:
                    item = msg[msg.find(' ')+1:msg.find('imported')-1]
                elif ' imported as ' in msg:
                    item = msg[msg.find(' ')+1:msg.find('imported')-1] + ' (as %s)' % msg[msg.rfind(' ')+1:]
                else:
                    raise RuntimeError("Can't parse message: '%s'" % msg)
                unused_import_items.append(item)
        else:
            unused_import_file = ''
            unused_import_num = 0
            unused_import_items = []
        
        return num_unused_import, unused_import_file, unused_import_num, unused_import_items
    
    def getUnusedVariables(self):
        """
        Get the information on unused variables.

        Returns
        -------
        set(int, str, int, list)
            Number of unused variables, file with unused variables, number of unused variables, list of unused variables.
        """
        unused_variable = 'W0612'
        msg_ids = [unused_variable]
        
        unused_variables = [msg['path'] 
                            for msg in self._report 
                            if msg['message-id'] in msg_ids]
        num_unused_variables = len(unused_variables)
        
        if num_unused_variables > 0:
            unused_variables_path, unused_variables_num = Counter(unused_variables).most_common()[0]
            unused_variables_file = unused_variables_path[unused_variables_path.find('/')+1:]
            unused_variables_messages = [(msg['message'], msg['line'])
                                         for msg in self._report 
                                         if msg['message-id'] in msg_ids and 
                                         msg['path'] == unused_variables_path]
            unused_variables_items = []
            for msg, line in unused_variables_messages:
                variable = msg[msg.rfind(" '")+2:-1]
                unused_variables_items.append("'%s' (l:%s)" % (variable, line))
            unused_variables_num = len(unused_variables_items)
        else:
            unused_variables_file = ''
            unused_variables_num = 0
            unused_variables_items = []
        
        return num_unused_variables, unused_variables_file, unused_variables_num, unused_variables_items
    
    def getUnusedArguments(self):
        """
        Get the information on unused arguments.

        Returns
        -------
        set(int, str, int, list)
            Number of unused arguments, file with unused arguments, number of unused arguments, list of unused arguments.
        """
        unused_arguments = 'W0613'
        msg_ids = [unused_arguments]
        
        unused_arguments = [msg['path'] 
                            for msg in self._report 
                            if msg['message-id'] in msg_ids]
        num_unused_arguments = len(unused_arguments)
        
        if num_unused_arguments > 0:
            unused_arguments_path, unused_arguments_num = Counter(unused_arguments).most_common()[0]
            unused_arguments_file = unused_arguments_path[unused_arguments_path.find('/')+1:]
            unused_arguments_messages = [(msg['message'], msg['line'], msg['obj'])
                                         for msg in self._report 
                                         if msg['message-id'] in msg_ids and 
                                         msg['path'] == unused_arguments_path]
            unused_arguments_items = []
            for msg, line, obj in unused_arguments_messages:
                variable = msg[msg.rfind(" '")+2:-1]
                unused_arguments_items.append("'%s(%s)' (l:%s)" % (obj, variable, line))
            unused_arguments_num = len(unused_arguments_items)
        else:
            unused_arguments_file = ''
            unused_arguments_num = 0
            unused_arguments_items = []
            
        return num_unused_arguments, unused_arguments_file, unused_arguments_num, unused_arguments_items

    def getUnreachableCode(self):
        """
        Get the information on unreachable code.

        Returns
        -------
        set(int, str, int, list)
            Number of unreachable code, file with unreachable code, number of unreachable code, list of unreachable code.
        """
        unreachable_code = 'W0101'
        msg_ids = [unreachable_code]
        
        unreachable_code = [msg['path'] for msg in self._report if msg['message-id'] in msg_ids]
        num_unreachable_code = len(unreachable_code)
        
        if num_unreachable_code > 0:
            unreachable_code_path, unreachable_code_num = Counter(unreachable_code).most_common()[0]
            unreachable_code_file = unreachable_code_path[unreachable_code_path.find('/')+1:]
            unreachable_code_messages = [(msg['line'], msg['obj'])
                                         for msg in self._report 
                                         if msg['message-id'] in msg_ids and 
                                         msg['path'] == unreachable_code_path]
            unreachable_code_items = []
            for line, obj in unreachable_code_messages:
                unreachable_code_items.append("'%s' (l:%s)" % (obj, line))
            unreachable_code_num = len(unreachable_code_items)
        else:
            unreachable_code_file = ''
            unreachable_code_num = 0
            unreachable_code_items = []
        
        return num_unreachable_code, unreachable_code_file, unreachable_code_num, unreachable_code_items

    def getDuplicateCode(self):
        """
        Get the information on duplicate code.

        Returns
        -------
        set(int, int, list, int)
            Number of duplicate code, maximum number of duplicate code, list of files with duplicate code, number of lines of duplicate code.
        """
        duplicate_code = 'R0801'
        duplicate_code2 = 'RP0801'
        msg_ids = [duplicate_code, duplicate_code2]
        
        duplicate_code = [msg for msg in self._report if msg['message-id'] in msg_ids]
        num_duplicate_code = len(duplicate_code)

        if num_duplicate_code > 0:
            duplicate_code_max = max([int(msg['message'][msg['message'].find(' in ')+4:msg['message'].find(' files')])
                                      for msg in duplicate_code])
            duplicate_code_txt = [msg['message'].split('\n')
                                    for msg in duplicate_code
                                    if duplicate_code_max == int(msg['message'][msg['message'].find(' in ')+4:msg['message'].find(' files')])][0]
            duplicate_code_files = duplicate_code_txt[1:1+duplicate_code_max]
            duplicate_code_files = [file_name[file_name.find('.')+1:] for file_name in duplicate_code_files]
            duplicate_code_lines = len(duplicate_code_txt[1+duplicate_code_max:])
        else:
            duplicate_code_max = 0
            duplicate_code_files = []
            duplicate_code_lines = 0
            
        return num_duplicate_code, duplicate_code_max, duplicate_code_files, duplicate_code_lines


    def getNumPy23Incompatibible(self):
        num_py23_incompatible = 0
        if sys.version_info.major == 2:
            if self._report3 is not None:
                num_py23_incompatible = len(self._report3)
            else:
                num_py23_incompatible = None

        return num_py23_incompatible

    def getPy23IncompatibibleItems(self):
        py23_incompatible_items = [''] * 10
        if sys.version_info.major == 2:
            if self._report3 is not None:
                if len(self._report3) > 0:
                    py23_incompatible_items = ['%s' % item['message']
                                               for item in self._report3[:min([10, len(self._report3)])]]
            else:
                py23_incompatible_items = ['No Python 2/3 incompatibilities found.']

        return tuple(py23_incompatible_items)

    def getPy23IncompatibibleItemLocs(self):
        py23_incompatible_item_locs = [''] * 10
        if sys.version_info.major == 2:
            if self._report3 is not None:
                if len(self._report3) > 0:
                    py23_incompatible_item_locs = ['%s, line %i' % (item['path'][item['path'].find('/')+1:],
                                                                    item['line'])
                                                   for item in self._report3[:min([10, len(self._report3)])]]
            else:
                py23_incompatible_item_locs = ['']

        return tuple(py23_incompatible_item_locs)
