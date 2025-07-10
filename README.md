# paper-llm-check

`paper-llm-check` 是一个用于检查论文源文件的简单工具。项目采用插件架构，可在扫描 LaTeX (`.tex`)与 BibTeX (`.bib`)文件时执行多种格式检查，帮助作者提前发现常见问题。

## 目录结构
- **core/**: 定义基础类和文件扫描器。
- **plugins/**: 各类检查插件的实现。
- **tests/**: pytest 单元测试。
- **main.py**: 命令行入口。

## 安装
1. 安装 Python 3.10+.
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用
运行检查器并指定包含 `.tex`/`.bib` 的路径：
```bash
python main.py --path path/to/project
```
程序会遍历给定目录下所有 `.tex` 文件，并在终端输出发现的问题。

## 已实现的检查
### Markdown 标识残留检测
检测未转换的 **加粗**、*斜体*等 Markdown 标识。

### 缩写重复定义检测
检查同一缩写及其全称是否被多次定义，避免在论文中重复介绍。

### BIB 参考文献重复检测
检测 `.bib` 文件中重复的论文标题，提示重复的参考文献条目。

### arXiv 引用验证
1. 从 `eprint` 字段或 `arxiv.org/abs/` URL 提取 arXiv ID。
2. 通过 arXiv API 获取论文元数据。
3. 比对本地标题与 API 标题相似度（阈值 95%）。
4. 支持 `@article` 和 `@misc` 条目类型。
5. 自动跳过非 `.bib` 文件。

### 图表标签重复检测
检测 `figure`/`table` 等环境中的 `\label` 是否被重复使用，避免交叉引用混乱。

### 未被引用的图表标签
统计论文中所有图表标签，找出从未被 `\ref` 等命令引用的标签。

## 开发自定义插件
新增检查时，只需继承 `BaseCheck` 并实现 `check_line`与 `get_report_header`，然后在插件模块中提供 `register_plugin` 函数返回插件实例即可。

## 运行测试
项目使用 `pytest` 编写单元测试，执行以下命令运行全部测试：
```bash
pytest
```

## TODO
- 支持更多文件类型（如 Markdown）。
- 增加命令行配置，允许用户自定义启用的规则。
- 与 `pre-commit` 集成，在提交时自动执行检查。

### 待开发插件
- 检查文档中残留的 `TODO`/`FIXME` 等占位符并给出提示。
- 检测 `\begin`/`\end` 环境是否匹配，发现缺失或多余的环境。
- 利用大模型或拼写词典进行英文拼写及语法错误检查。
- 交叉检查 `\cite` 与 `.bib` 条目，发现未定义或未引用的文献。
