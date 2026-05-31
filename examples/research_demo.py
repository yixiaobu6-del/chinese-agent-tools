"""
中文Agent工具链 - 使用示例
"""

from pathlib import Path
from tools.search import ChineseSearchTool
from tools.retriever import ChineseRetriever


def demo_search() -> None:
    """搜索工具演示"""
    print("=" * 50)
    print("搜索工具演示")
    print("=" * 50)

    search = ChineseSearchTool()
    results = search.search("新能源汽车市场")
    for r in results:
        print(f"  [{r['source']}] {r['title']}")
    print()


def demo_retriever() -> None:
    """检索工具演示"""
    print("=" * 50)
    print("资料库检索演示")
    print("=" * 50)

    retriever = ChineseRetriever()
    docs = [
        {'content': '机器学习是人工智能的核心领域之一，通过算法从数据中学习规律。'},
        {'content': '深度学习使用多层神经网络，在图像和语音识别上取得了突破性进展。'},
        {'content': '强化学习让智能体通过与环境的交互来学习最优策略。'},
        {'content': '自然语言处理使计算机能够理解、生成和处理人类语言。'},
        {'content': '计算机视觉研究如何让机器理解和分析图像和视频内容。'},
    ]
    retriever.add_documents(docs)

    results = retriever.search("神经网络深度学习")
    for r in results:
        print(f"  分数: {r['score']:.2f} | {r['content']}")
    print()


if __name__ == '__main__':
    demo_search()
    demo_retriever()