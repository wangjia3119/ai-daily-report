"""
通知模块 - Server酱微信推送
"""
import logging
import requests
from config import SERVER_CHAN_KEY, GITHUB_PAGES_URL

logger = logging.getLogger(__name__)


def push_wechat(title: str, content: str) -> bool:
    """
    通过 Server酱 推送微信通知
    申请地址: https://sct.ftqq.com
    """
    if not SERVER_CHAN_KEY:
        logger.warning("未配置 SERVER_CHAN_KEY，跳过微信推送")
        return False

    url = f"https://sctapi.ftqq.com/{SERVER_CHAN_KEY}.send"
    try:
        resp = requests.post(
            url,
            data={"title": title, "desp": content},
            timeout=10,
        )
        data = resp.json()
        if data.get("code") == 0:
            logger.info("微信推送成功")
            return True
        else:
            logger.error(f"微信推送失败: {data}")
            return False
    except Exception as e:
        logger.error(f"微信推送异常: {e}")
        return False


def notify_daily(date_str: str, cn_count: int, us_count: int, fashion_count: int):
    """日报推送通知"""
    base = GITHUB_PAGES_URL or "（本地生成）"

    if GITHUB_PAGES_URL:
        main_link    = f"{GITHUB_PAGES_URL}/daily/{date_str}.html"
        fashion_link = f"{GITHUB_PAGES_URL}/daily/{date_str}-fashion.html"
        link_text = f"\n\n📰 [AI行业日报]({main_link})\n👗 [时尚零售专报]({fashion_link})"
    else:
        link_text = "\n\n（文件已保存至本地 output/daily/）"

    title = f"📮 AI日报 {date_str} 已更新"
    content = (
        f"**今日速览**\n\n"
        f"- 🇨🇳 中国AI：{cn_count} 条\n"
        f"- 🇺🇸 美国AI：{us_count} 条\n"
        f"- 👗 时尚零售AI：{fashion_count} 条"
        f"{link_text}"
    )
    push_wechat(title, content)


def notify_weekly(week_range: str, total: int):
    """周报推送通知"""
    if GITHUB_PAGES_URL:
        from datetime import datetime
        iso = datetime.now().isocalendar()
        link = f"{GITHUB_PAGES_URL}/weekly/{iso.year}-W{iso.week:02d}.html"
        link_text = f"\n\n📊 [查看本周周报]({link})"
    else:
        link_text = "\n\n（文件已保存至本地 output/weekly/）"

    title = f"📋 AI周报 {week_range} 已发布"
    content = (
        f"**本周精选 {total} 条 AI 行业动态**\n\n"
        f"涵盖中国AI、美国AI、时尚零售AI三大板块。"
        f"{link_text}"
    )
    push_wechat(title, content)
