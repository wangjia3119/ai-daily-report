"""
新闻缓存模块 - 保存每日新闻，供周报汇总使用
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from config import DATA_DIR

logger = logging.getLogger(__name__)
CACHE_FILE = DATA_DIR / "news_cache.json"


def _load() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save(cache: dict):
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_today(main_data: dict, fashion_data: dict):
    """保存今日新闻到缓存"""
    cache = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    cache[today] = {"main": main_data, "fashion": fashion_data}
    _save(cache)
    logger.info(f"今日新闻已缓存: {today}")


def get_this_week() -> dict:
    """获取本周（周一~今天）的所有缓存新闻"""
    cache = _load()
    today = datetime.now()
    # 本周周一
    monday = today - timedelta(days=today.weekday())
    week_data = {}
    for i in range(7):
        day = monday + timedelta(days=i)
        key = day.strftime("%Y-%m-%d")
        if key in cache:
            week_data[key] = cache[key]
        if day.date() >= today.date():
            break
    logger.info(f"本周缓存: {list(week_data.keys())}")
    return week_data


def get_report_list() -> list:
    """获取所有已生成的报告列表，用于首页索引"""
    from config import DAILY_DIR, WEEKLY_DIR, GITHUB_PAGES_URL
    base = GITHUB_PAGES_URL or ""
    reports = []

    daily_files = sorted(DAILY_DIR.glob("????-??-??.html"), reverse=True)
    for f in daily_files:
        date_str = f.stem
        fashion_f = DAILY_DIR / f"{date_str}-fashion.html"
        reports.append({
            "date": date_str,
            "url_main":    f"{base}/daily/{f.name}" if base else f"daily/{f.name}",
            "url_fashion": f"{base}/daily/{fashion_f.name}" if base else f"daily/{fashion_f.name}",
        })
    return reports
