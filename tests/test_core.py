from pathlib import Path
from core.base_check import FileScanner
from plugins.markdown_checks import MarkdownImportantCheck

def test_scan_files(tmp_path):
    # 创建测试用.tex文件
    test_file = tmp_path / "test.tex"
    test_file.write_text("test content")
    
    scanner = FileScanner(str(tmp_path))
    files = list(scanner.scan_files())
    assert len(files) == 1
    assert files[0].name == "test.tex"


def test_plugin_loading():
    plugin = MarkdownImportantCheck()
    assert plugin.get_report_header() == "Markdown标记残留检测"
    
    test_line = "**Important** content"
    issues = plugin.check_line(test_line, Path("test.tex"))
    assert len(issues) == 1
    assert "未转换的Markdown标记" in issues[0]