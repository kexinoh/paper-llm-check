from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator
from pluggy import HookspecMarker

class BaseCheck(ABC):
    """插件基类，定义检测规则接口"""
    
    @abstractmethod
    def check_line(self, line: str, file_path: Path) -> list[str]:
        """单行检测方法"""
        
    @abstractmethod
    def get_report_header(self) -> str:
        """生成检测报告标题"""

class FileScanner:
    """文件扫描器，负责遍历目录和文件"""
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)

    def scan_files(self) -> Iterator[Path]:
        """生成器方法，遍历所有.tex文件"""
        return self.root_path.glob('**/*.tex')

# 插件系统挂钩规范
hookspec = HookspecMarker('paper_check')

@hookspec
def register_checks() -> list[BaseCheck]:
    """注册检测插件的钩子规范"""