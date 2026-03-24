"""
新闻抓取模块 - 使用 Tavily API 搜索最新 AI 行业新闻
"""
import logging
from datetime import datetime
from tavily import TavilyClient
from config import TAVILY_API_KEY

logger = logging.getLogger(__name__)


def _search(client: TavilyClient, query: str, max_results: int = 12) -> list:
    """带错误处理的搜索封装"""
    try:
        resp = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
        )
        results = resp.get("results", [])
        logger.info(f"搜索 [{query[:30]}...] → 获取 {len(results)} 条")
        return results
    except Exception as e:
        logger.error(f"搜索失败: {query[:40]} | {e}")
        return []


def fetch_all_news() -> dict:
    """
    抓取三类新闻：中国AI、美国AI、时尚零售AI
    返回结构：{"china_ai": [...], "us_ai": [...], "fashion_ai": [...]}
    """
    client = TavilyClient(api_key=TAVILY_API_KEY)
    today_cn = datetime.now().strftime("%Y年%m月%d日")
    today_en = datetime.now().strftime("%B %d %Y")

    return {
        "china_ai": _search(
            client,
            f"中国AI人工智能 大模型 最新动态 {today_cn}",
            max_results=15,
        ),
        "us_ai": _search(
            client,
            f"OpenAI Google DeepMind Meta AI artificial intelligence news {today_en}",
            max_results=15,
        ),
        "fashion_ai": _search(
            client,
            f"AI fashion retail luxury brand technology application {today_en} 时尚零售AI",
            max_results=10,
        ),
    }
