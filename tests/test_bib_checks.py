from pathlib import Path
from plugins.bib_checks import BibDuplicateCheck

def test_bib_detection(tmp_path):
    test_bib = tmp_path / "test.bib"
    test_bib.write_text('title = {Same Title}\ntitle = {Same Title}')
    
    checker = BibDuplicateCheck()
    issues = []
    with open(test_bib, 'r') as f:
        for line in f:
            issues.extend(checker.check_line(line.strip(), test_bib))
    
    assert len(issues) == 1
    assert "重复参考文献标题" in issues[0]


def test_report_header():
    checker = BibDuplicateCheck()
    assert checker.get_report_header() == "BIB参考文献重复检测"