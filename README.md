# paper-llm-check
This project provides some checks on the formatting of a paper, such as detecting missing Markdown markers when copying output from large models.

## 功能列表
- Markdown标记残留检测
- BIB参考文献标题重复检测

## 已实现检测规则
### Markdown标记残留检测
检测未转换的**加粗**、*斜体*等Markdown标记

### BIB参考文献重复检测
检测.bib文件中重复的论文标题，提示重复的参考文献条目
