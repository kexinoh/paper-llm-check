# paper-llm-check
This project provides some checks on the formatting of a paper, such as detecting missing Markdown markers when copying output from large models.

## 功能列表
- Markdown标记残留检测
- BIB参考文献标题重复检测
- arXiv引用验证

## 已实现检测规则
### Markdown标记残留检测
检测未转换的**加粗**、*斜体*等Markdown标记

### BIB参考文献重复检测
检测.bib文件中重复的论文标题，提示重复的参考文献条目

### arXiv引用验证
1. 从eprint字段或arxiv.org/abs/URL提取arXiv ID
2. 通过arXiv API获取论文元数据
3. 比对本地标题与API标题相似度（阈值80%）
4. 支持@article和@misc条目类型
5. 自动跳过非.bib文件
