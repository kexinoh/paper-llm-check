from pathlib import Path
from core.base_check import BaseCheck
import re  # 新增正则表达式模块导入

class MarkdownImportantCheck(BaseCheck):
    def check_line(self, line: str, file_path: Path) -> list[str]:
        # 分割行内容为公式部分（被$包裹）和非公式部分
        parts = re.split(r'(\$+.*?\$+)', line)
        issues = []
        for part in parts:
            # 跳过公式部分（以$开头和结尾的部分）
            if part.startswith('$') and part.endswith('$'):
                continue
            # 检查非公式部分是否有*符号
            if '*' in part:
                issues.append(f'发现未转换的Markdown标记（非公式区域）: {part.strip()}')
        return issues

    def get_report_header(self) -> str:
        return "Markdown标记残留检测"

def register_plugin() -> list[BaseCheck]:
    return [MarkdownImportantCheck()]