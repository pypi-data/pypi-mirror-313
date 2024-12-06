from __future__ import absolute_import

from coderadar.__main__ import CodeRadar


class TestCodeRadar():
    def setup_class(self):
        pass

    def teardown_class(self):
        pass
        
    def setup_method(self, test_method):
        pass
    
    def teardown_method(self, test_method):
        pass
        
    def test_init(self):
        my_report = CodeRadar('coderadar')
        assert isinstance(my_report, CodeRadar)
    
    
    def test_analyze(self, mocker):
        mock_pytest = mocker.patch('coderadar.__main__.runPytest')
        mock_pylint = mocker.patch('coderadar.__main__.runPylint')
        
        my_report = CodeRadar('coderadar')
        my_report.analyze()
        
        mock_pytest.assert_called_once()
        mock_pylint.assert_called_once()
        
    def test_report(self, mocker):
        test_package = 'package_name'
        mock_report_call = mocker.patch('coderadar.__main__.Report.summarizeCodeQuality')
        
        my_report = CodeRadar(test_package)
        my_report.report()
        
        mock_report_call.assert_called_once_with(test_package)
        