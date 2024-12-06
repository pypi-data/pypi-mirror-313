'''Testing __main__.py'''

from coderadar.__main__ import main


class TestMain():
    def setup_class(self):
        pass

    def teardown_class(self):
        pass
        
    def setup_method(self, test_method):
        pass
    
    def teardown_method(self, test_method):
        pass
    
    def test_main(self, mocker):
        test_package = 'package_name'
        mocker.patch('coderadar.__main__.sys.argv', ['__main__.py', test_package])
        mock_relpath = mocker.patch('coderadar.__main__.os.path.relpath')
        mock_relpath.return_value = test_package
        
        mock_coderadar = mocker.patch('coderadar.__main__.CodeRadar.__init__')
        mock_coderadar.return_value = None
        mock_analyze = mocker.patch('coderadar.__main__.CodeRadar.analyze')
        mock_analyze.return_value = None
        mock_report = mocker.patch('coderadar.__main__.CodeRadar.report')
        mock_report.return_value = None
        
        main()
        
        mock_coderadar.assert_called_once_with(test_package)
        mock_analyze.assert_called_once()
        mock_report.assert_called_once()