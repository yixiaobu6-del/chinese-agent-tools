"""
中文Agent工具链 - 搜索工具
封装中文搜索引擎能力
"""

import hashlib
import json
import time
from typing import Optional


class ChineseSearchTool:
    """中文搜索工具"""

    def __init__(self, config: Optional[dict] = None):
        """
        初始化搜索工具

        Args:
            config: 配置项，支持 engine, api_key, cache_ttl 等
        """
        self.config = config or {
            'engine': 'bing',
            'cache_ttl': 3600,
            'max_results': 10,
            'timeout': 10
        }
        self.cache = {}

    def _normalize_query(self, query: str) -> str:
        """规范化中文搜索词"""
        # 去除多余空格
        query = ' '.join(query.split())
        # 去除无意义的语气词前缀
        stop_prefixes = ['请问', '帮我', '我想知道', '帮我查一下', '搜索一下']
        for prefix in stop_prefixes:
            if query.startswith(prefix):
                query = query[len(prefix):].strip()
        return query

    def _get_cache_key(self, query: str) -> str:
        """生成缓存键"""
        return hashlib.md5(query.encode('utf-8')).hexdigest()

    def _check_cache(self, query: str) -> Optional[list]:
        """检查缓存"""
        cache_key = self._get_cache_key(query)
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['time'] < self.config['cache_ttl']:
                return cached['results']
        return None

    def _set_cache(self, query: str, results: list) -> None:
        """设置缓存"""
        cache_key = self._get_cache_key(query)
        self.cache[cache_key] = {
            'results': results,
            'time': time.time()
        }

    def search(self, query: str, max_results: int = 10) -> list:
        """
        执行搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        normalized_query = self._normalize_query(query)

        # 检查缓存
        cached = self._check_cache(normalized_query)
        if cached:
            return cached[:max_results]

        # 模拟搜索（实际使用需接入搜索引擎API）
        results = self._mock_search(normalized_query)

        # 缓存结果
        self._set_cache(normalized_query, results)

        return results[:max_results]

    def _mock_search(self, query: str) -> list:
        """模拟搜索（演示用，实际项目需替换为真实API调用）"""
        print(f"[搜索] 查询: {query}")

        return [
            {
                'title': f'{query} - 最新研究报告',
                'url': f'https://example.com/research/{hashlib.md5(query.encode()).hexdigest()[:8]}',
                'snippet': f'本文深入分析了{query}的最新发展趋势，包括市场规模、竞争格局和技术创新等方面。',
                'source': '研究报告',
                'date': '2024-06-15'
            },
            {
                'title': f'{query}的现状与未来展望',
                'url': f'https://example.com/analysis/{hashlib.md5(query.encode()).hexdigest()[:8]}',
                'snippet': f'从多个维度分析了{query}的发展现状，并对未来趋势进行了预测。',
                'source': '行业分析',
                'date': '2024-05-20'
            },
            {
                'title': f'2024年{query}白皮书',
                'url': f'https://example.com/whitepaper/{hashlib.md5(query.encode()).hexdigest()[:8]}',
                'snippet': f'本白皮书系统梳理了{query}的政策环境、技术路线和商业模式变革。',
                'source': '官方白皮书',
                'date': '2024-04-10'
            }
        ]

    def search_with_fallback(self, query: str) -> list:
        """带降级策略的搜索"""
        results = self.search(query)
        if not results:
            # 降级：简化查询词
            simplified = self._simplify_query(query)
            if simplified != query:
                results = self.search(simplified)
        return results

    def _simplify_query(self, query: str) -> str:
        """简化查询词"""
        # 去除修饰词
        modifiers = ['最新的', '关于', '我想找', '帮我找']
        for mod in modifiers:
            query = query.replace(mod, '')
        return query.strip()

    def batch_search(self, queries: list) -> dict:
        """批量搜索"""
        return {q: self.search(q) for q in queries}

    def search_with_categories(self, query: str) -> dict:
        """
        分类搜索

        Returns:
            按类别组织的结果
        """
        results = self.search(query)
        categorized = {
            'news': [],
            'articles': [],
            'reports': []
        }

        for result in results:
            source = result.get('source', '')
            if '报告' in source or '白皮书' in source:
                categorized['reports'].append(result)
            elif '新闻' in source:
                categorized['news'].append(result)
            else:
                categorized['articles'].append(result)

        return categorized


if __name__ == '__main__':
    search_tool = ChineseSearchTool()
    results = search_tool.search("人工智能在医疗领域的应用")
    for r in results:
        print(f"[{r['source']}] {r['title']}")
        print(f"  {r['snippet']}")