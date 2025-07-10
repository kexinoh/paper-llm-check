import re
from pathlib import Path
from typing import List


def get_ordered_tex_files(root_path: str, main_file: str = "main.tex") -> List[Path]:
    """Return LaTeX files in the order defined by ``\input``/``\include`` commands.

    If ``main_file`` does not exist, all ``.tex`` files under ``root_path`` are
    returned in arbitrary order.
    """
    root = Path(root_path)
    main_path = root / main_file
    if not main_path.exists():
        return list(root.glob("**/*.tex"))

    order = [main_path]
    pattern = re.compile(r"\\(?:input|include){([^}]+)}")
    with open(main_path, "r", encoding="utf-8") as f:
        for line in f:
            for match in pattern.finditer(line):
                name = match.group(1)
                file_path = root / (name if name.endswith(".tex") else f"{name}.tex")
                if file_path.exists():
                    order.append(file_path)
    return order
