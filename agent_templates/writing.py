"""
中文Agent工具链 - 写作型Agent模板
"""

import json
import random
from typing import Optional


class WritingAgent:
    """写作型Agent"""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {
            'name': '写作助手',
            'style': '通用',
            'max_length': 2000
        }

    def plan_article(self, topic: str) -> dict:
        """规划文章结构"""
        return {
            'title': topic,
            'sections': [
                {'heading': '引言', 'points': ['引出话题', '说明重要性']},
                {'heading': '正文', 'points': ['核心观点1', '核心观点2', '核心观点3']},
                {'heading': '结论', 'points': ['总结观点', '展望未来']}
            ],
            'suggested_length': self.config['max_length']
        }

    def write_section(self, section: dict) -> str:
        """撰写段落"""
        points = section.get('points', [])
        content = f"## {section['heading']}\n\n"
        for point in points:
            content += f"{point}。在当今快速变化的时代，这一问题值得深入探讨。\n\n"
        return content

    def write(self, topic: str) -> str:
        """执行写作任务"""
        plan = self.plan_article(topic)

        article = f"# {plan['title']}\n\n"
        for section in plan['sections']:
            article += self.write_section(section)

        return article


if __name__ == '__main__':
    agent = WritingAgent()
    article = agent.write("远程办公的未来趋势")
    print(article)