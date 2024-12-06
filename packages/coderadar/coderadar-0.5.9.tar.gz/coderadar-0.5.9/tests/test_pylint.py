from __future__ import absolute_import

from coderadar.pylint import PylintReport
import pytest

import sys
from collections import namedtuple

class TestPylintReport():
    

    def setup_class(self):
        pass

    def teardown_class(self):
        pass
        
    def setup_method(self, test_method):
        pass
    
    def teardown_method(self, test_method):
        pass


    def test_init(self, mocker):
        mock_load_report = mocker.patch('coderadar.pylint.PylintReport._loadJsonReport')
        my_report = PylintReport()
        assert isinstance(my_report, PylintReport)


    def test_json_empty(self, mocker):
        mock_open_report_file = mocker.patch('builtins.open')
        mock_open_report_file.return_value.read.return_value = ''
        mock_getsize = mocker.patch('os.path.getsize')
        mock_getsize.return_value = 0

        with pytest.raises(RuntimeError) as e:
            my_report = PylintReport()
        assert 'empty' in str(e)


    def test_json_invalid(self, mocker):
        mock_open_report_file = mocker.patch('builtins.open')
        mock_open_report_file.return_value.read.return_value = 'blah'
        mock_getsize = mocker.patch('os.path.getsize')
        mock_getsize.return_value = 5

        with pytest.raises(RuntimeError) as e:
            my_report = PylintReport()
        assert 'decode' in str(e)

    def test_loadJsonReport(self, mocker):
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)

        my_report = PylintReport()
        assert isinstance(my_report._report, list)


    def test_loadJson3Report_in_Python3(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(3, 10, 0, 'final', 0))
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)
        mock_exists = mocker.patch('os.path.exists')
        mock_exists.return_value = False

        my_report = PylintReport()
        assert my_report._report3 is None


    def test_loadJson3Report(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(2, 7, 15, 'final', 0))
        mock_exists = mocker.patch('os.path.exists')
        mock_exists.return_value = True
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)

        my_report = PylintReport()
        assert isinstance(my_report._report3, list)

    def test_has_py23report_in_Python3(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(3, 10, 0, 'final', 0))
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)
        my_report = PylintReport()

        assert my_report.hasPython23Report() is False

    def test_has_py23report(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(2, 7, 15, 'final', 0))
        mock_exists = mocker.patch('os.path.exists')
        mock_exists.return_value = True
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)
        my_report = PylintReport()

        assert my_report.hasPython23Report() is True


    def test_getNumPy23Incompatibible(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(2, 7, 15, 'final', 0))
        mock_exists = mocker.patch('os.path.exists')
        mock_exists.return_value = True
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)

        my_report = PylintReport()
        num_incompatible = my_report.getNumPy23Incompatibible()
        assert num_incompatible == 2


    def test_getNumPy23Incompatibible_no_py23_report(self, mocker):
        VersionInfo = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
        mock_version = mocker.patch.object(sys, 'version_info', VersionInfo(2, 7, 15, 'final', 0))
        mock_exists = mocker.patch('os.path.exists')
        mock_exists.return_value = False
        mocked_data = mocker.mock_open(read_data='[\n{"test": 1},\n{"testb": 2}\n]')
        mocker.patch('builtins.open', mocked_data)

        my_report = PylintReport()
        my_report._report3 = None
        num_incompatible = my_report.getNumPy23Incompatibible()
        assert num_incompatible is None
