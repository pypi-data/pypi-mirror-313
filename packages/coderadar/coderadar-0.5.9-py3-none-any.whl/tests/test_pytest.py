from __future__ import absolute_import

import pytest
from coderadar.pytest import CoverageReport


def test_CoverageReport():
    my_report = CoverageReport()
    assert isinstance(my_report, CoverageReport)


def test_coverage_file_does_not_exist(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = False

    my_report = CoverageReport()
    res = my_report.getTotalCoverage()
    assert res == -1


def test_coverage_file_empty(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True
    mocked_data = mocker.mock_open(read_data='')
    mocker.patch('builtins.open', mocked_data)

    my_report = CoverageReport()
    with pytest.raises(RuntimeError) as e:
        my_report.getTotalCoverage()
    assert 'empty' in str(e)


def test_coverage_file_no_data(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True
    mocked_data = mocker.mock_open(read_data='blah')
    mocker.patch('builtins.open', mocked_data)

    my_report = CoverageReport()
    with pytest.raises(RuntimeError) as e:
        my_report.getTotalCoverage()
    assert 'does not contain Pytest coverage report' in str(e)