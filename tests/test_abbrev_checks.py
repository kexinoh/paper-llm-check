from pathlib import Path
from plugins.abbrev_checks import AbbreviationOnceCheck


def test_abbrev_duplicate_detection():
    lines = [
        "Automatic Speech Recognition (ASR) is useful.",
        "We repeat Automatic Speech Recognition (ASR) again.",
        "CNN (Convolutional Neural Network) is popular.",
        "Another mention CNN (Convolutional Neural Network)."
    ]
    checker = AbbreviationOnceCheck()
    issues = []
    for line in lines:
        issues.extend(checker.check_line(line, Path('test.tex')))
    assert len(issues) == 2
    assert all('重复定义缩写' in issue for issue in issues)


def test_abbrev_header():
    checker = AbbreviationOnceCheck()
    assert checker.get_report_header() == '缩写重复定义检测'
