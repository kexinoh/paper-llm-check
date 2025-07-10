from pathlib import Path
import re
from core.base_check import BaseCheck


class AbbreviationOnceCheck(BaseCheck):
    def __init__(self):
        self.seen: dict[tuple[str, str], Path] = {}

    def _extract(self, line: str):
        # case: Full Term (ABBR)
        if m := re.search(r"\((\b[A-Z]{2,})\)", line):
            abbr = m.group(1)
            before = line[: m.start()].strip().split()
            words = []
            while before and before[-1][0].isupper():
                words.insert(0, before.pop())
            if len(words) >= 2:
                return abbr, " ".join(words)

        # case: ABBR (Full Term)
        if m := re.search(r"(\b[A-Z]{2,})\s*\(([^)]+)\)", line):
            abbr = m.group(1)
            full = m.group(2).strip()
            if all(w[0].isupper() for w in full.split() if w):
                return abbr, full
        return None

    def check_line(self, line: str, file_path: Path) -> list[str]:
        result = self._extract(line)
        if not result:
            return []
        abbr, full = result
        key = (abbr, full)
        if key in self.seen:
            return [f"重复定义缩写: {full} ({abbr})"]
        self.seen[key] = file_path
        return []

    def get_report_header(self) -> str:
        return "缩写重复定义检测"


def register_plugin() -> list[BaseCheck]:
    return [AbbreviationOnceCheck()]
