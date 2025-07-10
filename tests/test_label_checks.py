from pathlib import Path
from plugins.label_checks import LabelDuplicateCheck, UnusedLabelCheck


def test_label_duplicate():
    lines = [
        "\\begin{figure}\\label{fig:one}\\end{figure}",
        "text",
        "\\begin{table}\\label{fig:one}\\end{table}"
    ]
    checker = LabelDuplicateCheck()
    issues = []
    for line in lines:
        issues.extend(checker.check_line(line, Path('test.tex')))
    assert any('fig:one' in issue for issue in issues)
    assert len(issues) == 1


def test_unused_label():
    lines = [
        "\\begin{figure}\\label{fig:used}\\end{figure}",
        "see Figure~\\ref{fig:used}",
        "\\begin{table}\\label{tab:unused}\\end{table}"
    ]
    checker = UnusedLabelCheck()
    for line in lines:
        checker.check_line(line, Path('test.tex'))
    issues = checker.finalize()
    assert 'tab:unused' in ''.join(issues)
    assert len(issues) == 1
