from __future__ import absolute_import

from coderadar.report import Report



def test_Report():
    my_report = Report()
    assert isinstance(my_report, Report)

def test_summarizeCodeQuality_previousRunEmpty(mocker):
    mock_CoverageReport = mocker.patch('coderadar.pytest.CoverageReport.__init__')
    mock_CoverageReport.return_value = None
    mock_PylintReport = mocker.patch('coderadar.pylint.PylintReport.__init__')
    mock_PylintReport.return_value = None
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True
    mock_stat = mocker.patch('os.path.getsize')
    mock_stat.return_value = 0

    mock_CoverageReport = mocker.patch('coderadar.report.Report.getReportTemplate')
    mock_CoverageReport.return_value = 'blubb'
    mock_CoverageReport = mocker.patch('coderadar.report.Report._fillTemplate')
    mock_CoverageReport.return_value = 'blubb'

    mock_open = mocker.patch('builtins.open')

    from coderadar.report import Report
    my_report = Report()
    my_report.summarizeCodeQuality('my_module')


def test_getReportTemplate_str_Python2(mocker):
    mock_coverage = mocker.MagicMock()

    mock_pylint = mocker.MagicMock()
    mock_pylint.hasPython23Report.return_value = True

    report = Report()
    template = report.getReportTemplate(report_type='txt', coverage=mock_coverage, pylint=mock_pylint)
    assert 'Pytest' in template
    assert 'Pylint' in template
    assert 'Python 2/3' in template
    assert '###TEMPLATE_PY23' not in template


def test_getReportTemplateHtml_Python2(mocker):
    mock_coverage = mocker.MagicMock()

    mock_pylint = mocker.MagicMock()
    mock_pylint.hasPython23Report.return_value = True

    report = Report()
    template = report.getReportTemplate(report_type='html', coverage=mock_coverage, pylint=mock_pylint)
    assert 'Pytest' in template
    assert 'Pylint' in template
    assert 'Python 2/3' in template
    assert '###TEMPLATE_PY23' not in template

def test_getReportTemplate_str_Python3(mocker):
    mock_coverage = mocker.MagicMock()

    mock_pylint = mocker.MagicMock()
    mock_pylint.hasPython23Report.return_value = False

    report = Report()
    template = report.getReportTemplate(report_type='txt', coverage=mock_coverage, pylint=mock_pylint)
    assert 'Pytest' in template
    assert 'Pylint' in template
    assert 'Python 2/3' not in template
    assert '###TEMPLATE_PY23' not in template


def test_getReportTemplateHtml_Python3(mocker):
    mock_coverage = mocker.MagicMock()

    mock_pylint = mocker.MagicMock()
    mock_pylint.hasPython23Report.return_value = False

    report = Report()
    template = report.getReportTemplate(report_type='html', coverage=mock_coverage, pylint=mock_pylint)
    assert 'Pytest' in template
    assert 'Pylint' in template
    assert 'Python 2/3' not in template
    assert '###TEMPLATE_PY23' not in template


def test_fillTemplate(mocker):
    mock_coverage = mocker.MagicMock()
    mock_coverage.getTotalCoverage.return_value = 99
    mock_pylint = mocker.MagicMock()

    report = Report()
    template = report._fillTemplate('<coverage>', 'my_package', mock_coverage, mock_pylint)
    assert template == '99'


def test_fillTemplate_with_diff(mocker):
    mock_coverage = mocker.MagicMock()
    mock_coverage.getTotalCoverage.return_value = 99
    mock_coverage_old = mocker.MagicMock()
    mock_coverage_old.getTotalCoverage.return_value = 98

    mock_pylint = mocker.MagicMock()
    mock_pylint_old = mocker.MagicMock()

    report = Report()
    template = report._fillTemplate('<coverage><coverage_diff>', 'my_package', mock_coverage, mock_pylint, mock_coverage_old, mock_pylint_old)
    assert template == '99 (+1)'


def test_fillTemplate_with_missing_py27_report(mocker):
    mock_coverage = mocker.MagicMock()
    mock_coverage_old = mocker.MagicMock()

    mock_pylint = mocker.MagicMock()
    mock_pylint.getNumPy23Incompatibible.return_value = 0
    mock_pylint_old = mocker.MagicMock()
    mock_pylint_old.getNumPy23Incompatibible.return_value = None

    report = Report()
    template = report._fillTemplate('<num_py23_incompatible><num_py23_incompatible_diff>', 'my_package', mock_coverage, mock_pylint, mock_coverage_old, mock_pylint_old)
    assert template == '0'


def test_getDiffTxt(mocker):
    report = Report()
    res = report._getDiffTxt(98, 99)
    assert res == ' (+1)'


def test_getDiffTxt_None(mocker):
    report = Report()
    res = report._getDiffTxt(None, 99)
    assert res == ''


def test_getDiffHtml(mocker):
    report = Report()
    res = report._getDiffHtml(98, 99)
    assert res == ' (<span style="color:green">+1</span>)'


def test_getDiffHtml_None(mocker):
    report = Report()
    res = report._getDiffHtml(None, 99)
    assert res == ''
