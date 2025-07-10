from pathlib import Path
import re
from core.base_check import BaseCheck

class LabelDuplicateCheck(BaseCheck):
    def __init__(self):
        self.labels: dict[str, Path] = {}

    def check_line(self, line: str, file_path: Path) -> list[str]:
        issues = []
        if match := re.search(r"\\label{([^}]+)}", line):
            label = match.group(1)
            if label.startswith(('fig:', 'tab:')):
                if label in self.labels:
                    issues.append(f'重复定义图表标签: {label}')
                else:
                    self.labels[label] = file_path
        return issues

    def get_report_header(self) -> str:
        return '图表标签重复检测'

class UnusedLabelCheck(BaseCheck):
    def __init__(self):
        self.defined: set[str] = set()
        self.used: set[str] = set()

    def check_line(self, line: str, file_path: Path) -> list[str]:
        for m in re.finditer(r"\\label{([^}]+)}", line):
            label = m.group(1)
            if label.startswith(('fig:', 'tab:')):
                self.defined.add(label)
        for m in re.finditer(r"\\(?:ref|autoref|cref|Cref){([^}]+)}", line):
            self.used.add(m.group(1))
        return []

    def finalize(self) -> list[str]:
        unused = sorted(self.defined - self.used)
        return [f'未使用的图表标签: {label}' for label in unused]

    def get_report_header(self) -> str:
        return '未被引用的图表标签'

def register_plugin() -> list[BaseCheck]:
    return [LabelDuplicateCheck(), UnusedLabelCheck()]
