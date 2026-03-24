"""
主入口 - 每日日报 & 周报生成

用法:
  python main.py daily    # 生成今日日报（默认）
  python main.py weekly   # 生成本周周报（周五运行）
"""
import sys
import logging
from datetime import datetime
from pathlib import Path

# ── 日志配置 ──────────────────────────────────────────────
from config import LOG_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            LOG_DIR / f"{datetime.now().strftime('%Y-%m')}.log",
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger("main")


# ── 日报流程 ──────────────────────────────────────────────
def run_daily():
    from fetch_news   import fetch_all_news
    from process_news import process_main_news, process_fashion_news
    from render_html  import render_daily_main, render_daily_fashion, render_index
    from cache        import save_today, get_report_list
    from notify       import notify_daily
    from git_push     import git_push

    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"=== 开始生成日报 {today} ===")

    # 1. 抓取新闻
    logger.info("步骤 1/5：抓取新闻...")
    raw = fetch_all_news()

    # 2. Claude 处理
    logger.info("步骤 2/5：Claude 处理新闻...")
    main_data    = process_main_news(raw)
    fashion_data = process_fashion_news(raw)

    # 3. 渲染 HTML
    logger.info("步骤 3/5：渲染 HTML...")
    render_daily_main(main_data)
    render_daily_fashion(fashion_data)
    render_index(get_report_list())

    # 4. 保存缓存（供周报使用）
    logger.info("步骤 4/5：保存缓存...")
    save_today(main_data, fashion_data)

    # 5. 推送 & 通知
    logger.info("步骤 5/5：推送到 GitHub & 微信通知...")
    git_push(f"auto: 日报 {today}")
    notify_daily(
        today,
        cn_count      = len(main_data.get("china_news", [])),
        us_count      = len(main_data.get("us_news", [])),
        fashion_count = len(fashion_data.get("fashion_news", [])),
    )

    logger.info(f"=== 日报生成完成 {today} ===")


# ── 周报流程 ──────────────────────────────────────────────
def run_weekly():
    from process_news import process_weekly_summary
    from render_html  import render_weekly, render_index
    from cache        import get_this_week, get_report_list
    from notify       import notify_weekly
    from git_push     import git_push

    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"=== 开始生成周报 {today} ===")

    # 先生成当日日报
    run_daily()

    # 1. 读取本周缓存
    logger.info("步骤 1/3：读取本周缓存...")
    week_cache = get_this_week()
    if not week_cache:
        logger.warning("本周无缓存数据，跳过周报生成")
        return

    # 2. Claude 汇总
    logger.info("步骤 2/3：Claude 汇总周报...")
    weekly_data = process_weekly_summary(week_cache)

    # 3. 渲染 & 推送
    logger.info("步骤 3/3：渲染周报 & 推送...")
    render_weekly(weekly_data)
    render_index(get_report_list())
    git_push(f"auto: 周报 {today}")
    total = (
        len(weekly_data.get("china_news", []))
        + len(weekly_data.get("us_news", []))
        + len(weekly_data.get("fashion_news", []))
    )
    notify_weekly(weekly_data.get("week_range", today), total)

    logger.info(f"=== 周报生成完成 ===")


# ── 入口 ─────────────────────────────────────────────────
if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "daily"
    if mode == "weekly":
        run_weekly()
    else:
        run_daily()
