import pytest
from pathlib import Path
from unittest.mock import patch
from plugins.arxiv_checks import ArXivValidationCheck

@patch('plugins.arxiv_checks.requests.get')
def test_arxiv_id_extraction(mock_get):
    test_data = [
        ('eprint = {2310.09888}', '2310.09888'),
        ('url = {https://arxiv.org/abs/2105.12345}', '2105.12345'),
        ('note = {no id here}', None)
    ]
    
    checker = ArXivValidationCheck()
    for line, expected in test_data:
        assert checker._extract_arxiv_id(line) == expected

@patch('plugins.arxiv_checks.requests.get')
def test_title_matching(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '''
        <feed><entry><title>Real Title v1</title></entry></feed>
    '''
    
    bib_content = '''
    @article{test,
        eprint = {2310.09888},
        title = {Real Title}
    }
    '''
    
    checker = ArXivValidationCheck()
    issues = []
    for line in bib_content.split('\n'):
        issues.extend(checker.check_line(line.strip(), Path('test.bib')))
    
    assert len(issues) == 0

@patch('plugins.arxiv_checks.requests.get')
def test_low_similarity(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<feed><entry><title>Different Title</title></entry></feed>'
    
    bib_content = '''
    @misc{test,
        url = {https://arxiv.org/abs/2105.12345},
        title = {My Title}
    }
    '''
    
    checker = ArXivValidationCheck()
    issues = []
    for line in bib_content.split('\n'):
        issues.extend(checker.check_line(line.strip(), Path('test.bib')))
    
    assert any("标题匹配度低" in issue for issue in issues)

@patch('plugins.arxiv_checks.requests.get')
def test_api_failure(mock_get):
    mock_get.side_effect = Exception("Connection timeout")
    
    bib_content = '''
    @article{test,
        eprint = {2310.09888},
        title = {Test Title}
    }
    '''
    
    checker = ArXivValidationCheck()
    issues = []
    for line in bib_content.split('\n'):
        issues.extend(checker.check_line(line.strip(), Path('test.bib')))
    
    assert any("API请求失败" in issue for issue in issues)