# 中文Agent工具链

面向中文场景的Agent工具封装集合，让AI Agent能够更好地处理中文任务。

## 项目简介

本工具链封装了AI Agent在中文场景下常用的工具，包括中文搜索、OCR识别、资料库检索等功能。每个工具都经过中文优化，支持中文输入输出，适配中文语言习惯。

## 核心功能

- **中文搜索**：封装中文搜索引擎API，优化中文搜索词处理
- **中文OCR**：集成中文OCR识别能力，支持图片文字提取
- **资料库检索**：针对中文知识库的向量检索封装
- **任务分解**：中文任务理解与拆解框架
- **工具编排**：多个Agent工具的协调调度

## 技术架构

```
中文Agent工具链/
├── agent_templates/     # 各场景Agent模板
│   ├── research.py      # 调研型Agent
│   ├── writing.py       # 写作型Agent
│   ├── analysis.py      # 分析型Agent
│   └── coding.py        # 编码型Agent
├── tools/
│   ├── search.py        # 中文搜索工具
│   ├── ocr.py           # OCR工具封装
│   └── retriever.py     # 资料库检索工具
├── examples/
│   ├── research_demo.py # 调研场景示例
│   └── writing_demo.py  # 写作场景示例
├── requirements.txt
└── README.md
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用搜索工具

```python
from tools.search import ChineseSearchTool

search = ChineseSearchTool()
results = search.search("2024年人工智能发展趋势")
for result in results:
    print(f"标题: {result['title']}")
    print(f"摘要: {result['snippet']}")
```

### 使用Agent模板

```python
from agent_templates.research import ResearchAgent

agent = ResearchAgent()
report = agent.execute("调研中国新能源汽车产业现状")
print(report)
```

## 工具说明

### 搜索工具 (search.py)
- 支持百度、必应等搜索引擎
- 中文查询优化处理
- 搜索结果结构化提取

### OCR工具 (ocr.py)
- 支持多种图片格式
- 中文文字识别优化
- 表格文字识别

### 检索工具 (retriever.py)
- 中文文本向量化
- 语义相似度检索
- 知识库构建与查询

## Agent模板

| 模板 | 适用场景 | 核心能力 |
|------|----------|----------|
| 调研型 | 市场调研、竞品分析 | 多渠道信息整合、结构化报告输出 |
| 写作型 | 内容创作、文案撰写 | 风格模仿、素材组织、长文生成 |
| 分析型 | 数据分析、问题诊断 | 数据解读、模式识别、建议生成 |
| 编码型 | 代码生成、代码审查 | 理解需求、生成代码、调试修复 |

## 许可证

MIT License