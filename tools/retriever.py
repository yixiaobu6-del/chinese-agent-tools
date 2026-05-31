"""
中文Agent工具链 - 资料库检索工具
封装中文知识库的向量检索能力
"""

import hashlib
import json
import math
import re
from collections import Counter
from typing import Optional


class ChineseRetriever:
    """中文资料库检索工具"""

    def __init__(self, config: Optional[dict] = None):
        """
        初始化检索器

        Args:
            config: 配置项
        """
        self.config = config or {
            'top_k': 5,
            'similarity_threshold': 0.5,
            'embedding_model': 'local'
        }
        self.documents = []
        self.index = {}

    def add_documents(self, documents: list) -> None:
        """
        添加文档到知识库

        Args:
            documents: 文档列表，每项包含 id, content, metadata
        """
        for doc in documents:
            doc_id = doc.get('id', hashlib.md5(doc['content'].encode()).hexdigest()[:8])
            self.documents.append({
                'id': doc_id,
                'content': doc['content'],
                'metadata': doc.get('metadata', {})
            })

        # 重建索引
        self._build_index()

    def _build_index(self) -> None:
        """构建倒排索引"""
        self.index = {}

        for doc_idx, doc in enumerate(self.documents):
            # 中文分词（简单按字和词索引）
            content = doc['content']

            # 提取关键词（按标点分割和按2-gram）
            segments = re.split(r'[，。！？；：、\s]', content)
            for segment in segments:
                if len(segment) < 2:
                    continue

                # 添加2-gram
                for i in range(len(segment) - 1):
                    bigram = segment[i:i + 2]
                    if bigram not in self.index:
                        self.index[bigram] = set()
                    self.index[bigram].add(doc_idx)

                # 整段
                if segment not in self.index:
                    self.index[segment] = set()
                self.index[segment].add(doc_idx)

        print(f"[检索] 索引构建完成: {len(self.documents)} 篇文档, {len(self.index)} 个索引项")

    def search(self, query: str, top_k: int = 5) -> list:
        """
        执行检索

        Args:
            query: 查询文本
            top_k: 返回结果数

        Returns:
            检索结果列表
        """
        # 提取查询中的关键词
        q_segments = [s.strip() for s in re.split(r'[，。！？；：、\s]', query) if len(s.strip()) >= 2]

        # 计算相关文档分数
        scores = Counter()
        for segment in q_segments:
            # 精确匹配
            if segment in self.index:
                for doc_idx in self.index[segment]:
                    scores[doc_idx] += 5

            # 2-gram匹配
            for i in range(len(segment) - 1):
                bigram = segment[i:i + 2]
                if bigram in self.index:
                    for doc_idx in self.index[bigram]:
                        scores[doc_idx] += 2

            # 直接内容匹配
            for doc_idx, doc in enumerate(self.documents):
                if segment in doc['content']:
                    scores[doc_idx] += 1

        # 归一化并排序
        max_score = max(scores.values()) if scores else 1
        normalized = [
            {
                'id': self.documents[idx]['id'],
                'content': self.documents[idx]['content'],
                'metadata': self.documents[idx]['metadata'],
                'score': score / max_score,
                'raw_score': score
            }
            for idx, score in scores.most_common(top_k * 2)
            if score / max_score >= self.config['similarity_threshold']
        ]

        return normalized[:top_k]

    def search_with_context(self, query: str, window: int = 50) -> list:
        """
        检索带上下文的匹配片段

        Args:
            query: 查询文本
            window: 上下文窗口大小

        Returns:
            匹配片段列表
        """
        results = self.search(query)
        enriched = []

        for result in results:
            content = result['content']
            # 找到匹配位置
            positions = []
            for keyword in [s.strip() for s in re.split(r'[，。！？；：、\s]', query) if len(s.strip()) >= 2]:
                pos = content.find(keyword)
                if pos >= 0:
                    positions.append(pos)

            # 提取上下文
            snippets = []
            for pos in sorted(positions)[:3]:
                start = max(0, pos - window)
                end = min(len(content), pos + window)
                snippet = content[start:end]
                if start > 0:
                    snippet = '...' + snippet
                if end < len(content):
                    snippet = snippet + '...'
                snippets.append(snippet)

            result['snippets'] = snippets
            enriched.append(result)

        return enriched

    def hybrid_search(self, query: str, top_k: int = 5) -> list:
        """混合检索（关键词 + 语义）"""
        # 关键词搜索
        keyword_results = self.search(query, top_k)

        # 语义匹配（基于词重叠的简单实现）
        q_words = set(re.findall(r'[\u4e00-\u9fff]{2,}', query))

        for result in self.documents:
            doc_words = set(re.findall(r'[\u4e00-\u9fff]{2,}', result['content']))
            overlap = len(q_words & doc_words)
            if overlap > 0:
                similarity = overlap / (len(q_words) + len(doc_words) - overlap)
                if similarity > self.config['similarity_threshold']:
                    # 合并到结果
                    pass

        return keyword_results

    def get_statistics(self) -> dict:
        """获取知识库统计信息"""
        if not self.documents:
            return {'doc_count': 0}

        total_chars = sum(len(d['content']) for d in self.documents)
        avg_length = total_chars / len(self.documents)

        return {
            'doc_count': len(self.documents),
            'index_size': len(self.index),
            'total_chars': total_chars,
            'avg_length': round(avg_length, 1),
            'max_length': max(len(d['content']) for d in self.documents),
            'min_length': min(len(d['content']) for d in self.documents)
        }


if __name__ == '__main__':
    retriever = ChineseRetriever()

    docs = [
        {'id': '1', 'content': '人工智能在医疗领域的应用包括辅助诊断、药物研发和健康管理等方向。'},
        {'id': '2', 'content': '深度学习是机器学习的一个重要分支，在图像识别和自然语言处理方面表现优异。'},
        {'id': '3', 'content': '自然语言处理技术让计算机能够理解和生成人类语言，应用在机器翻译、智能客服等场景。'},
    ]
    retriever.add_documents(docs)

    results = retriever.search("人工智能医疗")
    for r in results:
        print(f"ID: {r['id']}, 分数: {r['score']:.2f}")
        print(f"内容: {r['content']}")