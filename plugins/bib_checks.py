from pathlib import Path
from core.base_check import BaseCheck
import re

class BibDuplicateCheck(BaseCheck):
    def __init__(self):
        self.titles = set()

    def check_line(self, line: str, file_path: Path) -> list[str]:
        if file_path.suffix == '.bib':
            if match := re.search(r'title\s*=\s*{(.*?)}', line):
                title = match.group(1).lower().strip()
                if title in self.titles:
                    return [f'发现重复参考文献标题: {title}']
                self.titles.add(title)
        return []

    def get_report_header(self) -> str:
        return "BIB参考文献重复检测"

def register_plugin() -> list[BaseCheck]:
    return [BibDuplicateCheck()]