from pathlib import Path
import re
import requests
from difflib import SequenceMatcher
from typing import List
from ..core.base_check import BaseCheck

class ArXivValidationCheck(BaseCheck):
    def __init__(self):
        self.current_id = None
        self.local_title = None

    def _extract_arxiv_id(self, line: str) -> str:
        # 从eprint字段提取
        if eprint_match := re.search(r'eprints*=s*{([0-9]{4}.[0-9]{5})}', line):
            return eprint_match.group(1)
        # 从url字段提取
        if url_match := re.search(r'arxiv.org/abs/([0-9]{4}.[0-9]{5})', line):
            return url_match.group(1)
        return None

    def _fetch_arxiv_title(self, arxiv_id: str) -> str:
        try:
            response = requests.get(
                f'http://export.arxiv.org/api/query?id_list={arxiv_id}',
                timeout=10
            )
            response.raise_for_status()
            if match := re.search(r'<title>[\s\S]*?([^<]+)</title>', response.text):
                return match.group(1).replace('\n', ' ').strip()
        except Exception as e:
            return f"API请求失败: {str(e)}"

    def _normalize_title(self, title: str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', title.lower())

    def check_line(self, line: str, file_path: Path) -> List[str]:
        if file_path.suffix != '.bib':
            return []

        # 捕获arxiv ID
        if not self.current_id:
            self.current_id = self._extract_arxiv_id(line)

        # 捕获本地标题
        if title_match := re.search(r'titles*=s*{(.*?)}', line):
            self.local_title = self._normalize_title(title_match.group(1))

        # 当同时存在ID和本地标题时进行验证
        if self.current_id and self.local_title:
            api_title = self._fetch_arxiv_title(self.current_id)
            if api_title.startswith('API请求失败'):
                return [api_title]
                
            similarity = SequenceMatcher(
                None, 
                self.local_title,
                self._normalize_title(api_title)
            ).ratio()
            
            if similarity < 0.8:
                return [f"标题匹配度低({similarity*100:.1f}%): 本地『{self.local_title}』 vs API『{api_title}』"]

            # 重置状态
            self.current_id = None
            self.local_title = None

        return []

    def get_report_header(self) -> str:
        return "arXiv引用验证"